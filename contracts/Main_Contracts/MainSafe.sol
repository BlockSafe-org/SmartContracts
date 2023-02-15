//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./User.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";



contract MainSafe is Ownable, IMainSafe {

    uint256 public userCounter;

    mapping(string => address) public emailToUser;
    mapping(string => address) public merchants;
    mapping(string  => address) internal tokens;
    mapping(string => address) internal priceFeed;

    constructor() {
    }

    function showNoOfUsers() external view returns(uint256) {
        return userCounter;
    }

    // Checks for tokens amongst the stored tokens;
    function checkForToken(string memory tokenName) external returns(address) {
        require(tokens[tokenName] != address(0), "Token Error: Invalid Token!");
        return tokens[tokenName];
    }

    // gets the token/usd price for a token from chainlink.
    function getPriceFeedAddress(string memory tokenName) external returns(address) {
        require(tokens[tokenName] != address(0), "Token Error: Invalid Token!");
        return priceFeed[tokenName];
    }

    // Adds a token.
    function addToken(string memory tokenName,address tokenAddress, address priceFeedAddress) external {
        require(_msgSender() == owner(), "Auth Error: You are not authorized to add a token!");
        require(tokens[tokenName] == address(0), "Token Error: Token already exists!");
        tokens[tokenName] = tokenAddress;
        priceFeed[tokenName] = priceFeedAddress;
    }

    // Removes a token.
    function removeToken(string memory tokenName) external {
        require(_msgSender() == owner(), "Auth Error: You are not authorized to add a token!");
        require(tokens[tokenName] != address(0), "Token Error: Token doesn't exist!");
        tokens[tokenName] = address(0);
        priceFeed[tokenName] = address(0);
    }

    // Swaps two tokens (This is called by the user contract).
    function swap(string memory _email, string memory to, uint256 amount) external {
        require(emailToUser[_email] != address(0), "Invalid email: User not registered!");
        require(tokens[to] != address(0), "Token Error: Invalid 'to' token!");
        (
            /* uint80 roundID */,
            int toPrice,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(priceFeed[to]).latestRoundData();
        uint256 toVal = (amount* 1000000000000000000)/uint256(toPrice);
        ERC20(tokens[to]).transfer(emailToUser[_email], toVal);
    }

    // Creates a user account.
    function addUser(string memory _email, address rewardToken) external {
        // Check if user already has an account.
        require(_msgSender() == owner(), "Ownable: Caller is not the owner of this contract!");
        require(emailToUser[_email] == address(0) ,"User already has an account!");
        User user = new User(_email , rewardToken ,address(this));
        emailToUser[_email] = address(user);
        userCounter += 1;
        emit AddUser(_email, emailToUser[_email]);
    }

    // Function to deposit ethereum
    function deposit() payable external {
        require(_msgSender() == owner(), "Ownable: Caller is not the owner of this contract!");
        emit DepositEth(_msgSender(), msg.value);
    }

    // Function to deposit tokens into mainsafe.
    function deposit(uint256 amount, address tokenAddress) external {
        require(_msgSender() == owner(), "Ownable: Caller is not the owner of this contract!");
        ERC20(tokenAddress).transferFrom(_msgSender(), address(this), amount);
        emit DepositToken(_msgSender() ,amount);
    }

    // Approves and deposits amount from user contract (called by user smart contract.)
    function approveDeposit(string memory tokenName, address userAddress, uint256 amount, string memory _email) external{
        require(emailToUser[_email] != address(0), "Invalid email: User not registered!");
        require(emailToUser[_email] == userAddress, "User unauthorized!");
        ERC20(tokens[tokenName]).transfer(userAddress, amount);
    }

    // Function to withdraw tokens
    function withdraw(uint256 amount ,address tokenAddress) external {
        require(owner() == _msgSender(), "Ownable: caller is not the owner");
        ERC20(tokenAddress).transfer(_msgSender(), amount);
        emit WithdrawToken(amount, _msgSender());
    }

    // Function to withdraw ethereum
    function withdraw(uint256 amount) external {
        require(owner() == _msgSender(), "Ownable: caller is not the owner");
        payable(_msgSender()).transfer(amount);
        emit WithdrawEth(amount, _msgSender());
    }

    // Function to check for an email within the mapping.
    function checkEmail(string memory _email) external returns(address) {
        require(emailToUser[_email] != address(0), "Invalid email: User not registered!");
        return emailToUser[_email];
    }

    // Checks the balance of this smart contract.
    function checkBalance() external view returns(uint256) {
        return address(this).balance;
    }

    function showOwner() external view returns(address) {
        return owner();
    }

    function addMerchant(string memory _email) external {
        require(_msgSender() == owner(), "Auth Error: You are not authorized to add merchant!");
        require(emailToUser[_email] != address(0), "Invalid email: User not registered!");
        require(merchants[_email] == address(0), "Invalid email: User already registered as Merchant!");
        merchants[_email] = emailToUser[_email];
    }

    function merchantFiatPayment(string memory _email, uint256 amount) external {
        require(_msgSender() == owner(), "Auth Error: You are not authorized!");
        require(merchants[_email] != address(0), "Invalid email: User not registered as Merchant!");
          (
            /* uint80 roundID */,
            int tokenPrice,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(priceFeed["USDT"]).latestRoundData();
        uint256 tokenVal = (((amount * 1000000000000000000) / uint256(tokenPrice))*98)/100;
        ERC20(tokens["USDT"]).transfer(emailToUser[_email], tokenVal);
    }

    function checkMerchant(string memory _email) external view returns(address) {
        require(_msgSender() == owner(), "Auth Error: You are not authorized!");
        require(merchants[_email] != address(0), "Invalid email: User not registered as Merchant!");
        return merchants[_email];
    }
    // Function to pay for subscription.
    // Amount is already calulated in ether.
    function merchantSubscribe(string memory _email, uint256 amount) external {
        require(_msgSender() == owner(), "Auth Error: You are not authorized!");
        require(merchants[_email] != address(0), "Invalid email: User not registered as Merchant!");
        IUser(merchants[_email]).approveSubscribe(tokens["USDT"], amount);
    }
}
