import json

from .utils import (
    ADDRS,
    CONTRACTS,
    KEYS,
    build_deploy_contract_tx,
    deploy_contract,
    send_transaction,
    w3_wait_for_new_blocks,
)


def test_gas_eth_tx(geth, okami_cluster):
    tx_value = 10

    # send a transaction with geth
    geth_gas_price = geth.w3.eth.gas_price
    tx = {"to": ADDRS["community"], "value": tx_value, "gasPrice": geth_gas_price}
    geth_receipt = send_transaction(geth.w3, tx, KEYS["validator"])

    # send an equivalent transaction with okami
    okami_gas_price = okami_cluster.w3.eth.gas_price
    tx = {"to": ADDRS["community"], "value": tx_value, "gasPrice": okami_gas_price}
    okami_receipt = send_transaction(okami_cluster.w3, tx, KEYS["validator"])

    assert geth_receipt.gasUsed == okami_receipt.gasUsed


def test_gas_deployment(geth, okami_cluster):
    # deploy an identical contract on geth and okami
    # ensure that the gasUsed is equivalent
    info = json.loads(CONTRACTS["TestERC20A"].read_text())
    geth_tx = build_deploy_contract_tx(geth.w3, info)
    okami_tx = build_deploy_contract_tx(okami_cluster.w3, info)

    # estimate tx gas
    geth_gas_estimation = geth.w3.eth.estimate_gas(geth_tx)
    okami_gas_estimation = okami_cluster.w3.eth.estimate_gas(okami_tx)

    assert geth_gas_estimation == okami_gas_estimation

    # sign and send tx
    geth_contract_receipt = send_transaction(geth.w3, geth_tx)
    okami_contract_receipt = send_transaction(okami_cluster.w3, okami_tx)
    assert geth_contract_receipt.status == 1
    assert okami_contract_receipt.status == 1

    assert geth_contract_receipt.gasUsed == okami_contract_receipt.gasUsed

    # gasUsed should be same as estimation
    assert geth_contract_receipt.gasUsed == geth_gas_estimation
    assert okami_contract_receipt.gasUsed == okami_gas_estimation


def test_gas_call(geth, okami_cluster):
    function_input = 10

    # deploy an identical contract on geth and okami
    # ensure that the contract has a function which consumes non-trivial gas
    geth_contract, _ = deploy_contract(geth.w3, CONTRACTS["BurnGas"])
    okami_contract, _ = deploy_contract(okami_cluster.w3, CONTRACTS["BurnGas"])

    # call the contract and get tx receipt for geth
    geth_gas_price = geth.w3.eth.gas_price
    geth_tx = geth_contract.functions.burnGas(function_input).build_transaction(
        {"from": ADDRS["validator"], "gasPrice": geth_gas_price}
    )
    geth_gas_estimation = geth.w3.eth.estimate_gas(geth_tx)
    geth_call_receipt = send_transaction(geth.w3, geth_tx)

    # repeat the above for okami
    okami_gas_price = okami_cluster.w3.eth.gas_price
    okami_tx = okami_contract.functions.burnGas(function_input).build_transaction(
        {"from": ADDRS["validator"], "gasPrice": okami_gas_price}
    )
    okami_gas_estimation = okami_cluster.w3.eth.estimate_gas(okami_tx)
    okami_call_receipt = send_transaction(okami_cluster.w3, okami_tx)

    # ensure gas estimation is the same
    assert geth_gas_estimation == okami_gas_estimation

    # ensure that the gasUsed is equivalent
    assert geth_call_receipt.gasUsed == okami_call_receipt.gasUsed

    # ensure gasUsed == gas estimation
    assert geth_call_receipt.gasUsed == geth_gas_estimation
    assert okami_call_receipt.gasUsed == okami_gas_estimation


def test_block_gas_limit(okami_cluster):
    tx_value = 10

    # get the block gas limit from the latest block
    w3_wait_for_new_blocks(okami_cluster.w3, 5)
    block = okami_cluster.w3.eth.get_block("latest")
    exceeded_gas_limit = block.gasLimit + 100

    # send a transaction exceeding the block gas limit
    okami_gas_price = okami_cluster.w3.eth.gas_price
    tx = {
        "to": ADDRS["community"],
        "value": tx_value,
        "gas": exceeded_gas_limit,
        "gasPrice": okami_gas_price,
    }

    # expect an error due to the block gas limit
    try:
        send_transaction(okami_cluster.w3, tx, KEYS["validator"])
    except Exception as error:
        assert "exceeds block gas limit" in error.args[0]["message"]

    # deploy a contract on okami
    okami_contract, _ = deploy_contract(okami_cluster.w3, CONTRACTS["BurnGas"])

    # expect an error on contract call due to block gas limit
    try:
        okami_txhash = okami_contract.functions.burnGas(exceeded_gas_limit).transact(
            {
                "from": ADDRS["validator"],
                "gas": exceeded_gas_limit,
                "gasPrice": okami_gas_price,
            }
        )
        (okami_cluster.w3.eth.wait_for_transaction_receipt(okami_txhash))
    except Exception as error:
        assert "exceeds block gas limit" in error.args[0]["message"]

    return
