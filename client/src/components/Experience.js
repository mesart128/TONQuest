import React from 'react';
const Experience = ({ xp }) => {
    return (React.createElement("div", { className: "border border-[rgba(255,255,255,0.2)] rounded-2xl p-2 flex items-center justify-between mt-4" },
        React.createElement("p", { className: "font-bold text-white" },
            xp,
            " XP")));
};
export default Experience;
