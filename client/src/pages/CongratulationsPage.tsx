import { useLocation, useNavigate } from 'react-router-dom';
import icon from '../assets/greeting-logo.png';
import { useDispatch } from 'react-redux';
import ConfettiExplosion from 'react-confetti-explosion';
import { useEffect, useState } from 'react';
import { mainButton } from '@telegram-apps/sdk-react';
import { Page } from '../Page';
import { useSelector } from 'react-redux';
import { API_BASE_URL } from '../api/Router';

const CongratulationsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { totalXP = 0, resetBranchCompletion } = location.state || {};
  const { branch, error, activeTask } = useSelector((state) => state.branch);
  const [isConfetti, setIsConfetti] = useState(false);
  const handleClose = () => {
    navigate('/tasks-page');
  };

  useEffect(() => {
    mainButton.setParams({
      isVisible: true,
      text: 'Go to your NFT pieces',
    });
    return mainButton.onClick(() => {
      navigate('/nft');
    });
  }, []);

  useEffect(() => {
    setIsConfetti(true);
  }, []);

  return (
    <Page back={false}>
      <div className="bg-transparent p-8 text-white text-center w-[100vw] min-h-screen flex items-center">
        <div className="bg-[#0096FF] w-full h-2/5 rounded-full absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[100px]"></div>
        <div className="absolute top-[50%] left-[50%]">
          {isConfetti && (
            <ConfettiExplosion
              force={0.9}
              width={1000}
              colors={['#45EBA5', '#21ABA5', '#163A5F', '#1D566E']}
              particleSize={6}
              particleCount={250}
              onComplete={() => {
                setIsConfetti(false);
              }}
            />
          )}
        </div>
        <div className="z-10 p-4 flex flex-col items-center">
          <div className="my-8">
            {branch?.pieces[0]?.image && (
              <img
                src={`${API_BASE_URL}/${branch?.pieces[0]?.image}`}
                alt="Target"
                className="w-24 h-24 mx-auto"
              />
            )}
          </div>

          <h2 className="text-2xl font-bold mb-2">Congratulations!</h2>

          <p className="text-gray-300 mb-6">
            You have learned how to change one token to another, keep it up!
          </p>

          <div className="text-sm backdrop-blur-lg bg-black/10 border border-white/60 rounded-xl p-2 w-fit flex justify-center">
            <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M3.46794 0.833314H11.5322C11.9715 0.833299 12.3504 0.833287 12.6626 0.85879C12.992 0.885707 13.3197 0.945137 13.635 1.1058C14.1054 1.34548 14.4879 1.72793 14.7276 2.19834C14.8882 2.51366 14.9477 2.84134 14.9746 3.17079C15.0001 3.48293 15.0001 3.86189 15.0001 4.30118L15.0001 4.95668C15.0003 5.24552 15.0005 5.50031 14.949 5.75129C14.9037 5.97194 14.8288 6.18547 14.7264 6.38606C14.6098 6.61422 14.4505 6.81306 14.2698 7.03847L11.2306 10.8374C12.9858 12.8007 12.9208 15.8169 11.0355 17.7022C9.08292 19.6548 5.91709 19.6548 3.96446 17.7022C2.07918 15.8169 2.01417 12.8006 3.76943 10.8373L0.730276 7.03845C0.549658 6.81305 0.390334 6.61422 0.273772 6.38606C0.171291 6.18547 0.0963914 5.97194 0.0511053 5.75129C-0.000403207 5.50031 -0.000200053 5.24552 3.04179e-05 4.95668L6.07169e-05 4.3012C4.58158e-05 3.86191 3.29611e-05 3.48293 0.025536 3.17079C0.0524535 2.84134 0.111883 2.51366 0.272545 2.19834C0.512229 1.72793 0.89468 1.34548 1.36509 1.1058C1.6804 0.945137 2.00808 0.885707 2.33754 0.85879C2.64967 0.833287 3.02867 0.833299 3.46794 0.833314ZM7.50004 8.64267L11.4358 3.58245C11.7043 3.23718 11.8386 3.06455 11.8373 2.91961C11.8363 2.79352 11.7782 2.6747 11.6793 2.59645C11.5656 2.50649 11.3469 2.50649 10.9095 2.50649L4.09055 2.50649C3.65314 2.50649 3.43444 2.50649 3.32079 2.59645C3.22192 2.6747 3.16381 2.79352 3.16274 2.91961C3.1615 3.06455 3.29577 3.23718 3.56431 3.58245L7.50004 8.64267Z"
                fill="white"
              />
            </svg>
            + NFT PIECE
          </div>
        </div>
        {/* <button 
            onClick={handleClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-white"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
            <ConfettiExplosion force={0.85} width={1000} colors={['#45EBA5', '#21ABA5', '#163A5F', '#1D566E']} particleSize={9} particleCount={400}/>
            
          </button> */}

        {/* <button
            onClick={handleClose}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-full py-3 transition-colors"
          >
            Ready to move on
          </button> */}
      </div>
    </Page>
  );
};

export default CongratulationsPage;
