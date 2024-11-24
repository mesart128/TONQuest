var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { claimPiece } from '../../api/Router';
export const claimPieceById = createAsyncThunk('piece/claimPieceById', (pieceId_1, _a) => __awaiter(void 0, [pieceId_1, _a], void 0, function* (pieceId, { rejectWithValue }) {
    try {
        const response = yield claimPiece(pieceId);
        return response;
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
const pieceSlice = createSlice({
    name: 'piece',
    initialState: {
        status: 'idle',
        error: null,
        claimedPiece: null,
    },
    reducers: {
        resetPieceState: (state) => {
            state.status = 'idle';
            state.error = null;
            state.claimedPiece = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(claimPieceById.pending, (state) => {
            state.status = 'loading';
            state.error = null;
        })
            .addCase(claimPieceById.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.claimedPiece = action.payload;
        })
            .addCase(claimPieceById.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.payload;
        });
    },
});
export const { resetPieceState } = pieceSlice.actions;
export default pieceSlice.reducer;
