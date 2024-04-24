import os
from hashboard.api import get_datasources, login, upload_files_to_hashboard
from hashboard.api.analytics.cli_with_tracking import CommandWithTracking, GroupWithTracking
from hashboard.api.datasource.utils import DatabaseTypes, _test, create_datasource_from_subtype
from hashboard.credentials import get_credentials
from hashboard.session import get_current_session
import click

# Common fields
data_source_name = click.option(
    "--name",
    type=str,
    required=True,
    help="""The user-facing name for the Hashboard data source you are creating.""",
    prompt=True,
)
data_source_user = click.option(
    "--user",
    type=str,
    required=True,
    help="""The user used to connect to the data source.""",
    prompt=True,
)
data_source_password = click.option(
    "--password",
    type=str,
    required=True,
    help="""The password used to connect to the data source.""",
    prompt=True,
    hide_input=True,
)
def data_source_db(required: bool):
    return click.option(
    "--database",
    type=str,
    required=required,
    help="""The name of the database to read from.""",
    prompt=True,
)
data_source_schema = click.option(
    "--schema",
    type=str,
    required=False,
    help="""Specify a schema to limit which tables are available. 
    Otherwise, Hashboard will make all accessible schemas and tables available.""",
    prompt=True,
)
data_source_host = click.option(
    "--host",
    type=str,
    required=True,
    help="""The address of your database.""",
    prompt=True,
)
def data_source_port(default_port: str, required: bool):
    return click.option(
    "--port",
    type=str,
    required=required,
    help=f"""The port used to connect to your data source. Default port: {default_port}""",
    prompt=True,
)

# Bigquery-specific fields
bigquery_json_key = click.option(
    "--json_key",
    required=True,
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
    help="""A path to a JSON file containing the BigQuery service account JSON key.""",
)

# Snowflake-specific fields
snowflake_account = click.option(
    "--account",
    required=True,
    type=str,
    help="""
    Your snowflake account identifier (opens in a new tab) is provided by Snowflake and
    included in the start of the URL you use to login to Snowflake: <account_identifier>.snowflakecomputing.com.
    """,
    prompt=True,
)

snowflake_warehouse = click.option(
    "--warehouse",
    required=True,
    type=str,
    help="""The warehouse to use in Snowflake. Warehouses correspond with compute resources.""",
    prompt=True,
)
snowflake_role = click.option(
    "--role",
    required=True,
    type=str,
    prompt=True,
)

# Athena-specific fields
athena_aws_region = click.option(
    "--aws_region",
    type=str,
    required=True,
    help="""The AWS region to use to query data.""",
    prompt=True,
)
athena_port = click.option(
    "--port",
    type=str,
    required=False,
    help="""The port to connect to.""",
    prompt=True,
)
athena_staging_directory = click.option(
    "--s3_staging_dir",
    type=str,
    required=True,
    help="""The S3 path where Athena will store query results.""",
    prompt=True,
)
athena_aws_access_key_id = click.option(
    "--aws_access_key_id",
    type=str,
    required=True,
    help="""The IAM user's access key.""",
    prompt=True,
)
athena_aws_secret_access_key = click.option(
    "--aws_secret_access_key",
    type=str,
    required=True,
    help="""The IAM user's scret access key.""",
    prompt=True,
    hide_input=True,
)
athena_query_parameters = click.option(
    "--additional_query_params",
    type=str,
    help="""Additional database connection parameters in the format workGroup=value&param=value.""",
    required=False,
    prompt=True,
)

# Motherduck-specific fields
motherduck_service_token = click.option(
    "--service_token",
    type=str,
    required=True,
    help="""Your MotherDuck service token.""",
    hide_input=True,
    prompt=True,
)

# Databricks-specific fields
databricks_http_path = click.option(
    "--http_path",
    type=str,
    required=True,
    help="""The HTTP path of the SQL warehouse. Can be found in the Connection Details tab of your SQL warehouse.""",
    prompt=True,
)
databricks_access_token = click.option(
    "--access_token",
    type=str,
    required=True,
    help="""A personal access token generated in Databricks for a user with access to the data you want to query.""",
    hide_input=True,
    prompt=True,
)
databricks_catalog = click.option(
    "--catalog",
    type=str,
    required=True,
    help="""The Databricks catalog within the warehouse to connect to.""",
    prompt=True,
)

@click.group(cls=GroupWithTracking)
@click.pass_context
def datasource(ctx):
    """Commands for managing Hashboard data sources."""
    pass

