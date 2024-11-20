import React from 'react';

const Experience = ({ xp }) => {
  return (
    <div className="bg-gradient-to-r from-[#9333EA]/20 via-[#3B82F6]/20 to-[#16A34A]/20 rounded-2xl p-2 flex items-center justify-between">
      {xp} XP
    </div>
  );
};

export default Experience;
