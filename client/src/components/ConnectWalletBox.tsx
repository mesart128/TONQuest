import React from 'react';
import { ArrowUpRight, Wallet } from 'lucide-react';
import { useTonConnectModal, useTonConnectUI } from '@tonconnect/ui-react';

const ConnectWalletBox = () => {
  const { state, open, close } = useTonConnectModal();

  return (
    <div className="bg-gradient-to-r from-[#9333EA] via-[#3B82F6] to-[#16A34A] rounded-xl my-0.5 px-0.5 flex items-center justify-between">
      <button onClick={open} className="p-1 rounded-xl hover:bg-primary/20 transition-all flex items-center flex-row gap-4">
        <Wallet />
        <h3 className="text-2xl text-white text-sm">Connect wallet</h3>
      </button>
    </div>
  );
};

export default ConnectWalletBox;
