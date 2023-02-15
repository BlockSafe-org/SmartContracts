//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";


interface IGencoin is IERC20 {
    function mintToken(uint256 amount ,address receiver) external;
}