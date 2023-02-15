import eth_utils
from brownie import (
    accounts, 
    network, 
    config, 
    MainSafe, 
    Gencoin, 
    TetherMock, 
    DAIMock 
    )
from web3 import Web3

LOCAL_ENVIRONMENTS = ["ganache-cli", "development"]
FORKED_ENVIRONMENTS = ["mainnet-fork-dev"]

amount = Web3.toWei(20, "ether")

def get_account(accNo = 0):
    if network.show_active() in LOCAL_ENVIRONMENTS or network.show_active() in FORKED_ENVIRONMENTS:
        if accNo == 0:
            return accounts[0]
        elif accNo == 1:
            return accounts[1]
        else:
            return "No account!"
    else:
        if accNo == 0:
            return accounts.add(config["wallets"]["test_key1"])
        elif accNo == 1:
            return accounts.add(config["wallets"]["test_key2"])
        else:
            return "No account!"

def deploy():
    account = get_account()
    if network.show_active() in LOCAL_ENVIRONMENTS or network.show_active() in FORKED_ENVIRONMENTS:
        tether = TetherMock.deploy({"from":account})
        dai = DAIMock.deploy({"from":account})
        mainsafe = MainSafe.deploy({"from":account})
        tether.transfer(mainsafe.address, amount, {"from":account})
        dai.transfer(mainsafe.address, amount, {"from":account})
        gencoin = Gencoin.deploy(mainsafe.address, {"from":account})
        tx = mainsafe.addToken("USDT",tether.address, "0x92C09849638959196E976289418e5973CC96d645", {"from":account})
        tx = mainsafe.addToken("DAI", dai.address, "0x0FCAa9c899EC5A91eBc3D5Dd869De833b06fB046", {"from":account})
        tx.wait(1)
        return mainsafe, gencoin
    else:
        if len(MainSafe) <= 0:
            if len(Gencoin) <= 0:
                mainsafe = MainSafe.deploy( {"from":account})
                gencoin = Gencoin.deploy(mainsafe.address, {"from":account})
                return mainsafe
            else:
                mainsafe = MainSafe.deploy({"from":account})
                return mainsafe
        else:
            return MainSafe[0]


def deployTether():
    account = get_account()
    mainsafe = deploy()
    if len(TetherMock) <= 0:
        tether =  TetherMock.deploy({"from":account})
        mainsafe.addToken("USDT",tether.address, "0x92C09849638959196E976289418e5973CC96d645", {"from":account})
        return tether
    else:
        return TetherMock[0]

def deployDAI():
    account = get_account()
    mainsafe = deploy()
    if len(DAIMock) <= 0:
        dai = DAIMock.deploy({"from":account})
        mainsafe.addToken("DAI", dai.address, "0x0FCAa9c899EC5A91eBc3D5Dd869De833b06fB046", {"from":account})
        return dai
    else:
        return DAIMock[0]    
