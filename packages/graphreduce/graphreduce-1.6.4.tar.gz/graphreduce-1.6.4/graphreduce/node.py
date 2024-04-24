#!/usr/bin/env python

# std lib
import abc
import datetime
import typing
import json

# third party
import pandas as pd
from dask import dataframe as dd
import pyspark
from structlog import get_logger

# internal
from graphreduce.enum import ComputeLayerEnum, PeriodUnit
from graphreduce.storage import StorageClient


logger = get_logger('Node')


class GraphReduceNode(metaclass=abc.ABCMeta): 
    fpath : str
    fmt : str
    prefix : str
    date_key : str
    pk : str 
    compute_layer : ComputeLayerEnum
    spark_sqlctx : typing.Optional[pyspark.sql.SQLContext]
    cut_date : datetime.datetime
    compute_period_val : typing.Union[int, float]
    compute_period_unit : PeriodUnit
    label_period_val : typing.Optional[typing.Union[int, float]]
    label_period_unit : typing.Optional[PeriodUnit] 
    label_field: typing.Optional[str]
    storage_client: typing.Optional[StorageClient]
    batch_features: typing.List
    online_features: typing.List
    on_demand_features: typing.List

    def __init__ (
            self,
            fpath : str,
            fmt : str,
            pk : str = None,
            prefix : str = None,
            date_key : str = None,
            compute_layer : ComputeLayerEnum = None,
            cut_date : datetime.datetime = datetime.datetime.now(),
            compute_period_val : typing.Union[int, float] = 365,
            compute_period_unit : PeriodUnit  = PeriodUnit.day,
            reduce : bool = True,
            label_period_val : typing.Optional[typing.Union[int, float]] = None,
            label_period_unit : typing.Optional[PeriodUnit] = None,
            label_field : typing.Optional[str] = None,
            spark_sqlctx : pyspark.sql.SQLContext = None,
            columns : list = [],
            storage_client: typing.Optional[StorageClient] = None,
            checkpoints: list = [],
            ):
        """
Constructor

Args
    fpath : file path
    fmt : format of file
    pk : primary key
    prefix : prefix to use for columns
    date_key : column containing the date - if there isn't one leave blank
    compute_layer : compute layer to use (e.g, ComputeLayerEnum.pandas)
    cut_date : date around which to orient the data
    compute_period_val : amount of time to consider
    compute_period_unit : unit of measure for compute period (e.g., PeriodUnit.day)
    reduce : whether or not to reduce the data
    label_period_val : optional period of time to compute labels
    label_period_unit : optional unit of measure for label period (e.g., PeriodUnit.day)
    label_field : optional field on which to compute the label
    columns : optional list of columns to include
    storage_client: optional storage client
        """
        # For when this is already set on the class definition.
        if not hasattr(self, 'pk'):
            self.pk = pk
        # For when this is already set on the class definition.
        if not hasattr(self, 'prefix'):
            self.prefix = prefix
        # For when this is already set on the class definition.
        if not hasattr(self, 'date_key'):
            self.date_key = date_key
        self.fpath = fpath
        self.fmt = fmt
        self.compute_layer = compute_layer
        self.cut_date = cut_date
        self.compute_period_val = compute_period_val
        self.compute_period_unit = compute_period_unit
        self.reduce = reduce
        self.label_period_val = label_period_val
        self.label_period_unit = label_period_unit
        self.label_field = label_field
        self.spark_sqlctx = spark_sqlctx
        self.columns = columns

        self._storage_client = storage_client
        # List of merged neighbor classes.
        self._merged = []
        # List of checkpoints.
        self._checkpoints = []

        # Logical types of the original columns from `woodwork`.
        self._logical_types = {}

        if not self.date_key:
            logger.warning(f"no `date_key` set for {self}")


    def __repr__ (
            self
            ):
        """
Instance representation
        """
        return f"<GraphReduceNode: fpath={self.fpath} fmt={self.fmt}>"

    def __str__ (
            self
            ):
        """
Instances string
        """
        return f"<GraphReduceNode: fpath={self.fpath} fmt={self.fmt}>"


    def reload (
            self
            ):
        """
Refresh the node.
        """
        self._merged = []
        self._checkpoints = []
        self.df = None
        self._logical_types = {}

    
    def do_data (
        self
    ) -> typing.Union[
        pd.DataFrame,
        dd.DataFrame,
        pyspark.sql.dataframe.DataFrame
    ]:
        """
Get some data
        """
        if self.compute_layer.value == 'pandas':
            if not hasattr(self, 'df') or (hasattr(self,'df') and not isinstance(self.df, pd.DataFrame)):
                self.df = getattr(pd, f"read_{self.fmt}")(self.fpath)

                # Initialize woodwork.
                self.df.ww.init()
                self._logical_types = self.df.ww.logical_types

                # Rename columns with prefixes.
                if len(self.columns):
                    self.df = self.df[[c for c in self.columns]]
                self.columns = list(self.df.columns)
                self.df.columns = [f"{self.prefix}_{c}" for c in self.df.columns]
        elif self.compute_layer.value == 'dask':
            if not hasattr(self, 'df') or (hasattr(self, 'df') and not isinstance(self.df, dd.DataFrame
)):
                self.df = getattr(dd, f"read_{self.fmt}")(self.fpath)

                # Initialize woodwork.
                self.df.ww.init()
                self._logical_types = self.df.ww.logical_types

                # Rename columns with prefixes.
                if len(self.columns):
                    self.df = self.df[[c for c in self.columns]]
                self.columns = list(self.df.columns)
                self.df.columns = [f"{self.prefix}_{c}" for c in self.df.columns]
        elif self.compute_layer.value == 'spark':
            if not hasattr(self, 'df') or (hasattr(self, 'df') and not isinstance(self.df, pyspark.sql.DataFrame)):
                self.df = getattr(self.spark_sqlctx.read, f"{self.fmt}")(self.fpath)
                if self.columns:
                    self.df = self.df.select(self.columns)
                for c in self.df.columns:
                    self.df = self.df.withColumnRenamed(c, f"{self.prefix}_{c}")

        # at this point of connectors we may want to try integrating
        # with something like fugue: https://github.com/fugue-project/fugue
        elif self.compute_layer.value == 'ray':
            pass

        elif self.compute_layer.value == 'snowflake':
            pass

        elif self.compute_layer.value == 'postgres':
            pass

        elif self.compute_layer.value == 'redshift':
            pass


    @abc.abstractmethod
    def do_filters (
        self
    ):
        """
do some filters on the data
        """
        pass
    

    @abc.abstractmethod
    def do_annotate(self):
        """
Implement custom annotation functionality
for annotating this particular data
        """
        pass

    
    @abc.abstractmethod
    def do_post_join_annotate(self):
        """
Implement custom annotation functionality
for annotating data after joining with 
child data
        """
        pass


    @abc.abstractmethod
    def do_normalize(self):
        pass


    def do_post_join_filters(self):
        """
Filter operations that require some
additional relational data to perform.
        """
        pass


    def auto_features (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            compute_layer : ComputeLayerEnum = ComputeLayerEnum.pandas,
            ):
        """
If we're doing automatic features
this function will run a series of
automatic aggregations.  The top-level
`GraphReduce` object will handle joining
the results together.
        """
        if compute_layer == ComputeLayerEnum.pandas:
            return self.pandas_auto_features(reduce_key=reduce_key, type_func_map=type_func_map)
        elif compute_layer == ComputeLayerEnum.dask:
            return self.dask_auto_features(reduce_key=reduce_key, type_func_map=type_func_map)
        elif compute_layer == ComputeLayerEnum.spark:
            return self.spark_auto_features(reduce_key=reduce_key, type_func_map=type_func_map)


    def auto_labels (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            compute_layer : ComputeLayerEnum = ComputeLayerEnum.pandas,
            ):
        """
If we're doing automatic features
this function will run a series of
automatic aggregations.  The top-level
`GraphReduce` object will handle joining
the results together.
        """
        if compute_layer == ComputeLayerEnum.pandas:
            return self.pandas_auto_labels(reduce_key=reduce_key, type_func_map=type_func_map)
        elif compute_layer == ComputeLayerEnum.dask:
            return self.dask_auto_labels(reduce_key=reduce_key, type_func_map=type_func_map)
        elif compute_layer == ComputeLayerEnum.spark:
            return self.spark_auto_labels(reduce_key=reduce_key, type_func_map=type_func_map)


    def pandas_auto_features (
            self,
            reduce_key : str,
            type_func_map : dict = {}
            ) -> pd.DataFrame:
        """
Pandas implementation of dynamic propagation of features.
This is basically automated feature engineering but suffixed
with `_propagation` to indicate that we are propagating data
upward through the graph from child nodes with no feature
definitions.
        """
        agg_funcs = {}
        for col, _type in dict(self.df.dtypes).items():
            _type = str(_type)
            if type_func_map.get(_type):
                for func in type_func_map[_type]:
                    col_new = f"{col}_{func}"
                    agg_funcs[col_new] = pd.NamedAgg(column=col, aggfunc=func)
        return self.prep_for_features().groupby(self.colabbr(reduce_key)).agg(
                **agg_funcs
                ).reset_index()


    def dask_auto_features (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            ) -> dd.DataFrame:
        """
Dask implementation of dynamic propagation of features.
This is basically automated feature engineering but suffixed
with `_propagation` to indicate that we are propagating data
upward through the graph from child nodes with no feature
definitions.
        """
        agg_funcs = {}
        for col, _type in dict(self.df.dtypes).items():
            _type = str(_type)
            if type_func_map.get(_type):
                for func in type_func_map[_type]:
                    col_new = f"{col}_{func}"
                    agg_funcs[col_new] = pd.NamedAgg(column=col, aggfunc=func)
        return self.prep_for_features().groupby(self.colabbr(reduce_key)).agg(
                **agg_funcs
                ).reset_index()


    def spark_auto_features (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            ) -> pyspark.sql.DataFrame:
        """
Spark implementation of dynamic propagation of features.
This is basically automated feature engineering but suffixed
with `_propagation` to indicate that we are propagating data
upward through the graph from child nodes with no feature
definitions.
        """
        agg_funcs = []
        for field in self.df.schema.fields:
            field_meta = json.loads(field.json())
            col = field_meta['name']
            _type = field_meta['type']
            if type_func_map.get(_type):
                for func in type_func_map[_type]:
                    col_new = f"{col}_{func}"
                    agg_funcs.append(getattr(F, func)(F.col(col)).alias(col_new))
        return self.prep_for_features().groupby(self.colabbr(reduce_key)).agg(
                *agg_funcs
                )


    def pandas_auto_labels (
            self,
            reduce_key : str,
            type_func_map : dict = {}
            ) -> pd.DataFrame:
        """
Pandas implementation of auto labeling based on
provided columns.
        """
        agg_funcs = {}
        for col, _type in dict(self.df.dtypes).items():
            if col.endswith('_label'):
                _type = str(_type)
                if type_func_map.get(_type):
                    for func in type_func_map[_type]:
                        col_new = f"{col}_{func}_label"
                        agg_funcs[col_new] = pd.NamedAgg(column=col, aggfunc=func)
        return self.prep_for_labels().groupby(self.colabbr(reduce_key)).agg(
                **agg_funcs
                ).reset_index()


    def dask_auto_labels (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            ) -> dd.DataFrame:
        """
Dask implementation of auto labeling based on
provided columns.
        """
        agg_funcs = {}
        for col, _type in dict(self.df.dtypes).items():
            if col.endswith('_label'):
                _type = str(_type)
                if type_func_map.get(_type):
                    for func in type_func_map[_type]:
                        col_new = f"{col}_{func}_label"
                        agg_funcs[col_new] = pd.NamedAgg(column=col, aggfunc=func)
        return self.prep_for_labels().groupby(self.colabbr(reduce_key)).agg(
                **agg_funcs
                ).reset_index()


    def spark_auto_labels (
            self,
            reduce_key : str,
            type_func_map : dict = {},
            ) -> pyspark.sql.DataFrame:
        """
Spark implementation of auto labeling based on
provided columns.
        """
        agg_funcs = []
        for field in self.df.schema.fields:
            field_meta = json.loads(field.json())
            col = field_meta['name']
            _type = field_meta['type']
            if col.endswith('_label'):
                if type_func_map.get(_type):
                    for func in type_func_map[_type]:
                        col_new = f"{col}_{func}_label"
                        agg_funcs.append(getattr(F, func)(F.col(col)).alias(col_new))
        return self.prep_for_labels().groupby(self.colabbr(reduce_key)).agg(
                *agg_funcs
                )


    @abc.abstractmethod
    def do_reduce (
            self, 
            reduce_key
            ):
        """
Reduce operation or the node

Args
    reduce_key : key to use to perform the reduce operation
    children : list of children nodes
        """
        pass
    
    
    @abc.abstractmethod
    def do_labels (
            self,
            reduce_key: typing.Optional[str] = None,
            ):
        """
Generate labels
        """
        pass
    
        
    def colabbr(self, col: str) -> str:
        return f"{self.prefix}_{col}"


    def compute_period_minutes (
            self,
            ) -> int:
        """
Convert the compute period to minutes
        """
        if self.compute_period_unit == PeriodUnit.second:
            return self.compute_period_val / 60
        elif self.compute_period_unit == PeriodUnit.minute:
            return self.compute_period_val
        elif self.compute_period_unit == PeriodUnit.hour:
            return self.compute_period_val * 60
        elif self.compute_period_unit == PeriodUnit.day:
            return self.compute_period_val * 1440
        elif self.compute_period_unit == PeriodUnit.week:
            return (self.compute_period_val * 7)*1440
        elif self.compute_period_unit == PeriodUnit.month:
            return (self.compute_period_val * 30.417)*1440


    def label_period_minutes (
            self,
            ) -> int:
        """
Convert the label period to minutes
        """
        if self.label_period_unit == PeriodUnit.second:
            return self.label_period_val / 60
        elif self.label_period_unit == PeriodUnit.minute:
            return self.label_period_val
        elif self.label_period_unit == PeriodUnit.hour:
            return self.label_period_val * 60
        elif self.label_period_unit == PeriodUnit.day:
            return self.label_period_val * 1440
        elif self.label_period_unit == PeriodUnit.week:
            return (self.label_period_val * 7)*1440
        elif self.label_period_unit == PeriodUnit.month:
            return (self.label_period_val * 30.417)*1440
    
    
    def prep_for_features (
            self,
            allow_null: bool = False
            ) -> typing.Union[pd.DataFrame, dd.DataFrame, pyspark.sql.dataframe.DataFrame]:
        """
Prepare the dataset for feature aggregations / reduce
        """
        if self.date_key:           
            if self.cut_date and isinstance(self.cut_date, str) or isinstance(self.cut_date, datetime.datetime):
                if isinstance(self.df, pd.DataFrame) or isinstance(self.df, dd.DataFrame):
                    return self.df[
                        (
                            (self.df[self.colabbr(self.date_key)] < str(self.cut_date))
                            &
                            (self.df[self.colabbr(self.date_key)] > str(self.cut_date - datetime.timedelta(minutes=self.compute_period_minutes())))
                        )
                        |
                        (self.df[self.colabbr(self.date_key)].isnull())
                    ]
                elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                    return self.df.filter(
                        (
                            (self.df[self.colabbr(self.date_key)] < self.cut_date)
                            &
                            (self.df[self.colabbr(self.date_key)] > (self.cut_date - datetime.timedelta(minutes=self.compute_period_minutes())))
                        )
                        |
                        (self.df[self.colabbr(self.date_key)].isNull())
                    )
            else:
                if isinstance(self.df, pd.DataFrame) or isinstance(self.df, dd.DataFrame):
                    return self.df[
                        (
                            (self.df[self.colabbr(self.date_key)] < datetime.datetime.now())
                            &
                            (self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(minutes=self.compute_period_minutes())))
                        )
                        |
                        (self.df[self.colabbr(self.date_key)].isnull())
                    ]
                elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                    return self.df.filter(
                            (self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(minutes=self.compute_period_minutes())))
                            |
                            (self.df[self.colabbr(self.date_key)].isNull())
                )
        # no-op
        return self.df
    
    
    def prep_for_labels (
            self
            ) -> typing.Union[pd.DataFrame, dd.DataFrame, pyspark.sql.dataframe.DataFrame]:
        """
Prepare the dataset for labels
        """
        if self.date_key:
            if self.cut_date and isinstance(self.cut_date, str) or isinstance(self.cut_date, datetime.datetime):
                if isinstance(self.df, pd.DataFrame):
                    return self.df[
                        (self.df[self.colabbr(self.date_key)] > str(self.cut_date))
                        &
                        (self.df[self.colabbr(self.date_key)] < str(self.cut_date + datetime.timedelta(minutes=self.label_period_minutes())))
                    ]
                elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                    return self.df.filter(
                        (self.df[self.colabbr(self.date_key)] > str(self.cut_date))
                        &
                        (self.df[self.colabbr(self.date_key)] < str(self.cut_date + datetime.timedelta(minutes=self.label_period_minutes())))
                    )
            else:
                if isinstance(self.df, pd.DataFrame):
                    return self.df[
                        self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(minutes=self.label_period_minutes()))
                    ]
                elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                    return self.df.filter(
                    self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(minutes=self.label_period_minutes()))
                )
        # no-op
        return self.df



    def default_label (
            self,
            op: typing.Union[str, callable],
            field: str,
            reduce_key: typing.Optional[str] = None,
            ) -> typing.Union[pd.DataFrame, dd.DataFrame, pyspark.sql.dataframe.DataFrame]:
        """
Default label operation.

        Arguments
        ----------
        op: operation to call for label
        field: str label field to call operation on
        reduce: bool whether or not to reduce
        """
        if self.colabbr(field) in self.df.columns:
            if self.compute_layer in [ComputeLayerEnum.pandas, ComputeLayerEnum.dask]:
                if self.reduce:
                    if callable(op):
                        return self.prep_for_labels().groupby(self.colabbr(reduce_key)).agg(**{
                            self.colabbr(field+'_label') : pd.NamedAgg(column=self.colabbr(field), aggfunc=op)
                        }).reset_index()
                    else:
                        return self.prep_for_labels().groupby(self.colabbr(reduce_key)).agg(**{
                            self.colabbr(field+'_label') : pd.NamedAgg(column=self.colabbr(field), aggfunc=op)
                            }).reset_index()
                else:
                    label_df = self.prep_for_labels()
                    if callable(op):
                        label_df[self.colabbr(field)+'_label'] = label_df[self.colabbr(field)].apply(op)
                    else:
                        label_df[self.colabbr(field)+'_label'] = label_df[self.colabbr(field)].apply(lambda x: getattr(x, op)())
                    return label_df[[self.colabbr(self.pk), self.colabbr(field)+'_label']]

            elif self.compute_layer == ComputeLayerEnum.spark:
                pass
            elif self.compute_layer == ComputeLayerEnum.snowflake:
                pass


    def online_features (
            self,
            ):
        """
Define online features.
        """
        pass


    def on_demand_features (
            self,
            ):
        """
Define on demand features for this node.
        """
        pass




class DynamicNode(GraphReduceNode):
    """
A dynamic architecture for entities with no logic 
needed in addition to the top-level GraphReduceNode
parameters
    """
    def __init__ (
            self,
            *args,
            **kwargs,
            ):
        """
Constructor
        """
        super().__init__(*args, **kwargs)

    def do_filters(self):
        pass

    def do_annotate(self):
        pass

    def do_post_join_annotate(self):
        pass

    def do_normalize(self):
        pass

    def do_post_join_filters(self):
        pass

    def do_reduce(self, reduce_key: str):
        pass

    def do_labels(self, reduce_key: str):
        pass
