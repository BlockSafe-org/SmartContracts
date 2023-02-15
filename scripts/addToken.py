from scripts.helpful_scripts import deploy, get_account, deployTether, deployDAI

from web3 import Web3

amount = Web3.toWei(100, "ether")

def main():
    account = get_account()
    mainsafe = deploy()
    tether = deployTether()
    tether.transfer(mainsafe.address, amount, {"from":account})
    dai = deployDAI()
    tx = dai.transfer(mainsafe.address, amount, {"from":account})
    tx.wait(1)