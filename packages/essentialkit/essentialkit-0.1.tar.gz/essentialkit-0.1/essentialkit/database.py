import configparser
import os

import pandas
from clickhouse_driver import Client


def load_clickhouse_credentials(clickhouse_instance: str, credentials_path: str) -> dict:
    """
    | Retrieve credentials for the requested clickhouse instance from the ini file

    :param clickhouse_instance: Name of the ClickHouse instance
    :param credentials_path: Location of the ini file
    :return: Credentials for the requested ClickHouse instance
    """
    dbconfig = configparser.ConfigParser()
    dbconfig.read(os.path.join(credentials_path, "config.ini"))
    return {
        "host": dbconfig[clickhouse_instance].get("host"),
        "user": dbconfig[clickhouse_instance].get("user"),
        "password": dbconfig[clickhouse_instance].get("password"),
    }


def execute_clickhouse_query(ch_credentials: dict, query: str) -> None:
    """
    | Executes the given query on the ClickHouse database.

    :param ch_credentials: Credentials for the ClickHouse database
    :param query: Query to be executed on the ClickHouse database
    :return: None
    """
    with Client(
        host=ch_credentials["host"],
        user=ch_credentials["user"],
        password=ch_credentials["password"],
        settings={"use_numpy": False},
    ) as client:
        client.execute(query)


def read_clickhouse_df(ch_credentials: dict, query: str) -> pandas.DataFrame:
    """
    | Executes the given query on the ClickHouse database and retrieve the result in a Pandas DataFrame.

    :param ch_credentials: Credentials for the ClickHouse database
    :param query: Query to be executed which should return a table
    :return: Pandas DataFrame which contains the result of the query
    @rtype: object
    """
    with Client(
        host=ch_credentials["host"],
        user=ch_credentials["user"],
        password=ch_credentials["password"],
        settings={"use_numpy": False},
    ) as client:
        return client.query_dataframe(query)


def save_clickhouse_dataframe(
    df: pandas.DataFrame, ch_credentials: dict, table: str, database: str, replace: bool = False
) -> None:
    """
    | Saves the desired Pandas DataFrame to the ClickHouse database.

    :param df: Pandas DataFrame to be saved
    :param ch_credentials: Credentials for the ClickHouse database
    :param table: Name of the table in which to save data
    :param database: Name of the database in which to save data
    :param replace: If True you remove the data first
    :return: None
    """
    with Client(
        host=ch_credentials["host"],
        user=ch_credentials["user"],
        password=ch_credentials["password"],
        settings={"use_numpy": True},
    ) as client:
        if replace:
            client.execute(f"TRUNCATE TABLE IF EXISTS {database}.{table}")
        client.insert_dataframe(f"INSERT INTO {database}.{table} VALUES", df)