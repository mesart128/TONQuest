import TaskCard from '../components/cards/TaskCard';
import TopContextMenu from '../components/TopContextMenu';

const TasksPage = () => {
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <TopContextMenu info={true} />
      <TaskCard />
    </div>
  );
};

export default TasksPage;
