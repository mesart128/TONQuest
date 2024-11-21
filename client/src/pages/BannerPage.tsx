//TODO: <NavBar /> кнопка назад - если task loading - на онклик вернуться в QuestPage, иначе слайдер назад
//TODO: кнопка закрыть - всегда на онклик вернуться на QuestPage; если таски загрузились то показывать инф кнопку
//taskBox - empty. как приходят таски то рендерим сюда их. useEffect -> initialState user.completedTasks, user.userWallet
//кнопка next - дергаем на онклик axios branches/{branch_id} - маппим таски и рендерим в компонент taskBox, (if task.isCompleted) - красивая иначе блюр. после загрузки тасок сменяем некст на старт the task
//кнопка start the task onclick - если userWallet -> useNavigate taskCard else -> bannerPage блюрится и выскакивает popup
//state под выполнение таски, чтоб получить урлу под выполнение таски
