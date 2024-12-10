import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setSelectedCard } from '../../store/slices/selectedCardSlice';
import { useSelector } from 'react-redux';
import { API_BASE_URL } from '../../api/Router';

const QuestCard = ({
  type,
  title,
  description,
  xpReward,
  imageUrl,
  branches,
  percentage,
  subtitle,
}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const cardSelectHandler = () => {
    dispatch(
      setSelectedCard({
        type,
        title,
        description,
        xpReward,
        imageUrl,
        branches,
        subtitle,
      }),
    );

    navigate('/banner-page');
  };

  const { branch, error, activeTask } = useSelector((state) => state.branch);

  return (
    <div
      className="w-full min-h-[200px] md:min-h-[700px] lg:min-h-[600px] xl:min-h-[700px]"
      onClick={cardSelectHandler}
    >
      <div
        className="rounded-3xl w-full flex flex-col justify-between
        text-white border-2 border-solid border-[#0096FF]
        shadow-2xl overflow-hidden
        bg-black/10 backdrop-blur-lg
        p-6 md:p-8 lg:p-10 xl:p-12 space-y-4 md:space-y-6 lg:space-y-8 xl:space-y-10
        min-h-[300px] md:min-h-[700px] lg:min-h-[700px] xl:min-h-[700px]"
      >
        <div className="text-center flex flex-col items-center justify-center space-y-4">
          <div className="space-y-1">
            <h2 className="text-xl md:text-2xl font-medium opacity-60">
              {type}
            </h2>
            <h1 className="text-2xl md:text-3xl font-medium">{title}</h1>
          </div>
          <p className="text-sm md:text-base text-blue-100 opacity-75 text-center">
            {description}
          </p>
        </div>

        <div className="flex justify-center my-4 w-full">
          <div className="w-1/2 max-w-[80%]">
            <div className="inset-0 flex items-center justify-center">
              <img
                className="w-full object-cover rounded"
                src={`${API_BASE_URL}/${imageUrl}`}
                alt={title}
              />
            </div>
          </div>
        </div>

        <div
          className="bg-gray-900/70 rounded-3xl p-4 text-white shadow-lg
        flex flex-row items-center gap-4 w-full"
        >
          <div className="text-sm md:text-base">{percentage}%</div>
          <div className="relative bg-gray-400 rounded-full h-[0.7rem] flex-1">
            <div
              className="absolute top-0 left-0 h-full bg-blue-500 rounded-full transition-all"
              style={{ width: `${percentage}%` }}
            />
          </div>
          <div
            className="text-xs md:text-sm bg-gradient-to-r from-[#0096FF80]
          via-[#0096FF] to-[#0096FF80] p-2 md:p-3 rounded-2xl text-center"
          >
            {xpReward} XP
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestCard;
