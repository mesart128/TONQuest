import { useEffect, useLayoutEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUser } from '../store/slices/userSlice';
import { useNavigate } from 'react-router-dom';
import {
  useTonConnectModal,
  useTonConnectUI,
  useTonAddress,
} from '@tonconnect/ui-react';
import { setUserAddress } from '../api/Router';
import { checkBranchById } from '../store/slices/branchSlice';
import { getConnectWalletTask } from '../utils';
import { checkTaskById, claimTaskById } from '../store/slices/taskSlice';

const ConnectWalletHandler = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const rawAddress = useTonAddress(false);
  const categories = useSelector((state) => state.category.list);
  const { user, status, error } = useSelector((state) => state.user);

  useEffect(() => {
    if (rawAddress && !user.wallet_address) {
      setUserAddress(rawAddress).then(async () => {
        dispatch(fetchUser());
        const connectWalletTask = getConnectWalletTask(categories);
        if (connectWalletTask) {
          const taskCompleted = await dispatch(checkTaskById(connectWalletTask.id)).unwrap();
          if (!taskCompleted) {
            return;
          }
          const taskClaimed = await dispatch(claimTaskById(connectWalletTask.id)).unwrap();
          if (!taskClaimed) {
            return;
          }
          const branchCompleted = await dispatch(checkBranchById(connectWalletTask.branch_id)).unwrap();
          if (!branchCompleted) {
            return;
          }
          navigate('/congratulations');
        }
        else {
          console.log('no connect wallet task');
        }
      });
    }
  }, [rawAddress]);


  return <></>;
};
export default ConnectWalletHandler;
