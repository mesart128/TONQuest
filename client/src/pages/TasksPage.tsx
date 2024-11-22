import { useEffect, useState } from 'react';
import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';
import { useLocation } from 'react-router-dom';
import { getBranchById } from '../api/Router';

const TasksPage = () => {
  const location = useLocation();
  const branchId = location?.state?.branches?.[0]?.id;

  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategory = async () => {
      try {
        const data = await getBranchById(branchId);
        setTasks(data?.tasks);
      } catch (error) {
        setError('Failed to fetch categories');
      } finally {
        setLoading(false);
      }
    };
    fetchCategory();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-b from-black via-[#00a1ff] to-black items-center min-w-[432px]">
      <TopContextMenu info={true} />
      <h2 className="text-center text-2xl font-bold mt-2">Tasks</h2>

      <div className="flex-grow overflow-y-auto w-full max-w-3xl px-4">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            part={task.queue}
            title={task.title}
            xp={task.xp}
            isLocked={task.locked}
            actionURL={task.action_url}
            callToAction={task.call_to_action}
          />
        ))}
      </div>

      <footer className="p-4 w-full max-w-3xl">
        <button className="bg-blue-500 hover:bg-blue-600 text-white w-full rounded-md py-2">
          Start the task
        </button>
      </footer>
    </div>
  );
};

export default TasksPage;
