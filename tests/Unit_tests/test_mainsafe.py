from brownie import exceptions, interface
from scripts.helpful_scripts import deploy, get_account
from web3 import Web3
import pytest


amount = Web3.toWei(10, "ether")

def test_deploy():
    mainsafe, gencoin = deploy()
    assert mainsafe != None

def test_show_no_of_users():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    tx = mainsafe.showNoOfUsers({"from":account})
    assert tx == 1

def test_add_user():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    assert mainsafe.userCounter() == 1

def test_checkForToken():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.checkForToken("USDT", {"from":account})
    tx.wait(1)

def test_getPriceFeedAddress():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.getPriceFeedAddress("USDT", {"from":account})
    tx.wait(1)
    assert tx.return_value == "0x92C09849638959196E976289418e5973CC96d645"

def test_addToken():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addToken("GCN", gencoin.address, "0xE097d6B3100777DC31B34dC2c58fB524C2e76921", {"from":account})
    tx.wait(1)
    tx = mainsafe.checkForToken("GCN",{"from":account})
    tx.wait(1)
    assert tx.return_value == gencoin.address

def test_removeToken():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addToken("GCN", gencoin.address, "0xE097d6B3100777DC31B34dC2c58fB524C2e76921", {"from":account})
    tx.wait(1)
    tx = mainsafe.checkForToken("GCN",{"from":account})
    tx.wait(1)
    assert tx.return_value == gencoin.address
    tx = mainsafe.removeToken("GCN",{"from":account})
    tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        tx = mainsafe.checkForToken("GCN",{"from":account})
        tx.wait(1)
        

def test_check_email():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address,{"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com",{"from":account})
    assert tx.return_value != "0x0000000000000000000000000000000000000000"

def test_deposit_eth():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.deposit({"from":account,"value":Web3.toWei(1, "ether")})
    tx.wait(1)
    assert mainsafe.balance() == Web3.toWei(1, "ether")

def test_deposit_token():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = gencoin.approve(mainsafe.address, amount, {"from":account})
    tx.wait(1)
    tx = mainsafe.deposit(amount, gencoin.address,{"from":account})
    tx.wait(1)
    assert gencoin.balanceOf(mainsafe.address,{"from":account}) == Web3.toWei(10, "ether")

def test_withdraw_eth():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.deposit({"from":account,"value":Web3.toWei(1, "ether")})
    tx.wait(1)
    tx = mainsafe.withdraw(Web3.toWei(0.1, "ether"), {"from":account})
    assert mainsafe.balance() == Web3.toWei(0.9, "ether")

def test_withdraw_token():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = gencoin.approve(mainsafe.address, amount, {"from":account})
    tx.wait(1)
    tx = mainsafe.deposit(amount, gencoin.address,{"from":account})
    tx.wait(1)
    assert gencoin.balanceOf(mainsafe.address, {"from":account}) == amount
    tx = mainsafe.withdraw(amount, gencoin.address,{"from":account})
    tx.wait(1)
    assert gencoin.balanceOf(mainsafe.address, {"from":account}) == 0


def test_check_balance():
    account = get_account()
    mainsafe, gencoin = deploy()    
    tx = mainsafe.deposit({"from":account,"value":Web3.toWei(1, "ether")})
    tx.wait(1)
    tx = mainsafe.checkBalance({"from":account})
    assert tx == Web3.toWei(1, "ether")

def test_addMerchant():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx = mainsafe.addMerchant("ssalibenjamin@gmail.com", {"from":account})
    assert mainsafe.merchants("ssalibenjamin@gmail.com") != "0x0000000000000000000000000000000000000000"

def test_checkMerchant():
    account = get_account()
    mainsafe, gencoin = deploy()
    mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    mainsafe.addMerchant("ssalibenjamin@gmail.com", {"from":account})
    assert mainsafe.checkMerchant("ssalibenjamin@gmail.com") != "0x0000000000000000000000000000000000000000"

def test_merchantSubscribe():
    account = get_account()
    mainsafe, gencoin = deploy()
    mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    mainsafe.addMerchant("ssalibenjamin@gmail.com", {"from":account})
    userAddress = mainsafe.emailToUser("ssalibenjamin@gmail.com")
    user = interface.IUser(userAddress)
    user.deposit("USDT", amount, "ssalibenjamin@gmail.com", {"from":account})
    mainsafe.merchantSubscribe("ssalibenjamin@gmail.com",Web3.toWei(0.2, "ether"), {"from":account})



