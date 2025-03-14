// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./BabyETH.sol";

contract Setup {
    bool private solved;
    BabyETH public babyETH;

    constructor() payable {
        babyETH = new BabyETH();
        babyETH.deposit{value: 0.5 ether}();
    }

    function isSolved() external view returns (bool) {
        return address(babyETH).balance == 0;
    }
}