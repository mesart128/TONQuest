import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import taskReducer from './slices/taskSlice';
import categoryReducer from './slices/categorySlice';
import branchReducer from './slices/branchSlice';

const store = configureStore({
  reducer: {
    user: userReducer,
    task: taskReducer,
    category: categoryReducer,
    branch: branchReducer,
  },
});

export default store;
