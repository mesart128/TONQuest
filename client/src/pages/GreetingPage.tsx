import React from 'react';
import logo from '../assets/greeting-logo.png';
import GradientButton from '../components/buttons/GradientButton.tsx';
import { useNavigate } from 'react-router-dom';

const GreetingPage = () => {
  const navigate = useNavigate();

  const handleContinue = () => {
    navigate('/quest');
  };

  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center px-16 py-8">
      <div className="text-2xl font-extrabold text-[#0096FF]">TONQuest</div>

      <div className="flex-1 flex flex-col justify-center max-w-md min-h-[500px]">
        <div className="flex flex-col items-center justify-center gap-4">
          <img src={logo} />
          <div className="gap-4 text-center">
            <h1 className="text-3xl font-bold text-white mb-4">Hi, Artur</h1>
            <p className="text-white text-center leading-5 mb-12 w-96">
              Welcome to TONQuest Are you ready to dive into the amazing world
              of cryptocurrencies? It's easier than ever with our app! Complete
              tasks, earn points and become a real expert in the field of
              blockchain.
            </p>
          </div>
        </div>
      </div>
      <GradientButton children="Continue" onClick={handleContinue} />
    </div>
  );
};

export default GreetingPage;
