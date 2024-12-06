import React from 'react';

const GradientButton = ({ children, onClick, blocked }) => {
  const blockedStyle = `bg-[#0096FF]/25 w-full disabled max-w-md p-1.5 text-white/65
                   rounded-[12px] z-10`;
  const activeStyle = `w-full max-w-md p-1.5 bg-gradient-to-r from-[#0096FF]/65 via-[#0096FF] to-[#0096FF]/65 hover:bg-[#0096FF]/50
                    text-white rounded-[12px]
                    backdrop-blur-sm transition-all duration-300
                    border border-white/10
                    active:transform active:scale-[0.98]
                    shadow-lg z-10`;
  return blocked ? (
    <button className={blockedStyle} disabled>
      {children}
    </button>
  ) : (
    <button onClick={onClick} className={activeStyle}>
      {children}
    </button>
  );
};

export default GradientButton;
