from typing import Iterable, Any

from dask.dataframe.core import DataFrame as DaskDataFrame
from modin.pandas.dataframe import DataFrame as ModinDataFrame
from pandas.core.frame import DataFrame as PandasDataFrame
from polars.dataframe.frame import DataFrame as PolarsDataFrame
from pyspark.sql.dataframe import DataFrame as SparkDataFrame


class DataFrame:
    """Generic (bear-agnostic) DataFrame type"""

    def __init__(self, df: PolarsDataFrame | PandasDataFrame | SparkDataFrame | DaskDataFrame | ModinDataFrame):
        self._df = df

    # TODO: property
    def shape(self) -> tuple[int, int]:
        if isinstance(self.df, (PolarsDataFrame, PandasDataFrame, ModinDataFrame)):
            return self.df.shape
        if isinstance(self.df, DaskDataFrame):
            ...  # TODO: figure out
        if isinstance(self.df, SparkDataFrame):
            ...  # TODO: figure out

    # TODO: property
    def columns(self) -> Iterable[Any]:
        return self.df.columns

    def n_columns(self) -> int:
        return len(self.columns())
