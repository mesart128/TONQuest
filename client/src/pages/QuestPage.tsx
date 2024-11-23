import React, { useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/pagination';

import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCategories } from '../store/slices/categorySlice';

const QuestPage = () => {
  const dispatch = useDispatch();

  const cards = useSelector((state) => state.category.list);

  useEffect(() => {
    dispatch(fetchCategories());
  }, [dispatch]);

  return (
    <div className="h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <div className="flex-1 flex flex-col px-4 mx-auto">
        <Navbar />
        <div className="flex flex-col flex-1 justify-center">
          <h2 className="text-2xl font-bold text-center mb-8">
            Welcome to Quest
          </h2>
          <section className="max-w-md">
            <div className="quest-slider-container relative">
              <Swiper
                modules={[Pagination]}
                spaceBetween={20}
                slidesPerView={1.2}
                centeredSlides={true}
                pagination={{
                  clickable: true,
                  bulletActiveClass: 'swiper-pagination-bullet-active',
                  bulletClass: 'swiper-pagination-bullet',
                  el: '.custom-pagination',
                }}
                className="quest-slider"
              >
                {cards?.map((card) => (
                  <SwiperSlide key={card.id} className="flex justify-center">
                    <div className="w-full max-w-sm">
                      <QuestCard
                        type={card.head}
                        title={card.title}
                        description={card.description}
                        xpReward={card.xp}
                        imageUrl={card.image}
                        isCompleted={true}
                        branches={card.branches}
                      />
                    </div>
                  </SwiperSlide>
                ))}
              </Swiper>
              <div className="custom-pagination swiper-pagination"></div>
            </div>
          </section>
        </div>
        <BottomMenu />
      </div>
    </div>
  );
};

export default QuestPage;
