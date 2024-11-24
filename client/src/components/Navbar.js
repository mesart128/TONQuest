import React, { useEffect } from 'react';
import { User } from 'lucide-react';
import Experience from './Experience.tsx';
import ConnectWalletBox from './ConnectWalletBox.tsx';
import { fetchUser } from '../store/slices/userSlice';
import { useDispatch } from 'react-redux';
const Navbar = ({ user }) => {
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(fetchUser());
    }, [dispatch]);
    useEffect(() => {
        if (user === null || user === void 0 ? void 0 : user.xp) {
            dispatch(fetchUser());
        }
    }, [user === null || user === void 0 ? void 0 : user.xp, dispatch]);
    return (React.createElement("nav", { className: "h-16 flex justify-between items-center w-full" },
        React.createElement("div", { className: "flex justify-between gap-4 w-full" },
            React.createElement("div", { className: "flex items-center gap-3" },
                React.createElement("button", { className: "p-2 rounded-full hover:bg-primary/20 transition-all mt-4" },
                    React.createElement(User, { className: "text-white", size: 30 })),
                user && React.createElement(Experience, { xp: user.xp })),
            user && React.createElement(ConnectWalletBox, { wallet_address: user.wallet_address }))));
};
export default Navbar;
