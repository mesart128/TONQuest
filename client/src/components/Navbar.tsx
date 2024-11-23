import React, { useEffect, useState } from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { fetchUser } from '../store/slices/userSlice';
import { useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

const Navbar = () => {
  const dispatch = useDispatch();
  const location = useLocation();
  const { user } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchUser);
  }, [dispatch]);

  return (
    <nav className="h-16 flex justify-between items-center w-full">
      <div className="flex justify-between gap-4 w-full">
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-full hover:bg-primary/20 transition-all">
            <User className="text-white" size={20} />
          </button>
          <Experience xp={user.xp} />
        </div>
        <ConnectWalletBox />
      </div>
    </nav>
  );
};

export default Navbar;
