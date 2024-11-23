import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { claimPiece } from '../../api/Router';

export const claimPieceById = createAsyncThunk(
    'piece/claimPieceById',
    async (pieceId, { rejectWithValue }) => {
      try {
        const response = await claimPiece(pieceId);
        return response;
      } catch (error) {
        return rejectWithValue(error.message);
      }
    }
  );
  
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
  