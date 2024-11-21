import React, { useEffect, useState } from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { getUser } from '../api/Router.js';

const Navbar = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await getUser();
        setUser(userData);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <nav className="bg-primary/10 px-4 py-3 flex justify-between items-center w-full">
      <div className="flex justify-between gap-4 w-full">
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-full hover:bg-primary/20 transition-all">
            <User className="text-white" size={20} />
          </button>
          <Experience xp={user.username} />
        </div>
        <ConnectWalletBox />
      </div>
    </nav>
  );
};

export default Navbar;
