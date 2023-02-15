from scripts.helpful_scripts import get_account, deploy
from brownie import interface
from web3 import Web3

amount = Web3.toWei(10, "ether")
value = 200000000


def main():
    account = get_account()
    mainsafe = deploy()
    #mainsafe.addUser("ssalibenjamin@gmail.com", Gencoin[0].address, {"from":account})
    # type: ignore 
    userAddress = mainsafe.emailToUser("ssalibenjamin@gmail.com")
   user = interface.IUser(userAddress)
    tx = user.deposit("USDT",amount,"ssalibenjamin@gmail.com", {"from":account})
    tx = user.swap("ssalibenjamin@gmail.com", "USDT", "DAI", value, {"from":account})