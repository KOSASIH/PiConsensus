pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/SafeERC20.sol";

contract Reserve {
    // Mapping of reserve balances
    mapping (address => uint256) public reserveBalances;

    // Event emitted when funds are deposited into the reserve
    event Deposit(address _sender, uint256 _amount);

    // Event emitted when funds are withdrawn from the reserve
    event Withdrawal(address _sender, uint256 _amount);

    // Event emitted when the stablecoin contract is updated with the latest reserve balance
    event ReserveBalanceUpdated(uint256 _newBalance);

    // Function to deposit funds into the reserve
    function deposit(uint256 _amount) public {
        // Transfer the funds from the sender to the reserve
        SafeERC20.safeTransferFrom(msg.sender, address(this), _amount);

        // Update the reserve balance
        reserveBalances[msg.sender] += _amount;

        // Emit the Deposit event
        emit Deposit(msg.sender, _amount);
    }

    // Function to withdraw funds from the reserve
    function withdraw(uint256 _amount) public {
        // Check if the sender has sufficient balance in the reserve
        require(reserveBalances[msg.sender] >= _amount, "Insufficient balance");

        // Transfer the funds from the reserve to the sender
        SafeERC20.safeTransfer(msg.sender, _amount);

        // Update the reserve balance
        reserveBalances[msg.sender] -= _amount;

        // Emit the Withdrawal event
        emit Withdrawal(msg.sender, _amount);
    }

    // Function to update the stablecoin contract with the latest reserve balance
    function updateStablecoinContract() public {
        // Get the latest reserve balance
        uint256 newBalance = getReserveBalance();

        // Update the stablecoin contract with the latest reserve balance
        StablecoinContract(address).updateReserveBalance(newBalance);

        // Emit the ReserveBalanceUpdated event
        emit ReserveBalanceUpdated(newBalance);
    }

    // Function to get the reserve balance
    function getReserveBalance() public view returns (uint256) {
        // Calculate the total reserve balance
        uint256 totalBalance = 0;
        for (address user in reserveBalances) {
            totalBalance += reserveBalances[user];
        }
        return totalBalance;
    }
}
