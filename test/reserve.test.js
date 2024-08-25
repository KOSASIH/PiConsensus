const { expect } = require('chai');
const { web3 } = require('@openzeppelin/test-helpers/src/setup');
const { BN } = web3.utils;

const Reserve = artifacts.require('Reserve');

contract('Reserve', (accounts) => {
  const [owner, user1, user2] = accounts;

  beforeEach(async () => {
    this.reserve = await Reserve.new({ from: owner });
  });

  describe('Initialization', () => {
    it('should have an initial reserve ratio of 20%', async () => {
      const reserveRatio = await this.reserve.reserveRatio();
      expect(reserveRatio).to.be.bignumber.equal(new BN('200000000000000000', 10));
    });
  });

  describe('Deposit', () => {
    it('should allow the owner to deposit tokens into the reserve', async () => {
      await this.reserve.deposit(new BN('100', 10), { from: owner });
      const reserveBalance = await this.reserve.balance();
      expect(reserveBalance).to.be.bignumber.equal(new BN('100', 10));
    });

    it('should not allow user1 to deposit tokens into the reserve', async () => {
      await expectRevert(
        this.reserve.deposit(new BN('100', 10), { from: user1 }),
        'Only the owner can deposit tokens into the reserve'
      );
    });
  });

  describe('Withdrawal', () => {
    it('should allow the owner to withdraw tokens from the reserve', async () => {
      await this.reserve.withdraw(new BN('50', 10), { from: owner });
      const reserveBalance = await this.reserve.balance();
      expect(reserveBalance).to.be.bignumber.equal(new BN('50', 10));
    });

    it('should not allow user1 to withdraw tokens from the reserve', async () => {
      await expectRevert(
        this.reserve.withdraw(new BN('50', 10), { from: user1 }),
        'Only the owner can withdraw tokens from the reserve'
      );
    });
  });
});
