import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getBranchById } from '../../api/Router';
import { completeBranch } from '../../api/Router';
import { checkBranch } from '../../api/Router';

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

export const completeBranchById = createAsyncThunk(
    'branch/completeBranchById',
    async (branchId, { rejectWithValue }) => {
      try {
        return await completeBranch(branchId);
      } catch (error) {
        return rejectWithValue(error.message);
      }
    },
  );

  export const checkBranchById = createAsyncThunk(
    'branch/checkBranchById',
    async (branchId, { rejectWithValue }) => {
      try {
        return await checkBranch(branchId);
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
    activeTask: null,
    error: null,
    currentSlideIndex: 0,
    isBranchChecked: false,
    branchCompleted: false,
  },
  reducers: {
    clearBranchState(state) {
      state.branch = null;
      state.tasks = [];
      state.status = 'idle';
      state.error = null;
      state.isBranchChecked = false;
    },
    setActiveTask: (state, action) => {
      state.activeTask = action.payload;
    },
    setCurrentSlide: (state, action) => {
      state.currentSlideIndex = action.payload;
    },
    setBranchCompleted(state, action) {
        state.branchCompleted = action.payload;
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
        state.activeTask = action.payload.tasks?.find(
          (task) => task.status === 'active',
        );
      })
      .addCase(fetchBranchById.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(completeBranchById.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(completeBranchById.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.branch = { ...state.branch, status: 'completed' };
      })
      .addCase(completeBranchById.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(checkBranchById.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(checkBranchById.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.isBranchChecked = action.payload.completed;
      })
      .addCase(checkBranchById.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  },
});

export const { clearBranchState, setActiveTask, setCurrentSlide, setBranchCompleted } =
  branchSlice.actions;
export default branchSlice.reducer;
