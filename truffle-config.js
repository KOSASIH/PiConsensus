module.exports = {
  // Network settings
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*", // Match any network id
      gas: 8000000,
      gasPrice: 20000000000
    },
    test: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*", // Match any network id
      gas: 8000000,
      gasPrice: 20000000000
    },
    mainnet: {
      provider: () => new Web3.providers.HttpProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"),
      network_id: 1,
      gas: 8000000,
      gasPrice: 20000000000
    }
  },

  // Compiler settings
  compilers: {
    solc: {
      version: "0.8.10",
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        }
      }
    }
  },

  // Migrations settings
  migrations: {
    deployer: {
      type: "truffle-deployer"
    }
  },

  // Test settings
  test: {
    testMatch: ["**/*.test.js"],
    testPath: "test",
    timeout: 30000
  }
};
