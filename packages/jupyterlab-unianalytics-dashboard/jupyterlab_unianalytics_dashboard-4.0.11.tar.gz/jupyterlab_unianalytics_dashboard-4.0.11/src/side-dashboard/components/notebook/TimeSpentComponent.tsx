import React, { useEffect, useState } from 'react';
import { ChartData } from 'chart.js';
import { NotebookCell } from '../../../redux/types';
import ChartContainer from './ChartContainer';
import { Scatter } from 'react-chartjs-2';
import { timeSpentOptions } from '../../../utils/chartOptions';
import { useSelector } from 'react-redux';
import { RootState } from '../../../redux/store';
import {
  fetchWithCredentials,
  generateQueryArgsString
} from '../../../utils/utils';
import { BACKEND_API_URL } from '../../..';

const TimeSpentComponent = (props: { notebookId: string }) => {
  const [timeSpentData, setTimeSpentData] = useState<ChartData<'scatter'>>({
    labels: [],
    datasets: []
  });

  const dashboardQueryArgsRedux = useSelector(
    (state: RootState) => state.commondashboard.dashboardQueryArgs
  );
  const refreshRequired = useSelector(
    (state: RootState) => state.commondashboard.refreshBoolean
  );
  const notebookCells = useSelector(
    (state: RootState) => state.commondashboard.notebookCells
  );

  // fetching access time data
  useEffect(() => {
    fetchWithCredentials(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_cell_time?${generateQueryArgsString(dashboardQueryArgsRedux, props.notebookId)}`
    )
      .then(response => response.json())
      .then(data => {
        const chartData: ChartData<'scatter'> = {
          labels: notebookCells
            ? Array.from(
                { length: notebookCells.length },
                (_, index) => index + 1
              )
            : [],
          datasets: [
            {
              label: 'time spent on a cell by a user',
              data:
                notebookCells?.flatMap((cell: NotebookCell, index: number) => {
                  const foundData = data.find(
                    (item: any) => item.cell === cell.id
                  );
                  if (foundData) {
                    return foundData.durations.map((d: number) => ({
                      x: index + 1,
                      y: d
                    }));
                  }
                  return [];
                }) || [],
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
              pointRadius: 1
            }
          ]
        };
        setTimeSpentData(chartData);
      });
  }, [dashboardQueryArgsRedux, refreshRequired]);

  return (
    <ChartContainer
      PassedComponent={
        <Scatter data={timeSpentData} options={timeSpentOptions} />
      }
      title="Amount of time spent on each cell"
    />
  );
};

export default TimeSpentComponent;
