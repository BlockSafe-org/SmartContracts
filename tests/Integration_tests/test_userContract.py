from brownie import interface, exceptions
from scripts.helpful_scripts import deploy, get_account
from web3 import Web3

amount = Web3.toWei(100, "ether")
value = 20000000

def test_swap():
    account = get_account()
    mainsafe = deploy()
    mainsafe.addUser("ssalibenjamin@gmail.com", "0x3936F274cc05b28229308F4aaD46AB5217Ed0F80", {"from":account})
    userAddress = mainsafe.emailToUser("ssalibenjamin@gmail.com")
    user = interface.IUser(userAddress)
    tx = user.deposit("USDT",amount,"ssalibenjamin@gmail.com", {"from":account})
    tx = user.swap("ssalibenjamin@gmail.com", "USDT", "DAI", value, {"from":account})
