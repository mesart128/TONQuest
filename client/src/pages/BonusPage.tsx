import React from 'react';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import spiral from '../assets/spiral-min.png';

const BonusPage = () => {
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#B428B4] to-black flex flex-col items-center min-w-[432px] w-full">
      <div className="flex-1 flex flex-col px-4 mx-auto w-full">
        <Navbar />
        <div className="flex flex-col flex-1 mt-8">
          <section className="max-w-md flex flex-col flex-1">
            <div className="flex items-center justify-center">
              <img className="w-full object-cover rounded" src={spiral} />
            </div>
            <h2 className="text-5xl font-bold text-center tracking-tight text-white">
              1200 XP
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
          </section>
        </div>
        <BottomMenu />
      </div>
    </div>
  );
};

export default BonusPage;
