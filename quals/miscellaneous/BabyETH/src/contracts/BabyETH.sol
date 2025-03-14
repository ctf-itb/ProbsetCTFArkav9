// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BabyETH {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) public {
        uint256 currBalance = balances[msg.sender];
        require(currBalance >= amount, "Insufficient balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        currBalance -= amount;
        balances[msg.sender] = currBalance;
    }

    // Function to receive ETH
    receive() external payable {}
}
