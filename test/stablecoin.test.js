const { expect } = require('chai');
const { web3 } = require('@openzeppelin/test-helpers/src/setup');
const { BN } = web3.utils;

const Stablecoin = artifacts.require('Stablecoin');

contract('Stablecoin', (accounts) => {
  const [owner, user1, user2] = accounts;

  beforeEach(async () => {
    this.stablecoin = await Stablecoin.new({ from: owner });
  });

  describe('Initialization', () => {
    it('should have an initial supply of 1 million tokens', async () => {
      const totalSupply = await this.stablecoin.totalSupply();
      expect(totalSupply).to.be.bignumber.equal(new BN('1000000', 10));
    });

    it('should have the owner as the initial admin', async () => {
      const isAdmin = await this.stablecoin.isAdmin(owner);
      expect(isAdmin).to.be.true;
    });
  });

  describe('Transfer', () => {
    it('should allow the owner to transfer tokens to user1', async () => {
      await this.stablecoin.transfer(user1, new BN('100', 10), { from: owner });
      const user1Balance = await this.stablecoin.balanceOf(user1);
      expect(user1Balance).to.be.bignumber.equal(new BN('100', 10));
    });

    it('should not allow user2 to transfer tokens without approval', async () => {
      await expectRevert(
        this.stablecoin.transfer(user1, new BN('100', 10), { from: user2 }),
        'Only approved accounts can transfer tokens'
      );
    });
  });

  describe('Interest', () => {
    it('should accrue interest for user1', async () => {
      await this.stablecoin.accrueInterest({ from: owner });
      const user1Balance = await this.stablecoin.balanceOf(user1);
      expect(user1Balance).to.be.bignumber.gt(new BN('100', 10));
    });

    it('should not accrue interest for user2 without a balance', async () => {
      await expectRevert(
        this.stablecoin.accrueInterest({ from: user2 }),
        'Only accounts with a balance can accrue interest'
      );
    });
  });

  describe('Admin', () => {
    it('should allow the owner to add a new admin', async () => {
      await this.stablecoin.addAdmin(user2, { from: owner });
      const isAdmin = await this.stablecoin.isAdmin(user2);
      expect(isAdmin).to.be.true;
    });

    it('should not allow user1 to add a new admin', async () => {
      await expectRevert(
        this.stablecoin.addAdmin(user2, { from: user1 }),
        'Only the owner can add new admins'
      );
    });
  });
});
