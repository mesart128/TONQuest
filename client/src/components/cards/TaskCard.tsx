import React, { useEffect, useState } from 'react';
import GradientButton from '../buttons/GradientButton';
import { useSelector, useDispatch } from 'react-redux';
import { claimTaskById, checkTaskById } from '../../store/slices/taskSlice';
import { toast } from 'react-toastify';
import { completeBranchById, checkBranchById } from '../../store/slices/branchSlice';
import { claimPieceById } from '../../store/slices/pieceSlice';
import { fetchUser } from '../../store/slices/userSlice';

const TaskCard = ({ part, title, xp, status, actionURL, callToAction, onTaskComplete }) => {
  const dispatch = useDispatch();
  const { branch, error, activeTask } = useSelector((state) => state.branch);
  const { imageUrl, description, type, branches } = useSelector(
    (state) => state.selectedCard,
  );

  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [earnedXP, setEarnedXP] = useState(0);
  const [localStatus, setLocalStatus] = useState(status);

  useEffect(() => {
    setLocalStatus(status);
  }, [status]);

  const areAllTasksCompleted = () => {
    if (!branch?.tasks?.length) {
      return false;
    }
    return branch.tasks.every(task => task.status === 'claimed' || task.completed);
  };

  const refreshTaskState = async () => {
    try {
      const branchCheck = await dispatch(checkBranchById(branch.id)).unwrap();
      console.log(`branchId: ${branch.id}`);
      if (areAllTasksCompleted()) {
        setLocalStatus('claimed');
        setShowSuccessModal(true);
      }
      
      if (onTaskComplete) {
        onTaskComplete();
      }
    } catch (error) {
      console.error('Error refreshing task state:', error);
    }
  };
  
  const validateTaskCompletion = async (taskId) => {
    try {
      const taskCheck = await dispatch(checkTaskById(taskId)).unwrap();
      console.log(`taskId: ${taskId}`);
      if (!taskCheck?.completed) {
        toast.error("Task is not completed.");
        return false;
      }
    
      const taskClaim = await dispatch(claimTaskById(taskId)).unwrap();
      if (!taskClaim?.success) {
        toast.error("Error claiming task.");
        return false;
      }
      
      toast.success("Task successfully claimed");
      setLocalStatus('claimed');
      
      await refreshTaskState();
      
      return true;
    } catch (error) {
      console.error('Error in validateTaskCompletion:', error);
      return false;
    }
  };
  
  const validateBranchCompletion = async (branchId) => {
    if (!areAllTasksCompleted()) {
      return false;
    }

    try {
      const branchCheck = await dispatch(checkBranchById(branchId)).unwrap();

      if (!branchCheck?.completed) {
        toast.error("Branch is not completed.");
        return false;
      }
    
      const branchCompletion = await dispatch(completeBranchById(branchId)).unwrap();
      if (!branchCompletion.success) {
        toast.error("Error occurred.");
        return false;
      }
    
      await refreshTaskState();
      return true;
    } catch (error) {
      console.error('Error in validateBranchCompletion:', error);
      return false;
    }
  };
  
  const claimReward = async (pieceId) => {
    try {
      const pieceClaim = await dispatch(claimPieceById(pieceId)).unwrap();
      if (!pieceClaim?.success) {
        toast.error("Failed to claim the piece.");
        return false;
      }
      
      setEarnedXP(xp);
      setShowSuccessModal(true);
      await dispatch(fetchUser());
      return true;
    } catch (error) {
      console.error('Error in claimReward:', error);
      return false;
    }
  };

  const checkIsCompleted = async () => {
    try {
      if (!activeTask?.id) {
        toast.error("No active task found.");
        return;
      }

      const isTaskCompleted = await validateTaskCompletion(activeTask.id);
      if (!isTaskCompleted) return;

      if (areAllTasksCompleted()) {
        const isBranchCompleted = await validateBranchCompletion(branch.id);
        if (!isBranchCompleted) return;
    
        const isRewardClaimed = await claimReward(branch.pieces[0].id);
        if (!isRewardClaimed) return;

        setLocalStatus('claimed');
      }
    } catch (error) {
      toast.error(typeof error === 'string' ? error : 'An error occurred');
    }
  };

  return (
    <div className="w-full max-w-md">
      {localStatus === 'blocked' ? (
        <div className="bg-gray-800 text-white p-4 rounded-lg mb-4 relative overflow-hidden">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Part {part}</span>
            <span className="text-sm bg-gray-700 rounded-full px-2 py-1">
              +{xp} XP
            </span>
          </div>
          <h3 className="text-lg font-bold mb-4">
            Unlock after the {part - 1} task
          </h3>
          <div className="absolute inset-0 flex justify-center items-center backdrop-blur bg-black/30">
            <div className="bg-black/50 p-3 rounded-full">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="2"
                stroke="currentColor"
                className="w-8 h-8 text-gray-300"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 15v.01M12 9a1.5 1.5 0 100 3 1.5 1.5 0 100-3zm0 6.75c.38.56.62 1.2.7 1.89.11.81.09 1.61-.06 2.36a.75.75 0 01-.64.51h-.08a.75.75 0 01-.64-.51c-.15-.75-.17-1.55-.06-2.36.08-.69.32-1.33.7-1.89zm0 0c-.38-.56-.62-1.2-.7-1.89-.11-.81-.09-1.61.06-2.36a.75.75 0 01.64-.51h.08a.75.75 0 01.64.51c.15.75.17 1.55.06 2.36-.08.69-.32 1.33-.7-1.89z"
                />
              </svg>
            </div>
          </div>
        </div>
      ) : localStatus === 'active' ? (
        <div className="bg-gradient-to-r from-[#003E6B] via-[#004F8C] to-[#003E6B] text-white p-4 rounded-lg mb-4 shadow-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Part {part}</span>
            <span className="text-sm bg-blue-500 rounded-full px-2 py-1">
              +{xp} XP
            </span>
          </div>
          <h3 className="text-lg font-bold mb-4">{title}</h3>
          <GradientButton
            blocked={false}
            children="Check the execution"
            onClick={checkIsCompleted}
          />
        </div>
      ) : localStatus === 'claimed' ? (
        <div className="bg-gray-500 from-[#003E6B] via-[#004F8C] to-[#003E6B] text-white p-4 rounded-lg mb-4 shadow-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Part {part}</span>
            <span className="text-sm bg-blue-500 rounded-full px-2 py-1">
              +{xp} XP
            </span>
          </div>
          <h3 className="text-lg font-bold mb-4">{title}</h3>
          <GradientButton
            blocked={true}
            children="Check the execution"
            onClick={checkIsCompleted}
          />
        </div>
      ) : (
        <></>
      )}
      {showSuccessModal && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-gradient-to-b from-blue-900 to-black p-8 rounded-lg text-white text-center max-w-md w-full mx-4">
            <button 
              onClick={() => setShowSuccessModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <h2 className="text-2xl font-bold mb-2">The task is completed</h2>
            
            <div className="my-8">
              <img 
                src="/path-to-your-target-icon.svg" 
                alt="Target" 
                className="w-24 h-24 mx-auto"
              />
            </div>

            <p className="text-gray-300 mb-6">
              You have learned how to change one token to another, keep it up!
            </p>

            <div className="inline-flex items-center bg-opacity-20 bg-blue-500 rounded-full px-4 py-2 mb-8">
              <svg className="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M..." />
              </svg>
              +{earnedXP} XP
            </div>

            <button
              onClick={() => setShowSuccessModal(false)}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-full py-3 transition-colors"
            >
              Ready to move on
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskCard;