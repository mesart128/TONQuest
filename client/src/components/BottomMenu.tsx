import React from 'react';
import flag from '../assets/svg/flag.svg';
import nft from '../assets/svg/nft-square.svg';
import coins from '../assets/svg/coins.svg';

const BottomMenu = () => {
  return (
    <div className="flex justify-between items-center px-4 py-2 text-white w-full mt-auto mb-10 px-11">
      <div>
        <img src={flag} alt="flag" />
      </div>
      <div>
        <img src={nft} alt="nft" />
      </div>
      <div>
        <img src={coins} alt="coins" />
      </div>
    </div>
  );
};

export default BottomMenu;