@datasource.command("ls", cls=CommandWithTracking)
@click.pass_context
def list_datasources(ctx):
    """See your available database connections.

    A database connection can be added in the Settings tab on hashboard.com."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    datasources = get_datasources(s, project_id)

    from hashboard.cli import _echo_datasources
    _echo_datasources(datasources)

# Commands for create are defined in datasource_management.py
@datasource.group(
    "create", 
    cls=GroupWithTracking,
    context_settings=dict(),
)
@click.pass_context
def create(ctx):
    """Commands for creating Hashboard data sources."""
    pass

@create.command("bigquery")
@data_source_name
@bigquery_json_key
@click.pass_context
def create_bigquery(ctx, **kwargs):
    """Create a BigQuery data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/bigquery
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.BIGQUERY.value, **kwargs)

@create.command("snowflake")
@data_source_name
@snowflake_account
@data_source_user
@data_source_password
@data_source_db(required=True)
@data_source_schema
@snowflake_warehouse
@snowflake_role
@click.pass_context
def create_snowflake(ctx, **kwargs):
    """Create a Snowflake data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/snowflake
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.SNOWFLAKE.value, **kwargs)

@create.command("postgres")
@data_source_name
@data_source_host
@data_source_port(default_port="5432", required=True)
@data_source_user
@data_source_password
@data_source_db(required=True)
@data_source_schema
@click.pass_context
def create_postgres(ctx, **kwargs):
    """Create a Postgres data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.POSTGRES.value, **kwargs)

@create.command("redshift")
@data_source_name
@data_source_host
@data_source_port(default_port="5432", required=True)
@data_source_user
@data_source_password
@data_source_db(required=True)
@data_source_schema
@click.pass_context
def create_redshift(ctx, **kwargs):
    """Create a Redshift data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.REDSHIFT.value, **kwargs)

@create.command("athena")
@data_source_name
@athena_aws_region
@athena_port
@data_source_schema
@athena_staging_directory
@athena_aws_access_key_id
@athena_aws_secret_access_key
@athena_query_parameters
@click.pass_context
def create_athena(ctx, **kwargs):
    """Create an Athena data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/athena
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.ATHENA.value, **kwargs)

@create.command("clickhouse")
@data_source_name
@data_source_port(default_port="9440", required=True)
@data_source_host
@data_source_user
@data_source_password
@data_source_db(required=True)
@click.pass_context
def create_clickhouse(ctx, **kwargs):
    """Create a Clickhouse data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/clickhouse
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.CLICKHOUSE.value, **kwargs)

@create.command("mysql")
@data_source_name
@data_source_host
@data_source_user
@data_source_password
@data_source_db(required=False)
@click.pass_context
def create_mysql(ctx, **kwargs):
    """Create a MySql data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/mysql
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.MYSQL.value, **kwargs)

@create.command("motherduck")
@data_source_name
@data_source_db(required=True)
@click.pass_context
def create_motherduck(ctx, **kwargs):
    """Create a MotherDuck data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/motherduck
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.MOTHERDUCK.value, **kwargs)

@create.command("databricks")
@data_source_name
@data_source_host
@data_source_port(default_port="443", required=False)
@databricks_http_path
@databricks_access_token
@databricks_catalog
@data_source_schema
@click.pass_context
def create_databricks(ctx, **kwargs):
    """Create a Databricks data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/databricks
    """
    create_datasource_from_subtype(ctx, DatabaseTypes.DATABRICKS.value, **kwargs)

@datasource.command(
    "upload",
    cls=CommandWithTracking,
    context_settings=dict(),
)
@click.argument(
    "filepaths",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
)
@click.pass_context
def upload(ctx, filepaths):
    """
    Upload file(s) to Hashboard that can be queried using duckdb and
    used as the basis for a data model.
    """

    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])

    files_noun = f"{len(filepaths)} file{'' if len(filepaths) == 1 else 's'}"
    click.echo(f"📄 Uploading {files_noun} to Hashboard...")
    for filepath in filepaths:
        fp = os.path.expanduser(filepath)
        uploaded_name = upload_files_to_hashboard(s, project_id, fp)
        click.echo(f'   Uploaded "{uploaded_name}"')
    click.echo(f"✅ Successfully uploaded {files_noun}.")

@datasource.command(
    "test",
    cls=CommandWithTracking,
    context_settings=dict(),
)
@click.argument(
    "name",
    required=True,
    type=str,
)
@click.pass_context
def test(ctx, name):
    """Test a data connection by its name."""
    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])
    _test(s, name, project_id)

