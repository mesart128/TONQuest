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
import { getBranchById } from '../../api/Router';
import { completeBranch } from '../../api/Router';
import { checkBranch } from '../../api/Router';
export const fetchBranchById = createAsyncThunk('branch/fetchBranchById', (branchId_1, _a) => __awaiter(void 0, [branchId_1, _a], void 0, function* (branchId, { rejectWithValue }) {
    try {
        return yield getBranchById(branchId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const completeBranchById = createAsyncThunk('branch/completeBranchById', (branchId_1, _a) => __awaiter(void 0, [branchId_1, _a], void 0, function* (branchId, { rejectWithValue }) {
    try {
        return yield completeBranch(branchId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const checkBranchById = createAsyncThunk('branch/checkBranchById', (branchId_1, _a) => __awaiter(void 0, [branchId_1, _a], void 0, function* (branchId, { rejectWithValue }) {
    try {
        return yield checkBranch(branchId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
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
            var _a;
            state.status = 'succeeded';
            state.branch = action.payload;
            state.tasks = action.payload.tasks || [];
            state.activeTask = (_a = action.payload.tasks) === null || _a === void 0 ? void 0 : _a.find((task) => task.status === 'active');
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
            state.branch = Object.assign(Object.assign({}, state.branch), { status: 'completed' });
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
export const { clearBranchState, setActiveTask, setCurrentSlide, setBranchCompleted } = branchSlice.actions;
export default branchSlice.reducer;
