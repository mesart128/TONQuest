import { useEffect, useLayoutEffect, useState } from 'react';
import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchBranchById } from '../store/slices/branchSlice';
import { useLocation, useNavigate } from 'react-router-dom';
import { setSelectedCard } from '../store/slices/selectedCardSlice';
import { useTonConnectModal, useTonConnectUI, useTonAddress } from '@tonconnect/ui-react';
import { setUserAddress } from '../api/Router';
import { checkBranchById } from '../store/slices/branchSlice';
import { getTask } from '../api/Router';

const TasksPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { state, open, close } = useTonConnectModal();
  const rawAddress = useTonAddress(false);
  const user = useSelector((state) => state.user.user);
  const { branch, status, error, activeTask } = useSelector(
    (state) => state.branch,
  );
  console.log(activeTask);

  const isBranchCompleted = !branch?.tasks.some((el) => el.status === 'active' );

  const { imageUrl, description, title, type, branches } = useSelector(
    (state) => state.selectedCard,
  );

  const onSliderHandler = async () => {
    if (user?.wallet_address)  {
      navigate('/task-slider');
    }
    else {
      console.log('no wallet');
      if (rawAddress) {
        console.log('address connected');
        await setUserAddress(rawAddress);
      }
      else {
        console.log('address not connected');
        open();
      }
    }
  };
  

  useEffect(() => {
    const branchId = branches?.[0]?.id;
    if (branchId) {
      dispatch(fetchBranchById(branchId));
    }
  }, [title, type, branches, dispatch]);

  useEffect(() => {
    if (rawAddress) {
      console.log(rawAddress);
    }
  }
  , [rawAddress]);

  if (error) {
    return <div>{error}</div>;
  }

  const refreshAllTasks = async () => {
    try {
      if (!branch?.id) return;
      
      const branchCheck = await dispatch(checkBranchById(branch.id)).unwrap();
      
      if (branchCheck) {
        await dispatch(checkBranchById(branch.id));
      }
    } catch (error) {
      console.error('Error refreshing tasks:', error);
    }
  };
  
  return (
    <div className="min-h-screen relative flex flex-col items-center w-full flex flex-col items-center">
      <div className="bg-[#0096FF] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[200px]"></div>
      <TopContextMenu info={true} title={title} type={type} />
      <h2 className="text-center text-2xl font-bold mt-2">Tasks</h2>

      <div className="flex-grow overflow-y-auto w-full max-w-3xl px-4">
        {branch?.tasks?.map((task) => (
          <TaskCard
            key={task.id}
            part={task.queue}
            title={task.title}
            xp={task.xp}
            status={task.status}
            task_type={task.task_type}
            actionURL={task.action_url}
            callToAction={task.call_to_action}
            onTaskComplete={refreshAllTasks}
          />
        ))}
      </div>

      <footer className="p-4 w-full max-w-3xl">
        
          {isBranchCompleted ? (
            <button
          className="bg-gray-500 disabled text-white w-full rounded-md py-2 mb-2"
        >
          Start the task
        </button>
          ) : (
            <button
            onClick={onSliderHandler}
          className="bg-blue-500 hover:bg-blue-600 text-white w-full rounded-md py-2 mb-2"
        >
          Start the task
        </button>
          )
}
        
      </footer>
    </div>
  );
};

export default TasksPage;
