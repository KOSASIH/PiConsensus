import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Gamification = () => {
    const [points, setPoints] = useState(0);
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => {
        // Fetch user points and leaderboard data when the component mounts
        fetchUser Points();
        fetchLeaderboard();
    }, []);

    const fetchUser Points = async () => {
        try {
            const response = await axios.get('/api/user/points'); // Adjust the endpoint as necessary
            setPoints(response.data.points);
        } catch (error) {
            console.error('Error fetching user points:', error);
        }
    };

    const fetchLeaderboard = async () => {
        try {
            const response = await axios.get('/api/leaderboard'); // Adjust the endpoint as necessary
            setLeaderboard(response.data);
        } catch (error) {
            console.error('Error fetching leaderboard:', error);
        }
    };

    const handleCompleteTask = async () => {
        try {
            const response = await axios.post('/api/tasks/complete'); // Adjust the endpoint as necessary
            if (response.data.success) {
                setPoints(prevPoints => prevPoints + response.data.pointsEarned);
                alert(`You earned ${response.data.pointsEarned} points!`);
            }
        } catch (error) {
            console.error('Error completing task:', error);
        }
    };

    return (
        <div className="gamification">
            <h2>Gamification</h2>
            <div className="points">
                <h3>Your Points: {points}</h3>
                <button onClick={handleCompleteTask}>Complete Task</button>
            </div>
            <div className="leaderboard">
                <h3>Leaderboard</h3>
                <ul>
                    {leaderboard.map((user, index) => (
                        <li key={user.id}>
                            {index + 1}. {user.username} - {user.points} points
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Gamification;
