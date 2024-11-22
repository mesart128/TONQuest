import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getTask, claimTask, completeTask } from '../../api/Router';

export const fetchTask = createAsyncThunk('task/fetchTask', async (taskId, { rejectWithValue }) => {
  try {
    return await getTask(taskId);
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

export const claimTaskById = createAsyncThunk('task/claimTask', async (taskId, { rejectWithValue }) => {
  try {
    return await claimTask(taskId);
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const taskSlice = createSlice({
  name: 'task',
  initialState: {
    tasks: {},
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTask.fulfilled, (state, action) => {
        state.tasks[action.payload.id] = action.payload;
      })
      .addCase(claimTaskById.fulfilled, (state, action) => {
        const task = state.tasks[action.meta.arg];
        if (task) task.claimed = true;
      });
  },
});

export default taskSlice.reducer;
