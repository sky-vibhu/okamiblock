from pathlib import Path

import pytest

from .network import create_snapshots_dir, setup_custom_okami
from .utils import memiavl_config, wait_for_block


@pytest.fixture(scope="module")
def custom_okami(tmp_path_factory):
    path = tmp_path_factory.mktemp("no-abci-resp")
    yield from setup_custom_okami(
        path,
        26260,
        Path(__file__).parent / "configs/discard-abci-resp.jsonnet",
    )


@pytest.fixture(scope="module")
def custom_okami_rocksdb(tmp_path_factory):
    path = tmp_path_factory.mktemp("no-abci-resp-rocksdb")
    yield from setup_custom_okami(
        path,
        26810,
        memiavl_config(path, "discard-abci-resp"),
        post_init=create_snapshots_dir,
        chain_binary="okamid-rocksdb",
    )


@pytest.fixture(scope="module", params=["okami", "okami-rocksdb"])
def okami_cluster(request, custom_okami, custom_okami_rocksdb):
    """
    run on okami and
    okami built with rocksdb (memIAVL + versionDB)
    """
    provider = request.param
    if provider == "okami":
        yield custom_okami
    elif provider == "okami-rocksdb":
        yield custom_okami_rocksdb
    else:
        raise NotImplementedError


def test_gas_eth_tx(okami_cluster):
    """
    When node does not persist ABCI responses
    eth_gasPrice should return an error instead of crashing
    """
    wait_for_block(okami_cluster.cosmos_cli(), 3)
    try:
        okami_cluster.w3.eth.gas_price
        raise Exception("This query should have failed")
    except Exception as error:
        assert "node is not persisting abci responses" in error.args[0]["message"]
