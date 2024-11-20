import React from 'react';
import logo from '../assets/greeting-logo.png';

const GreetingPage = () => {
    const handleContinue = () => {
        // Handle continue button click
        console.log('Continue clicked');
    };

    return (
        <div className="min-h-screen relative bg-gradient-to-b from-black via-emerald-600 to-black flex flex-col items-center px-6">
            <div className="mt-12 text-2xl font-bold text-white">
                TONQuest
            </div>

            <div className="flex-1 flex flex-col items-center justify-center text-center max-w-md -mt-20">
                <img src={logo}/>
                <h1 className="text-3xl font-bold text-white mb-4">
                    Hi, Artur <span className="inline-block ml-1">👋</span>
                </h1>
                <p className="text-white/90 text-center leading-relaxed mb-12">
                    Welcome to TONQuest! Are you ready to dive into the amazing world of cryptocurrencies? It's easier than ever with our app! Complete tasks, earn points and become a real expert in the field of blockchain.
                </p>
                <button
                    onClick={handleContinue}
                    className="w-full py-4 px-8 bg-blue-500/30 hover:bg-blue-500/40
                     text-white font-semibold rounded-2xl
                     backdrop-blur-sm transition-all duration-300
                     border border-white/10
                     active:transform active:scale-[0.98]
                     shadow-lg"
                >
                    Continue
                </button>
            </div>

            <div className="h-16" />
        </div>
    );
};

export default GreetingPage;
