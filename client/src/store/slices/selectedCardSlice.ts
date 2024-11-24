import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  imageUrl: '',
  description: '',
  title: '',
  type: '',
  branches: [],
};

const selectedCardSlice = createSlice({
  name: 'selectedCard',
  initialState,
  reducers: {
    setSelectedCard: (state, action) => {
      return { ...state, ...action.payload };
    },
    clearSelectedCard: () => initialState,
  },
});

export const { setSelectedCard, clearSelectedCard } = selectedCardSlice.actions;
export default selectedCardSlice.reducer;
