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
import { getCategories, getCategoryById } from '../../api/Router';
export const fetchCategories = createAsyncThunk('categories/fetchCategories', (_1, _a) => __awaiter(void 0, [_1, _a], void 0, function* (_, { rejectWithValue }) {
    try {
        return yield getCategories();
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const fetchCategoryById = createAsyncThunk('categories/fetchCategoryById', (categoryId_1, _a) => __awaiter(void 0, [categoryId_1, _a], void 0, function* (categoryId, { rejectWithValue }) {
    try {
        return yield getCategoryById(categoryId);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
const categorySlice = createSlice({
    name: 'categories',
    initialState: {
        list: [],
        selectedCategory: null,
        status: 'idle',
        error: null,
    },
    reducers: {
        clearSelectedCategory(state) {
            state.selectedCategory = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchCategories.pending, (state) => {
            state.status = 'loading';
            state.error = null;
        })
            .addCase(fetchCategories.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.list = action.payload;
        })
            .addCase(fetchCategories.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.payload;
        })
            .addCase(fetchCategoryById.pending, (state) => {
            state.status = 'loading';
            state.error = null;
        })
            .addCase(fetchCategoryById.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.selectedCategory = action.payload;
        })
            .addCase(fetchCategoryById.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.payload;
        });
    },
});
export const { clearSelectedCategory } = categorySlice.actions;
export default categorySlice.reducer;
