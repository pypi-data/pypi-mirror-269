import { MiddlewareAPI, Dispatch, AnyAction } from '@reduxjs/toolkit';
import { STORAGE_KEY } from '../utils/constants';

export const localStorageMiddleware =
  (store: MiddlewareAPI) => (next: Dispatch) => (action: AnyAction) => {
    const result = next(action);
    // regexp: only execute the middleware logic for actions with type starting with 'commondashboard/'
    if (action.type.startsWith('commondashboard/')) {
      const state = store.getState();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.commondashboard));
    }
    return result;
  };
