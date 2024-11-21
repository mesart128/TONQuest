import React, { useState, useEffect } from 'react';
import flag from '../assets/svg/flag.svg';
import nft from '../assets/svg/nft-square.svg';
import coins from '../assets/svg/coins.svg';
import { useNavigate } from 'react-router-dom';

const BottomMenu = ({ isQuestPage, isNFTPage, isExpPage }) => {
  const navigate = useNavigate();

  const [activePage, setActivePage] = useState('');

  useEffect(() => {
    if (isQuestPage) setActivePage('quest');
    else if (isNFTPage) setActivePage('nft');
    else if (isExpPage) setActivePage('exp');
  }, [isQuestPage, isNFTPage, isExpPage]);

  const onQuestPageHandler = () => {
    setActivePage('quest');
    navigate('/quest');
  };

  const onNFTPageHandler = () => {
    setActivePage('nft');
    navigate('/nft');
  };

  const onExpPageHandler = () => {
    setActivePage('exp');
    navigate('/exp');
  };

  return (
    <div className="flex justify-between items-center px-4 py-2 text-white w-full mt-auto mb-10 px-11">
      <div
        onClick={onQuestPageHandler}
        className="relative flex flex-col items-center cursor-pointer"
      >
        <img
          src={flag}
          alt="flag"
          className={`transition-all ${
            activePage === 'quest' ? 'opacity-100' : 'opacity-50'
          }`}
        />
        {activePage === 'quest' && (
          <div className="absolute bottom-[-16px] w-2 h-2 bg-white rounded-full"></div>
        )}
      </div>
      <div
        onClick={onNFTPageHandler}
        className="relative flex flex-col items-center cursor-pointer"
      >
        <img
          src={nft}
          alt="nft"
          className={`transition-all ${
            activePage === 'nft' ? 'opacity-100' : 'opacity-50'
          }`}
        />
        {activePage === 'nft' && (
          <div className="absolute bottom-[-16px] w-2 h-2 bg-white rounded-full"></div>
        )}
      </div>

      <div
        onClick={onExpPageHandler}
        className="relative flex flex-col items-center cursor-pointer"
      >
        <img
          src={coins}
          alt="coins"
          className={`transition-all ${
            activePage === 'exp' ? 'opacity-100' : 'opacity-50'
          }`}
        />
        {activePage === 'exp' && (
          <div className="absolute bottom-[-16px] w-2 h-2 bg-white rounded-full"></div>
        )}
      </div>
    </div>
  );
};

export default BottomMenu;
