import { useLocation, useNavigate } from 'react-router-dom';
import icon from '../assets/congratulations.png';
import { useDispatch } from 'react-redux';
import { setBranchCompleted } from '../store/slices/branchSlice';
const Congratulations = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const { totalXP = 0, resetBranchCompletion } = location.state || {};
    const handleClose = () => {
        dispatch(setBranchCompleted(false));
        navigate('/tasks-page');
    };
    return (React.createElement("div", { className: "fixed inset-0 flex items-center justify-center z-50" },
        React.createElement("div", { className: "bg-gradient-to-b from-blue-900 to-black p-8 rounded-lg text-white text-center max-w-md w-full mx-4" },
            React.createElement("button", { onClick: handleClose, className: "absolute top-4 right-4 text-gray-400 hover:text-white" },
                React.createElement("svg", { className: "w-6 h-6", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor" },
                    React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: 2, d: "M6 18L18 6M6 6l12 12" }))),
            React.createElement("h2", { className: "text-2xl font-bold mb-2" }, "The task is completed"),
            React.createElement("div", { className: "my-8" },
                React.createElement("img", { src: icon, alt: "Target", className: "w-24 h-24 mx-auto" })),
            React.createElement("p", { className: "text-gray-300 mb-6" }, "You have learned how to change one token to another, keep it up!"),
            React.createElement("div", { className: "inline-flex items-center bg-opacity-20 bg-blue-500 rounded-full px-4 py-2 mb-8" },
                React.createElement("svg", { className: "w-5 h-5 mr-2", viewBox: "0 0 20 20", fill: "currentColor" },
                    React.createElement("path", { d: "M..." })),
                "+",
                totalXP,
                " XP"),
            React.createElement("button", { onClick: handleClose, className: "w-full bg-blue-500 hover:bg-blue-600 text-white rounded-full py-3 transition-colors" }, "Ready to move on"))));
};
export default Congratulations;
