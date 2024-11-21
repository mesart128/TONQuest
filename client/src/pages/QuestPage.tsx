import QuestCard from '../components/cards/QuestCard';
import Navbar from '../components/Navbar';
import BottomMenu from '../components/BottomMenu';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';
import React, { useState, useEffect } from 'react';
import { getCategories } from '../api/Router';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

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
    // console.log(categories);
    fetchCategories();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Пока идет загрузка
  }

  if (error) {
    return <div>{error}</div>; // Если ошибка
  }

  return (
    <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center">
      <Navbar />

      <div className="px-4 flex flex-col items-center justify-center max-w-md mt-8">
        <section>
          <h2 className="text-2xl font-bold mb-4 text-center mb-8">
            Welcome to Quest
          </h2>
          <div className="flex justify-between gap-4 min-h-[500px]">
          <Swiper
              modules={[Navigation, Pagination]}
              spaceBetween={30}
              slidesPerView={1}
              navigation
              pagination={{ clickable: true }}
              centeredSlides={true}
              className="w-full"
            >
              {cards.map((card) => (
                <SwiperSlide key={card.id} className="flex justify-center">
                  <QuestCard
                    type={card.head}
                    title={card.map}
                    description={card.description}
                    xpReward={50}
                    isCompleted={true}
                  />
                </SwiperSlide>
              ))}
            </Swiper>
          </div>
        </section>
      </div>
      <BottomMenu />
    </div>
  );
};

export default QuestPage;
