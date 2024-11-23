import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import QuestPage from './pages/QuestPage';
import NFTPage from './pages/NFTPage';
import BonusPage from './pages/BonusPage';
import GreetingPage from './pages/GreetingPage';
import BannerPage from './pages/BannerPage';
import TaskPage from './pages/TasksPage';
import ExpPage from './pages/ExpPage';
import Congratulations from './pages/Congratulations';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import SliderPage from './pages/SliderPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  // useEffect(() => {
  //     const tg = window.Telegram.WebApp;
  //     tg.ready();
  //     tg.expand();
  // }, []);
  document.body.classList.add('bg-black');
  return (
    <TonConnectUIProvider manifestUrl="https://raw.githubusercontent.com/isamarcev/CryptoWallet/refs/heads/TEMPORARY/web3_wallet_logo.json">
      <ToastContainer
        className="toast-position"
        position="top-center"
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
          <Route path="/task_slider" element={<SliderPage />} />
          <Route path="/congratulations" element={<Congratulations />} />
        </Routes>
      </Router>
    </TonConnectUIProvider>
  );
}

export default App;
