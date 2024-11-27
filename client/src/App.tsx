import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import QuestPage from './pages/QuestPage';
import NFTPage from './pages/NFTPage';
import BonusPage from './pages/BonusPage';
import GreetingPage from './pages/GreetingPage';
import BannerPage from './pages/BannerPage';
import TaskPage from './pages/TasksPage';
import ExpPage from './pages/ExpPage';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import SliderPage from './pages/SliderPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUser, updateUserAddress } from './store/slices/userSlice';
import { on, retrieveLaunchParams, postEvent, init, backButton, showBackButton } from '@telegram-apps/sdk';
import { api } from './api/Router';

function App() {
  const dispatch = useDispatch();
  // init();
  // backButton.mount()
  // if (backButton.show.isAvailable()) {
  //   backButton.show();
  // }
  // showBackButton();
  const { initDataRaw, initData } = retrieveLaunchParams();
  // console.log(telegramApp.WebApp.initData); 1232123xfchgjvbknlm,mjinougyfjtd gitch
  // const TOKEN = 'query_id=AAGOkjdJAAAAAI6SN0lDtNz9&user=%7B%22id%22%3A1228378766%2C%22first_name%22%3A%22%5B%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%5D%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22thinkfull%22%2C%22language_code%22%3A%22uk%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FO7kJtb7caW-l-UgHnh9ORATe5Ku_evvsvmZVI_6uCMI.svg%22%7D&auth_date=1732117099&signature=dUMV-_0Y-X96X7wcCy0CB5_ddeoH0-ZOjTObuKA26XDhdqS4TKGgGFb6qviJBXHPsT0R_v4y1e79-kVSKIkBDg&hash=43b9d3336c940d1f39d71e32f61ecb39b430ee2de887be1f3083ada3a84c68cb';
  api.defaults.headers.common = {
    "Authorization": initDataRaw,
    "web-app-auth": initDataRaw
  };
  // web_app_setup_back_button
  // postEvent('web_app_setup_closing_behavior', true);

  // useEffect(() => {
  //   console.log('location', window.location.pathname);
  //   if (window.location.pathname !== '/quest') {
  //     postEvent('web_app_setup_back_button', true);
  //   }
  //   else {
  //     postEvent('web_app_setup_back_button', false);
  //   }
  // }, [window.location.pathname]);

  const { user, status, error } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);
  document.body.classList.add('bg-black');
  return (
    <TonConnectUIProvider manifestUrl="https://raw.githubusercontent.com/isamarcev/CryptoWallet/refs/heads/TEMPORARY/web3_wallet_logo.json">
      <ToastContainer
        className="toast-position"
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        theme="dark"
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <Router>
        <Routes>
          <Route path="/" element={<GreetingPage />} />
          <Route path="/quest" element={<QuestPage />} />
          <Route path="/nft" element={<NFTPage />} />
          <Route path="/bonus" element={<BonusPage />} />
          <Route path="/banner-page" element={<BannerPage />} />
          <Route path="/tasks-page" element={<TaskPage />} />
          <Route path="/exp" element={<ExpPage />} />
          <Route path="/task-slider" element={<SliderPage />} />
        </Routes>
      </Router>
    </TonConnectUIProvider>
  );
}

export default App;
