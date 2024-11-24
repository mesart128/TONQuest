import React from 'react';
const Modal = ({ children, onClose }) => {
    return (React.createElement("div", { className: "fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50" },
        React.createElement("div", { className: "bg-white rounded-lg p-6 relative max-w-md w-full" },
            React.createElement("button", { onClick: onClose, className: "absolute top-2 right-2 text-gray-500 hover:text-gray-700" }, "\u2716"),
            children)));
};
export default Modal;
