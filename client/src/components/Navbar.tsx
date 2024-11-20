import React from 'react';
import { User, Wallet } from 'lucide-react';
import Experience from "./Experience.tsx";
import ConnectWalletBox from "./ConnectWalletBox.tsx";

const Navbar = () => {
    return (
        <nav className="bg-primary/10 px-4 py-3 flex justify-between items-center w-full">
            <div className="flex justify-between gap-4 w-full">
                <div className="flex items-center gap-3">
                    <button className="p-2 rounded-full hover:bg-primary/20 transition-all">
                        <User className="text-white" size={20} />
                    </button>
                    <Experience />
                </div>
                <button className="p-2 rounded-full hover:bg-primary/20 transition-all">
                    <ConnectWalletBox />
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
