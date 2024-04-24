from copy import deepcopy
from enum import Enum
import pathlib
import click

from hashboard.api import create_data_source, login, test_data_source
from hashboard.credentials import get_credentials
from hashboard.session import get_current_session

# Make sure this stays consistent with glean/db/database_types.py
class DatabaseTypes(Enum):
    ATHENA = "athena"
    BIGQUERY = "big_query"
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SNOWFLAKE = "snowflake"
    DUCKDB = "duckdb"
    CLICKHOUSE = "clickhouse"
    MOTHERDUCK = "motherduck"
    DATABRICKS = "databricks"
    REDSHIFT = "redshift"


def create_datasource_from_subtype(ctx, subtype, **kwargs):
    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])
    
    datasource_kwargs = deepcopy(kwargs)

    def replace_field(old_field_name, new_field_name):
        if old_field_name in datasource_kwargs:
            datasource_kwargs[new_field_name] = datasource_kwargs[old_field_name]
            del datasource_kwargs[old_field_name]

    # Converting user-friendly external argument names to our internal datasource fields
    kwarg_replacements = {
        "password": "secretCredential",
        "aws_region": "athenaRegionName",
        "s3_staging_dir": "athenaS3StagingDir",
        "aws_access_key_id": "athenaAWSAccessKeyID",
        "aws_secret_access_key": "secretCredential",
        "additional_query_params": "additionalQueryParams",
        "service_token": "secretCredential",
        "http_path": "httpPath",
        "access_token": "secretCredential",
    }

    if subtype == DatabaseTypes.BIGQUERY.value:
        json_key_filepath = kwargs["json_key"]
        if pathlib.Path(json_key_filepath).suffix != ".json":
            raise Exception("BigQuery JSON key must be a .json file.")
        with open(json_key_filepath, "r") as f:
            json_file = f.read()
            datasource_kwargs["secretCredential"] = json_file
        del datasource_kwargs["json_key"]
    else:
        for old_field_name, new_field_name in kwarg_replacements.items():
            replace_field(old_field_name, new_field_name)

    datasource = {
        "project": project_id,
        "type": "glean_database",
        "subType": subtype,
        **datasource_kwargs,
    }

    from hashboard.cli import _echo_datasource_creation_errors_and_exit
    try:
        create_data_source(s, datasource)
        click.echo(f"📊 Successfully created data source: {kwargs['name']}.")
        _test(s, kwargs["name"], project_id)
    except Exception as e:
        _echo_datasource_creation_errors_and_exit([str(e)])


def _test(s, name, project_id):
    click.echo(f"🔍 Testing connection to {name}...")
    try:
        test_data_source(s, name, project_id)
        click.echo(f"🎉 Successfully connected to {name}.")
    except Exception as e:
        click.echo(f"❌ {e}")
