import React, { useEffect, useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTask } from '../store/slices/taskSlice';
import GradientButton from '../components/buttons/GradientButton';
import { useNavigate } from 'react-router-dom';
const SliderPage = () => {
    var _a, _b, _c;
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { activeTask } = useSelector((state) => state.branch);
    const tasks = useSelector((state) => state.task.tasks);
    const slides = (_a = tasks === null || tasks === void 0 ? void 0 : tasks[activeTask === null || activeTask === void 0 ? void 0 : activeTask.id]) === null || _a === void 0 ? void 0 : _a.slides;
    const xp = (_b = tasks === null || tasks === void 0 ? void 0 : tasks[activeTask === null || activeTask === void 0 ? void 0 : activeTask.id]) === null || _b === void 0 ? void 0 : _b.xp;
    const actionURL = (_c = tasks === null || tasks === void 0 ? void 0 : tasks[activeTask === null || activeTask === void 0 ? void 0 : activeTask.id]) === null || _c === void 0 ? void 0 : _c.action_url;
    const [activeIndex, setActiveIndex] = useState(0);
    useEffect(() => {
        if (activeTask === null || activeTask === void 0 ? void 0 : activeTask.id) {
            dispatch(fetchTask(activeTask.id));
        }
    }, [activeTask, dispatch]);
    const onCloseHandler = () => {
        navigate('/tasks-page');
    };
    const goToHandler = () => {
        navigate();
    };
    return (React.createElement("div", { className: "h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]" },
        React.createElement("div", { className: "w-full max-w-md px-4" },
            React.createElement(Swiper, { modules: [Pagination], pagination: {
                    clickable: true,
                    type: 'bullets',
                    bulletActiveClass: 'swiper-pagination-bullet-active bg-blue-500',
                    bulletClass: 'swiper-pagination-bullet bg-gray-400 mx-1',
                }, spaceBetween: 30, slidesPerView: 1, centeredSlides: true, className: "w-full h-full", onSlideChange: (swiper) => setActiveIndex(swiper.activeIndex) }, slides === null || slides === void 0 ? void 0 : slides.map((slide) => (React.createElement(SwiperSlide, { key: slide.id },
                React.createElement("div", { className: "p-6 h-full" },
                    React.createElement("div", { className: "flex justify-between items-center mb-6" },
                        React.createElement("div", { className: "bg-blue-600 text-white px-4 py-2 rounded-full" },
                            "+",
                            xp,
                            " XP"),
                        React.createElement("button", { onClick: onCloseHandler, className: "bg-gray-800 text-white px-4 py-2 rounded-lg" }, "Close")),
                    React.createElement("h1", { className: "text-white text-4xl font-bold mb-4" }, "Task description"),
                    React.createElement("p", { className: "text-gray-300 text-lg mb-8" }, slide.description),
                    React.createElement("div", { className: "relative rounded-3xl overflow-hidden mb-8" },
                        React.createElement("img", { src: `data:image/png;base64,${slide.image}`, alt: slide.title, style: {
                                maxHeight: '400px',
                                maxWidth: '100%',
                                objectFit: 'contain',
                            }, className: "m-auto" })),
                    activeIndex === slides.length - 1 && (React.createElement("a", { href: actionURL, target: "_blank" },
                        React.createElement(GradientButton, { children: "Go to service", onClick: goToHandler })))))))))));
};
export default SliderPage;
