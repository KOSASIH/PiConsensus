pragma solidity ^0.8.17;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC20/SafeERC20.sol";

contract PiCoin {
    // Mapping of balances
    mapping (address => uint256) public balances;

    // Total supply of Pi Coin
    uint256 public totalSupply;

    // Decimal places for Pi Coin
    uint256 public constant decimals = 18;

    // Initial supply of Pi Coin
    uint256 public constant INITIAL_SUPPLY = 314159000000000000000; // $314.159

    // Event emitted when tokens are transferred
    event Transfer(address indexed from, address indexed to, uint256 value);

    // Event emitted when tokens are minted
    event Mint(address indexed to, uint256 value);

    // Event emitted when tokens are burned
    event Burn(address indexed from, uint256 value);

    /**
     * @dev Initializes the contract by setting the total supply and minting the initial supply to the owner.
     */
    constructor() public {
        totalSupply = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        emit Mint(msg.sender, INITIAL_SUPPLY);
    }

    /**
     * @dev Transfers tokens from one address to another.
     * @param _from The address to transfer from.
     * @param _to The address to transfer to.
     * @param _value The amount of tokens to transfer.
     */
    function transfer(address _from, address _to, uint256 _value) public {
        require(_value <= balances[_from], "Insufficient balance");
        balances[_from] -= _value;
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
    }

    /**
     * @dev Mints new tokens and adds them to the total supply.
     * @param _to The address to mint tokens to.
     * @param _value The amount of tokens to mint.
     */
    function mint(address _to, uint256 _value) public {
        totalSupply += _value;
        balances[_to] += _value;
        emit Mint(_to, _value);
    }

    /**
     * @dev Burns tokens from the total supply.
     * @param _from The address to burn tokens from.
     * @param _value The amount of tokens to burn.
     */
    function burn(address _from, uint256 _value) public {
        require(_value <= balances[_from], "Insufficient balance");
        totalSupply -= _value;
        balances[_from] -= _value;
        emit Burn(_from, _value);
    }
}
