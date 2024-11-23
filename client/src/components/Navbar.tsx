import React, { useEffect, useState } from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { fetchUser } from '../store/slices/userSlice';
import { useDispatch } from 'react-redux';

const Navbar = ({user}) => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  useEffect(() => {
    if (user?.xp) {
      dispatch(fetchUser());
    }
  }, [user?.xp, dispatch]);


  return (
    <nav className="h-16 flex justify-between items-center w-full">
      <div className="flex justify-between gap-4 w-full">
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-full hover:bg-primary/20 transition-all mt-4">
            <User className="text-white" size={30} />
          </button>
          {user && <Experience xp={user.xp} />}
        </div>
        {user && <ConnectWalletBox wallet_address={user.wallet_address}/>}
      </div>
    </nav>
  );
};

export default Navbar;
