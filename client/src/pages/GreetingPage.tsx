import React, { useEffect } from 'react';
import logo from '../assets/greeting-logo.png';
import GradientButton from '../components/buttons/GradientButton.tsx';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUser, updateUserAddress } from '../store/slices/userSlice';
import ClipLoader from "react-spinners/ClipLoader";
import { mainButton } from '@telegram-apps/sdk-react';

const GreetingPage = () => {

  const navigate = useNavigate();

  useEffect(() => {
    mainButton.setParams({
      isVisible: true,
      text: 'Continue',
    });
    return mainButton.onClick(() => {
      navigate('/quest');
    });
  }, []);

  //if (error) return <p>Error: {error}</p>;
  const { user, status, error } = useSelector((state) => state.user);

  const handleContinue = () => {
    navigate('/quest');
  };

  return (
    <div className="h-screen w-screen flex flex-col items-center bg-gradient-to-b from-black via-[#00a1ff] to-black p-10">
      {status === 'loading' && <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
      <ClipLoader color="#36d7b7" size={50} />
      </div>}
      <div className="text-2xl font-extrabold text-[#0096FF]">TONQuest</div>

      <div className="flex-1 flex flex-col items-center justify-center text-center max-w-md -mt-20 min-h-[500px]">
        <img src={logo} />
        <h1 className="text-3xl font-bold text-white mb-4">
          Hi, {user?.username}{' '}
        </h1>
        <p className="text-white/80 text-center leading-6 mb-12 w-96">
          Welcome to TONQuest Are you ready to dive into the amazing world of
          cryptocurrencies? It's easier than ever with our app! Complete tasks,
          earn points and become a real expert in the field of blockchain.
        </p>
      </div>
      {/* <GradientButton blocked={false} children="Continue" onClick={handleContinue} /> */}
    </div>
  );
};

export default GreetingPage;
