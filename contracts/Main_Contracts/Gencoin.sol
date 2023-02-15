//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../../interfaces/IMainsafe.sol";

contract Gencoin is ERC20 {
    
    IMainSafe internal mainSafe;

    constructor(address mainSafeAddress) ERC20("Gencoin", "GCN") {
        _mint(msg.sender, 21000000 ether);
        mainSafe = IMainSafe(mainSafeAddress);
    }

    function mintToken(uint256 amount , string memory email) external {
        address receiverAddress = mainSafe.checkEmail(email);
        _mint(receiverAddress, amount);
    }
} 