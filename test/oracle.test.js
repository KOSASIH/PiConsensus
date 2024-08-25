const { expect } = require('chai');
const { web3 } = require('@openzeppelin/test-helpers/src/setup');
const { BN } = web3.utils;

const Oracle = artifacts.require('Oracle');

contract('Oracle', (accounts) => {
  const [owner, user1, user2] = accounts;

  beforeEach(async () => {
    this.oracle = await Oracle.new({ from: owner });
  });

  describe('Initialization', () => {
    it('should have an initial price of 1 USD per token', async () => {
      const price = await this.oracle.getPrice();
      expect(price).to.be.bignumber.equal(new BN('100000000', 10));
    });
  });

  describe('Price Updates', () => {
    it('should allow the owner to update the price', async () => {
      await this.oracle.updatePrice(new BN('150000000', 10), { from: owner });
      const newPrice = await this.oracle.getPrice();
      expect(newPrice).to.be.bignumber.equal(new BN('150000000', 10));
    });

    it('should not allow user1 to update the price', async () => {
      await expectRevert(
        this.oracle.updatePrice(new BN('150000000', 10), { from: user1 }),
        'Only the owner can update the price'
      );
    });
  });

  describe('Query', () => {
    it('should return the current price for a query', async () => {
      const price = await this.oracle.query();
      expect(price).to.be.bignumber.equal(new BN('100000000', 10));
    });
  });
});
