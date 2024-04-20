#  Copyright (c) 2024 zfit

from __future__ import annotations

from contextlib import suppress
from functools import partial
from typing import TYPE_CHECKING, Literal, Optional, Union

import pydantic
from pydantic import Field
from tensorflow.python.util.deprecation import deprecated

from ..exception import OutsideLimitsError, SpecificFunctionNotImplementedError
from ..serialization.serializer import BaseRepr, Serializer
from .data import convert_to_data
from .serialmixin import SerializableMixin

if TYPE_CHECKING:
    import zfit

import abc
import warnings
from collections.abc import Callable, Iterable, Mapping

import tensorflow as tf
from ordered_set import OrderedSet

import zfit.z.numpy as znp

from .. import settings, z
from ..util import ztyping
from ..util.checks import NONE
from ..util.container import convert_to_container, is_container
from ..util.deprecation import deprecated_args
from ..util.exception import (
    BehaviorUnderDiscussion,
    BreakingAPIChangeError,
    IntentionAmbiguousError,
    NotExtendedPDFError,
)
from ..util.warnings import warn_advanced_feature
from ..z.math import (
    autodiff_gradient,
    autodiff_hessian,
    autodiff_value_gradients,
    automatic_value_gradients_hessian,
    numerical_gradient,
    numerical_hessian,
    numerical_value_gradient,
    numerical_value_gradients_hessian,
)
from .baseobject import BaseNumeric, extract_filter_params
from .constraint import BaseConstraint
from .dependents import _extract_dependencies
from .interfaces import ZfitBinnedData, ZfitData, ZfitLoss, ZfitParameter, ZfitPDF, ZfitSpace
from .parameter import convert_to_parameters, set_values

DEFAULT_FULL_ARG = True


@z.function(wraps="loss")
def _unbinned_nll_tf(
    model: ztyping.PDFInputType,
    data: ztyping.DataInputType,
    fit_range: ZfitSpace,
    log_offset,
):
    """Return the unbinned negative log likelihood for a PDF.

    Args:
        model: |@doc:loss.init.model| PDFs that return the normalized probability for
               *data* under the given parameters.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit. |@docend:loss.init.model|
        data: |@doc:loss.init.data| Dataset that will be given to the *model*.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit.
               If the data is not a ``ZfitData`` object, i.e. it doesn't have ha space
               it has to be withing the limits of the model, otherwise, an
               :py:class:`~zfit.exception.IntentionAmbiguousError` will be raised. |@docend:loss.init.data|
        fit_range:

    Returns:
        The unbinned nll value as a scalar
    """

    if is_container(model):
        nlls = [
            _unbinned_nll_tf(model=p, data=d, fit_range=r, log_offset=log_offset)
            for p, d, r in zip(model, data, fit_range)
        ]
        nlls_summed = znp.sum(nlls, axis=0)

        nll_finished = nlls_summed
    else:
        if fit_range is not None:
            data = data.with_obs(fit_range)
            probs = model.pdf(data, norm_range=fit_range)
        else:
            probs = model.pdf(data)
        log_probs = znp.log(probs + znp.asarray(1e-307, dtype=znp.float64))  # minor offset to avoid NaNs from log(0)
        if log_offset is None:
            log_offset = znp.array([0.0], dtype=znp.float64)
        nll = _nll_calc_unbinned_tf(
            log_probs=log_probs,
            weights=data.weights if data.weights is not None else None,
            log_offset=log_offset,
        )
        nll_finished = nll
    return nll_finished


@z.function(wraps="tensor", keepalive=True)
def _nll_calc_unbinned_tf(log_probs, weights, log_offset):
    """Calculate the negative log likelihood from the log probabilities."""

    if weights is not None:
        log_probs *= weights  # because it's prob ** weights
    if log_offset is not False:
        log_probs -= log_offset
    return -znp.sum(log_probs, axis=0)
    # nll = -tfp.math.reduce_kahan_sum(input_tensor=log_probs, axis=0)


def _constraint_check_convert(constraints):
    checked_constraints = []
    for constr in constraints:
        if isinstance(constr, BaseConstraint):
            checked_constraints.append(constr)
        else:
            msg = (
                "Constraints have to be of type `Constraint`, a simple"
                " constraint from a function can be constructed with"
                " `SimpleConstraint`."
            )
            raise BreakingAPIChangeError(msg)
    return checked_constraints


class BaseLossRepr(BaseRepr):
    _implementation = None
    _owndict = pydantic.PrivateAttr(default_factory=dict)
    hs3_type: Literal["BaseLoss"] = Field("BaseLoss", alias="type")
    model: Union[
        Serializer.types.PDFTypeDiscriminated,
        list[Serializer.types.PDFTypeDiscriminated],
    ]
    data: Union[
        Serializer.types.DataTypeDiscriminated,
        list[Serializer.types.DataTypeDiscriminated],
    ]
    constraints: Optional[list[Serializer.types.ConstraintTypeDiscriminated]] = Field(default_factory=list)
    options: Optional[Mapping] = Field(default_factory=dict)

    @pydantic.validator("model", "data", "constraints", pre=True)
    def _check_container(cls, v):
        if cls.orm_mode(v):
            v = convert_to_container(v, list)
        return v


class GradientNotImplementedError(SpecificFunctionNotImplementedError):
    pass


class ValueGradientNotImplementedError(SpecificFunctionNotImplementedError):
    pass


class ValueGradientHessianNotImplementedError(SpecificFunctionNotImplementedError):
    pass


class HessianNotImplementedError(SpecificFunctionNotImplementedError):
    pass


