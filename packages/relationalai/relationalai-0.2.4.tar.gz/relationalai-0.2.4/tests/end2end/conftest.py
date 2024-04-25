import os
import random

import pytest
import snowflake.connector

import relationalai as rai
from relationalai.clients import config as cfg
from relationalai.debugging import logger
from relationalai.util.snowflake_logger import SnowflakeLogger

def create_engine(engine_name: str):
    config = make_config(engine_name)

    sf_compute_pool = os.getenv("SF_TEST_COMPUTE_POOL", config.get("compute_pool", ""))

    provider = rai.Resources(config=config)
    print(f"Creating engine {engine_name}")
    provider.create_engine(name=engine_name, size="XS", pool=sf_compute_pool)
    print(f"Engine {engine_name} created")


def delete_engine(engine_name: str):
    print(f"Deleting engine {engine_name}")
    config = make_config(engine_name)
    provider = rai.Resources(config=config)
    provider.delete_engine(engine_name)
    print(f"Engine {engine_name} deleted")


@pytest.fixture(scope="session")
def engine_config():
    # Check for an externally provided engine name
    # It is used in GitHub Actions to run tests against a specific engine
    engine_name = os.getenv("ENGINE_NAME")
    if engine_name:
        config = make_config(engine_name)
    else:
        # If there's a local config file, use it, including
        # the engine specified there.
        config = cfg.Config()
        if config.file_path is not None:
            yield config
            return

        # Otherwise, create a new engine and delete it afterwards.
        random_number = random.randint(1000000000, 9999999999)
        engine_name = f"pyrel_test_{random_number}"
        create_engine(engine_name)

        yield config

        delete_engine(engine_name)
        return

    # If engine name was provided, just yield the config
    yield config


def make_config(engine_name: str) -> cfg.Config:
    cloud_provider = os.getenv("RAI_CLOUD_PROVIDER")

    match cloud_provider:
        case None:
            raise ValueError("RAI_CLOUD_PROVIDER must be set")
        case "azure":
            client_id = os.getenv("RAI_CLIENT_ID")
            client_secret = os.getenv("RAI_CLIENT_SECRET")
            if client_id is None or client_secret is None:
                raise ValueError(
                    "RAI_CLIENT_ID, RAI_CLIENT_SECRET must be set if RAI_CLOUD_PROVIDER is set to 'azure'"
                )
            # Running against prod
            return cfg.Config(
                {
                    "platform": "azure",
                    "host": "azure.relationalai.com",
                    "port": "443",
                    "region": "us-east",
                    "scheme": "https",
                    "client_credentials_url": "https://login.relationalai.com/oauth/token",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "engine": engine_name,
                }
            )
        case "snowflake":
            sf_username = os.getenv("SF_TEST_ACCOUNT_USERNAME")
            sf_password = os.getenv("SF_TEST_ACCOUNT_PASSWORD")
            sf_account = os.getenv("SF_TEST_ACCOUNT_NAME")
            sf_warehouse = os.getenv("SF_TEST_WAREHOUSE_NAME")
            sf_app_name = os.getenv("SF_TEST_APP_NAME")
            sf_compute_pool = os.getenv("SF_TEST_COMPUTE_POOL")
            if sf_username is None or sf_password is None:
                raise ValueError(
                    "SF_TEST_ACCOUNT_USERNAME, SF_TEST_ACCOUNT_PASSWORD, SF_TEST_ACCOUNT_NAME must be set if RAI_CLOUD_PROVIDER is set to 'snowflake'"
                )
            return cfg.Config(
                {
                    "platform": "snowflake",
                    "user": sf_username,
                    "password": sf_password,
                    "account": sf_account,
                    "role": "rai_integration_consumer",
                    "warehouse": sf_warehouse,
                    "rai_app_name": sf_app_name,
                    "engine": engine_name,
                    "compute_pool": sf_compute_pool,
                }
            )
        case _:
            raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

# Attach Snowflake logger; shutting down that the end of the session

SNOWFLAKE_LOGGER = None

if os.getenv("SF_REPORTING_USER") is not None:
    conn = snowflake.connector.connect(
        user=os.getenv("SF_REPORTING_USER"),
        password=os.getenv("SF_REPORTING_PASSWORD"),
        account=os.getenv("SF_REPORTING_ACCOUNT"),
        role=os.getenv("SF_REPORTING_ROLE"),
        warehouse=os.getenv("SF_REPORTING_WAREHOUSE"),
        database=os.getenv("SF_REPORTING_DATABASE"),
        schema=os.getenv("SF_REPORTING_SCHEMA"),
    )
    SNOWFLAKE_LOGGER = SnowflakeLogger(conn)
    logger.addHandler(SNOWFLAKE_LOGGER)
else:
    print('benchmarking logger disabled since config env vars not present')


def pytest_sessionfinish(session, exitstatus):
    if SNOWFLAKE_LOGGER:
        SNOWFLAKE_LOGGER.shut_down()
