import { configureStore } from '@reduxjs/toolkit';
import ToCDashboardReducer from './reducers/ToCDashboardReducer';
import SideDashboardReducer from './reducers/SideDashboardReducer';
import CommonDashboard, {
  initialCommonDashboardState
} from './reducers/CommonDashboardReducer';
import { STORAGE_KEY } from '../utils/constants';
import { localStorageMiddleware } from './localStorage';

const preloadedState = {
  // if commondashboard is already defined in localStorage, use it as part of the initial state
  commondashboard: localStorage.getItem(STORAGE_KEY)
    ? JSON.parse(localStorage.getItem(STORAGE_KEY) as string)
    : initialCommonDashboardState
};

export const store = configureStore({
  reducer: {
    tocdashboard: ToCDashboardReducer,
    sidedashboard: SideDashboardReducer,
    commondashboard: CommonDashboard
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware().concat(localStorageMiddleware),
  preloadedState: preloadedState
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
