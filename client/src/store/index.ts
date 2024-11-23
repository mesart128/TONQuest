import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import taskReducer from './slices/taskSlice';
import categoryReducer from './slices/categorySlice';
import branchReducer from './slices/branchSlice';
import selectedCardReducer from './slices/selectedCardSlice';

const store = configureStore({
  reducer: {
    user: userReducer,
    task: taskReducer,
    category: categoryReducer,
    branch: branchReducer,
    selectedCard: selectedCardReducer,
  },
});

export default store;
