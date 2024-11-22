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

function App() {
  // useEffect(() => {
  //     const tg = window.Telegram.WebApp;
  //     tg.ready();
  //     tg.expand();
  // }, []);

  return (
    <TonConnectUIProvider manifestUrl="https://raw.githubusercontent.com/isamarcev/CryptoWallet/refs/heads/TEMPORARY/web3_wallet_logo.json">
    <Router>
      <Routes>
        <Route path="/" element={<GreetingPage />} />
        <Route path="/quest" element={<QuestPage />} />
        <Route path="/nft" element={<NFTPage />} />
        <Route path="/bonus" element={<BonusPage />} />
        <Route path="/banner-page" element={<BannerPage />} />
        <Route path="/tasks-page" element={<TaskPage />} />
        <Route path="/exp" element={<ExpPage />} />
      </Routes>
    </Router>
     </TonConnectUIProvider>
  );
}

export default App;
