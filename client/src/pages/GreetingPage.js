import React, { useEffect } from 'react';
import logo from '../assets/greeting-logo.png';
import GradientButton from '../components/buttons/GradientButton.tsx';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
// import { useTelegram } from '../providers/TelegramContext';
import { fetchUser } from '../store/slices/userSlice';
import ClipLoader from "react-spinners/ClipLoader";
import { api } from '../api/Router';
import { retrieveLaunchParams } from '@telegram-apps/sdk';
const GreetingPage = () => {
    const { initDataRaw, initData } = retrieveLaunchParams();
    // const { telegramApp, isLoading } = useTelegram();
    // console.log(telegramApp.WebApp.initData);
    // const TOKEN =
    // 'query_id=AAGOkjdJAAAAAI6SN0lDtNz9&user=%7B%22id%22%3A1228378766%2C%22first_name%22%3A%22%5B%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%5D%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22thinkfull%22%2C%22language_code%22%3A%22uk%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FO7kJtb7caW-l-UgHnh9ORATe5Ku_evvsvmZVI_6uCMI.svg%22%7D&auth_date=1732117099&signature=dUMV-_0Y-X96X7wcCy0CB5_ddeoH0-ZOjTObuKA26XDhdqS4TKGgGFb6qviJBXHPsT0R_v4y1e79-kVSKIkBDg&hash=43b9d3336c940d1f39d71e32f61ecb39b430ee2de887be1f3083ada3a84c68cb';
    api.defaults.headers.common = {
        "Authorization": initDataRaw,
        "web-app-auth": initDataRaw
    };
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const { user, status, error } = useSelector((state) => state.user);
    useEffect(() => {
        dispatch(fetchUser());
    }, [dispatch]);
    if (error)
        return React.createElement("p", null,
            "Error: ",
            error);
    const handleContinue = () => {
        navigate('/quest');
    };
    return (React.createElement("div", { className: "min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center px-16 py-8" },
        status === 'loading' && React.createElement("div", { style: { display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" } },
            React.createElement(ClipLoader, { color: "#36d7b7", size: 50 })),
        React.createElement("div", { className: "text-2xl font-extrabold text-[#0096FF]" }, "TONQuest"),
        React.createElement("div", { className: "flex-1 flex flex-col items-center justify-center text-center max-w-md -mt-20 min-h-[500px]" },
            React.createElement("img", { src: logo }),
            React.createElement("h1", { className: "text-3xl font-bold text-white mb-4" },
                "Hi, ", user === null || user === void 0 ? void 0 :
                user.username,
                ' '),
            React.createElement("p", { className: "text-white/80 text-center leading-6 mb-12 w-96" }, "Welcome to TONQuest Are you ready to dive into the amazing world of cryptocurrencies? It's easier than ever with our app! Complete tasks, earn points and become a real expert in the field of blockchain.")),
        React.createElement(GradientButton, { blocked: false, children: "Continue", onClick: handleContinue })));
};
export default GreetingPage;
