import React, { useEffect, useState } from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { fetchUser } from '../store/slices/userSlice';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const Navbar = ({user}) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  useEffect(() => {
    if (user?.xp) {
      dispatch(fetchUser());
    }
  }, [user?.xp, dispatch]);


  return (
    <nav className="h-16 flex justify-between w-full pl-5 pr-5 z-10 sticky top-0 items-center backdrop-blur-lg ">
      <div className="flex justify-between gap-4 w-full">
        <div className="flex items-center gap-3">
          <button className="p-[0] rounded-full hover:bg-primary/20 transition-all max-w-[40px]"
            onClick={() => {navigate('/bonus')}}>
          {user.image ? 
            (
              <img src={user.image} alt="user" className="w-full rounded-full" />
            )
            :
            (<User className="text-white" size={30} />)
          }
          </button>
          {user && <Experience xp={user.xp} />}
        </div>
        {user && <ConnectWalletBox wallet_address={user.wallet_address}/>}
      </div>
    </nav>
  );
};

export default Navbar;
