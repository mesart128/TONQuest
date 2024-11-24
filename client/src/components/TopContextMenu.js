import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
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
    return (React.createElement("div", { className: "flex justify-around w-full" },
        info && (React.createElement(React.Fragment, null,
            React.createElement("button", { onClick: backButtonHandler }, "Back"),
            React.createElement("div", { className: "flex items-center" },
                title,
                " (",
                type,
                ")",
                ' '))),
        info ? (React.createElement("div", { className: "relative" },
            React.createElement("span", { className: "text-blue-500 cursor-pointer", onClick: toggleTooltip },
                React.createElement("i", { className: "fas fa-info-circle" })),
            isVisible && (React.createElement("div", { className: "absolute transform top-6 -translate-x-1/2 bottom-full mb-2 bg-gray-800 text-white text-sm px-2 py-1 rounded" }, "Lorem, ipsum dolor sit amet consectetur adipisicing elit.")),
            step && React.createElement("span", { className: "text-white text-lg" },
                "Step ",
                step))) : (React.createElement("button", { onClick: closeButtonHandler }, "Close"))));
};
export default TopContextMenu;
