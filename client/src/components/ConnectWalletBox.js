import React from 'react';
import { Wallet } from 'lucide-react';
import { useTonConnectModal } from '@tonconnect/ui-react';
const ConnectWalletBox = ({ wallet_address }) => {
    const { state, open, close } = useTonConnectModal();
    console.log(wallet_address);
    return (React.createElement("div", { className: "bg-gradient-to-r from-[#9333EA] via-[#3B82F6] to-[#16A34A] rounded-xl px-0.5 py-0.5 flex items-center justify-between mt-4 flex-grow-0 self-center" }, wallet_address !== null ?
        (React.createElement("button", { className: "py-1 px-2 rounded-xl hover:bg-primary/20 transition-all flex items-center flex-row" },
            React.createElement(Wallet, { className: "mr-2 stroke-white" }),
            React.createElement("h3", { className: "text-white text-sm font-semibold" }, wallet_address.substring(0, 5) + '...')))
        :
            (React.createElement("button", { onClick: open, className: "py-1 px-2 rounded-xl hover:bg-primary/20 transition-all flex items-center flex-row" },
                React.createElement(Wallet, { className: "mr-2 stroke-white" }),
                React.createElement("h3", { className: "text-white text-sm font-semibold" }, "Connect wallet")))));
};
export default ConnectWalletBox;
