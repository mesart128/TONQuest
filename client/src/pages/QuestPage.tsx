import React, { useState, useEffect } from 'react';

import 'swiper/css';
import 'swiper/css/pagination';

import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCategories } from '../store/slices/categorySlice';
import ClipLoader from 'react-spinners/ClipLoader';
import { useNavigate } from 'react-router-dom';
import { Page } from '../Page';

import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const QuestPage = () => {
  const dispatch = useDispatch();

  const cards = useSelector((state) => state.category.list);
  const { user, status, error } = useSelector((state) => state.user);

  const [currentSlide, setCurrentSlide] = useState(() => {
    const savedSlide = sessionStorage.getItem('currentSlide');
    return savedSlide ? parseInt(savedSlide, 10) : 0;
  });

  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchCategories());
  }, [dispatch]);

  const sliderSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    touchThreshold: 10,
    swipeToSlide: true,
    slidesToScroll: 1,
    initialSlide: currentSlide,
    preventDefaultTouchMove: true,
    afterChange: (index) => {
      setCurrentSlide(index);
      sessionStorage.setItem('currentSlide', index);
    },
    appendDots: (dots) => (
      <div
        style={{
          bottom: '30px',
          position: 'relative',
        }}
      >
        <ul
          style={{
            margin: '0px',
            padding: '0px',
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          {dots}
        </ul>
      </div>
    ),
    customPaging: (i) => (
      <div
        style={{
          width: '10px',
          height: '10px',
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.5)',
          transition: 'all 0.3s ease',
        }}
      ></div>
    ),
    arrows: false,
  };

  return (
    <Page back={false} disableMainButton={true}>
      <div className="min-h-screen flex flex-col">
        <div className="bg-[#0096FF] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[100px]"></div>
        {!cards && (
          <div className="flex-1 flex justify-center items-center">
            <ClipLoader color="#36d7b7" size={50} />
          </div>
        )}
        <div className="flex-1 flex flex-col">
          <Navbar user={user} />
          <div className="flex-1 flex items-center justify-center">
            <div className="w-full max-w-[90vw] md:max-w-[700px] lg:max-w-[800px] lg:max-h-[650px] xl:max-w-[700px] px-4 h-full">
              <Slider {...sliderSettings} className="quest-slider">
                {cards?.map((card) => (
                  <div
                    key={card.id}
                    className="px-2 py-4 md:py-6 lg:py-8 xl:py-10"
                  >
                    <div className="flex items-center justify-center">
                      <div className="w-full">
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
                    </div>
                  </div>
                ))}
              </Slider>
            </div>
          </div>
        </div>
        <BottomMenu />
      </div>
    </Page>
  );
};

export default QuestPage;
