import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getBranchById } from '../../api/Router';

export const fetchBranchById = createAsyncThunk(
  'branch/fetchBranchById',
  async (branchId, { rejectWithValue }) => {
    try {
      return await getBranchById(branchId);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

const branchSlice = createSlice({
  name: 'branch',
  initialState: {
    branch: null,
    tasks: [],
    status: 'idle',
    error: null,
  },
  reducers: {
    clearBranchState(state) {
      state.branch = null;
      state.tasks = [];
      state.status = 'idle';
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchBranchById.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchBranchById.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.branch = action.payload;
        state.tasks = action.payload.tasks || [];
      })
      .addCase(fetchBranchById.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  },
});

export const { clearBranchState } = branchSlice.actions;
export default branchSlice.reducer;
