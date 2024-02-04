from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(0)


def generate_id_by_snowflake():
    snowflake_id = next(gen)
    return snowflake_id
