import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';

const QuestPage = () => {
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center">
      <Navbar />

      <div className="px-4 flex flex-col items-center justify-center max-w-md mt-8">
        <section>
          <h2 className="text-2xl font-bold mb-4 text-center mb-8">
            Welcome to Quest
          </h2>
          <div className="flex justify-between gap-4 min-h-[500px]">
            <QuestCard
              type="DEX"
              title="Easy start"
              description="You will learn how to use decentralized exchanges tools"
              xpReward={50}
              isCompleted={true}
            />
          </div>
        </section>
      </div>
      <BottomMenu />
    </div>
  );
};

export default QuestPage;
