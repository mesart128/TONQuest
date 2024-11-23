import React, { useEffect, useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { useSelector, useDispatch } from 'react-redux';
import { setCurrentSlide } from '../store/slices/branchSlice';
import { fetchTask } from '../store/slices/taskSlice';
import TopContextMenu from '../components/TopContextMenu';
import GradientButton from '../components/buttons/GradientButton';
import { useNavigate } from 'react-router-dom';

const SliderPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { activeTask } = useSelector((state) => state.branch);
  const tasks = useSelector((state) => state.task.tasks);
  const slides = tasks?.[activeTask?.id]?.slides;
  const xp = tasks?.[activeTask?.id]?.xp;
  const actionURL = tasks?.[activeTask?.id]?.action_url;

  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    if (activeTask?.id) {
      dispatch(fetchTask(activeTask.id));
    }
  }, [activeTask, dispatch]);

  const onCloseHandler = () => {
    navigate('/tasks-page');
  };

  const goToHandler = () => {
    navigate();
  };

  return (
    <div className="h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center min-w-[432px]">
      <div className="w-full max-w-md px-4">
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
          onSlideChange={(swiper) => setActiveIndex(swiper.activeIndex)}
        >
          {slides?.map((slide) => (
            <SwiperSlide key={slide.id}>
              <div className="p-6 h-full">
                <div className="flex justify-between items-center mb-6">
                  <div className="bg-blue-600 text-white px-4 py-2 rounded-full">
                    +{xp} XP
                  </div>
                  <button
                    onClick={onCloseHandler}
                    className="bg-gray-800 text-white px-4 py-2 rounded-lg"
                  >
                    Close
                  </button>
                </div>

                <h1 className="text-white text-4xl font-bold mb-4">
                  Task description
                </h1>

                <p className="text-gray-300 text-lg mb-8">
                  {slide.description}
                </p>

                <div className="relative rounded-3xl overflow-hidden mb-8">
                  <img
                    src={`data:image/png;base64,${slide.image}`}
                    alt={slide.title}
                    style={{
                      maxHeight: '400px',
                      maxWidth: '100%',
                      objectFit: 'contain',
                    }}
                    className="m-auto"
                  />
                </div>

                {activeIndex === slides.length - 1 && (
                  <a href={actionURL} target="_blank">
                    <GradientButton
                      children="Go to service"
                      onClick={goToHandler}
                    />
                  </a>
                )}
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </div>
  );
};

export default SliderPage;
