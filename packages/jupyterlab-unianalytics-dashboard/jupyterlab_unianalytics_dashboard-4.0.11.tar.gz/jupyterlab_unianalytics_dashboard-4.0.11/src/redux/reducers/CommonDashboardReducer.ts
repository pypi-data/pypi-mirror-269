import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { NotebookCell, CommonDashboardState } from '../types';
import { areListsEqual } from '../../utils/utils';

export const initialCommonDashboardState: CommonDashboardState = {
  notebookCells: null,
  refreshBoolean: false,
  sortBy: {},
  dashboardQueryArgs: {
    displayRealTime: {},
    t1ISOString: {},
    selectedGroups: {}
  }
};

export const commonDashboardSlice = createSlice({
  name: 'commondashboard',
  initialState: initialCommonDashboardState,
  reducers: {
    setDashboardQueryArgsTimeFilter: (
      state,
      action: PayloadAction<{ notebookId: string; t1ISOString: string | null }>
    ) => {
      const { notebookId, t1ISOString } = action.payload;
      state.dashboardQueryArgs.t1ISOString[notebookId] = t1ISOString;
    },
    setDashboardQueryArgsSelectedGroups: (
      state,
      action: PayloadAction<{
        notebookId: string;
        groups: string[];
      }>
    ) => {
      const { notebookId, groups } = action.payload;
      const currentGroups =
        state.dashboardQueryArgs.selectedGroups[notebookId] || [];

      // check if the new value is different from the current one
      if (!areListsEqual(currentGroups, groups)) {
        // return immutable-friendly state modification
        return {
          ...state,
          dashboardQueryArgs: {
            ...state.dashboardQueryArgs,
            selectedGroups: {
              ...state.dashboardQueryArgs.selectedGroups,
              [notebookId]: groups
            }
          }
        };
      }
    },
    setDashboardQueryArgsDisplayRealTime: (
      state,
      action: PayloadAction<{ notebookId: string; displayRealTime: boolean }>
    ) => {
      const { notebookId, displayRealTime } = action.payload;
      state.dashboardQueryArgs.displayRealTime[notebookId] = displayRealTime;
    },
    setSortBy: (
      state,
      action: PayloadAction<{ notebookId: string; sortCriterion: string }>
    ) => {
      const { notebookId, sortCriterion } = action.payload;
      state.sortBy[notebookId] = sortCriterion;
    },
    setNotebookCells: (state, action: PayloadAction<NotebookCell[] | null>) => {
      state.notebookCells = action.payload;
    },
    refreshDashboards: state => {
      state.refreshBoolean = !state.refreshBoolean;
    }
  }
});

export const {
  setDashboardQueryArgsTimeFilter,
  setDashboardQueryArgsSelectedGroups,
  setDashboardQueryArgsDisplayRealTime,
  setSortBy,
  setNotebookCells,
  refreshDashboards
} = commonDashboardSlice.actions;

export default commonDashboardSlice.reducer;
