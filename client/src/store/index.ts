import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import taskReducer from './slices/taskSlice';
import categoryReducer from './slices/categorySlice';

const store = configureStore({
  reducer: {
    user: userReducer,
    task: taskReducer,
    category: categoryReducer,
  },
});

export default store;