var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { getNft } from "../../api/Router.ts";
export const fetchNft = createAsyncThunk('nft', (_1, _a) => __awaiter(void 0, [_1, _a], void 0, function* (_, { rejectWithValue }) {
    try {
        return yield getNft();
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
const initialState = {
    cards: [],
    nft: {},
};
const nftCardSlice = createSlice({
    name: 'nftCard',
    initialState,
    reducers: {
        setNftCard: (state, action) => {
            return Object.assign(Object.assign({}, state), action.payload);
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