class BaseLoss(ZfitLoss, BaseNumeric):
    def __init__(
        self,
        model: ztyping.ModelsInputType,
        data: ztyping.DataInputType,
        fit_range: ztyping.LimitsTypeInput = None,
        constraints: ztyping.ConstraintsTypeInput = None,
        options: Mapping | None = None,
    ):
        # first doc line left blank on purpose, subclass adds class docstring (Sphinx autodoc adds the two)
        """A "simultaneous fit" can be performed by giving one or more ``model``, ``data``, ``fit_range`` to the loss.
        The length of each has to match the length of the others.

        Args:
            model: The model or models to evaluate the data on
            data: Data to use
            fit_range: The fitting range. It's the norm_range for the models (if
                they
                have a norm_range) and the data_range for the data.
            constraints: A Tensor representing a loss constraint. Using
                ``zfit.constraint.*`` allows for easy use of predefined constraints.
            options: Different options for the loss calculation.
        """
        super().__init__(name=type(self).__name__, params={})
        if fit_range is not None and all(fr is not None for fr in fit_range):
            warnings.warn(
                "The fit_range argument is depreceated and will maybe removed in future releases. "
                "It is preferred to define the range in the space"
                " when creating the data and the model or directly cut the data correctly.",
                stacklevel=2,
            )

        model, data, fit_range = self._input_check(pdf=model, data=data, fit_range=fit_range)
        self._model = model
        self._data = data
        self._fit_range = fit_range

        options = self._check_init_options(options, data)

        self._options = options
        self._subtractions = {}
        if constraints is None:
            constraints = []
        self._constraints = _constraint_check_convert(convert_to_container(constraints, list))

        self.is_precompiled = False
        self._precompiled_hashes = []

        # not ideal, should be in parametrized. But we don't have too many base classes, so this should work
        self._assert_params_unique()

    @property
    def is_precompiled(self):
        for data, h in zip(self.data, self._precompiled_hashes):
            if data.hashint != h:
                self.is_precompiled = False
                break
        return self._is_precompiled

    @is_precompiled.setter
    def is_precompiled(self, value):
        self._is_precompiled = value
        if value:
            self._precompiled_hashes = [data.hashint for data in self.data]

    def _check_init_options(self, options, data):
        try:
            nevents = sum(d.nevents for d in data)
        except RuntimeError:  # can happen if not yet sampled. What to do? Approx_nevents?
            nevents = 150_000  # sensible default
        options = {} if options is None else options

        if options.get("numhess") is None:
            options["numhess"] = True

        if options.get("numgrad") is None:
            options["numgrad"] = settings.options["numerical_grad"]

        if options.get("kahansum") is None:
            options["kahansum"] = nevents > 500_000  # start using kahan if we have more than 500k events

        if options.get("subtr_const") is None:  # TODO: balance better?
            # if nevents < 200_000:
            #     subtr_const = True
            # elif nevents < 1_000_000:
            #     subtr_const = 'kahan'
            # else:
            #     subtr_const = 'elewise'
            subtr_const = True
            options["subtr_const"] = subtr_const

        return options

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._name = "UnnamedSubBaseLoss"

    def _get_params(
        self,
        floating: bool | None = True,
        is_yield: bool | None = None,
        extract_independent: bool | None = True,
    ) -> set[ZfitParameter]:
        params = OrderedSet()
        params = params.union(
            *(
                model.get_params(
                    floating=floating,
                    is_yield=is_yield,
                    extract_independent=extract_independent,
                )
                for model in self.model
            )
        )

        return params.union(
            *(
                constraint.get_params(
                    floating=floating,
                    is_yield=False,
                    extract_independent=extract_independent,
                )
                for constraint in self.constraints
            )
        )

    def _input_check(self, pdf, data, fit_range):
        if isinstance(pdf, tuple):
            msg = "`pdf` has to be a pdf or a list of pdfs, not a tuple."
            raise TypeError(msg)
        if isinstance(data, tuple):
            msg = "`data` has to be a data or a list of data, not a tuple."
            raise TypeError(msg)

        # pdf, data = (convert_to_container(obj, non_containers=[tuple]) for obj in (pdf, data))
        pdf, data = self._check_convert_model_data(pdf, data, fit_range)
        # TODO: data, range consistency?
        if fit_range is None:
            fit_range = []
            non_consistent = {"data": [], "model": [], "range": []}
            for p, d in zip(pdf, data):
                if p.norm != d.data_range:
                    non_consistent["data"].append(d)
                    non_consistent["model"].append(p)
                    non_consistent["range"].append((p.space, d.data_range))
                fit_range.append(None)
            if non_consistent["range"]:  # TODO: test
                warn_advanced_feature(
                    f"PDFs {non_consistent['model']} as "
                    f"well as `data` {non_consistent['data']}"
                    f" have different ranges {non_consistent['range']} they"
                    f" are defined in. The data range will cut the data while the"
                    f" norm range defines the normalization.",
                    identifier="inconsistent_fitrange",
                )
        else:
            fit_range = convert_to_container(fit_range, non_containers=[tuple])

        if not len(pdf) == len(data) == len(fit_range):
            msg = (
                "pdf, data and fit_range don't have the same number of components:"
                f"\npdf: {pdf}"
                f"\ndata: {data}"
                f"\nfit_range: {fit_range}"
            )
            raise ValueError(msg)

        # sanitize fit_range
        fit_range = [
            p._convert_sort_space(limits=range_) if range_ is not None else None for p, range_ in zip(pdf, fit_range)
        ]
        # TODO: sanitize pdf, data?
        self.add_cache_deps(cache_deps=pdf)
        self.add_cache_deps(cache_deps=data)
        return pdf, data, fit_range

    def check_precompile(self, *, params=None, force=False):
        from zfit import run

        if (not run.executing_eagerly()) or (self.is_precompiled and not force):
            return params, False
        with self._check_set_input_params(params, guarantee_checked=False) as checked_params:
            if do_subtr := self._options.get("subtr_const", False):
                if do_subtr is not True:
                    self._options["subtr_const_value"] = do_subtr
                log_offset = self._options.get("subtr_const_value")
                if log_offset is None:
                    run.assert_executing_eagerly()  # first time subtr
                    nevents_tot = znp.sum([d._approx_nevents for d in self.data])
                    log_offset_sum = (
                        self._call_value(
                            data=self.data,
                            model=self.model,
                            fit_range=self.fit_range,
                            constraints=self.constraints,
                            # presumably were not at the minimum,
                            # so the loss will decrease
                            log_offset=z.convert_to_tensor(0.0),
                        )
                        - 10000.0
                    )
                    log_offset = tf.stop_gradient(-znp.divide(log_offset_sum, nevents_tot))
                    self._options["subtr_const_value"] = log_offset
        self.is_precompiled = True
        return checked_params, True

    def _check_convert_model_data(self, model, data, fit_range):
        model, data = tuple(convert_to_container(obj) for obj in (model, data))

        model_checked = []
        data_checked = []
        for mod, dat in zip(model, data):
            if not isinstance(dat, (ZfitData, ZfitBinnedData)):
                if fit_range is not None:
                    msg = "Fit range should not be used if data is not ZfitData."
                    raise TypeError(msg)
                try:
                    dat = convert_to_data(data=dat, obs=mod.space, check_limits=True)
                except OutsideLimitsError as error:
                    msg = (
                        f"Data {dat} is not a zfit Data (and therefore has no Space that defines possible limits) "
                        f"and is not fully within the limits {mod.space} of the model {mod}."
                        f"If the data should be what it is, please convert to zfit Data (`zfit.Data(data, obs=obs)`) "
                        f"or remove events outside the space"
                    )
                    raise IntentionAmbiguousError(msg) from error
            model_checked.append(mod)
            data_checked.append(dat)
        return model_checked, data_checked

    def _input_check_params(self, params):
        return tuple(self.get_params()) if params is None else convert_to_container(params)

    @deprecated(None, "Use `create_new` instead and fill the constraints there.")
    def add_constraints(self, constraints):
        constraints = convert_to_container(constraints)
        return self._add_constraints(constraints)

    def _add_constraints(self, constraints):
        constraints = _constraint_check_convert(convert_to_container(constraints, container=list))
        self._constraints.extend(constraints)
        return constraints

    @property
    def name(self):
        return self._name

    @property
    def model(self):
        return self._model

    @property
    def data(self):
        return self._data

    @property
    def fit_range(self):
        return self._fit_range

    @property
    def constraints(self):
        return self._constraints

    def _get_dependencies(self):  # TODO: fix, add constraints
        pdf_dependents = _extract_dependencies(self.model)
        pdf_dependents |= _extract_dependencies(self.constraints)
        return pdf_dependents

    @abc.abstractmethod
    def _loss_func(self, model, data, fit_range, constraints, log_offset):
        raise NotImplementedError

    @property
    def errordef(self) -> float | int:
        return self._errordef

    def __call__(
        self,
        _x: ztyping.DataInputType = None,
        # *, full: bool = None,  # Not added, breaks iminuit.
    ) -> znp.array:
        """Calculate the loss value with the given input for the free parameters.

        Args:
            *positional*: Array-like argument to set the parameters. The order of the values correspond to
                the position of the parameters in :py:meth:`~BaseLoss.get_params()` (called without any arguments).
                For more detailed control, it is always possible to wrap :py:meth:`~BaseLoss.value()` and set the
                desired parameters manually.
            full: |@doc:loss.value.full| If True, return the full loss value, otherwise
               allow for the removal of constants and only return
               the part that depends on the parameters. Constants
               don't matter for the task of optimization, but
               they can greatly help with the numerical stability of the loss function. |@docend:loss.value.full|

        Returns:
            Calculated loss value as a scalar.
        """
        if _x is None:
            msg = (
                "Currently, calling a loss requires to give the arguments explicitly."
                " If you think this behavior should be changed, please open an issue"
                " https://github.com/zfit/zfit/issues/new/choose"
            )
            raise BehaviorUnderDiscussion(msg)
        if isinstance(_x, dict):
            msg = "Dicts are not supported when calling a loss, only array-like values."
            raise TypeError(msg)
        if _x is None:
            return self.value(full=True)  # has to be full, otherwise iminuit breaks
        else:
            params = self.get_params()
            with set_values(params, _x):
                return self.value(full=True)

    def value(self, *, params: ztyping.ParamTypeInput = None, full: bool | None = None) -> znp.ndarray:
        """Calculate the loss value with the current values of the free parameters.

        Args:
            params: |@doc:loss.args.params| Mapping of the parameter names to the actual
               values. The parameter names refer to the names of the parameters,
               typically :py:class:`~zfit.Parameter`, that is returned by
               `get_params()`. If no params are given, the current default
               values of the parameters are used. |@docend:loss.args.params|
            full: |@doc:loss.value.full| If True, return the full loss value, otherwise
               allow for the removal of constants and only return
               the part that depends on the parameters. Constants
               don't matter for the task of optimization, but
               they can greatly help with the numerical stability of the loss function. |@docend:loss.value.full|


        Returns:
            Calculated loss value as a scalar.
        """
        params, checked = self.check_precompile(params=params)
        if full is None:
            full = DEFAULT_FULL_ARG
        log_offset = 0.0 if full else self._options.get("subtr_const_value")

        if log_offset is not None:
            log_offset = z.convert_to_tensor(log_offset)

        # log_offset = z.convert_to_tensor(log_offset)
        with self._check_set_input_params(params, guarantee_checked=checked):
            return self._call_value(self.model, self.data, self.fit_range, self.constraints, log_offset)

    def _call_value(self, model, data, fit_range, constraints, log_offset):
        return self._value(
            model=model,
            data=data,
            fit_range=fit_range,
            constraints=constraints,
            log_offset=log_offset,
        )
        # if self._subtractions.get('kahan') is None:
        #     self._subtractions['kahan'] = value
        # value_subtracted = (value[0] - self._subtractions['kahan'][0]) - (
        #         value[1] - self._subtractions['kahan'][1])
        # return value_subtracted
        # value = value_substracted[0] - value_substracted[1]

    def _value(self, model, data, fit_range, constraints, log_offset):
        return self._loss_func(
            model=model,
            data=data,
            fit_range=fit_range,
            constraints=constraints,
            log_offset=log_offset,
        )

    def __add__(self, other):
        if not isinstance(other, BaseLoss):
            msg = "Has to be a subclass of `BaseLoss` or overwrite `__add__`."
            raise TypeError(msg)
        if type(other) != type(self):
            msg = "cannot safely add two different kind of loss."
            raise ValueError(msg)
        model = self.model + other.model
        data = self.data + other.data
        fit_range = self.fit_range + other.fit_range
        constraints = self.constraints + other.constraints
        kwargs = {"model": model, "data": data, "constraints": constraints}
        if any(fitrng is not None for fitrng in fit_range):
            kwargs["fit_range"] = fit_range
        return type(self)(**kwargs)

    def gradient(
        self, params: ztyping.ParamTypeInput = None, *, numgrad=None, paramvals: ztyping.ParamTypeInput = None
    ) -> tf.Tensor:
        """Calculate the gradient of the loss with respect to the given parameters.

        Args:
            params: The parameters with respect to which the gradient is calculated. If `None`, all parameters
                are used.
            numgrad: |@doc:loss.args.numgrad| If ``True``, calculate the numerical gradient/Hessian
               instead of using the automatic one. This is
               usually slower if called repeatedly but can
               be used if the automatic gradient fails (e.g. if
               the model is not differentiable, written not in znp.* etc).
               Default will fall back to what the loss is set to. |@docend:loss.args.numgrad|
            paramvals: |@doc:loss.args.params| Mapping of the parameter names to the actual
               values. The parameter names refer to the names of the parameters,
               typically :py:class:`~zfit.Parameter`, that is returned by
               `get_params()`. If no params are given, the current default
               values of the parameters are used. |@docend:loss.args.params|


        Returns:
            The gradient of the loss with respect to the given parameters.
        """
        params = self._input_check_params(params)
        numgrad = self._options["numgrad"] if numgrad is None else numgrad
        paramvals, checked = self.check_precompile(params=paramvals)
        with self._check_set_input_params(paramvals, guarantee_checked=checked):
            return self._call_gradient(params, numgrad)

    @z.function(wraps="loss")
    def _call_gradient(self, params, numgrad):
        with suppress(GradientNotImplementedError):
            return self._gradient(params=params, numgrad=numgrad)

        with suppress(ValueGradientNotImplementedError):
            return self._value_gradient(params=params, numgrad=numgrad, full=False)[1]
        return self._fallback_gradient(params=params, numgrad=numgrad)

    def gradients(self, *_, **__):
        msg = "`gradients` is deprecated, use `gradient` instead."
        raise BreakingAPIChangeError(msg)

    def _gradient(self, params, numgrad):  # noqa: ARG002
        raise GradientNotImplementedError

    def _fallback_gradient(self, params, numgrad):
        self_value = partial(self.value, full=False)
        if numgrad:
            gradient = numerical_gradient(self_value, params=params)
        else:
            gradient = autodiff_gradient(self_value, params=params)
        return gradient

    def value_gradient(
        self,
        params: ztyping.ParamTypeInput = None,
        *,
        full: bool | None = None,
        numgrad: bool | None = None,
        paramvals: ztyping.ParamTypeInput = None,
    ) -> tuple[tf.Tensor, tf.Tensor]:
        """Calculate the loss value and the gradient with the current values of the free parameters.

        Args:
            params: The parameters to calculate the gradient for. If not given, all free parameters are used.
            full: |@doc:loss.value.full| If True, return the full loss value, otherwise
               allow for the removal of constants and only return
               the part that depends on the parameters. Constants
               don't matter for the task of optimization, but
               they can greatly help with the numerical stability of the loss function. |@docend:loss.value.full|
            numgrad: |@doc:loss.args.numgrad| If ``True``, calculate the numerical gradient/Hessian
               instead of using the automatic one. This is
               usually slower if called repeatedly but can
               be used if the automatic gradient fails (e.g. if
               the model is not differentiable, written not in znp.* etc).
               Default will fall back to what the loss is set to. |@docend:loss.args.numgrad|
            paramvals: |@doc:loss.args.params| Mapping of the parameter names to the actual
               values. The parameter names refer to the names of the parameters,
               typically :py:class:`~zfit.Parameter`, that is returned by
               `get_params()`. If no params are given, the current default
               values of the parameters are used. |@docend:loss.args.params|

        Returns:
            Calculated loss value as a scalar and the gradient as a tensor.
        """
        params = self._input_check_params(params)
        numgrad = self._options["numgrad"]
        if full is None:
            full = DEFAULT_FULL_ARG
        paramvals, checked = self.check_precompile(params=paramvals)
        with self._check_set_input_params(paramvals, guarantee_checked=checked):
            value, gradient = self._call_value_gradient(params, numgrad, full)
        return value, gradient

    @z.function(wraps="loss")
    def _call_value_gradient(self, params, numgrad, full):
        with suppress(ValueGradientNotImplementedError):
            return self._value_gradient(params=params, numgrad=numgrad, full=full)
        with suppress(GradientNotImplementedError):
            gradient = self._gradient(params=params, numgrad=numgrad)
            return self.value(full=full), gradient
        return self._fallback_value_gradient(params=params, numgrad=numgrad, full=full)

    def value_gradients(self, *_, **__):
        msg = "`value_gradients` is deprecated, use `value_gradient` instead."
        raise BreakingAPIChangeError(msg)

    def _value_gradient(self, params, numgrad, full):  # noqa: ARG002
        raise ValueGradientNotImplementedError

    def _fallback_value_gradient(self, params, numgrad=False, *, full: bool | None = None):
        if full is None:
            full = DEFAULT_FULL_ARG
        self_value = partial(self.value, full=full)
        if numgrad:
            value, gradient = numerical_value_gradient(self_value, params=params)
        else:
            value, gradient = autodiff_value_gradients(self_value, params=params)
        return value, gradient

    def hessian(
        self,
        params: ztyping.ParamTypeInput = None,
        hessian=None,
        *,
        numgrad: bool | None = None,
        paramvals: ztyping.ParamTypeInput = None,
    ) -> tf.Tensor:
        """Calculate the hessian of the loss with respect to the given parameters.

        Args:
        params: The parameters with respect to which the hessian is calculated. If `None`, all parameters
            are used.
        hessian: Can be 'full' or 'diag'.
        numgrad: |@doc:loss.args.numgrad| If ``True``, calculate the numerical gradient/Hessian
               instead of using the automatic one. This is
               usually slower if called repeatedly but can
               be used if the automatic gradient fails (e.g. if
               the model is not differentiable, written not in znp.* etc).
               Default will fall back to what the loss is set to. |@docend:loss.args.numgrad|
        """
        params = self._input_check_params(params)
        numgrad = self._options["numgrad"] if numgrad is None else numgrad
        paramvals, checked = self.check_precompile(params=paramvals)
        with self._check_set_input_params(paramvals, guarantee_checked=checked):
            return self._call_hessian(params, numgrad, hessian)

    def _call_hessian(self, params, numgrad, hessian):
        with suppress(HessianNotImplementedError):
            return self._hessian(params=params, hessian=hessian, numgrad=numgrad)
        with suppress(ValueGradientHessianNotImplementedError):
            return self._value_gradient_hessian(params=params, hessian=hessian, numerical=numgrad, full=False)[2]
        return self._fallback_hessian(params=params, hessian=hessian, numgrad=numgrad)

    def _hessian(self, params, hessian, numgrad):  # noqa: ARG002
        raise HessianNotImplementedError

    def _fallback_hessian(self, params, hessian, numgrad):
        self_value = partial(self.value, full=False)
        if numgrad:
            hessian = numerical_hessian(self_value, params=params, hessian=hessian)
        else:
            hessian = autodiff_hessian(self_value, params=params, hessian=hessian)
        return hessian

    def value_gradient_hessian(
        self,
        params: ztyping.ParamTypeInput = None,
        *,
        hessian=None,
        full: bool | None = None,
        numgrad=None,
        paramvals: ztyping.ParamTypeInput = None,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        """Calculate the loss value, the gradient and the hessian with the current values of the free parameters.

        Args:
            params: The parameters to calculate the gradient for. If not given, all free parameters are used.
            hessian: Can be 'full' or 'diag'.
            full: |@doc:loss.value.full| If True, return the full loss value, otherwise
               allow for the removal of constants and only return
               the part that depends on the parameters. Constants
               don't matter for the task of optimization, but
               they can greatly help with the numerical stability of the loss function. |@docend:loss.value.full|
            numgrad: |@doc:loss.args.numgrad| If ``True``, calculate the numerical gradient/Hessian
               instead of using the automatic one. This is
               usually slower if called repeatedly but can
               be used if the automatic gradient fails (e.g. if
               the model is not differentiable, written not in znp.* etc).
               Default will fall back to what the loss is set to. |@docend:loss.args.numgrad|
            paramvals: |@doc:loss.args.params| Mapping of the parameter names to the actual
               values. The parameter names refer to the names of the parameters,
               typically :py:class:`~zfit.Parameter`, that is returned by
               `get_params()`. If no params are given, the current default
               values of the parameters are used. |@docend:loss.args.params|

        Returns:
            Calculated loss value as a scalar, the gradient as a tensor and the hessian as a tensor.
        """
        params = self._input_check_params(params)
        numgrad = self._options["numhess"] if numgrad is None else numgrad
        if full is None:
            full = DEFAULT_FULL_ARG
        paramvals, checked = self.check_precompile(params=paramvals)
        with self._check_set_input_params(paramvals, guarantee_checked=checked):
            return self._call_value_gradient_hessian(params, numgrad, full, hessian)

    @z.function(wraps="loss")
    def _call_value_gradient_hessian(self, params, numgrad, full, hessian):
        with suppress(ValueGradientHessianNotImplementedError):
            return self._value_gradient_hessian(params=params, hessian=hessian, numerical=numgrad, full=full)
        with suppress(HessianNotImplementedError):
            hessian = self._hessian(params=params, hessian=hessian, numgrad=numgrad)
            return *self.value_gradient(params=params, numgrad=numgrad, full=full), hessian
        return self._fallback_value_gradient_hessian(params=params, hessian=hessian, numgrad=numgrad, full=full)

    def value_gradients_hessian(self, *_, **__):
        msg = "`value_gradients_hessian` is deprecated, use `value_gradient_hessian` instead."
        raise BreakingAPIChangeError(msg)

    def _value_gradient_hessian(self, params, hessian, numerical=False, full: bool | None = None):  # noqa: ARG002
        raise ValueGradientHessianNotImplementedError

    def _fallback_value_gradient_hessian(self, params, hessian, numgrad=False, *, full: bool | None = None):
        self_value = partial(self.value, full=full)
        if numgrad:
            return numerical_value_gradients_hessian(
                func=self_value, gradient=self.gradient, params=params, hessian=hessian
            )
        else:
            return automatic_value_gradients_hessian(self_value, params=params, hessian=hessian)

    def __repr__(self) -> str:
        class_name = repr(self.__class__)[:-2].split(".")[-1]
        return (
            f"<{class_name} "
            f"model={one_two_many([model.name for model in self.model])} "
            f"data={one_two_many([data.name for data in self.data])} "
            f'constraints={one_two_many(self.constraints, many="True")} '
            f">"
        )

    def __str__(self) -> str:
        class_name = repr(self.__class__)[:-2].split(".")[-1]
        return (
            f"<{class_name}"
            f" model={one_two_many(list(self.model))}"
            f" data={one_two_many(list(self.data))}"
            f' constraints={one_two_many(self.constraints, many="True")}'
            f">"
        )


def one_two_many(values, n=3, many="multiple"):
    values = convert_to_container(values)
    if len(values) > n:
        values = many
    return values


class BaseUnbinnedNLL(BaseLoss, SerializableMixin):
    def create_new(
        self,
        model: ZfitPDF | Iterable[ZfitPDF] | None = NONE,
        data: ZfitData | Iterable[ZfitData] | None = NONE,
        fit_range=NONE,
        constraints=NONE,
        options=NONE,
    ):
        r"""Create a new loss from the current loss and replacing what is given as the arguments.

        This creates a "copy" of the current loss but replaces any argument that is explicitly given.
        Equivalent to creating a new instance but with some arguments taken.

        A loss has more than a model and data (and constraints), it can have internal optimizations
        and more that may do alter the behavior of a naive re-instantiation in unpredictable ways.

        Args:
            model: If not given, the current one will be used.
                |@doc:loss.init.model| PDFs that return the normalized probability for
               *data* under the given parameters.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit. |@docend:loss.init.model|
            data: If not given, the current one will be used.
                |@doc:loss.init.data| Dataset that will be given to the *model*.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit.
               If the data is not a ``ZfitData`` object, i.e. it doesn't have ha space
               it has to be withing the limits of the model, otherwise, an
               :py:class:`~zfit.exception.IntentionAmbiguousError` will be raised. |@docend:loss.init.data|
            fit_range:
            constraints: If not given, the current one will be used.
                |@doc:loss.init.constraints| Auxiliary measurements ("constraints")
               that add a likelihood term to the loss.

               .. math::
                 \mathcal{L}(\theta) = \mathcal{L}_{unconstrained} \prod_{i} f_{constr_i}(\theta)

               Usually, an auxiliary measurement -- by its very nature -S  should only be added once
               to the loss. zfit does not automatically deduplicate constraints if they are given
               multiple times, leaving the freedom for arbitrary constructs.

               Constraints can also be used to restrict the loss by adding any kinds of penalties. |@docend:loss.init.constraints|
            options: If not given, the current one will be used.
                |@doc:loss.init.options| Additional options (as a dict) for the loss.
               Current possibilities include:

               - 'subtr_const' (default True): subtract from each points
                 log probability density a constant that
                 is approximately equal to the average log probability
                 density in the very first evaluation before
                 the summation. This brings the initial loss value closer to 0 and increases,
                 especially for large datasets, the numerical stability.

                 The value will be stored ith 'subtr_const_value' and can also be given
                 directly.

                 The subtraction should not affect the minimum as the absolute
                 value of the NLL is meaningless. However,
                 with this switch on, one cannot directly compare
                 different likelihoods absolute value as the constant
                 may differ! Use ``create_new`` in order to have a comparable likelihood
                 between different losses or use the ``full`` argument in the value function
                 to calculate the full loss with all constants.


               These settings may extend over time. In order to make sure that a loss is the
               same under the same data, make sure to use ``create_new`` instead of instantiating
               a new loss as the former will automatically overtake any relevant constants
               and behavior. |@docend:loss.init.options|
        """
        if model is NONE:
            model = self.model
        if data is NONE:
            data = self.data
        if fit_range is NONE:
            fit_range = self.fit_range
        if constraints is NONE:
            constraints = self.constraints
            if constraints is not None:
                constraints = constraints.copy()
        if options is NONE:
            options = self._options
            if isinstance(options, dict):
                options = options.copy()
        return type(self)(
            model=model,
            data=data,
            fit_range=fit_range,
            constraints=constraints,
            options=options,
        )


class UnbinnedNLL(BaseUnbinnedNLL):
    _name = "UnbinnedNLL"

    def __init__(
        self,
        model: ZfitPDF | Iterable[ZfitPDF],
        data: ZfitData | Iterable[ZfitData],
        fit_range=None,
        constraints: ztyping.ConstraintsInputType = None,
        options: Mapping[str, object] | None = None,
    ):
        r"""Unbinned Negative Log Likelihood.

        |@doc:loss.init.explain.unbinnednll| The unbinned log likelihood can be written as

        .. math::
            \mathcal{L}_{non-extended}(x | \theta) = \prod_{i} f_{\theta} (x_i)

        where :math:`x_i` is a single event from the dataset *data* and f is the *model*. |@docend:loss.init.explain.unbinnednll|

        |@doc:loss.init.explain.simultaneous| A simultaneous fit can be performed by giving one or more ``model``, ``data``, to the loss. The
        length of each has to match the length of the others

        .. math::
            \mathcal{L}_{simultaneous}(\theta | {data_0, data_1, ..., data_n})
            = \prod_{i} \mathcal{L}(\theta_i, data_i)

        where :math:`\theta_i` is a set of parameters and
        a subset of :math:`\theta` |@docend:loss.init.explain.simultaneous|

        |@doc:loss.init.explain.negativelog| For optimization purposes, it is often easier
        to minimize a function and to use a log transformation. The actual loss is given by

        .. math::
             \mathcal{L} = - \sum_{i}^{n} ln(f(\theta|x_i))

        and therefore being called "negative log ..." |@docend:loss.init.explain.negativelog|

        |@doc:loss.init.explain.weightednll| If the dataset has weights, a weighted likelihood will be constructed instead

        .. math::
            \mathcal{L} = - \sum_{i}^{n} w_i \cdot ln(f(\theta|x_i))

        Note that this is not a real likelihood anymore! Calculating uncertainties
        can be done with hesse (as it has a correction) but will yield wrong
        results with profiling methods. The minimum is however fully valid. |@docend:loss.init.explain.weightednll|
        Args:
            model: |@doc:loss.init.model| PDFs that return the normalized probability for
               *data* under the given parameters.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit. |@docend:loss.init.model|
            data: |@doc:loss.init.data| Dataset that will be given to the *model*.
               If multiple model and data are given, they will be used
               in the same order to do a simultaneous fit.
               If the data is not a ``ZfitData`` object, i.e. it doesn't have ha space
               it has to be withing the limits of the model, otherwise, an
               :py:class:`~zfit.exception.IntentionAmbiguousError` will be raised. |@docend:loss.init.data|
            constraints: |@doc:loss.init.constraints| Auxiliary measurements ("constraints")
               that add a likelihood term to the loss.

               .. math::
                 \mathcal{L}(\theta) = \mathcal{L}_{unconstrained} \prod_{i} f_{constr_i}(\theta)

               Usually, an auxiliary measurement -- by its very nature -S  should only be added once
               to the loss. zfit does not automatically deduplicate constraints if they are given
               multiple times, leaving the freedom for arbitrary constructs.

               Constraints can also be used to restrict the loss by adding any kinds of penalties. |@docend:loss.init.constraints|
            options: If not given, the current one will be used.
                |@doc:loss.init.options| Additional options (as a dict) for the loss.
               Current possibilities include:

               - 'subtr_const' (default True): subtract from each points
                 log probability density a constant that
                 is approximately equal to the average log probability
                 density in the very first evaluation before
                 the summation. This brings the initial loss value closer to 0 and increases,
                 especially for large datasets, the numerical stability.

                 The value will be stored ith 'subtr_const_value' and can also be given
                 directly.

                 The subtraction should not affect the minimum as the absolute
                 value of the NLL is meaningless. However,
                 with this switch on, one cannot directly compare
                 different likelihoods absolute value as the constant
                 may differ! Use ``create_new`` in order to have a comparable likelihood
                 between different losses or use the ``full`` argument in the value function
                 to calculate the full loss with all constants.


               These settings may extend over time. In order to make sure that a loss is the
               same under the same data, make sure to use ``create_new`` instead of instantiating
               a new loss as the former will automatically overtake any relevant constants
               and behavior. |@docend:loss.init.options|
        """
        super().__init__(
            model=model,
            data=data,
            fit_range=fit_range,
            constraints=constraints,
            options=options,
        )
        self._errordef = 0.5
        extended_pdfs = [pdf for pdf in self.model if pdf.is_extended]
        if extended_pdfs and type(self) == UnbinnedNLL:
            warn_advanced_feature(
                f"Extended PDFs ({extended_pdfs}) are given to a normal UnbinnedNLL. "
                f" This won't take the yield "
                "into account and simply treat the PDFs as non-extended PDFs. To create an "
                "extended NLL, use the `ExtendedUnbinnedNLL`.",
                identifier="extended_in_UnbinnedNLL",
            )

    def _loss_func(self, model, data, fit_range, constraints, log_offset):
        return self._loss_func_watched(
            data=data,
            model=model,
            fit_range=fit_range,
            constraints=constraints,
            log_offset=log_offset,
        )

    @property
    def is_extended(self):
        return False

    @z.function(wraps="loss")
    def _loss_func_watched(self, data, model, fit_range, constraints, log_offset):
        nll = _unbinned_nll_tf(model=model, data=data, fit_range=fit_range, log_offset=log_offset)
        if constraints:
            constraints = z.reduce_sum([c.value() for c in constraints])
            nll += constraints
        return nll

    def _get_params(
        self,
        floating: bool | None = True,
        is_yield: bool | None = None,
        extract_independent: bool | None = True,
    ) -> set[ZfitParameter]:
        if not self.is_extended:
            is_yield = False  # the loss does not depend on the yields
        return super()._get_params(floating, is_yield, extract_independent)


class UnbinnedNLLRepr(BaseLossRepr):
    _implementation = UnbinnedNLL
    hs3_type: Literal["UnbinnedNLL"] = pydantic.Field("UnbinnedNLL", alias="type")


class ExtendedUnbinnedNLL(BaseUnbinnedNLL):
    def __init__(
        self,
        model: ZfitPDF | Iterable[ZfitPDF],
        data: ZfitData | Iterable[ZfitData],
        fit_range=None,
        constraints: ztyping.ConstraintsInputType = None,
        options: Mapping[str, object] | None = None,
    ):
        r"""An Unbinned Negative Log Likelihood with an additional poisson term for the number of events in the dataset.

        |@doc:loss.init.explain.unbinnednll| The unbinned log likelihood can be written as

        .. math::
            \mathcal{L}_{non-extended}(x | \theta) = \prod_{i} f_{\theta} (x_i)

        where :math:`x_i` is a single event from the dataset *data* and f is the *model*. |@docend:loss.init.explain.unbinnednll|

        |@doc:loss.init.explain.extendedterm| The extended likelihood has an additional term

        .. math::
            \mathcal{L}_{extended term} = poiss(N_{tot}, N_{data})
            = N_{data}^{N_{tot}} \frac{e^{- N_{data}}}{N_{tot}!}

        and the extended likelihood is the product of both. |@docend:loss.init.explain.extendedterm|

        |@doc:loss.init.explain.simultaneous| A simultaneous fit can be performed by giving one or more ``model``, ``data``, to the loss. The
        length of each has to match the length of the others

        .. math::
            \mathcal{L}_{simultaneous}(\theta | {data_0, data_1, ..., data_n})
            = \prod_{i} \mathcal{L}(\theta_i, data_i)

        where :math:`\theta_i` is a set of parameters and
        a subset of :math:`\theta` |@docend:loss.init.explain.simultaneous|

        |@doc:loss.init.explain.negativelog| For optimization purposes, it is often easier
        to minimize a function and to use a log transformation. The actual loss is given by

        .. math::
             \mathcal{L} = - \sum_{i}^{n} ln(f(\theta|x_i))

        and therefore being called "negative log ..." |@docend:loss.init.explain.negativelog|

        |@doc:loss.init.explain.weightednll| If the dataset has weights, a weighted likelihood will be constructed instead

        .. math::
            \mathcal{L} = - \sum_{i}^{n} w_i \cdot ln(f(\theta|x_i))

        Note that this is not a real likelihood anymore! Calculating uncertainties
        can be done with hesse (as it has a correction) but will yield wrong
        results with profiling methods. The minimum is however fully valid. |@docend:loss.init.explain.weightednll|
        """
        super().__init__(
            model=model,
            data=data,
            constraints=constraints,
            options=options,
            fit_range=fit_range,
        )
        self._errordef = 0.5

    @z.function(wraps="loss")
    def _loss_func(self, model, data, fit_range, constraints, log_offset):
        nll = _unbinned_nll_tf(model=model, data=data, fit_range=fit_range, log_offset=log_offset)
        if constraints:
            constraints = z.reduce_sum([c.value() for c in constraints])
            nll += constraints
        yields = []
        nevents_collected = []
        for mod, dat in zip(model, data):
            if not mod.is_extended:
                msg = f"The pdf {mod} is not extended but has to be (for an extended fit)"
                raise NotExtendedPDFError(msg)
            nevents = dat.n_events if dat.weights is None else z.reduce_sum(dat.weights)
            nevents = znp.asarray(nevents, tf.float64)
            nevents_collected.append(nevents)
            yields.append(mod.get_yield())
        yields = znp.stack(yields, axis=0)
        nevents_collected = znp.stack(nevents_collected, axis=0)

        term_new = tf.nn.log_poisson_loss(nevents_collected, znp.log(yields), compute_full_loss=log_offset is False)
        if log_offset is not False:
            log_offset = znp.asarray(log_offset, dtype=znp.float64)
            term_new += log_offset
        nll += znp.sum(term_new, axis=0)
        return nll

    @property
    def is_extended(self):
        return True

    def _get_params(
        self,
        floating: bool | None = True,
        is_yield: bool | None = None,
        extract_independent: bool | None = True,
    ) -> set[ZfitParameter]:
        return super()._get_params(floating, is_yield, extract_independent)


class ExtendedUnbinnedNLLRepr(BaseLossRepr):
    _implementation = ExtendedUnbinnedNLL
    hs3_type: Literal["ExtendedUnbinnedNLL"] = pydantic.Field("ExtendedUnbinnedNLL", alias="type")


class SimpleLoss(BaseLoss):
    _name = "SimpleLoss"

    @deprecated_args(None, "Use params instead.", ("deps", "dependents"))
    def __init__(
        self,
        func: Callable,
        params: Iterable[zfit.Parameter] | None = None,
        errordef: float | None = None,
        *,
        gradient: Callable | None = None,
        hessian: Callable | None = None,
        # legacy
        deps: Iterable[zfit.Parameter] = NONE,
        dependents: Iterable[zfit.Parameter] = NONE,
    ):
        r"""Loss from a (function returning a) Tensor.

        This allows for a very generic loss function as the functions only restriction is that is
        should depend on ``zfit.Parameter``.

        Args:
            func: Callable that constructs the loss and returns a tensor without taking an argument.
            params: The dependents (independent ``zfit.Parameter``) of the loss. Essentially the (free) parameters that
              the ``func`` depends on.
            errordef: Definition of which change in the loss corresponds to a change of 1 sigma.
                For example, 1 for Chi squared, 0.5 for negative log-likelihood.
            gradient: Function that calculates the gradient of the loss with respect to the parameters. If not given,
                the gradient will be calculated automatically.
            hessian: Function that calculates the hessian of the loss with respect to the parameters.
                If not given, the hessian will be calculated automatically.

        Usage:

        .. code-block:: python

            import zfit
            import zfit.z.numpy as znp
            import tensorflow as tf


            param1 = zfit.Parameter('param1', 5, 1, 10)
            # we can build a model here if we want, but in principle, it's not necessary

            x = znp.random.uniform(size=(100,))
            y = x * tf.random.normal(mean=4, stddev=0.1, shape=x.shape, dtype=znp.float64)


            def squared_loss(params):
                param1 = params[0]
                y_pred = x*param1  # this is very simple, but we can of course use any
                # zfit PDF or Func inside
                squared = (y_pred - y)**2
                mse = znp.mean(squared)
                return mse


            loss = zfit.loss.SimpleLoss(squared_loss, param1, errordef=1)

        which can then be used in combination with any zfit minimizer such as Minuit

        .. code:: python

            minimizer = zfit.minimize.Minuit()
            result = minimizer.minimize(loss)
        """
        super().__init__(model=[], data=[], options={"subtr_const": False})
        if dependents is not NONE and params is None:
            params = dependents
        elif deps is not NONE and params is None:  # depreceation
            params = deps
        elif params is None:  # legacy, remove in 0.7
            msg = (
                "params need to be specified explicitly due to the upgrade to 0.4."
                "More information can be found in the upgrade guide on the website."
            )
            raise BreakingAPIChangeError(msg)

        if hasattr(func, "errordef"):
            if errordef is not None:
                msg = "errordef is not allowed if func has an errordef attribute or vice versa."
                raise ValueError(msg)
            errordef = func.errordef

        if errordef is None:
            msg = (
                f"{self} cannot minimize {func} as `errordef` is missing: "
                f"it has to be set as an attribute. Typically 1 (chi2) or 0.5 (NLL)."
            )
            raise ValueError(msg)

        self._simple_func = func
        self._errordef = errordef
        self._grad_fn = gradient
        self._hess_fn = hessian
        params = convert_to_parameters(params, prefer_constant=False)
        self._params = params
        self._simple_func_params = _extract_dependencies(params)

    def _get_dependencies(self):
        return self._simple_func_params

    def _get_params(
        self,
        floating: bool | None = True,
        is_yield: bool | None = None,
        extract_independent: bool | None = True,
    ) -> set[ZfitParameter]:
        params = super()._get_params(floating, is_yield, extract_independent)
        own_params = extract_filter_params(self._params, floating=floating, extract_independent=extract_independent)
        return params.union(own_params)

    def _gradient(self, params, numgrad):
        del numgrad
        if self._grad_fn is not None:
            return self._grad_fn(params)
        raise GradientNotImplementedError

    def _hessian(self, params, hessian, numgrad):
        del hessian, numgrad
        if self._hess_fn is not None:
            return self._hess_fn(params)
        raise HessianNotImplementedError

    @property
    def errordef(self):
        errordef = self._errordef
        if errordef is None:
            msg = "For this SimpleLoss, no error calculation is possible."
            raise RuntimeError(msg)
        return errordef

    def _loss_func(self, model, data, fit_range, constraints=None, log_offset=None):  # noqa: ARG002
        if log_offset is not None and log_offset is not False:
            pass
            # raise ValueError(msg)
        try:
            params = self._simple_func_params
            params = tuple(params)
            value = self._simple_func(params)
        except TypeError as error:
            if "takes 0 positional arguments but 1 was given" in str(error):
                value = self._simple_func()
            else:
                raise error
        return znp.asarray(value)

    def __add__(self, other):
        msg = "Cannot add a SimpleLoss, 'addition' of losses can mean anything." "Add them manually"
        raise IntentionAmbiguousError(msg)

    def create_new(
        self,
        func: Callable = NONE,
        params: Iterable[zfit.Parameter] = NONE,
        errordef: float | None = NONE,
    ):
        if func is NONE:
            func = self._simple_func
        if params is NONE:
            params = self._params
        if errordef is NONE:
            errordef = self.errordef

        return type(self)(func=func, params=params, errordef=errordef)
