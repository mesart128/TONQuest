import React, { useEffect, useState } from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { getUser } from '../api/Router.js';

const Navbar = () => {
  const [user, setUser] = useState(null); // For storing the user data
  const [loading, setLoading] = useState(true); // For loading state
  const [error, setError] = useState(null); // For storing any error

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await getUser(); // Fetch data from API
        setUser(userData); // Update state with fetched data
        setLoading(false); // Set loading to false after data is fetched
      } catch (err) {
        setError(err); // Set error if something goes wrong
        setLoading(false); // Set loading to false even if there is an error
      }
    };

    fetchUserData(); // Call the fetch function
  }, []); // Empty dependency array means this effect runs once when the component mounts

  // Return JSX based on the current state (loading, error, or user data)
  if (loading) {
    return <div>Loading...</div>; // Show loading indicator
  }

  if (error) {
    return <div>Error: {error.message}</div>; // Show error message if there was an error
  }

  return (
    <nav className="bg-primary/10 px-4 py-3 flex justify-between items-center w-full">
      <div className="flex justify-between gap-4 w-full">
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-full hover:bg-primary/20 transition-all">
            <User className="text-white" size={20} />
            {user.username}
          </button>
          <Experience xp={user.username} />
        </div>
        <ConnectWalletBox />
      </div>
    </nav>
  );
};

export default Navbar;
