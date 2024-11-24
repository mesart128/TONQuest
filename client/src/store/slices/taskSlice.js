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
import { getTask, claimTask, completeTask, checkTask } from '../../api/Router';
export const fetchTask = createAsyncThunk('task/fetchTask', (taskId_1, _a) => __awaiter(void 0, [taskId_1, _a], void 0, function* (taskId, { rejectWithValue }) {
    try {
        return yield getTask(taskId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const completeTaskById = createAsyncThunk('task/completeTask', (taskId_1, _a) => __awaiter(void 0, [taskId_1, _a], void 0, function* (taskId, { rejectWithValue }) {
    try {
        return yield completeTask(taskId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const claimTaskById = createAsyncThunk('task/claimTask', (taskId_1, _a) => __awaiter(void 0, [taskId_1, _a], void 0, function* (taskId, { rejectWithValue }) {
    try {
        return yield claimTask(taskId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const checkTaskById = createAsyncThunk('task/checkTask', (taskId_1, _a) => __awaiter(void 0, [taskId_1, _a], void 0, function* (taskId, { rejectWithValue }) {
    try {
        return yield checkTask(taskId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
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
            if (task)
                task.claimed = true;
        })
            .addCase(completeTaskById.fulfilled, (state, action) => {
            var _a;
            if (((_a = action.payload) === null || _a === void 0 ? void 0 : _a.branchId) === state.branch.id) {
                state.branch.completed = true;
            }
        })
            .addCase(checkTaskById.fulfilled, (state, action) => {
            const task = state.tasks[action.meta.arg];
            if (task)
                task.checked = action.payload.checked;
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
