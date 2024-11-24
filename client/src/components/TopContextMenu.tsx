import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import React from 'react'
const TopContextMenu = ({ info, title, type, step }) => {
  const navigate = useNavigate();

  const [isVisible, setIsVisible] = useState(false);

  const toggleTooltip = () => {
    setIsVisible(!isVisible);
  };

  const backButtonHandler = () => {
    navigate('/quest');
  };

  const closeButtonHandler = () => {
    navigate('/quest');
  };

  return (
    <div className="flex justify-around w-full">
      {info && (
        <>
          <button onClick={backButtonHandler}>Back</button>
          <div className="flex items-center">
            {title} ({type}){' '}
          </div>
        </>
      )}
      {info ? (
        <div className="relative">
          <span
            className="text-blue-500 cursor-pointer"
            onClick={toggleTooltip}
          >
            <i className="fas fa-info-circle"></i>
          </span>
          {isVisible && (
            <div className="absolute transform top-6 -translate-x-1/2 bottom-full mb-2 bg-gray-800 text-white text-sm px-2 py-1 rounded">
              Lorem, ipsum dolor sit amet consectetur adipisicing elit.
            </div>
          )}
          {step && <span className="text-white text-lg">Step {step}</span>}
        </div>
      ) : (
        <button onClick={closeButtonHandler}>Close</button>
      )}
    </div>
  );
};

export default TopContextMenu;
