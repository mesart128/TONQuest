import React from 'react';

const Experience = ({ xp }) => {
  return (
    <div className="border border-[rgba(255,255,255,0.2)] rounded-2xl p-2 flex items-center justify-between mt-4">
      <p className="font-bold text-white">{xp} XP</p>
    </div>
  );
};

export default Experience;
