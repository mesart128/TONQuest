'use client';
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createContext, useContext, useEffect, useState } from 'react';
import Script from 'next/script';
import { usePathname, useRouter } from 'next/navigation';
import { createUser, getUser } from '@/services/api';
export const TelegramContext = createContext({ isLoading: true });
export const TelegramProvider = ({ children, }) => {
    const [webApp, setWebApp] = useState(undefined);
    const [isLoading, setLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();
    useEffect(() => {
        const app = window.Telegram;
        if (app) {
            app.WebApp.ready();
            app.WebApp.expand();
            app.WebApp.setHeaderColor('#000');
            app.WebApp.setBackgroundColor('#000');
            setWebApp(app);
            setLoading(false);
            console.log(webApp);
        }
    }, [pathname]);
    useEffect(() => {
        if (webApp) {
            if (pathname !== '/') {
                webApp.WebApp.BackButton.show();
                webApp.WebApp.BackButton.onClick(() => router.back());
            }
            else {
                webApp.WebApp.BackButton.hide();
            }
        }
    }, [webApp, pathname, router]);
    useEffect(() => {
        (() => __awaiter(void 0, void 0, void 0, function* () {
            var _a;
            if ((_a = webApp === null || webApp === void 0 ? void 0 : webApp.WebApp.initDataUnsafe) === null || _a === void 0 ? void 0 : _a.user) {
                const user = yield getUser(webApp.WebApp.initDataUnsafe.user.id);
                // console.log(user.error)
                if (!user) {
                    yield createUser({
                        telegram_id: webApp.WebApp.initDataUnsafe.user.id,
                        first_name: webApp.WebApp.initDataUnsafe.user.first_name,
                        username: webApp.WebApp.initDataUnsafe.user.username,
                        last_name: webApp.WebApp.initDataUnsafe.user.last_name,
                    });
                }
            }
        }))();
    }, [webApp]);
    return (React.createElement(TelegramContext.Provider, { value: { telegramApp: webApp, isLoading } },
        React.createElement(Script, { src: "https://telegram.org/js/telegram-web-app.js", strategy: "beforeInteractive" }),
        children));
};
export const useTelegram = () => useContext(TelegramContext);
