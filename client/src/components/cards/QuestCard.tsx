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
    <div className="max-w-sm mx-auto flex mb-16" onClick={cardSelectHandler}>
      <div
        className="rounded-3xl flex flex-col justify-around  p-6 text-white
      border border-solid border-[#0096FF] shadow-2xl relative overflow-hidden min-h-[500px]"
      >
        <div className="text-center mb-8 flex flex-col items-center justify-center space-y-4">
          <div className="space-y-1">
            <h2 className="text-4xl font-bold opacity-50">{type}</h2>
            <h1 className="text-3xl font-bold">{title}</h1>
          </div>
          <p className="text-xl text-blue-100 opacity-75">{description}</p>
        </div>

        <div className="flex justify-center mb-8">
          <div className="relative w-24 h-24">
            <div className="absolute inset-0 flex items-center justify-center">
              <img
                className="w-full max-h-48 object-cover rounded"
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
