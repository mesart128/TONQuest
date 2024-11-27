import React, { useEffect, useState } from 'react';
import { Swiper, SwiperSlide, useSwiper } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { useSelector, useDispatch } from 'react-redux';
import { setCurrentSlide } from '../store/slices/branchSlice';
import { fetchTask } from '../store/slices/taskSlice';
import TopContextMenu from '../components/TopContextMenu';
import { useNavigate } from 'react-router-dom';
import { Page } from '../Page';
import NextSlideButton from '../components/buttons/NextSlideButton';
import { API_BASE_URL } from '../api/Router';

const SliderPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate(); 

  const { activeTask } = useSelector((state) => state.branch);
  const tasks = useSelector((state) => state.task.tasks);
  const slides = tasks?.[activeTask?.id]?.slides;
  const xp = tasks?.[activeTask?.id]?.xp;
  const actionURL = tasks?.[activeTask?.id]?.action_url;

  useEffect(() => {
    if (activeTask?.id) {
      dispatch(fetchTask(activeTask.id));
    }
  }, [activeTask, dispatch]);

  const onCloseHandler = () => {
    navigate('/tasks-page');
  };

  console.log(slides)

  return (
    <Page>
      <div className="min-h-screen relative flex flex-col items-center w-full flex flex-col items-center">
        <div className="bg-[#0096FF] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[200px]"></div>
        <div className="w-full max-w-[100vw]">
          <div className="flex justify-between items-center mb-6 px-10 w-full fixed top-0 left-0 z-10 sticky top-0">
            <div className="text-sm backdrop-blur-lg bg-black/10 border border-white/60 rounded-xl p-2">
              +{xp} XP
            </div>
            <button
              onClick={onCloseHandler}
              className="bg-gray-800 text-white px-4 py-2 rounded-lg"
            >
              Close
            </button>
          </div>
          <Swiper
            modules={[Pagination]}
            pagination={{
              clickable: true,
              type: 'bullets',
              bulletActiveClass: 'swiper-pagination-bullet-active bg-blue-500',
              bulletClass: 'swiper-pagination-bullet bg-gray-400 mx-1',
            }}
            spaceBetween={30}
            slidesPerView={1}
            centeredSlides={true}
            className="w-full h-full"
            // onSlideChange={(swiper) => setIsLastSlide(swiper.activeIndex === slides?.length - 1)}
          >
            {slides?.map((slide) => (
              <SwiperSlide key={slide.id}>
                <div className="p-6 h-full">

                  <h1 className="text-white text-3xl font-bold mb-4">
                    {slide.title}
                  </h1>

                  <p className="text-gray-300 text-lg mb-8">
                    {slide.description}
                  </p>

                  <div className="rounded-3xl overflow-hidden mb-8">
                    <img
                      src={`${API_BASE_URL}/${slide.image}`}
                      alt={slide.title}
                      style={{
                        maxHeight: '75vh',
                        // maxWidth: '75%',
                        objectFit: 'contain',
                      }}
                      className="m-auto"
                    />
                  </div>

                  
                </div>
              </SwiperSlide>
            ))}
            <NextSlideButton actionURL={actionURL} />
          </Swiper>
        </div>
      </div>
    </Page>
  );
};

export default SliderPage;
