import React, { useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCategories } from '../store/slices/categorySlice';
import ClipLoader from "react-spinners/ClipLoader";
const QuestPage = () => {
    const dispatch = useDispatch();
    const cards = useSelector((state) => state.category.list);
    const { user, status, error } = useSelector((state) => state.user);
    useEffect(() => {
        dispatch(fetchCategories());
    }, [dispatch]);
    return (React.createElement("div", { className: "h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]" },
        !cards && React.createElement("div", { style: { display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" } },
            React.createElement(ClipLoader, { color: "#36d7b7", size: 50 })),
        React.createElement("div", { className: "flex-1 flex flex-col px-4 mx-auto" },
            React.createElement(Navbar, { user: user }),
            React.createElement("div", { className: "flex flex-col flex-1 justify-center" },
                React.createElement("h2", { className: "text-2xl font-bold text-center mb-8" }, "Welcome to Quest"),
                React.createElement("section", { className: "max-w-md" },
                    React.createElement("div", { className: "quest-slider-container relative" },
                        React.createElement(Swiper, { modules: [Pagination], spaceBetween: 20, slidesPerView: 1.2, centeredSlides: true, pagination: {
                                clickable: true,
                                bulletActiveClass: 'swiper-pagination-bullet-active',
                                bulletClass: 'swiper-pagination-bullet',
                                el: '.custom-pagination',
                            }, className: "quest-slider" }, cards === null || cards === void 0 ? void 0 : cards.map((card) => (React.createElement(SwiperSlide, { key: card.id, className: "flex justify-center" },
                            React.createElement("div", { className: "w-full max-w-sm" },
                                React.createElement(QuestCard, { type: card.head, title: card.title, description: card.description, xpReward: card.xp, imageUrl: card.image, branches: card.branches, percentage: card.percentage })))))),
                        React.createElement("div", { className: "custom-pagination swiper-pagination" })))),
            React.createElement(BottomMenu, null))));
};
export default QuestPage;
