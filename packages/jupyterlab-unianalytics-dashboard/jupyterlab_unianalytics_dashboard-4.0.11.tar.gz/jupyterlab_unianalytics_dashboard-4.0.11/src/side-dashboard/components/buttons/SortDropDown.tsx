import React from 'react';
import { Dropdown } from 'react-bootstrap';
import { SortUp as SortLogo } from 'react-bootstrap-icons';
import { InteractionRecorder } from '../../../utils/interactionRecorder';
import { DashboardClickOrigin } from '../../../utils/interfaces';
import { store, AppDispatch, RootState } from '../../../redux/store';
import { setSortBy } from '../../../redux/reducers/CommonDashboardReducer';
import { DropdownSortingValues } from '../../../utils/constants';
import { useSelector } from 'react-redux';

const dispatch = store.dispatch as AppDispatch;

const SortDropDown = (props: { notebookId: string }): JSX.Element => {
  const sortByCriterionRedux: string | undefined = useSelector(
    (state: RootState) => state.commondashboard.sortBy[props.notebookId]
  );

  return (
    <Dropdown
      id="order-by-dropdown"
      onSelect={eventKey => {
        if (eventKey) {
          InteractionRecorder.sendInteraction({
            click_type: 'ON',
            signal_origin: DashboardClickOrigin.CELL_DASHBOARD_FILTER_SORT
          });
          dispatch(
            setSortBy({
              notebookId: props.notebookId,
              sortCriterion: eventKey
            })
          );
        }
      }}
      className="custom-dropdown"
    >
      <Dropdown.Toggle className="dashboard-button">
        <SortLogo className="dashboard-icon" />
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Header>Sort cells by</Dropdown.Header>
        <Dropdown.Divider />
        {DropdownSortingValues.map(
          (sortingValue: { key: string; label: string }, index: number) => {
            return (
              <Dropdown.Item
                id={`sort-item-${index}`}
                eventKey={sortingValue.key}
                className={`${sortByCriterionRedux && sortByCriterionRedux === sortingValue.key ? 'highlighted' : ''}`}
              >
                {sortingValue.label}
              </Dropdown.Item>
            );
          }
        )}
        {/* <Dropdown.Item eventKey="timeDesc">
          Time (most recent 1st)
        </Dropdown.Item>
        <Dropdown.Item eventKey="timeAsc">Time (oldest 1st)</Dropdown.Item>
        <Dropdown.Item eventKey="inputAsc">Input (shortest 1st)</Dropdown.Item>
        <Dropdown.Item eventKey="inputDesc">Input (longest 1st)</Dropdown.Item>
        <Dropdown.Item eventKey="outputAsc">
          Output (shortest 1st)
        </Dropdown.Item>
        <Dropdown.Item eventKey="outputDesc">
          Output (longest 1st)
        </Dropdown.Item> */}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default SortDropDown;
