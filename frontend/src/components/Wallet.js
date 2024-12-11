import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import './Wallet.css'; // Assuming you have some CSS for styling

const Wallet = () => {
    const [walletAddress, setWalletAddress] = useState('');
    const [balance, setBalance] = useState('0');
    const [amount, setAmount] = useState('');
    const [recipient, setRecipient] = useState('');
    const [provider, setProvider] = useState(null);

    useEffect(() => {
        const initWallet = async () => {
            if (window.ethereum) {
                const provider = new ethers.providers.Web3Provider(window.ethereum);
                setProvider(provider);
                const accounts = await provider.send("eth_requestAccounts", []);
                setWalletAddress(accounts[0]);
                fetchBalance(accounts[0], provider);
            } else {
                alert('Please install MetaMask!');
            }
        };
        initWallet();
    }, []);

    const fetchBalance = async (address, provider) => {
        const balance = await provider.getBalance(address);
        setBalance(ethers.utils.formatEther(balance));
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!provider) return;

        const signer = provider.getSigner();
        const tx = {
            to: recipient,
            value: ethers.utils.parseEther(amount),
        };

        try {
            const transaction = await signer.sendTransaction(tx);
            await transaction.wait();
            alert('Transaction successful!');
            fetchBalance(walletAddress, provider); // Refresh balance
        } catch (error) {
            console.error('Transaction failed:', error);
            alert('Transaction failed. Please check the console for details.');
        }
    };

    return (
        <div className="wallet-container">
            <h2>Wallet</h2>
            <div className="wallet-info">
                <p><strong>Address:</strong> {walletAddress}</p>
                <p><strong>Balance:</strong> {balance} ETH</p>
            </div>
            <form onSubmit={handleSend} className="send-form">
                <h3>Send Cryptocurrency</h3>
                <input
                    type="text"
                    placeholder="Recipient Address"
                    value={recipient}
                    onChange={(e) => setRecipient(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Amount (ETH)"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default Wallet;
