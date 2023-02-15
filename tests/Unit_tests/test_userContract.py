from brownie import interface
from scripts.helpful_scripts import deploy, get_account
from web3 import Web3

amount = Web3.toWei(0.1, "ether")

def test_show_email():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    userAddress = tx.return_value
    user = interface.IUser(userAddress)
    tx = user.showEmail({"from":account})
    assert tx == "ssalibenjamin@gmail.com"


def test_deposit():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    userAddress = tx.return_value
    user = interface.IUser(userAddress)
    tx = mainsafe.addToken("TEN", tetherMock.address, "0xE097d6B3100777DC31B34dC2c58fB524C2e76921", {"from":account})
    tetherMock.transfer(mainsafe.address, amount*2, {"from":account})
    tx = user.deposit("TEN",amount,"ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    assert tetherMock.balanceOf(userAddress, {"from":account}) == amount

def test_withdraw():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    userAddress = tx.return_value
    user = interface.IUser(userAddress)
    tx = user.deposit( "USDT",amount,"ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    assert tetherMock.balanceOf(userAddress, {"from":account}) == amount
    tx = user.withdraw("USDT", amount,"ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    assert tetherMock.balanceOf(userAddress, {"from":account}) == 0
   

def test_send_tokens_email():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    tx = mainsafe.addUser("benzidarwin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    userAddress = tx.return_value
    tx = mainsafe.addToken("TEN", tetherMock.address, "0xE097d6B3100777DC31B34dC2c58fB524C2e76921", {"from":account})
    tx = tetherMock.transfer(userAddress, amount*2, {"from":account})
    tx.wait(1)
    user = interface.IUser(userAddress)
    tx = user.sendTokensEmail("TEN", amount, "benzidarwin@gmail.com","ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)

def test_send_tokens_eth():
    account = get_account()
    mainsafe, gencoin = deploy()
    tx = mainsafe.addUser("ssalibenjamin@gmail.com", gencoin.address, {"from":account})
    tx.wait(1)
    tx = mainsafe.checkEmail("ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)
    userAddress = tx.return_value
    tx = mainsafe.addToken("TEN", tetherMock.address, "0xE097d6B3100777DC31B34dC2c58fB524C2e76921", {"from":account})
    tetherMock.transfer(userAddress, amount*2, {"from":account})
    user = interface.IUser(userAddress)
    tx =  user.sendTokensAddress("TEN", amount, get_account(1),"ssalibenjamin@gmail.com", {"from":account})
    tx.wait(1)