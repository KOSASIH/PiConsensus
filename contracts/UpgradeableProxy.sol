// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title UpgradeableProxy — PiConsensus Self-Upgrading Smart Contract Framework
 * @notice Enables secure contract upgrades via governance or admin, following industry-standard proxy patterns.
 *         Designed for unstoppable, future-proof smart contracts.
 */

contract UpgradeableProxy {
    // Storage slot for the address of the current implementation
    bytes32 private constant IMPLEMENTATION_SLOT = keccak256("piconsensus.proxy.implementation");
    // Storage slot for the proxy admin
    bytes32 private constant ADMIN_SLOT = keccak256("piconsensus.proxy.admin");
    // Storage slot for contract version
    bytes32 private constant VERSION_SLOT = keccak256("piconsensus.proxy.version");

    event Upgraded(address indexed newImplementation, string version);
    event AdminChanged(address indexed previousAdmin, address indexed newAdmin);

    modifier onlyAdmin() {
        require(msg.sender == _admin(), "Not admin");
        _;
    }

    constructor(address _initialImplementation, string memory _initialVersion) {
        _setAdmin(msg.sender);
        _upgradeTo(_initialImplementation, _initialVersion);
    }

    function _implementation() internal view returns (address impl) {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            impl := sload(slot)
        }
    }

    function _admin() internal view returns (address adm) {
        bytes32 slot = ADMIN_SLOT;
        assembly {
            adm := sload(slot)
        }
    }

    function _version() public view returns (string memory ver) {
        bytes32 slot = VERSION_SLOT;
        assembly {
            ver := sload(slot)
        }
    }

    function admin() external view returns (address) {
        return _admin();
    }

    function changeAdmin(address newAdmin) external onlyAdmin {
        require(newAdmin != address(0), "Zero address");
        emit AdminChanged(_admin(), newAdmin);
        _setAdmin(newAdmin);
    }

    function upgradeTo(address newImplementation, string memory newVersion) external onlyAdmin {
        _upgradeTo(newImplementation, newVersion);
    }

    function _upgradeTo(address newImplementation, string memory newVersion) internal {
        require(newImplementation != address(0), "Zero address");
        bytes32 implSlot = IMPLEMENTATION_SLOT;
        bytes32 versionSlot = VERSION_SLOT;
        assembly {
            sstore(implSlot, newImplementation)
            sstore(versionSlot, newVersion)
        }
        emit Upgraded(newImplementation, newVersion);
    }

    // Delegate all call data to the implementation
    fallback() external payable {
        address impl = _implementation();
        require(impl != address(0), "No implementation");
        assembly {
            // Copy msg.data
            calldatacopy(0, 0, calldatasize())
            // Delegatecall to the implementation
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            let size := returndatasize()
            returndatacopy(0, 0, size)
            switch result
            case 0 { revert(0, size) }
            default { return(0, size) }
        }
    }

    receive() external payable {}

    function _setAdmin(address newAdmin) internal {
        bytes32 slot = ADMIN_SLOT;
        assembly {
            sstore(slot, newAdmin)
        }
    }
}
