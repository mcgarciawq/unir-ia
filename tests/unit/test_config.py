from urllib.parse import quote_plus

from src.core import config


def test_build_database_uri_encodes_azure_sql_connection_string() -> None:
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:example.database.windows.net,1433;"
        "Database=task-db;"
        "Uid=user;"
        "Pwd=p@ss word;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    uri = config.build_database_uri(
        azure_sql_connection_string=connection_string,
        database_url=None,
    )

    assert uri == f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"


def test_build_database_uri_prefers_database_url_without_azure_sql() -> None:
    uri = config.build_database_uri(
        azure_sql_connection_string=None,
        database_url="sqlite:///local.db",
    )

    assert uri == "sqlite:///local.db"
