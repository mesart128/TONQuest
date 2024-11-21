import React, { useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import { getCategories } from '../api/Router';

const QuestPage = () => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCategories();
        setCards(data);
      } catch (error) {
        setError('Failed to fetch categories');
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="min-h-screen max-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <Navbar />

      <div className="w-full px-4 flex flex-col items-center justify-center mt-8">
        <section className="w-full max-w-md">
          <h2 className="text-2xl font-bold text-center mb-8">
            Welcome to Quest
          </h2>
          <div className="quest-slider-container relative ">
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
              {cards.map((card) => (
                <SwiperSlide key={card.id} className="flex justify-center">
                  <div className="w-full max-w-sm">
                    <QuestCard
                      type={card.head}
                      title={card.title}
                      description={card.description}
                      xpReward={card.xp}
                      imageUrl={card.image}
                      isCompleted={true}
                    />
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
            <div className="custom-pagination swiper-pagination"></div>
            <BottomMenu isQuestPage={true} />
          </div>
        </section>
      </div>
    </div>
  );
};

export default QuestPage;