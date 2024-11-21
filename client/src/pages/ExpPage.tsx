import BottomMenu from '../components/BottomMenu';

const ExpPage = () => {
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <BottomMenu isExpPage={true} />
    </div>
  );
};

export default ExpPage;
