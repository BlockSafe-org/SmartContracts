//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IUser {

    event Deposit(uint256 amount);

    event Withdraw(uint256 amount);

    event SendTokensToEmail(uint256 amount ,string receiver);

    event SendTokensToAddress(uint256 amount ,address receiver);

    function deposit(string calldata tokenName, uint256 amount, string calldata _email) external;

    function withdraw(string calldata tokenName,uint256 amount, string calldata _email) external;

    function sendTokensEmail(string calldata tokenName, uint256 amount ,string memory receiverEmail, string calldata _email) external;

    function sendTokensAddress(string calldata tokenName ,uint256 amount ,address receiverAddress, string calldata _email) external;

    function showEmail() external view returns(string memory);
    
    function swap(string calldata _email, string calldata from, string calldata to, uint256 amount) external;

    function approveSubscribe(address paymentToken, uint256 amount) external;
}