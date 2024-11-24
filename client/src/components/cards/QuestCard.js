import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setSelectedCard } from '../../store/slices/selectedCardSlice';
import { useSelector } from 'react-redux';
const QuestCard = ({ type, title, description, xpReward, imageUrl, branches, percentage }) => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const cardSelectHandler = () => {
        dispatch(setSelectedCard({
            type,
            title,
            description,
            xpReward,
            imageUrl,
            branches,
        }));
        navigate('/banner-page');
    };
    const { branch, error, activeTask } = useSelector((state) => state.branch);
    return (React.createElement("div", { className: "max-w-sm mx-auto flex mb-16", onClick: cardSelectHandler },
        React.createElement("div", { className: "rounded-3xl flex flex-col justify-around  p-6 text-white\r\n      border border-solid border-[#0096FF] shadow-2xl relative overflow-hidden min-h-[500px]" },
            React.createElement("div", { className: "text-center mb-8 flex flex-col items-center justify-center space-y-4" },
                React.createElement("div", { className: "space-y-1" },
                    React.createElement("h2", { className: "text-4xl font-bold opacity-50" }, type),
                    React.createElement("h1", { className: "text-3xl font-bold" }, title)),
                React.createElement("p", { className: "text-xl text-blue-100 opacity-75" }, description)),
            React.createElement("div", { className: "flex justify-center mb-8" },
                React.createElement("div", { className: "relative w-24 h-24" },
                    React.createElement("div", { className: "absolute inset-0 flex items-center justify-center" },
                        React.createElement("img", { className: "w-full max-h-48 object-cover rounded", src: `data:image/png;base64,${imageUrl}` })))),
            React.createElement("div", { className: "mt-auto bg-gray-900/70 rounded-3xl p-4 text-white shadow-lg flex flex-row items-center gap-4" },
                React.createElement("div", null,
                    percentage,
                    "%"),
                React.createElement("div", { className: "relative bg-white rounded-full h-2 w-32 flex-1" },
                    React.createElement("div", { className: "absolute top-0 left-0 h-full bg-blue-500 rounded-full transition-all", style: { width: `${percentage}%` } })),
                React.createElement("div", { className: "text-xs bg-gradient-to-r from-[#0096FF80] via-[#0096FF] to-[#0096FF80] p-3 rounded-2xl text-center" },
                    xpReward,
                    " XP")))));
};
export default QuestCard;
