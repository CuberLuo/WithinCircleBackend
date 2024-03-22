from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(0)


def generate_id_by_snowflake():
    snowflake_id = next(gen)
    # 移除雪花算法生成id的后三位，避免js中大位数整数出现精度丢失的问题
    snowflake_id = int(snowflake_id / 1000)
    return snowflake_id
