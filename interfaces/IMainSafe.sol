//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


interface IMainSafe {

    event AddUser(string name,address userAddress);

    event DepositToken(address msgSender ,uint256 amount);

    event DepositEth(address msgSender ,uint256 amount);

    event ApproveToken(uint256 amount ,address tokenAddress);

    event WithdrawEth(uint256 amount, address contractCaller);

    event WithdrawToken(uint256 amount, address contractCaller);

    event UserStake(uint256 amount ,address tokenAddress ,address user);

    event ShowContractAddress(address user);

    function showNoOfUsers() external view returns(uint256);

    function addUser(string calldata _email , address rewardToken) external;

    function addToken(string calldata tokenName,address tokenAddress, address priceFeedAddress) external;

    function getPriceFeedAddress(string calldata name) external returns(address);

    function checkForToken(string calldata name) external returns(address);

    function deposit() payable external;

    function deposit(uint256 amount, address tokenAdress) external;

    function withdraw(uint256 amount) external;

    function withdraw(uint256 amount, address tokenAddress) external;

    function checkEmail(string calldata _email) external returns(address);

    function swap(string calldata _email, string calldata to, uint256 amount) external;

    function approveDeposit(string calldata tokenName, address userAddress, uint256 amount, string memory _email) external;

    function showOwner() external view returns(address);

    function merchantSubscribe(string calldata _email, uint256 amount) external;

    function checkMerchant(string calldata _email) external returns(address);

    function merchantFiatPayment(string calldata email, uint256 amount) external;
}