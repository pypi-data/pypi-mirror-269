# -*- coding: utf-8 -*-
# Copyright (c) 2022 RaptorML authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The LabSDK provides a set of decorators that can be used to configure the assets in a way that can be translated to an
optimized production-ready solution by Raptor.
"""

import inspect
import sys
import types
from datetime import timedelta
from typing import Union, List, Dict, Optional, Callable
from warnings import warn

from pandas import DataFrame
from pydantic import TypeAdapter
from typing_extensions import TypedDict, _TypedDictMeta

from . import local_state, config, replay
from ._internal import durpy
from .program import Program
from .program import normalize_selector
from .types import FeatureSpec, AggrSpec, AggregationFunction, Primitive, DataSourceSpec, ModelFramework, ModelServer, \
    KeepPreviousSpec, ModelImpl
from .types.dsrc_config_stubs.protocol import SourceProductionConfig
from .types.dsrc_config_stubs.rest import RestConfig

if sys.version_info >= (3, 8):
    from typing import _TypedDictMeta as typing_TypedDictMeta
else:
    typing_TypedDictMeta = type(None)


def _wrap_decorator_err(f):
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            back_frame = e.__traceback__.tb_frame.f_back
            tb = types.TracebackType(tb_next=None,
                                     tb_frame=back_frame,
                                     tb_lasti=back_frame.f_lasti,
                                     tb_lineno=back_frame.f_lineno)
            raise Exception(f'in {args[0].__name__}: {str(e)}').with_traceback(tb)

    return wrap


@_wrap_decorator_err
def _opts(func, options: dict):
    if hasattr(func, 'raptor_spec'):
        raise Exception('option decorators must be before the registration decorator')
    if not hasattr(func, '__raptor_options'):
        func.__raptor_options = {}

    for k, v in options.items():
        func.__raptor_options[k] = v
    return func


# ** Shared **
def namespace(namespace: str):
    """
    Register a namespace for the asset.
    :type namespace: str
    :param namespace: the name of namespace to attach the asset to.

    **Example**:

    ```python
    @namespace('my_namespace')
    ```
    """

    def decorator(func):
        return _opts(func, {'namespace': namespace})

    return decorator


def runtime(
    packages: Optional[List[str]],  # list of PIP installable packages
    env_name: Optional[str],  # the Raptor virtual environment name
):
    """
    Register the runtime environment for the asset.
    :type packages: list of str
    :param packages: list of PIP installable packages. You can specify a version pip notation, e.g. 'numpy==1.19.5' or
        'numpy>=1.19.5'.
    :type env_name: str
    :param env_name: the name of the runtime virtual environment name. The environment should be pre-configured in
        the Raptor Core installation by your DevOps. Defaults to the 'default' runtime if not specified.

    **Example**:

    >>> @runtime(packages=['numpy==1.21.1', 'phonenumbers'], env_name='default')
    """

    def decorator(func):
        return _opts(func, {'runtime': {
            'packages': packages,
            'env_name': env_name,
        }})

    return decorator


def freshness(
    max_age: Union[str, timedelta],
    max_stale: Optional[Union[str, timedelta]] = None,  # defaults to == max_age
    timeout: Optional[Union[str, timedelta]] = timedelta(seconds=1),  # defaults to 1 seconds
):
    """
    Set the freshness policy, and timeout of a feature or model. It is required so Raptor will be able to match the
    production behaviour with the development behaviour.
    This decorator must be used in conjunction with a feature or model decorator.

    Feature or Model values are considered fresh if they are younger than the `max_age`.
    If the value is older than `max_age`, we'll try to recompute it with a timeout of `timeout`.
    If we fail to recompute the value within `timeout`, we'll return the stale value as long as it is younger than
    `max_stale`.

    :type max_age: timedelta or str of the form '2h 3m 4s'
    :param max_age: the maximum age of a feature or model value. If the calculated value is older than `max_age`, we'll
        try to recompute the value.
    :type max_stale: timedelta or str of the form '2h 3m 4s'
    :param max_stale: the time after which the feature or model is considered stale. If the
        value is older than `max_stale`, we'll return `None`. Defaults to `max_age`.
    :type timeout: timedelta or str of the form '2h 3m 4s'
    :param timeout: the maximum time allowed for the feature to be computed. defaults to 1 second.

    **Example**:

    ```python
    @freshness(max_age='1h', max_stale='2h', timeout='10s')
    ```
    """
    if max_stale is None:
        max_stale = max_age

    def decorator(func):
        return _opts(func, {'freshness': {
            'max_age': max_age,
            'max_stale': max_stale,
            'timeout': timeout,
        }})

    return decorator


def labels(labels: Dict[str, str]):
    """
    Register labels for the asset.
    :type labels: dict<str,str> (key, value)
    :param labels: a dictionary of tags.

    **Example**:

    ```python
    @labels({'owner': '@AlmogBaku', 'team': 'search'})
    ```
    """

    def decorator(func):
        return _opts(func, {'labels': labels})

    return decorator


# ** Data Source **

def data_source(
    training_data: DataFrame,  # training data
    keys: Optional[Union[str, List[str]]] = None,
    name: Optional[str] = None,  # inferred from class name
    timestamp: Optional[str] = None,  # what column has the timestamp
    production_config: Optional[SourceProductionConfig] = None,  # production stub configuration
):
    """
    Register a DataSource asset. The data source is a class that represents the schema of the data source in production.
    It is used to validate the data source in production and to connect the data source to the feature and model assets.

    **Class signature**:

    This decorator should wrap a class that inherits from `typing_extensions.TypedDict`, the class content is optional
    and should reflect the schema of the data source.


    :type training_data: DataFrame
    :param training_data: DataFrame of training data. This should reflect the schema of the data source in production.
    :type keys: str or list of str
    :param keys: list of columns that are keys.
    :type name: str
    :param name: name of the data source. Defaults to the class name.
    :type timestamp: str
    :param timestamp: name of the timestamp column. If not specified, the timestamp is inferred from the training data.
    :type production_config: SourceProductionConfig
    :type production_config: this is a stub for the production configuration. It is not used in training, but is helpful
            for making sense of the source, the production behavior, and a preparation for the production deployment.
            To connect the data source to the production data source, your DevOps should configure the production
            configuration later, with the generated stub.

    :returns:
    A wrapped class with additional methods and properties:
        - `raptor_spec` - the Raptor specification object.
        - `manifest(to_file: bool = False)` - a function that returns the data source manifest. If `to_file` is True,
            the manifest is written to a file.
        - `export()` - a function that exports the data source to the `out` directory.

    **Example**:

    ```python
    @data_source(
        training_data=pd.read_csv('deals.csv'),
        keys=['id', 'account_id'],
        timestamp='event_at',
    )
    class Deal(typing_extensions.TypedDict):
        id: int
        event_at: pd.Timestamp
        account_id: str
        amount: float
        currency: str
        is_win: bool
    ```
    """

    options = {}

    if isinstance(keys, str):
        keys = [keys]

    @_wrap_decorator_err
    def decorator(cls: TypedDict):
        if isinstance(cls, typing_TypedDictMeta):
            raise Exception('You should use typing_extensions.TypedDict instead of typing.TypedDict')
        elif not isinstance(cls, _TypedDictMeta):
            raise Exception('data_source decorator must be used on a class that extends typing_extensions.TypedDict')

        nonlocal name
        if name is None:
            name = cls.__name__

        spec = DataSourceSpec(name=name, description=cls.__doc__, keys=keys, timestamp=timestamp,
                              production_config=production_config)
        spec.local_df = training_data

        if hasattr(cls, '__raptor_options'):
            for k, v in cls.__raptor_options.items():
                options[k] = v

        if 'labels' in options:
            spec.labels = options['labels']

        if 'namespace' in options:
            spec.namespace = options['namespace']

        # convert cls to json schema
        spec.schema = TypeAdapter(cls).json_schema()

        # register
        cls.raptor_spec = spec
        cls.manifest = spec.manifest
        cls.export = spec.manifest
        local_state.register_spec(spec)

        if hasattr(cls, '__raptor_options'):
            del cls.__raptor_options

        return cls

    return decorator


# ** Feature **

def aggregation(
    function: Union[AggregationFunction, List[AggregationFunction], str, List[str]],
    over: Union[str, timedelta, None],
    granularity: Union[str, timedelta, None],
):
    """
    Registers aggregations for the Feature Definition.
    :type function: AggregationFunction or List[AggregationFunction] or str or List[str]
    :param function: a list of :func:`AggrFn`.
    :type over: str or timedelta in the form '2h 3m 4s'
    :param over: the time period over which to aggregate.
    :type granularity: str or timedelta in the form '2h 3m 4s'
    :param granularity: the granularity of the aggregation (this is overriding the freshness' `max_age`).

    **Example**:

    ```python
    @aggregation(
       function=['sum', 'count', 'avg'],
       over='1d',
       granularity='1h',
    )
    ```
    """

    if isinstance(function, str):
        function = [AggregationFunction.parse(function)]

    if not isinstance(function, List):
        function = [function]

    for i, f in enumerate(function):
        if isinstance(f, str):
            function[i] = AggregationFunction.parse(f)

    if isinstance(over, str):
        over = durpy.from_str(over)
    if isinstance(granularity, str):
        granularity = durpy.from_str(granularity)

    def decorator(func):
        for fn in function:
            if fn == AggregationFunction.Unknown:
                raise Exception('Unknown aggr function')
        return _opts(func, {'aggr': AggrSpec(function, over, granularity)})

    return decorator


def keep_previous(versions: int, over: Union[str, timedelta]):
    """
    Keep previous versions of the feature.
    :type versions: int
    :param versions: the number of versions to keep (excluding the current value).
    :type over: str or timedelta in the form '2h 3m 4s'
    :param over: the maximum time period to keep a previous values in the history since the last update. You can specify
                    `0` to keep the value until the next update.

    **Example**:

    ```python
    @keep_previous(versions=3, over='1d')
    ```
    """

    if isinstance(over, str):
        over = durpy.from_str(over)

    def decorator(func):
        return _opts(func, {'keep_previous': KeepPreviousSpec(versions, over)})

    return decorator


def feature(
    keys: Union[str, List[str]],
    name: Optional[str] = None,  # set to function name if not provided
    data_source: Optional[Union[str, object]] = None,  # set to None for sourceless
    sourceless_markers_df: Optional[DataFrame] = None,  # timestamp and keys markers for training sourceless features
):
    """
    Registers a Feature Definition within the LabSDK.

    A feature definition is a Python handler function that process a calculation request and calculates the feature
    value.


    **Feature signature**:

    The function signature of a feature definition must accept two arguments:

    1. `this_row` - A dictionary of the current row (this is reflects the schema of the data source).
    2. `Context` - A dictionary of the context. See [Context](/docs/how-it-works/features/context) for
       more details.

    It must use a return type annotation to indicate the primitive type of the feature value.

    :type keys: str or List[str]
    :param keys: a list of indexing keys, indicated the owner of the feature value.
    :type name: str
    :param name: the name of the feature. If not provided, the function name will be used.
    :type data_source: str or DataSource object
    :param data_source: the (fully qualified) name of the DataSource or a reference to the DataSource object.
    :type sourceless_markers_df: DataFrame
    :param sourceless_markers_df: a DataFrame with the timestamp and keys markers for training sourceless features. It
            a timestamp column, and a column for each key.

    :rtype: function
    :returns:
    It returns a wrapped function with a few additional methods/properties:
        * `raptor_spec` - The Raptor specification of the feature.
        * `replay()` - A function that can be used to replay the feature calculation using the training sata of the source.
        * `manifest(to_file=False)` - A function that returns the manifest of the feature.
        * `export(with_dependent_source=True)` - A function that exports the feature to `out` directory.

    **Example**:
    ```python
    @feature(keys='account_id', data_source=Deal)
    @freshness(max_age='1h', max_stale='2h')
    def last_amount(this_row: Deal, ctx: Context) -> float:
        return this_row['amount']
    ```
    """
    options = {}

    if not isinstance(keys, List):
        keys = [keys]

    if data_source is not None:
        if hasattr(data_source, 'raptor_spec'):
            if not isinstance(data_source.raptor_spec, DataSourceSpec):
                raise Exception(
                    'data_source decorator must be used on a class that extends typing_extensions.TypedDict')
        elif not isinstance(data_source, str):
            raise Exception('data_source must be a string or a DataSource class')

    if sourceless_markers_df is not None:
        if hasattr(sourceless_markers_df, 'raptor_spec'):
            if isinstance(sourceless_markers_df.raptor_spec, DataSourceSpec):
                sourceless_markers_df = sourceless_markers_df.raptor_spec.local_df
            else:
                raise Exception('sourceless_markers_df must be a pandas.DataFrame or a DataSource class')
        elif not isinstance(sourceless_markers_df, DataFrame):
            raise Exception('sourceless_markers_df must be a pandas.DataFrame or a DataSource class')

    @_wrap_decorator_err
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__

        spec = FeatureSpec(name=name, description=func.__doc__, keys=keys)

        if hasattr(func, '__raptor_options'):
            for k, v in func.__raptor_options.items():
                options[k] = v

        spec.data_source = data_source
        spec.sourceless_df = sourceless_markers_df

        # append annotations
        if 'labels' in options:
            spec.labels = options['labels']

        if 'namespace' in options:
            spec.namespace = options['namespace']

        if 'aggr' in options:
            spec.freshness = options['aggr'].granularity
            spec.staleness = options['aggr'].over
            if data_source is not None and isinstance(data_source, RestConfig):
                warn('Beware: aggregations for REST might not behave as you expect. '
                     'Read the documentation for more info.')

        if 'freshness' in options:
            spec.freshness = options['freshness']['max_age']
            spec.staleness = options['freshness']['max_stale']
            spec.timeout = options['freshness']['timeout']

        if 'keep_previous' in options:
            spec.keep_previous = options['keep_previous']

        if spec.freshness is None or spec.staleness is None:
            raise Exception('You must specify freshness or aggregation for a feature')

        if 'runtime' in options:
            spec.builder.runtime = options['runtime']['env_name']
            spec.builder.packages = options['runtime']['packages']

        # parse the program
        def feature_obj_resolver(obj: str) -> str:
            """
            Resolve a feature object to its fully qualified name.
            :param obj:  the object name as defined in the global scope of the feature function.
            :return: the fully qualified name of the object.
            """
            frame = inspect.currentframe().f_back.f_back

            feat: Union[FeatureSpec, None] = None
            if obj in frame.f_globals:
                if hasattr(frame.f_globals[obj], 'raptor_spec'):
                    feat = frame.f_globals[obj].raptor_spec
            elif obj in frame.f_locals:
                if hasattr(frame.f_locals[obj], 'raptor_spec'):
                    feat = frame.f_locals[obj].raptor_spec
            if feat is None:
                raise Exception(f'Cannot resolve {obj} to an FQN')

            if feat.aggr is not None:
                raise Exception('You must specify a Feature Selector with AggrFn(i.e. `namespace.name+sum`) for '
                                'aggregated features')

            return feat.fqn()

        spec.program = Program(func, feature_obj_resolver)
        spec.primitive = Primitive.parse(spec.program.primitive)

        # aggr parsing should be after program parsing
        if 'aggr' in options:
            for f in options['aggr'].funcs:
                if not f.supports(spec.primitive):
                    raise Exception(
                        f'{func.__name__} aggr function {f} not supported for primitive {spec.primitive}')
            spec.aggr = options['aggr']

        # register
        func.raptor_spec = spec
        func.replay = replay.new_replay(spec)
        func.manifest = spec.manifest
        func.export = spec.manifest
        local_state.register_spec(spec)

        if hasattr(func, '__raptor_options'):
            del func.__raptor_options

        return func

    return decorator


# ** Model **

def model(
    keys: Union[str, List[str]],  # required
    input_features: Union[str, List[str], Callable, List[Callable]],  # required
    input_labels: Union[str, List[str], Callable, List[Callable]],
    model_framework: Union[ModelFramework, str],
    model_server: Optional[Union[ModelServer, str]] = None,
    key_feature: Optional[Union[str, Callable]] = None,  # optional
    prediction_output_schema: Optional[TypedDict] = None,
    name: Optional[str] = None,  # set to function name if not provided
):
    """
    Register a Model Definition within the LabSDK.

    **Function Signature**:

    This decorator should wrap a training function that returns a trained model.
    The function signature of a model definition must accept `TrainingContext` as an argument.

    :type keys: str or list of str
    :param keys: the keys of the model. The keys are required for fetching the features.
    :type input_features: str or list of str or callable or list of callable
    :param input_features: the features that are used as input to the model.
    :type input_labels: str or list of str or callable or list of callable
    :param input_labels: the labels that are used as input to the model.
    :type model_framework: ModelFramework or str
    :param model_framework: the model framework used to train the model.
    :type model_server: ModelServer or str
    :param model_server: the model server used to serve the model.
    :type key_feature: str or callable
    :param key_feature: the feature that is used for joining the features together.
    :type prediction_output_schema: TypedDict
    :param prediction_output_schema: the schema of the prediction output.
    :type name: str
    :param name: the name of the model. If not provided, the name will be the function name.

    :rtype: class
    :returns:
    a wrapped function `train()` that runs your training function with the `TrainingContext` provided.

    It also provides a few new methods/properties to the returned function:

    * `raptor_spec` - The Raptor spec of the model.
    * `train()` - The training function.
    * `features_and_labels()` - A function that returns a DataFrame of the features and labels.
    * `manifest(to_file=False)` - A function that returns the manifest of the model.
    * `export(with_dependent_features=True, with_dependent_sources=True)` - A function that exports the model to the `out` directory.
    * `keys` - the keys of the model.
    * `input_features` - the input features of the model.
    * `input_labels` - the input labels of the model.

    :rtype: function

    **Example**:

    ```python
    @model(
        keys=['customer_id'],
        input_features=['total_spend+sum'],
        input_labels=[amount],
        model_framework='sklearn',
        model_server='sagemaker-ack',
    )
    @freshness(max_age='1h', max_stale='100h')
    def amount_prediction(ctx: TrainingContext):
        from sklearn.linear_model import LinearRegression

        df = ctx.features_and_labels()

        trainer = LinearRegression()
        trainer.fit(df[ctx.input_features], df[ctx.input_labels])

        return trainer
    ```
    """
    options = {}

    if not isinstance(keys, List):
        keys = [keys]

    if model_server is not None:
        model_server = ModelServer.parse(model_server)

    model_framework = ModelFramework.parse(model_framework)

    def normalize_features(features: Union[str, List[str], Callable, List[Callable]]) -> List[str]:
        if not isinstance(features, List):
            features = [features]

        fts = []
        for f in features:
            if type(f) is str:
                local_state.feature_spec_by_selector(f)
                fts.append(normalize_selector(f, config.default_namespace))
            elif isinstance(f, Callable):
                if not hasattr(f, 'raptor_spec'):
                    raise Exception(f'{f.__name__} is not a registered feature')
                if f.raptor_spec.aggr is not None:
                    raise Exception(f'{f.__name__} is an aggregated feature. You must specify a Feature Selector.')
                fts.append(f.raptor_spec.fqn())
            elif isinstance(f, FeatureSpec):
                fts.append(f.fqn())
        return fts

    input_features = normalize_features(input_features)
    input_labels = normalize_features(input_labels)
    key_feature = normalize_features(key_feature)[0] if key_feature is not None else None

    @_wrap_decorator_err
    def decorator(func):
        if len(inspect.signature(func).parameters) != 1:
            raise Exception(f'{func.__name__} must have a single parameter of type ModelContext')

        nonlocal name
        if name is None:
            name = func.__name__
        if name.endswith('_model'):
            name = name[:-6]
        if name.endswith('_trainer'):
            name = name[:-8]
        if name.endswith('_train'):
            name = name[:-6]
        if name.startswith('train_'):
            name = name[6:]

        spec = ModelImpl(name=name, description=func.__doc__, keys=keys, model_framework=model_framework,
                         model_server=model_server)

        spec.features = input_features
        spec.label_features = input_labels
        spec.key_feature = key_feature

        if hasattr(func, '__raptor_options'):
            for k, v in func.__raptor_options.items():
                options[k] = v

        if 'namespace' in options:
            spec.namespace = options['namespace']
        if 'labels' in options:
            spec.labels = options['labels']

        if 'freshness' in options:
            spec.freshness = options['freshness']['max_age']
            spec.staleness = options['freshness']['max_stale']
            spec.timeout = options['freshness']['timeout']

        if spec.freshness is None or spec.staleness is None:
            raise Exception('You must specify freshness')

        if 'runtime' in options:
            spec.runtime.runtime = options['runtime']['env_name']
            spec.runtime.packages = options['runtime']['packages']

        local_state.register_spec(spec)

        if hasattr(func, '__raptor_options'):
            del func.__raptor_options

        spec.training_function = func

        def trainer():
            return spec.train()

        trainer.train = trainer
        trainer.raptor_spec = spec
        trainer.features_and_labels = spec.features_and_labels
        trainer.manifest = spec.manifest
        trainer.export = spec.export
        trainer.keys = spec.keys
        trainer.input_labels = spec.label_features
        trainer.input_features = spec.features

        return trainer

    return decorator
