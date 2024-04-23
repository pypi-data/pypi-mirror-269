import React, { useEffect, useState } from 'react';
import { Dropdown, Form, Button } from 'react-bootstrap';
import { PeopleFill as GroupLogo } from 'react-bootstrap-icons';
// import { InteractionRecorder } from '../../../utils/interactionRecorder';
// import { DashboardClickOrigin } from '../../../utils/interfaces';
import { fetchWithCredentials } from '../../../utils/utils';
import { AppDispatch, RootState, store } from '../../../redux/store';
import { setDashboardQueryArgsSelectedGroups } from '../../../redux/reducers/CommonDashboardReducer';
import { useSelector } from 'react-redux';
import { BACKEND_API_URL } from '../../..';

const dispatch = store.dispatch as AppDispatch;

const GroupDropDown = (props: { notebookId: string }): JSX.Element => {
  const [showDropdown, setShowDropdown] = useState(false);

  const [groupList, setGroupList] = useState<
    { name: string; checked: boolean }[]
  >([]);

  const selectedGroupNamesRedux: string[] | undefined = useSelector(
    (state: RootState) =>
      state.commondashboard.dashboardQueryArgs.selectedGroups[props.notebookId]
  );

  // if no group name is already selected, check the include-all checkbox
  const [includeAllChecked, setIncludeAllChecked] = useState(
    selectedGroupNamesRedux === undefined ||
      selectedGroupNamesRedux.length === 0
  );

  // fetch the group names
  useEffect(() => {
    fetchWithCredentials(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/getgroups`
    )
      .then(response => response.json())
      .then((data: string[]) => {
        const updatedGroupList = data
          .map(name => ({
            name,
            checked: selectedGroupNamesRedux?.includes(name) // check if name exists in selectedGroupNames
          }))
          .sort((a, b) => {
            if (a.checked !== b.checked) {
              return b.checked ? 1 : -1; // checked items first
            }

            // if checked status is the same, sort alphabetically by name
            return a.name.localeCompare(b.name);
          }); // sort checked groups first
        setGroupList(updatedGroupList);
      });
  }, []);

  const resetOpeningStates = () => {
    // check the includeAll checkbox in case there's no selected group
    setIncludeAllChecked(
      selectedGroupNamesRedux === undefined ||
        selectedGroupNamesRedux.length === 0
    );
    const updatedGroupList = groupList
      .map((value: { name: string; checked: boolean }) => ({
        name: value.name,
        checked: selectedGroupNamesRedux?.includes(value.name) // check if name exists in selectedGroupNames
      }))
      .sort((a, b) => {
        if (a.checked !== b.checked) {
          return b.checked ? 1 : -1; // checked items first
        }

        // if checked status is the same, sort alphabetically by name
        return a.name.localeCompare(b.name);
      });
    setGroupList(updatedGroupList);
  };

  const handleOK = () => {
    let checkedGroups: string[];
    if (includeAllChecked) {
      checkedGroups = [];
    } else {
      checkedGroups = groupList
        .filter(group => group.checked === true)
        .map(group => group.name);
    }
    dispatch(
      setDashboardQueryArgsSelectedGroups({
        notebookId: props.notebookId,
        groups: checkedGroups
      })
    );
    toggleMenu();
  };

  const handleCancel = () => {
    toggleMenu();
  };

  const toggleMenu = () => {
    if (!showDropdown) {
      // opening the dropdown with the correct states
      resetOpeningStates();
    }
    setShowDropdown(!showDropdown);
  };

  const handleToggleGroup = (index: number) => {
    setGroupList(prevGroupList => {
      // create a copy of the previous group list array
      const newGroupList = [...prevGroupList];

      // toggle the checked value of the group at the specified index
      newGroupList[index] = {
        ...newGroupList[index],
        checked: !newGroupList[index].checked
      };

      return newGroupList;
    });
  };

  return (
    <Dropdown
      id="group-dropdown"
      className="custom-dropdown"
      show={showDropdown}
      onToggle={toggleMenu}
    >
      <Dropdown.Toggle className="dashboard-button">
        <GroupLogo className="dashboard-icon" />
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Header>Filter by group of users</Dropdown.Header>
        <Dropdown.Divider />

        <div className="custom-dropdown-container custom-dropdown-item">
          <Form.Check
            id="group-checkbox-include-all"
            type="checkbox"
            label="Include all users"
            checked={includeAllChecked}
            onChange={e => setIncludeAllChecked(e.target.checked)}
          />
        </div>

        <Dropdown.Divider />

        <div
          className={`group-dropdown-scroll ${includeAllChecked ? 'disabled' : ''}`}
        >
          {groupList.length > 0 ? (
            groupList.map((value, index) => (
              <div
                className={`custom-dropdown-item ${includeAllChecked ? 'disabled' : ''}`}
              >
                <Form.Check
                  id={`group-checkbox-${index}`}
                  type="checkbox"
                  disabled={includeAllChecked ? true : undefined}
                  label={value.name}
                  title={value.name}
                  checked={value.checked}
                  onChange={() => handleToggleGroup(index)}
                />
              </div>
            ))
          ) : (
            <Dropdown.Item disabled>No groups available</Dropdown.Item>
          )}
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

export default GroupDropDown;
