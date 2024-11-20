import React from 'react';
import { ArrowUpRight, Wallet } from 'lucide-react';

const ConnectWalletBox = () => {
    return (
        <div className="bg-gradient-to-r from-[#9333EA]/20 via-[#3B82F6]/20 to-[#16A34A]/20 rounded-2xl p-6 flex items-center justify-between">
            <div className="flex items-center flex-row gap-4">
                <Wallet />
                <h3 className="text-2xl font-bold text-white">Connect wallet</h3>
            </div>
        </div>
    );
};

export default ConnectWalletBox;
