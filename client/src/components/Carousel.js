import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
const Carousel = ({ items }) => {
    return (React.createElement("div", { className: "w-full max-w-lg mx-auto mt-4 h-[300px]" },
        React.createElement(Swiper, { spaceBetween: 20, slidesPerView: 2.5, loop: true, className: "h-full w-full" }, items.map(({ title, subtitle, subtasks, status, image, alt }, idx) => (React.createElement(SwiperSlide, { key: idx },
            React.createElement("div", { className: "h-full w-full flex justify-center items-center rounded-3xl shadow-md" },
                React.createElement("div", { className: "flex flex-col h-full w-full rounded-3xl overflow-hidden border border-zinc-400/80 relative" },
                    React.createElement("div", { className: "py-0.5 px-1 bg-white text-center border-4 border-black rounded-2xl font-medium absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" },
                        React.createElement("p", { className: "text-black tracking-tight whitespace-nowrap" }, status)),
                    React.createElement("div", { className: "h-[50%] bg-gradient-to-b from-black to-[#C3FF00] flex items-center justify-center" },
                        React.createElement("img", { src: image, alt: alt, className: "h-[60%] w-auto object-contain" })),
                    React.createElement("div", { className: "h-[50%] bg-black flex flex-col items-center text-center" },
                        React.createElement("div", { className: "flex flex-1 justify-between mx-2" },
                            React.createElement("div", { className: "mt-8 flex flex-col flex-1" },
                                React.createElement("p", { className: "text-md text-white text-lg font-semibold" }, title),
                                React.createElement("p", { className: "text-md text-white/70 leading-4 mt-0.5" }, subtitle),
                                React.createElement("p", { className: `text-md text-white/70 leading-4 mt-0.5 'line-through' : ''}` },
                                    "Total ",
                                    subtasks.length,
                                    " tasks"))),
                        React.createElement("div", { className: "flex w-full gap-1 px-4" }, subtasks.map((subtask) => (React.createElement("div", { className: `mx-auto h-1 rounded-full ${subtask.isCompleted ? 'bg-[#C3FF00]' : 'bg-gray-50'} mb-5 flex-1 flex-shrink-0` })))))))))))));
};
export default Carousel;
