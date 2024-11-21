import React from 'react';
import questRecycle from '../../assets/quest-recycle.png';

const QuestCard = () => {
  return (
    <div className="max-w-sm mx-auto">
      <div className="rounded-3xl flex flex-col justify-around gap-16 p-6 text-white
      border border-solid border-[#0096FF] shadow-2xl relative overflow-hidden min-h-[500px]">
        <div className="text-center mb-8 flex flex-col items-center justify-center gap-4">
          <h2 className="text-4xl font-bold mb-2 opacity-50">DEX</h2>
          <h1 className="text-3xl font-bold mb-4">Easy start</h1>
          <p className="text-xl text-blue-100 opacity-75">
            You will learn how to use decentralized exchanges tools
          </p>
        </div>

        <div className="flex justify-center mb-8">
          <div className="relative w-24 h-24">
            <div className="absolute inset-0 flex items-center justify-center">
              <img className="max-w-lg" src={questRecycle} />
            </div>
          </div>
        </div>

        <div
            className="mt-auto bg-gray-900/70 rounded-3xl p-4 text-white shadow-lg flex flex-row items-center gap-4">
          {/*<div className="items-center justify-between text-sm mb-2 flex flex-row">*/}
          <div>0%</div>
          <div className="bg-white rounded-full h-2 w-32"/>
          {/*<div className="bg-blue-400 bg-opacity-40 rounded-full h-2">*/}
          {/*</div>*/}
          <div className="text-xs bg-gradient-to-r from-[#0096FF80] via-[#0096FF] to-[#0096FF80] p-3 rounded-2xl">2/6 NFT + 100 XP</div>
        </div>
        {/*</div>*/}
      </div>
    </div>
  );
};

export default QuestCard;
