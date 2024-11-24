var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import React, { useEffect, useState } from 'react';
import GradientButton from '../buttons/GradientButton';
import { useSelector, useDispatch } from 'react-redux';
import { claimTaskById, checkTaskById } from '../../store/slices/taskSlice';
import { toast } from 'react-toastify';
import { completeBranchById, checkBranchById, fetchBranchById } from '../../store/slices/branchSlice';
import { claimPieceById } from '../../store/slices/pieceSlice';
import { fetchUser } from '../../store/slices/userSlice';
const TaskCard = ({ part, title, xp, status, actionURL, callToAction, onTaskComplete, onEarnedXP }) => {
    const dispatch = useDispatch();
    const { branch, activeTask } = useSelector((state) => state.branch);
    const { imageUrl, description, type, branches } = useSelector((state) => state.selectedCard);
    const [earnedXP, setEarnedXP] = useState(0);
    const [localStatus, setLocalStatus] = useState(status);
    useEffect(() => {
        if (status === 'completed') {
            const earnedXP = xp;
            if (onEarnedXP) {
                onEarnedXP(earnedXP);
            }
            if (onTaskComplete) {
                onTaskComplete();
            }
        }
    }, [status, xp, onEarnedXP, onTaskComplete]);
    useEffect(() => {
        setLocalStatus(status);
    }, [status]);
    const areAllTasksCompleted = () => {
        var _a;
        if (!((_a = branch === null || branch === void 0 ? void 0 : branch.tasks) === null || _a === void 0 ? void 0 : _a.length))
            return false;
        return branch.tasks.every(task => task.status === 'claimed' || task.completed);
    };
    const refreshTaskState = () => __awaiter(void 0, void 0, void 0, function* () {
        try {
            yield dispatch(fetchBranchById(branch.id)).unwrap();
            if (onTaskComplete) {
                onTaskComplete();
            }
        }
        catch (error) {
            console.error('Error refreshing task state:', error);
        }
    });
    const validateTaskCompletion = (taskId) => __awaiter(void 0, void 0, void 0, function* () {
        try {
            const taskCheck = yield dispatch(checkTaskById(taskId)).unwrap();
            console.log(`taskId: ${taskId}`);
            if (!(taskCheck === null || taskCheck === void 0 ? void 0 : taskCheck.completed)) {
                toast.error("Task is not completed.");
                return false;
            }
            const taskClaim = yield dispatch(claimTaskById(taskId)).unwrap();
            if (!(taskClaim === null || taskClaim === void 0 ? void 0 : taskClaim.success)) {
                toast.error("Error claiming task.");
                return false;
            }
            toast.success("Task successfully claimed");
            setLocalStatus('claimed');
            yield refreshTaskState();
            return true;
        }
        catch (error) {
            console.error('Error in validateTaskCompletion:', error);
            return false;
        }
    });
    const validateBranchCompletion = (branchId) => __awaiter(void 0, void 0, void 0, function* () {
        if (!areAllTasksCompleted())
            return false;
        try {
            const branchCheck = yield dispatch(checkBranchById(branchId)).unwrap();
            console.log(`branchId: ${branchId}`);
            if (!(branchCheck === null || branchCheck === void 0 ? void 0 : branchCheck.completed)) {
                toast.error("Branch is not completed.");
                return false;
            }
            const branchCompletion = yield dispatch(completeBranchById(branchId)).unwrap();
            if (!branchCompletion.success) {
                toast.error("Error occurred.");
                return false;
            }
            yield refreshTaskState();
            return true;
        }
        catch (error) {
            console.error('Error in validateBranchCompletion:', error);
            return false;
        }
    });
    const claimReward = (pieceId) => __awaiter(void 0, void 0, void 0, function* () {
        try {
            const pieceClaim = yield dispatch(claimPieceById(pieceId)).unwrap();
            if (!(pieceClaim === null || pieceClaim === void 0 ? void 0 : pieceClaim.success)) {
                toast.error("Failed to claim the piece.");
                return false;
            }
            setEarnedXP(xp);
            yield dispatch(fetchUser());
            return true;
        }
        catch (error) {
            console.error('Error in claimReward:', error);
            return false;
        }
    });
    const checkIsCompleted = () => __awaiter(void 0, void 0, void 0, function* () {
        try {
            if (!(activeTask === null || activeTask === void 0 ? void 0 : activeTask.id)) {
                toast.error("No active task found.");
                return;
            }
            const isTaskCompleted = yield validateTaskCompletion(activeTask.id);
            if (!isTaskCompleted)
                return;
            if (areAllTasksCompleted()) {
                const isBranchCompleted = yield validateBranchCompletion(branch.id);
                if (!isBranchCompleted)
                    return;
                const isRewardClaimed = yield claimReward(branch.pieces[0].id);
                if (!isRewardClaimed)
                    return;
            }
        }
        catch (error) {
            toast.error(typeof error === 'string' ? error : 'An error occurred');
        }
    });
    return (React.createElement("div", { className: "w-full max-w-md" }, localStatus === 'blocked' ? (React.createElement("div", { className: "bg-gray-800 text-white p-4 rounded-lg mb-4 relative overflow-hidden" },
        React.createElement("div", { className: "flex justify-between items-center mb-2" },
            React.createElement("span", { className: "text-sm font-medium" },
                "Part ",
                part),
            React.createElement("span", { className: "text-sm bg-gray-700 rounded-full px-2 py-1" },
                "+",
                xp,
                " XP")),
        React.createElement("h3", { className: "text-lg font-bold mb-4" },
            "Unlock after the ",
            part - 1,
            " task"),
        React.createElement("div", { className: "absolute inset-0 flex justify-center items-center backdrop-blur bg-black/30" },
            React.createElement("div", { className: "bg-black/50 p-3 rounded-full" },
                React.createElement("svg", { xmlns: "http://www.w3.org/2000/svg", fill: "none", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", className: "w-8 h-8 text-gray-300" },
                    React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M12 15v.01M12 9a1.5 1.5 0 100 3 1.5 1.5 0 100-3zm0 6.75c.38.56.62 1.2.7 1.89.11.81.09 1.61-.06 2.36a.75.75 0 01-.64.51h-.08a.75.75 0 01-.64-.51c-.15-.75-.17-1.55-.06-2.36.08-.69.32-1.33.7-1.89zm0 0c-.38-.56-.62-1.2-.7-1.89-.11-.81-.09-1.61.06-2.36a.75.75 0 01.64-.51h.08a.75.75 0 01.64.51c.15.75.17 1.55.06 2.36-.08.69-.32 1.33-.7-1.89z" })))))) : localStatus === 'active' ? (React.createElement("div", { className: "bg-gradient-to-r from-[#003E6B] via-[#004F8C] to-[#003E6B] text-white p-4 rounded-lg mb-4 shadow-lg" },
        React.createElement("div", { className: "flex justify-between items-center mb-2" },
            React.createElement("span", { className: "text-sm font-medium" },
                "Part ",
                part),
            React.createElement("span", { className: "text-sm bg-blue-500 rounded-full px-2 py-1" },
                "+",
                xp,
                " XP")),
        React.createElement("h3", { className: "text-lg font-bold mb-4" }, title),
        React.createElement(GradientButton, { blocked: false, children: "Check the execution", onClick: checkIsCompleted }))) : localStatus === 'claimed' ? (React.createElement("div", { className: "bg-gray-500 from-[#003E6B] via-[#004F8C] to-[#003E6B] text-white p-4 rounded-lg mb-4 shadow-lg" },
        React.createElement("div", { className: "flex justify-between items-center mb-2" },
            React.createElement("span", { className: "text-sm font-medium" },
                "Part ",
                part),
            React.createElement("span", { className: "text-sm bg-blue-500 rounded-full px-2 py-1" },
                "+",
                xp,
                " XP")),
        React.createElement("h3", { className: "text-lg font-bold mb-4" }, title),
        React.createElement(GradientButton, { blocked: true, children: "Check the execution", onClick: checkIsCompleted }))) : (React.createElement(React.Fragment, null))));
};
export default TaskCard;
