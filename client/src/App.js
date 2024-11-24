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
    return (React.createElement(TonConnectUIProvider, { manifestUrl: "https://raw.githubusercontent.com/isamarcev/CryptoWallet/refs/heads/TEMPORARY/web3_wallet_logo.json" },
        React.createElement(ToastContainer, { className: "toast-position", position: "top-center", position: "top-center", autoClose: 5000, hideProgressBar: false, newestOnTop: false, closeOnClick: true, rtl: false, theme: "dark", pauseOnFocusLoss: true, draggable: true, pauseOnHover: true }),
        React.createElement(Router, null,
            React.createElement(Routes, null,
                React.createElement(Route, { path: "/", element: React.createElement(GreetingPage, null) }),
                React.createElement(Route, { path: "/quest", element: React.createElement(QuestPage, null) }),
                React.createElement(Route, { path: "/nft", element: React.createElement(NFTPage, null) }),
                React.createElement(Route, { path: "/bonus", element: React.createElement(BonusPage, null) }),
                React.createElement(Route, { path: "/banner-page", element: React.createElement(BannerPage, null) }),
                React.createElement(Route, { path: "/tasks-page", element: React.createElement(TaskPage, null) }),
                React.createElement(Route, { path: "/exp", element: React.createElement(ExpPage, null) }),
                React.createElement(Route, { path: "/task_slider", element: React.createElement(SliderPage, null) }),
                React.createElement(Route, { path: "/congratulations", element: React.createElement(Congratulations, null) })))));
}
export default App;
