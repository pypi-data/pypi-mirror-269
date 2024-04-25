from pathlib import Path
import relationalai as rai

import pytest
import random
from gentest.exec import path_to_slug, validate_query_results
from relationalai import debugging
from relationalai.clients import config as cfg

test_case_dir = Path(__file__).parent / "test_cases"
test_case_files = [path for path in test_case_dir.rglob("*.py")]

# This test absorbs the latency of the engine being created
def test_engine_creation_dummy(engine_config: cfg.Config):
    pass

def randomize(name: str) -> str:
    return f"{name}_{random.randint(1000000000, 9999999999)}"

@pytest.mark.parametrize(
    "file_path", test_case_files, ids=lambda path: path_to_slug(path, test_case_dir)
)
def test_snapshots(file_path: Path, snapshot, engine_config: cfg.Config):
    test_name = file_path.stem
    provider = rai.Resources(config=engine_config)
    cloud_provider_str = engine_config.get("platform", "snowflake")
    with debugging.span("test", name=test_name, cloud_provider=cloud_provider_str):
        for i in range(1):
            with debugging.span("run", idx=i):
                db_name = randomize(test_name)
                validate_query_results(
                    file_path,
                    snapshot,
                    {
                        "name": db_name,
                        "config": engine_config,
                    }
                )
                try:
                    provider.delete_graph(db_name)
                except Exception as e:
                    print(f"Failed to delete graph {db_name}: {e}")
