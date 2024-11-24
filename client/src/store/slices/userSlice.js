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
import { getUser, setUserAddress } from '../../api/Router';
export const fetchUser = createAsyncThunk('user/fetchUser', (_1, _a) => __awaiter(void 0, [_1, _a], void 0, function* (_, { rejectWithValue }) {
    try {
        return yield getUser();
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
export const updateUserAddress = createAsyncThunk('user/updateAddress', (address_1, _a) => __awaiter(void 0, [address_1, _a], void 0, function* (address, { rejectWithValue }) {
    try {
        return yield setUserAddress(address);
    }
    catch (error) {
        return rejectWithValue(error.message);
    }
}));
const userSlice = createSlice({
    name: 'user',
    initialState: {
        user: null,
        status: 'idle',
        error: null,
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchUser.pending, (state) => {
            state.status = 'loading';
        })
            .addCase(fetchUser.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.user = action.payload;
        })
            .addCase(fetchUser.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.payload;
        })
            .addCase(updateUserAddress.fulfilled, (state, action) => {
            state.user = Object.assign(Object.assign({}, state.user), { address: action.payload });
        });
    },
});
export default userSlice.reducer;
