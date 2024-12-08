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
import ClipLoader from "react-spinners/ClipLoader";
import {useNavigate} from 'react-router-dom';
import { Page } from '../Page';

const QuestPage = () => {
  const dispatch = useDispatch();

  const cards = useSelector((state) => state.category.list);
  const { user, status, error } = useSelector((state) => state.user);
  
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchCategories());
  }, [dispatch]);



  return (
    <Page back={false} disableMainButton={true}>
    <div className="h-screen flex flex-col items-center">
      <div className="bg-[#0096FF] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[100px]"></div>
      {!cards && <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
      <ClipLoader color="#36d7b7" size={50} />
      </div>}
      <div className="flex-1 flex flex-col w-[100vw]">
        <Navbar user={user}/>
        {/* <h2 className="text-2xl font-bold text-center mt-5 mr-8">
            Welcome to Quest
          </h2> */}
        <div className="flex flex-col flex-1 justify-center mb-10 ">
          
          <section className="max-w-[85vw] m-auto">
            <div className="quest-slider-container relative">
              <Swiper
                modules={[Pagination]}
                spaceBetween={20}
                slidesPerView={1}
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
                        branches={card.branches}
                        percentage={card.percentage}
                        subtitle={card.subtitle}
                      />
                    </div>
                  </SwiperSlide>
                ))}
              </Swiper>
              <div className="custom-pagination swiper-pagination"></div>
            </div>
          </section>
        </div>
      </div>
      <BottomMenu />
      
    </div>
    </Page>
  );
};

export default QuestPage;
