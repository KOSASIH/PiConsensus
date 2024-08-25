const { deployer, web3 } = require('@truffle/deployer');
const { BN } = web3.utils;

const Stablecoin = artifacts.require('Stablecoin');

module.exports = async (deployer) => {
  // Get the deployed Stablecoin contract
  const stablecoin = await Stablecoin.deployed();

  // Add a new admin to the Stablecoin contract
  const newAdmin = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e';
  await stablecoin.addAdmin(newAdmin, { from: deployer.accounts[0] });

  console.log(`Added ${newAdmin} as a new admin to the Stablecoin contract`);

  // Set the interest rate for the Stablecoin contract
  const interestRate = new BN('500000000000000000', 10); // 5% interest rate
  await stablecoin.setInterestRate(interestRate, { from: deployer.accounts[0] });

  console.log(`Set interest rate to ${interestRate} for the Stablecoin contract`);

  // Set the reserve ratio for the Stablecoin contract
  const reserveRatio = new BN('200000000000000000', 10); // 20% reserve ratio
  await stablecoin.setReserveRatio(reserveRatio, { from: deployer.accounts[0] });

  console.log(`Set reserve ratio to ${reserveRatio} for the Stablecoin contract`);
};
