import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getTask, claimTask, completeTask, checkTask } from '../../api/Router';

export const fetchTask = createAsyncThunk(
  'task/fetchTask',
  async (taskId, { rejectWithValue }) => {
    try {
      return await getTask(taskId);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

export const completeTaskById = createAsyncThunk(
  'task/completeTask',
  async (taskId, { rejectWithValue }) => {
    try {
      return await completeTask(taskId);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

export const claimTaskById = createAsyncThunk(
  'task/claimTask',
  async (taskId, { rejectWithValue }) => {
    try {
      return await claimTask(taskId);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

export const checkTaskById = createAsyncThunk(
  'task/checkTask',
  async (taskId, { rejectWithValue }) => {
    try {
      return await checkTask(taskId);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

const taskSlice = createSlice({
  name: 'task',
  initialState: {
    tasks: {},
    branch: {},
    status: 'idle',
    error: null,
    activeTask: null,
  },
  reducers: {
    setActiveTask: (state, action) => {
      state.activeTask = action.payload;
    },
    setBranch: (state, action) => {
      state.branch = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTask.fulfilled, (state, action) => {
        state.tasks[action.payload.id] = action.payload;
      })
      .addCase(claimTaskById.fulfilled, (state, action) => {
        const task = state.tasks[action.meta.arg];
        if (task) task.claimed = true;
      })
      .addCase(completeTaskById.fulfilled, (state, action) => {
        if (action.payload?.branchId === state.branch.id) {
          state.branch.completed = true;
        }
      })
      .addCase(checkTaskById.fulfilled, (state, action) => {
        const task = state.tasks[action.meta.arg];
        if (task) task.checked = action.payload.checked;
        state.status = 'succeeded';
      })
      .addCase(checkTaskById.rejected, (state, action) => {
        state.error = action.payload;
        state.status = 'failed';
      });
  },
});

export const { setActiveTask, setBranch } = taskSlice.actions;

export default taskSlice.reducer;
