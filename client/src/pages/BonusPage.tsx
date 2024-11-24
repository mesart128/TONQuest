import React, { useEffect } from 'react';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import spiral from '../assets/spiral-min.png';
import nft from '../assets/nft.png';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUser } from '../store/slices/userSlice';


const BonusPage = () => {
  const dispatch = useDispatch();

  const { user, status, error } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  return (
    <div className="min-h-screen relative flex flex-col items-center min-w-[432px] w-full">
      <div className="bg-[#B428B4] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[250px]"></div>
      <div className="flex-1 flex flex-col px-4 mx-auto w-full z-10">
        <Navbar />
        <div className="flex flex-col flex-1 mt-8">
          <section className="max-w-md flex flex-col flex-1">
            <div className="flex items-center justify-center">
              <img className="w-full object-cover rounded" src={spiral} />
            </div>
            <h2 className="text-5xl font-bold text-center tracking-tight text-white">
              {user.xp} XP
            </h2>
            <p className="text-center text-white/80 leading-5 mt-2">
              Complete quests and earn experience points, which can later be
              exchanged for TON, exclusive NFTs, and more.{' '}
            </p>
            {/* TODO: this trick won't work with transparent backgrounds, need to find a workaround */}
            <div className="bg-gradient-to-r from-[#9333EA] via-[#3B82F6] to-[#16A34A] rounded-xl px-0.5 py-0.5 flex items-center justify-between mt-4 flex-grow-0 self-center">
              <button className="rounded-xl hover:bg-primary/20 transition-all flex-grow-0">
                <h3 className="text-white text-sm font-semibold">My history</h3>
              </button>
            </div>
            <div className="border border-zinc-400 py-4 px-6 rounded-2xl mt-12 flex flex-row justify-between">
              <div>
                <h3 className="text-3xl font-bold">Coming soon</h3>
                <ul className="max-w-md space-y-1 text-white/80 list-disc list-inside mt-4">
                  <li>Exchange PTS for TON</li>
                  <li>Rare NFTs</li>
                  <li>Integrations with other services</li>
                </ul>
                <p className="text-white/80 mt-2">Follow for updates...</p>
              </div>
              <div className="flex items-center justify-center">
                <img
                  className="w-full object-cover rounded h-[125px] rotate-12"
                  src={nft}
                  alt="nft"
                />
              </div>
            </div>
          </section>
        </div>
        <BottomMenu />
      </div>
    </div>
  );
};

export default BonusPage;
