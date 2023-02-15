//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/IUser.sol";
import "./Gencoin.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract User is Ownable, IUser {

    string private email;
    address internal gencoin;
    IMainSafe internal mainSafe;
    mapping(address => uint256) public accountBalances;

    constructor(string memory _email, address _gencoin, address _mainSafe) {
        email = _email;
        gencoin = _gencoin;
        mainSafe = IMainSafe(_mainSafe);
        transferOwnership(_msgSender());
    }

    function showEmail() external view returns(string memory){
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        return email;
    }

    // Mainsafe deposits an amount of tokens on the user's account / Also used to send staking rewards to user's account.
    function deposit(string memory tokenName, uint256 amount, string memory _email) external {
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        mainSafe.checkEmail(_email);
        address tokenAddress = mainSafe.checkForToken(tokenName);
        mainSafe.approveDeposit(tokenName, address(this), amount, _email);
        Gencoin(gencoin).mintToken(amount/10, email);
        accountBalances[tokenAddress] += amount;
        emit Deposit(amount);
    }

    // Mainsafe calls a function to withdraw an amount of users tokens.
    function withdraw(string memory tokenName, uint256 amount, string memory _email) external {
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        mainSafe.checkEmail(_email);
        address tokenAddress = mainSafe.checkForToken(tokenName);
        require(accountBalances[tokenAddress] <= amount, "Insufficient Funds!");
        ERC20(tokenAddress).transfer(address(mainSafe), amount);
        emit Withdraw(amount);
    }

    // Sends tokens to a User Contract.
    function sendTokensEmail(string memory tokenName, uint256 amount, string memory receiverEmail, string memory _email) external {
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        address tokenAddress = mainSafe.checkForToken(tokenName);
        mainSafe.checkEmail(_email);
        address receiverAddress = mainSafe.checkEmail(receiverEmail);
        ERC20(tokenAddress).transfer(receiverAddress, amount);
        ERC20(tokenAddress).transfer(address(mainSafe), (amount * 2)/100);
        emit SendTokensToEmail(amount, receiverEmail);
    }

    // Sends tokens to an ethereum address.
    function sendTokensAddress(string memory tokenName, uint256 amount, address receiverAddress, string memory _email) external {
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        address tokenAddress = mainSafe.checkForToken(tokenName);
        ERC20(tokenAddress).transfer(receiverAddress, amount);
        ERC20(tokenAddress).transfer(address(mainSafe), (amount * 2)/100);
        emit SendTokensToAddress(amount, receiverAddress);
    }

        // Swaps two tokens.
     function swap(string memory _email, string memory from, string memory to, uint256 amount) external {
        require(_msgSender() == mainSafe.showOwner(), "Ownable: caller is not the owner");
        mainSafe.checkEmail(_email);
        address fromPriceFeedAddress = mainSafe.getPriceFeedAddress(from);
        address fromTokenAddress = mainSafe.checkForToken(from);
          (
            /* uint80 roundID */,
            int fromPrice,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(fromPriceFeedAddress).latestRoundData();
        uint256 fromVal = calculateRate(amount, uint256(fromPrice));
        ERC20(fromTokenAddress).transfer(address(mainSafe), fromVal);
        uint256 toAmount = (amount * 98) / 100;
        mainSafe.swap(_email, to, toAmount);
        Gencoin(gencoin).mintToken(amount/10, email);
     }

    function calculateRate(uint256 amount, uint256 fromPrice) internal pure returns(uint256) {
        return (amount * 1000000000000000000) / uint256(fromPrice);
    }

    function approveSubscribe(address paymentToken, uint256 amount) external {
        require(_msgSender() == address(mainSafe), "Ownable: caller is not the mainsafe!");
        ERC20(paymentToken).transfer(address(mainSafe), amount);
    }
}