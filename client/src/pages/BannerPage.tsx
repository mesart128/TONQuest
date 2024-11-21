//TODO: <NavBar /> кнопка назад - если task loading - на онклик вернуться в QuestPage, иначе слайдер назад
//TODO: кнопка закрыть - всегда на онклик вернуться на QuestPage; если таски загрузились то показывать инф кнопку
//taskBox - empty. как приходят таски то рендерим сюда их. useEffect -> initialState user.completedTasks, user.userWallet
//кнопка next - дергаем на онклик axios branches/{branch_id} - маппим таски и рендерим в компонент taskBox, (if task.isCompleted) - красивая иначе блюр. после загрузки тасок сменяем некст на старт the task
//кнопка start the task onclick - если userWallet -> useNavigate taskCard else -> bannerPage блюрится и выскакивает popup
//state под выполнение таски, чтоб получить урлу под выполнение таски
import questRecycle from '../assets/quest-recycle.png';
import TopContextMenu from '../components/TopContextMenu';
import { useNavigate, useLocation } from 'react-router-dom';

const BannerPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { imageUrl, description, title, type } = location?.state;

  console.log(imageUrl, description, title);

  const nextButtonHandler = () => {
    navigate('/tasks-page');
  };
  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <TopContextMenu title={title} type={type}/>


        <div className="flex flex-col items-center justify-center gap-12 mt-16">
          <img className="max-w-lg" src={imageUrl} />
          <h1 className="text-3xl font-bold mb-4">{title} ({type})</h1>
          <p className="text-xl text-blue-100 opacity-75 max-w-sm text-center">{description}</p>
        </div>
      <div className="mt-auto mb-14">
        <button onClick={nextButtonHandler}>Next</button>
      </div>
    </div>
  );
};

export default BannerPage;