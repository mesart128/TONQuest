import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getUser, setUserAddress } from '../../api/Router';

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (_, { rejectWithValue }) => {
    try {
      return await getUser();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

export const updateUserAddress = createAsyncThunk(
  'user/updateAddress',
  async (address, { rejectWithValue }) => {
    try {
      return await setUserAddress(address);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

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
        state.user = { ...state.user, address: action.payload };
      });
  },
});

export default userSlice.reducer;
