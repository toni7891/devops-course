# Add Redux Slice

Create a Redux Toolkit slice for: $ARGUMENTS

Read these files before generating code to match exact patterns:
- `Client/src/redux/slices/userSlice.ts` (slice + async thunk pattern)
- `Client/src/redux/store.ts` (store configuration)
- `Client/src/redux/hooks.ts` (typed hooks)

## Steps

### 1. Create slice in `Client/src/redux/slices/<feature>Slice.ts`

```typescript
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Types
interface <Feature>State {
  <feature>: I<Feature> | null;  // or I<Feature>[]
  loading: boolean;
  error: string | null;
}

const initialState: <Feature>State = {
  <feature>: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetch<Feature> = createAsyncThunk(
  "<feature>/fetch<Feature>",
  async (payload: <PayloadType>, { rejectWithValue }) => {
    try {
      // API call using service functions
      return data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || "Failed to fetch");
    }
  }
);

// Slice
const <feature>Slice = createSlice({
  name: "<feature>",
  initialState,
  reducers: {
    set<Feature>: (state, action) => { state.<feature> = action.payload; },
    setLoading: (state, action) => { state.loading = action.payload; },
    setError: (state, action) => { state.error = action.payload; },
    clearError: (state) => { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetch<Feature>.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetch<Feature>.fulfilled, (state, action) => {
        state.loading = false;
        state.<feature> = action.payload;
      })
      .addCase(fetch<Feature>.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { set<Feature>, setLoading, setError, clearError } = <feature>Slice.actions;
export default <feature>Slice.reducer;
```

### 2. Register in store at `Client/src/redux/store.ts`
- Import the reducer: `import <feature>Reducer from "./slices/<feature>Slice"`
- Add to `configureStore({ reducer: { ..., <feature>: <feature>Reducer } })`

### 3. Usage in components
```typescript
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import { fetch<Feature> } from "@/redux/slices/<feature>Slice";

const { <feature>, loading, error } = useAppSelector((state) => state.<feature>);
const dispatch = useAppDispatch();
dispatch(fetch<Feature>(payload));
```

## When to use Redux vs TanStack Query
- **Redux**: Global app state that many components share (current user, theme, permissions)
- **TanStack Query**: Server data fetching with caching (lists, detail views, search results)
- Use `/add-service` command for TanStack Query approach instead
