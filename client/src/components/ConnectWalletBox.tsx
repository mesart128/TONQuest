import React, { useEffect } from 'react';
import { ArrowUpRight, Wallet } from 'lucide-react';
import {
  useTonConnectModal,
} from '@tonconnect/ui-react';

const ConnectWalletBox = ({ wallet_address }) => {
  const { state, open, close } = useTonConnectModal();
  console.log(wallet_address);

  return (
    <div className="bg-gradient-to-r from-[#9333EA] via-[#3B82F6] to-[#16A34A] rounded-xl px-0.5 py-0.5 flex items-center justify-between flex-grow-0 self-center">
      {wallet_address !== null ? (
        <div className="py-1 px-2 rounded-xl hover:bg-primary/20 transition-all flex items-center flex-row bg-black/80">
          <Wallet className="mr-2 stroke-white" />
          <h3 className="text-white text-sm font-semibold">
            {wallet_address.substring(0, 5) + '...'}
          </h3>
        </div>
      ) : (
        <button
          onClick={open}
          className="py-1 px-2 rounded-xl hover:bg-primary/20 transition-all flex items-center flex-row"
        >
          <Wallet className="mr-2 stroke-white" />
          <h3 className="text-white text-sm font-semibold">Connect wallet</h3>
        </button>
      )}
    </div>
  );
};

export default ConnectWalletBox;
