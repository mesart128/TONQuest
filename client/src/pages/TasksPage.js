var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { useEffect, useState } from 'react';
import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchBranchById } from '../store/slices/branchSlice';
import { useNavigate } from 'react-router-dom';
import { useTonConnectModal, useTonAddress } from '@tonconnect/ui-react';
import { setUserAddress } from '../api/Router';
import { checkBranchById } from '../store/slices/branchSlice';
import { setBranchCompleted } from '../store/slices/branchSlice';
const TasksPage = () => {
    var _a;
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [totalXP, setTotalXP] = useState(0);
    const branchCompleted = useSelector((state) => state.branch.branchCompleted);
    const { state, open, close } = useTonConnectModal();
    const rawAddress = useTonAddress(false);
    const user = useSelector((state) => state.user.user);
    const { branch, status, error, activeTask } = useSelector((state) => state.branch);
    console.log(activeTask);
    const isBranchCompleted = !(branch === null || branch === void 0 ? void 0 : branch.tasks.some((el) => el.status === 'active'));
    const { imageUrl, description, title, type, branches } = useSelector((state) => state.selectedCard);
    const onSliderHandler = () => __awaiter(void 0, void 0, void 0, function* () {
        if (user === null || user === void 0 ? void 0 : user.wallet_address) {
            navigate('/task_slider');
        }
        else {
            console.log('no wallet');
            if (rawAddress) {
                console.log('address connected');
                yield setUserAddress(rawAddress);
            }
            else {
                console.log('address not connected');
                open();
            }
        }
    });
    useEffect(() => {
        const fetchBranch = () => __awaiter(void 0, void 0, void 0, function* () {
            var _a;
            const branchId = (_a = branches === null || branches === void 0 ? void 0 : branches[0]) === null || _a === void 0 ? void 0 : _a.id;
            if (branchId) {
                yield dispatch(fetchBranchById(branchId));
            }
        });
        fetchBranch();
    }, [branches, dispatch]);
    useEffect(() => {
        if (rawAddress) {
            console.log(rawAddress);
        }
    }, [rawAddress]);
    if (error) {
        return React.createElement("div", null, error);
    }
    const refreshAllTasks = () => __awaiter(void 0, void 0, void 0, function* () {
        if (isRefreshing)
            return;
        try {
            setIsRefreshing(true);
            if (!(branch === null || branch === void 0 ? void 0 : branch.id))
                return;
            yield dispatch(checkBranchById(branch.id)).unwrap();
            yield dispatch(fetchBranchById(branch.id)).unwrap();
        }
        catch (error) {
            console.error('Error refreshing tasks:', error);
        }
        finally {
            setIsRefreshing(false);
        }
    });
    const handleEarnedXP = (xp) => {
        setTotalXP((prevXP) => prevXP + xp);
    };
    useEffect(() => {
        if (branchCompleted) {
            dispatch(setBranchCompleted(false));
            navigate('/congratulations', { state: { totalXP } });
        }
    }, [branchCompleted, navigate, totalXP]);
    return (React.createElement("div", { className: "h-screen flex flex-col bg-gradient-to-b from-black via-[#00a1ff] to-black items-center min-w-[432px]" },
        React.createElement(TopContextMenu, { info: true, title: title, type: type }),
        React.createElement("h2", { className: "text-center text-2xl font-bold mt-2" }, "Tasks"),
        React.createElement("div", { className: "flex-grow overflow-y-auto w-full max-w-3xl px-4" }, (_a = branch === null || branch === void 0 ? void 0 : branch.tasks) === null || _a === void 0 ? void 0 : _a.map((task) => (React.createElement(TaskCard, { key: task.id, part: task.queue, title: task.title, xp: task.xp, status: task.status, actionURL: task.action_url, callToAction: task.call_to_action, onTaskComplete: refreshAllTasks, onEarnedXP: handleEarnedXP })))),
        React.createElement("footer", { className: "p-4 w-full max-w-3xl" },
            React.createElement("button", { onClick: isBranchCompleted ? undefined : onSliderHandler, className: `${isBranchCompleted
                    ? 'bg-gray-500 cursor-not-allowed'
                    : 'bg-blue-500 hover:bg-blue-600'} text-white w-full rounded-md py-2 mb-2`, disabled: isBranchCompleted }, "Start the task"))));
};
export default TasksPage;
