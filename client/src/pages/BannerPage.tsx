//TODO: <NavBar /> кнопка назад - если task loading - на онклик вернуться в QuestPage, иначе слайдер назад
//TODO: кнопка закрыть - всегда на онклик вернуться на QuestPage; если таски загрузились то показывать инф кнопку
//taskBox - empty. как приходят таски то рендерим сюда их. useEffect -> initialState user.completedTasks, user.userWallet
//кнопка next - дергаем на онклик axios branches/{branch_id} - маппим таски и рендерим в компонент taskBox, (if task.isCompleted) - красивая иначе блюр. после загрузки тасок сменяем некст на старт the task
//кнопка start the task onclick - если userWallet -> useNavigate taskCard else -> bannerPage блюрится и выскакивает popup
//state под выполнение таски, чтоб получить урлу под выполнение таски

import TopContextMenu from '../components/TopContextMenu';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { Page } from '../Page';
import { mainButton } from '@telegram-apps/sdk-react';
import { API_BASE_URL } from '../api/Router';

const BannerPage = () => {
  const navigate = useNavigate();

  const { imageUrl, description, title, type, branches, subtitle } =
    useSelector((state) => state.selectedCard);
  useEffect(() => {
    mainButton.setParams({
      isVisible: true,
      text: 'Next',
    });
    return mainButton.onClick(() => {
      navigate('/tasks-page');
    });
  }, []);

  return (
    <Page>
      <div className="min-h-screen relative flex items-center w-[100vw]">
        <div className="bg-[#0096FF] w-full h-3/5 rounded-full absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[100px]"></div>
        <div className="flex flex-col items-center justify-center gap-2 z-10">
          <img
            className="max-w-[50%] mb-5"
            src={`${API_BASE_URL}/${imageUrl}`}
          />
          <h1 className="text-2xl font-bold mb-2 text-center text-white max-w-[70%]">
            {title} ({type})
          </h1>
          <p className="text-l text-white opacity-75 max-w-[85%] text-center ">
            {subtitle}
          </p>
        </div>
        {/* <div className="mt-auto mb-14"> */}
        {/* </div> */}
      </div>
    </Page>
  );
};

export default BannerPage;
