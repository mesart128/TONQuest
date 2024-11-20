import React from 'react';

const QuestPage = () => {
    return (
        <div className="min-h-screen bg-gradient-to-b from-black to-gray-900 text-white flex flex-col items-center justify-center">
            <div className="w-full max-w-md text-center px-4">
                <h1 className="text-3xl font-bold mb-4">Welcome to Quest</h1>
                <p className="text-gray-400 mb-6">Start your journey with easy and rewarding quests!</p>
                <div className="bg-blue-800 p-4 rounded-lg shadow-lg">
                    <h2 className="text-xl font-bold mb-2">DEX Easy Start</h2>
                    <p className="text-sm text-gray-300 mb-4">Perform token swaps and earn rewards!</p>
                    <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">
                        Start
                    </button>
                </div>
            </div>
        </div>
    );
};

export default QuestPage;
