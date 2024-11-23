import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import {getNft} from "../../api/Router.ts";
import {fetchCategories, fetchCategoryById} from "./categorySlice.ts";


export const fetchNft = createAsyncThunk(
    'nft',
    async (_, { rejectWithValue }) => {
        try {
        return await getNft();
        } catch (error) {
        return rejectWithValue(error.message);
        }
    },
    );

const initialState = {
  cards: [],
  nft: {},
};

const nftCardSlice = createSlice({
  name: 'nftCard',
  initialState,
  reducers: {
    setNftCard: (state, action) => {
      return { ...state, ...action.payload };
    },
    clearNftCard: () => initialState,
  },
    extraReducers: (builder) => {
    builder
      .addCase(fetchNft.fulfilled, (state, action) => {
        state.cards = action.payload.cards;
        state.nft = action.payload.nft[0];
      });
  },

});

export const { setNftCard, clearNftCard } = nftCardSlice.actions;
export default nftCardSlice.reducer;
