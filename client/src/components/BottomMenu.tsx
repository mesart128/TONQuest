import React from 'react';
import flag from '../assets/svg/flag.svg';
import nft from '../assets/svg/nft-square.svg';
import coins from '../assets/svg/coins.svg';
import { useNavigate, useLocation } from 'react-router-dom';

const menuItems = [
  { path: '/quest', imgSrc: flag, alt: 'flag' },
  { path: '/nft', imgSrc: nft, alt: 'nft' },
  { path: '/bonus', imgSrc: coins, alt: 'bonus' },
];

const BottomMenu = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="flex justify-between py-4">
      {menuItems?.map(({ path, imgSrc, alt }) => {
        const isCurrentPage = location.pathname === path;

        return (
          <div
            onClick={() => navigate(path)}
            className="flex flex-col gap-2 justify-center items-center cursor-pointer"
          >
            <img
              src={imgSrc}
              alt={alt}
              className={`transition-all ${
                isCurrentPage ? 'opacity-100' : 'opacity-50'
              }`}
            />
            <div
              className={`w-2 h-2 rounded-full ${isCurrentPage ? 'bg-white' : 'bg-transparent'}`}
            />
          </div>
        );
      })}
    </div>
  );
};

export default BottomMenu;
