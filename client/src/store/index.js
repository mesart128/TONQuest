import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import taskReducer from './slices/taskSlice';
import categoryReducer from './slices/categorySlice';
import branchReducer from './slices/branchSlice';
import selectedCardReducer from './slices/selectedCardSlice';
import nftReducer from './slices/nftSlice.ts';
// const store = configureStore({
//   reducer: {
//     user: userReducer,
//     task: taskReducer,
//     category: categoryReducer,
//     branch: branchReducer,
//     selectedCard: selectedCardReducer,
//     nft: nftReducer,
//   },
import pieceReducer from './slices/pieceSlice';
import storage from 'redux-persist/lib/storage';
import { persistStore, persistReducer } from 'redux-persist';
import { combineReducers } from 'redux';
const persistConfig = {
    key: 'root',
    storage,
};
const rootReducer = combineReducers({
    user: userReducer,
    task: taskReducer,
    category: categoryReducer,
    branch: branchReducer,
    selectedCard: selectedCardReducer,
    piece: pieceReducer,
    nft: nftReducer,
});
const persistedReducer = persistReducer(persistConfig, rootReducer);
export const store = configureStore({
    reducer: persistedReducer,
});
export const persistor = persistStore(store);
