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
  nft: [],
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
      .addCase(fetchNft.pending, (state) => {
        state.cards = a;
        state.error = null;
      });
  },

});

export const { setNftCard, clearNftCard } = nftCardSlice.actions;
export default nftCardSlice.reducer;
