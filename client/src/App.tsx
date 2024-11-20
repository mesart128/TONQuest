import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import QuestPage from './pages/QuestPage';
import NFTPage from './pages/NFTPage';
import BonusPage from './pages/BonusPage';
import GreetingPage from "./pages/GreetingPage.tsx";

function App() {
    // useEffect(() => {
    //     const tg = window.Telegram.WebApp;
    //     tg.ready();
    //     tg.expand();
    // }, []);

    return (
        <Router>
            <Routes>
                <Route path="/" element={<GreetingPage />} />
                <Route path="/quest" element={<QuestPage />} />
                <Route path="/nft" element={<NFTPage />} />
                <Route path="/bonus" element={<BonusPage />} />
            </Routes>
        </Router>
    );
}

export default App
