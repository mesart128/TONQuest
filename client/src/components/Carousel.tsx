import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { Card } from '../pages/NFTPage';

type CarouselProps = {
  items: Card[];
};

const Carousel = ({ items }: CarouselProps) => {
  return (
    <div className="w-full max-w-lg mx-auto mt-4 h-[300px]">
      <Swiper
        spaceBetween={20}
        slidesPerView={2.5}
        loop={true}
        className="h-full w-full"
      >
        {items.map(({ title, subtitle, subtasks, status, image, alt }, idx) => (
          <SwiperSlide key={idx}>
            <div className="h-full w-full flex justify-center items-center rounded-3xl shadow-md">
              <div className="flex flex-col h-full w-full rounded-3xl overflow-hidden border border-zinc-400/80 relative">
                <div className="py-0.5 px-1 bg-white text-center border-4 border-black rounded-2xl font-medium absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <p className="text-black tracking-tight whitespace-nowrap">
                    {status}
                  </p>
                </div>
                <div className="h-[50%] bg-gradient-to-b from-black to-[#C3FF00] flex items-center justify-center">
                  <img
                    src={image}
                    alt={alt}
                    className="h-[60%] w-auto object-contain"
                  />
                </div>
                <div className="h-[50%] bg-black flex flex-col items-center text-center">
                  <div className="flex flex-1 justify-between mx-2">
                    <div className="mt-8 flex flex-col flex-1">
                      <p className="text-md text-white text-lg font-semibold">
                        {title}
                      </p>
                      <p className="text-md text-white/70 leading-4 mt-0.5">
                        {subtitle}
                      </p>
                        <p className={`text-md text-white/70 leading-4 mt-0.5 'line-through' : ''}`}>
                            Total {subtasks.length} tasks
                        </p>
                    </div>
                  </div>
                  <div className="flex w-full gap-1 px-4">
                    {subtasks.map((subtask) => (
                      <div
                        className={`mx-auto h-1 rounded-full ${subtask.isCompleted ? 'bg-[#C3FF00]' : 'bg-gray-50'} mb-5 flex-1 flex-shrink-0`}
                      ></div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
};

export default Carousel;
