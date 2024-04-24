from pyspark.sql.types import UserDefinedType, BinaryType, IntegralType
from pyspark import SparkContext
from pyspark.sql.column import _to_java_column, Column


class YsonType(UserDefinedType):
    @classmethod
    def typeName(cls):
        return "yson"

    @classmethod
    def sqlType(cls):
        return BinaryType()

    @classmethod
    def module(cls):
        return 'spyt.types'

    @classmethod
    def scalaUDT(cls):
        return 'org.apache.spark.sql.yson.YsonType'

    def needConversion(self):
        return True

    def serialize(self, obj):
        return obj

    def deserialize(self, datum):
        return datum

    def simpleString(self):
        return 'yson'


UINT64_MAX = 0xffffffffffffffff


class UInt64Type(IntegralType):
    """Unsigned 64-bit integer type
    """
    def simpleString(self):
        return 'uint64'

    @classmethod
    def typeName(cls):
        return "uint64"

    def needConversion(self):
        return True

    def toInternal(self, py_integer):
        if py_integer is None:
            return None
        if py_integer < 0 or py_integer > UINT64_MAX:
            raise ValueError(f"object of UInt64Type out of range, got: {py_integer}")
        return py_integer if py_integer <= 0x7fffffffffffffff else py_integer - UINT64_MAX - 1

    def fromInternal(self, j_long):
        return j_long if j_long is None or j_long >= 0 else (j_long & UINT64_MAX)


def uint64_to_string(number):
    if number is None:
        return None
    else:
        # convert to unsigned value
        return str(number & UINT64_MAX)


def string_to_uint64(number):
    if number is None:
        return None
    else:
        return int(number)


def uint64_to_string_udf(s_col):
    sc = SparkContext._active_spark_context
    cols = sc._gateway.new_array(sc._jvm.Column, 1)
    cols[0] = _to_java_column(s_col)
    jc = sc._jvm.org.apache.spark.sql.yson.UInt64Long.toStringUdf().apply(cols)
    return Column(jc)


def string_to_uint64_udf(s_col):
    sc = SparkContext._active_spark_context
    cols = sc._gateway.new_array(sc._jvm.Column, 1)
    cols[0] = _to_java_column(s_col)
    jc = sc._jvm.org.apache.spark.sql.yson.UInt64Long.fromStringUdf().apply(cols)
    return Column(jc)


def xx_hash64_zero_seed_udf(*s_cols):
    sc = SparkContext._active_spark_context
    sz = len(s_cols)
    cols = sc._gateway.new_array(sc._jvm.Column, sz)
    for i in range(sz):
        cols[i] = _to_java_column(s_cols[i])
    jc = sc._jvm.tech.ytsaurus.spyt.common.utils.XxHash64ZeroSeed.xxHash64ZeroSeedUdf(cols)
    return Column(jc)


def register_xxHash64ZeroSeed(spark):
    sc = SparkContext._active_spark_context
    sc._jvm.tech.ytsaurus.spyt.common.utils.XxHash64ZeroSeed.registerFunction(spark._jsparkSession)


def cityhash_udf(*s_cols):
    sc = SparkContext._active_spark_context
    sz = len(s_cols)
    cols = sc._gateway.new_array(sc._jvm.Column, sz)
    for i in range(sz):
        cols[i] = _to_java_column(s_cols[i])
    jc = sc._jvm.tech.ytsaurus.spyt.common.utils.CityHash.cityHashUdf(cols)
    return Column(jc)


def register_cityHash(spark):
    sc = SparkContext._active_spark_context
    sc._jvm.tech.ytsaurus.spyt.common.utils.CityHash.registerFunction(spark._jsparkSession)


def tuple_type(element_types):
    """
    :param element_types: List[DataType]
    :return: StructType
    """
    from pyspark.sql.types import StructType, StructField
    struct_fields = [StructField("_{}".format(i + 1), element_type) for i, element_type in enumerate(element_types)]
    return StructType(struct_fields)


def variant_over_struct_type(elements):
    """
    :param elements: List[Tuple[str, DataType]]
    :return: StructType
    """
    from pyspark.sql.types import StructType, StructField
    struct_fields = [StructField("_v{}".format(element_name), element_type) for element_name, element_type in elements]
    return StructType(struct_fields)


def variant_over_tuple_type(element_types):
    """
    :param element_types: List[DataType]
    :return: StructType
    """
    elements = [("_{}".format(i + 1), element_type) for i, element_type in enumerate(element_types)]
    return variant_over_struct_type(elements)
