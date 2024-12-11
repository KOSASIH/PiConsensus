import React, { useEffect, useState } from 'react';
import './Dashboard.css'; // Assuming you have some CSS for styling

const Dashboard = () => {
    const [userStats, setUser Stats] = useState({
        totalBalance: 0,
        totalTransactions: 0,
        recentActivities: [],
    });

    useEffect(() => {
        // Simulate fetching user statistics from an API
        const fetchUser Stats = async () => {
            // Replace with your API call
            const stats = await new Promise((resolve) => {
                setTimeout(() => {
                    resolve({
                        totalBalance: 5.23, // Example balance in ETH
                        totalTransactions: 12, // Example transaction count
                        recentActivities: [
                            { id: 1, type: 'Sent', amount: 0.5, date: '2023-10-01' },
                            { id: 2, type: 'Received', amount: 1.0, date: '2023-09-28' },
                            { id: 3, type: 'Sent', amount: 0.2, date: '2023-09-25' },
                        ],
                    });
                }, 1000);
            });

            setUser Stats(stats);
        };

        fetchUser Stats();
    }, []);

    return (
        <div className="dashboard-container">
            <h2>Dashboard</h2>
            <div className="stats">
                <div className="stat-item">
                    <h3>Total Balance</h3>
                    <p>{userStats.totalBalance} ETH</p>
                </div>
                <div className="stat-item">
                    <h3>Total Transactions</h3>
                    <p>{userStats.totalTransactions}</p>
                </div>
            </div>
            <div className="recent-activities">
                <h3>Recent Activities</h3>
                <ul>
                    {userStats.recentActivities.map(activity => (
                        <li key={activity.id}>
                            {activity.type} {activity.amount} ETH on {activity.date}
                        </li>
                    ))}
                </ul>
            </div>
            <div className="quick-access">
                <h3>Quick Access</h3>
                <button onClick={() => alert('Navigate to Wallet')}>Go to Wallet</button>
                <button onClick={() => alert('Navigate to Settings')}>Settings</button>
            </div>
        </div>
    );
};

export default Dashboard;
