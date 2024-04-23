import React, { useState } from 'react';
import {
  Dropdown,
  Button,
  ButtonGroup,
  ToggleButton,
  Form
} from 'react-bootstrap';
import { CalendarWeek as TimeLogo } from 'react-bootstrap-icons';
import { store, AppDispatch, RootState } from '../../../redux/store';
import {
  setDashboardQueryArgsDisplayRealTime,
  setDashboardQueryArgsTimeFilter
} from '../../../redux/reducers/CommonDashboardReducer';
import { InteractionRecorder } from '../../../utils/interactionRecorder';
import { DashboardClickOrigin } from '../../../utils/interfaces';
import { convertToLocaleString } from '../../../toc-dashboard/ExportCSVButton';
import { useSelector } from 'react-redux';

const dispatch = store.dispatch as AppDispatch;

const RadioTimeFilterValues = [
  { value: 1, displayName: 'All Data', disabledDatePicker: true },
  {
    value: 2,
    displayName: 'From t<sub>1</sub>',
    disabledDatePicker: false
  }
];

const TimeDropDown = (props: { notebookId: string }): JSX.Element => {
  const queryArgsRedux = useSelector(
    (state: RootState) => state.commondashboard.dashboardQueryArgs
  );

  // compute the initial values for the component states from the redux stored values
  const computeRadioValue = () => {
    const index = queryArgsRedux.t1ISOString[props.notebookId] ? 1 : 0;
    return RadioTimeFilterValues[index];
  };

  const computeT1 = (): Date => {
    const t1FromRedux = queryArgsRedux.t1ISOString[props.notebookId];
    if (t1FromRedux) {
      return new Date(t1FromRedux);
    } else {
      return new Date();
    }
  };

  const computeRealTimeValue = (): boolean => {
    // by default, set to true
    if (queryArgsRedux.displayRealTime[props.notebookId] === undefined) {
      return true;
    } else {
      return queryArgsRedux.displayRealTime[props.notebookId];
    }
  };

  const [radioFilterValue, setRadioFilterValue] = useState(computeRadioValue());

  const [t1, setT1] = useState<Date>(computeT1());

  const [realTimeChecked, setRealTimeChecked] =
    useState<boolean>(computeRealTimeValue);

  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  const currentDateString = convertToLocaleString(new Date());

  const handleOK = () => {
    dispatch(
      setDashboardQueryArgsTimeFilter({
        notebookId: props.notebookId,
        t1ISOString: radioFilterValue.disabledDatePicker
          ? null
          : t1.toISOString()
      })
    );
    dispatch(
      setDashboardQueryArgsDisplayRealTime({
        notebookId: props.notebookId,
        displayRealTime: realTimeChecked
      })
    );
    InteractionRecorder.sendInteraction({
      // if value === 1 => including all data, therefore sending OFF interaction signal
      click_type: radioFilterValue.value === 1 ? 'OFF' : 'ON',
      signal_origin: DashboardClickOrigin.DASHBOARD_FILTER_TIME
    });
    toggleMenu();
  };

  const handleCancel = () => {
    toggleMenu();
  };

  const toggleMenu = () => {
    if (!showDropdown) {
      // opening with either current date or with previously selected dates
      setT1(computeT1());
      setRadioFilterValue(computeRadioValue());
      setRealTimeChecked(computeRealTimeValue());
    }
    setShowDropdown(!showDropdown);
  };

  return (
    <Dropdown
      show={showDropdown}
      onToggle={toggleMenu}
      className="custom-dropdown"
    >
      <Dropdown.Toggle className="dashboard-button">
        <TimeLogo className="dashboard-icon" />
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Header>Data Timeframe Selector</Dropdown.Header>
        <Dropdown.Divider />

        <div className="custom-dropdown-container custom-dropdown-item">
          <Form.Check
            id="time-checkbox-include-all"
            type="checkbox"
            label="Only show active users"
            checked={realTimeChecked}
            onChange={e => setRealTimeChecked(e.target.checked)}
          />
        </div>

        <Dropdown.Divider />

        <div className="dashboard-calendar-container">
          <div className="cell-radio-container">
            <ButtonGroup size="sm">
              {RadioTimeFilterValues.map((radioValue, idx) => (
                <ToggleButton
                  key={`calendar-filter-${idx}`}
                  id={`calendar-filter-${idx}`}
                  type="radio"
                  variant="outline-primary"
                  name="radio"
                  value={radioValue.value}
                  checked={radioFilterValue.value === radioValue.value}
                  onChange={(e: any) => {
                    setRadioFilterValue(
                      RadioTimeFilterValues[Number(e.currentTarget.value) - 1]
                    );
                  }}
                >
                  <span
                    dangerouslySetInnerHTML={{ __html: radioValue.displayName }}
                  />
                </ToggleButton>
              ))}
            </ButtonGroup>
          </div>
        </div>
        <div className="dashboard-calendar-container">
          <div
            className={`dashboard-calendar-input-wrapper ${radioFilterValue.disabledDatePicker ? 'disabled' : ''}`}
          >
            <div>
              t<sub>1</sub>
            </div>
            <input
              className="dashboard-calendar-input"
              type="datetime-local"
              value={convertToLocaleString(t1)}
              onChange={e => setT1(new Date(e.target.value))}
              max={currentDateString}
            />
          </div>
        </div>
        <div className="dashboard-calendar-button-container">
          <Button variant="secondary" onClick={handleCancel}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleOK}>
            Ok
          </Button>
        </div>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default TimeDropDown;
