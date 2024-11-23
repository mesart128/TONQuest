import { useEffect, useLayoutEffect, useState } from 'react';
import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchBranchById } from '../store/slices/branchSlice';
import { useLocation, useNavigate } from 'react-router-dom';
import { setSelectedCard } from '../store/slices/selectedCardSlice';

const TasksPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { branch, status, error, activeTask } = useSelector(
    (state) => state.branch,
  );

  const isBranchCompleted = !branch.tasks.some((el) => el.status === 'active' );

  const { imageUrl, description, title, type, branches } = useSelector(
    (state) => state.selectedCard,
  );

  const onSliderHandler = () => {
    navigate('/task_slider');
  };

  useEffect(() => {
    const branchId = branches[0]?.id;

    if (branchId) {
      dispatch(fetchBranchById(branchId));
    }
  }, [title, type, branches, dispatch]);

  if (error) {
    return <div>{error}</div>;
  }

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
