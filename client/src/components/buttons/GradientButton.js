import React from 'react';
const GradientButton = ({ children, onClick, blocked }) => {
    const blockedStyle = `bg-gray-600 w-full disabled max-w-md py-4 px-8
                    font-semibold rounded-2xl`;
    const activeStyle = `w-full max-w-md py-4 px-8 bg-gradient-to-r from-[#00C7FF]/30 via-[#0096FF] to-[#00C7FF]/30 hover:bg-[#0096FF]/50
                    text-white font-semibold rounded-2xl
                    backdrop-blur-sm transition-all duration-300
                    border border-white/10
                    active:transform active:scale-[0.98]
                    shadow-lg`;
    return blocked ? (React.createElement("button", { className: blockedStyle, disabled: true }, children)) : (React.createElement("button", { onClick: onClick, className: activeStyle }, children));
};
export default GradientButton;
