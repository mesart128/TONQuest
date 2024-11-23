import React from 'react';
import BottomMenu from '../components/BottomMenu';
import Navbar from '../components/Navbar';

const NFTPage = () => {
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#C3FF00] to-black flex flex-col items-center min-w-[432px] w-full">
      <div className="flex-1 flex flex-col px-4 mx-auto w-full">
        <Navbar />
        <div className="flex flex-col flex-1 mt-8">
          <section className="max-w-md flex flex-col flex-1">
            {/* TODO: probably easier to display an image for now, implementing the unlocking logic will take time */}
            <div className="w-[80%] mx-auto h-[500px] border border-solid border-gray-200 opacity-30 bg-gray-100 rounded-3xl"></div>
            <h2 className="text-3xl font-bold mt-8 text-center text-white">
              NFT in pieces
            </h2>
            <p className="text-center text-white leading-5 mt-2 shadow-black">
              Complete the tasks below and assemble the NFT piece by piece
            </p>
          </section>
        </div>
        <BottomMenu />
      </div>
    </div>
  );
};

export default NFTPage;
