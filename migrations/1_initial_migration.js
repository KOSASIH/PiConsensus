const { deployer, web3 } = require('@truffle/deployer');
const { BN } = web3.utils;

const Oracle = artifacts.require('Oracle');
const Reserve = artifacts.require('Reserve');
const Stablecoin = artifacts.require('Stablecoin');

module.exports = async (deployer) => {
  // Set up the Oracle contract
  const oracle = await deployer.deploy(Oracle, '0x0000000000000000000000000000000000000001', {
    gas: 5000000,
    gasPrice: new BN('20000000000', 10),
  });

  console.log(`Oracle contract deployed at ${oracle.address}`);

  // Set up the Reserve contract
  const reserve = await deployer.deploy(Reserve, oracle.address, {
    gas: 5000000,
    gasPrice: new BN('20000000000', 10),
  });

  console.log(`Reserve contract deployed at ${reserve.address}`);

  // Set up the Stablecoin contract
  const stablecoin = await deployer.deploy(Stablecoin, oracle.address, reserve.address, {
    gas: 5000000,
    gasPrice: new BN('20000000000', 10),
  });

  console.log(`Stablecoin contract deployed at ${stablecoin.address}`);

  // Initialize the Stablecoin contract with an initial supply of 1 million tokens
  await stablecoin.initialize(1000000, { from: deployer.accounts[0] });

  console.log('Stablecoin contract initialized with 1 million tokens');

  // Set the Oracle and Reserve contracts as dependencies for the Stablecoin contract
  await stablecoin.setOracle(oracle.address, { from: deployer.accounts[0] });
  await stablecoin.setReserve(reserve.address, { from: deployer.accounts[0] });

  console.log('Oracle and Reserve contracts set as dependencies for Stablecoin contract');
};
