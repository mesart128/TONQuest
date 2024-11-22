import React from 'react';

const TaskCard = ({ part, title, xp, isLocked, actionURL, callToAction }) => {

  return (
    <div className="w-full max-w-md">
      {isLocked ? (
        <div className="bg-gray-800 text-white p-4 rounded-lg mb-4 relative overflow-hidden">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Part {part}</span>
            <span className="text-sm bg-gray-700 rounded-full px-2 py-1">
              +{xp} XP
            </span>
          </div>
          <h3 className="text-lg font-bold mb-4">
            Unlock after the {part - 1} task
          </h3>
          <div className="absolute inset-0 flex justify-center items-center backdrop-blur bg-black/30">
            <div className="bg-black/50 p-3 rounded-full">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="2"
                stroke="currentColor"
                className="w-8 h-8 text-gray-300"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 15v.01M12 9a1.5 1.5 0 100 3 1.5 1.5 0 100-3zm0 6.75c.38.56.62 1.2.7 1.89.11.81.09 1.61-.06 2.36a.75.75 0 01-.64.51h-.08a.75.75 0 01-.64-.51c-.15-.75-.17-1.55-.06-2.36.08-.69.32-1.33.7-1.89zm0 0c-.38-.56-.62-1.2-.7-1.89-.11-.81-.09-1.61.06-2.36a.75.75 0 01.64-.51h.08a.75.75 0 01.64.51c.15.75.17 1.55.06 2.36-.08.69-.32 1.33-.7 1.89z"
                />
              </svg>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-gradient-to-r from-[#003E6B] via-[#004F8C] to-[#003E6B] text-white p-4 rounded-lg mb-4 shadow-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Part {part}</span>
            <span className="text-sm bg-blue-500 rounded-full px-2 py-1">
              +{xp} XP
            </span>
          </div>
          <h3 className="text-lg font-bold mb-4">{title}</h3>
          <button className="bg-blue-500 hover:bg-blue-600 text-white rounded-md py-2 px-4">
            <a href={actionURL} className="no-underline text-inherit">Check the execution</a>
          </button>
        </div>
      )}
    </div>
  );
};

export default TaskCard;
