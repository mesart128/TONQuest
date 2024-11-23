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
import { setBranchCompleted } from '../store/slices/branchSlice';

const TasksPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const { branch } = useSelector((state) => state.branch);
  const { title, type, branches } = useSelector((state) => state.selectedCard);

  const [isRefreshing, setIsRefreshing] = useState(false);
  const [totalXP, setTotalXP] = useState(0);
  const branchCompleted = useSelector((state) => state.branch.branchCompleted);
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
      navigate('/task_slider');
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
    const fetchBranch = async () => {
      const branchId = branches?.[0]?.id;
      if (branchId) {
        await dispatch(fetchBranchById(branchId));
      }
    };
    fetchBranch();
  }, [branches, dispatch]);

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
    if (isRefreshing) return;
    
    try {
      setIsRefreshing(true);
      if (!branch?.id) return;
      
      await dispatch(checkBranchById(branch.id)).unwrap();
      await dispatch(fetchBranchById(branch.id)).unwrap();
    } catch (error) {
      console.error('Error refreshing tasks:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleEarnedXP = (xp) => {
    setTotalXP((prevXP) => prevXP + xp);
  };

  useEffect(() => {
    if (branchCompleted) {
        dispatch(setBranchCompleted(false));
        navigate('/congratulations', { state: { totalXP } });
    }
}, [branchCompleted, navigate, totalXP]);
  
  return (
    <div className="h-screen flex flex-col bg-gradient-to-b from-black via-[#00a1ff] to-black items-center min-w-[432px]">
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
          actionURL={task.action_url}
          callToAction={task.call_to_action}
          onTaskComplete={refreshAllTasks}
          onEarnedXP={handleEarnedXP}
          />
        ))}
      </div>

      <footer className="p-4 w-full max-w-3xl">
        <button
          onClick={isBranchCompleted ? undefined : onSliderHandler}
          className={`${
            isBranchCompleted 
              ? 'bg-gray-500 cursor-not-allowed' 
              : 'bg-blue-500 hover:bg-blue-600'
          } text-white w-full rounded-md py-2 mb-2`}
          disabled={isBranchCompleted}
        >
          Start the task
        </button>
      </footer>
    </div>
  );
};

export default TasksPage;
