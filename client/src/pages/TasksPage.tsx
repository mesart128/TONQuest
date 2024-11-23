import { useEffect, useLayoutEffect, useState } from 'react';
import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchBranchById } from '../store/slices/branchSlice';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const TasksPage = () => {
  const location = useLocation();
  const branchId = location?.state?.branches?.[0]?.id;
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { branch, status, error } = useSelector((state) => state.branch);

  useEffect(() => {
    dispatch(fetchBranchById(branchId));
  }, [branchId, dispatch]);

  const onSliderHandler = () => {
    navigate('/task_slider');
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-b from-black via-[#00a1ff] to-black items-center min-w-[432px]">
      <TopContextMenu info={true} />
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
          />
        ))}
      </div>

      <footer className="p-4 w-full max-w-3xl">
        <button onClick={onSliderHandler} className="bg-blue-500 hover:bg-blue-600 text-white w-full rounded-md py-2">
          Start the task
        </button>
      </footer>
    </div>
  );
};

export default TasksPage;
