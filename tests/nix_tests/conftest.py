import pytest

from .network import setup_okami, setup_okami_rocksdb, setup_geth


@pytest.fixture(scope="session")
def okami(tmp_path_factory):
    path = tmp_path_factory.mktemp("okami")
    yield from setup_okami(path, 26650)


@pytest.fixture(scope="session")
def okami_rocksdb(tmp_path_factory):
    path = tmp_path_factory.mktemp("okami-rocksdb")
    yield from setup_okami_rocksdb(path, 20650)


@pytest.fixture(scope="session")
def geth(tmp_path_factory):
    path = tmp_path_factory.mktemp("geth")
    yield from setup_geth(path, 8545)


@pytest.fixture(scope="session", params=["okami", "okami-ws"])
def okami_rpc_ws(request, okami):
    """
    run on both okami and okami websocket
    """
    provider = request.param
    if provider == "okami":
        yield okami
    elif provider == "okami-ws":
        okami_ws = okami.copy()
        okami_ws.use_websocket()
        yield okami_ws
    else:
        raise NotImplementedError


@pytest.fixture(scope="module", params=["okami", "okami-ws", "okami-rocksdb", "geth"])
def cluster(request, okami, okami_rocksdb, geth):
    """
    run on okami, okami websocket,
    okami built with rocksdb (memIAVL + versionDB)
    and geth
    """
    provider = request.param
    if provider == "okami":
        yield okami
    elif provider == "okami-ws":
        okami_ws = okami.copy()
        okami_ws.use_websocket()
        yield okami_ws
    elif provider == "geth":
        yield geth
    elif provider == "okami-rocksdb":
        yield okami_rocksdb
    else:
        raise NotImplementedError


@pytest.fixture(scope="module", params=["okami", "okami-rocksdb"])
def okami_cluster(request, okami, okami_rocksdb):
    """
    run on okami default build &
    okami with rocksdb build and memIAVL + versionDB
    """
    provider = request.param
    if provider == "okami":
        yield okami
    elif provider == "okami-rocksdb":
        yield okami_rocksdb
    else:
        raise NotImplementedError
