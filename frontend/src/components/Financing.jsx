import React, { useState } from "react";
import { Pie } from "react-chartjs-2";
import axios from "../utils/axios-config";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { getAuthHeader } from "../utils/user";
import { Button, Typography, Box, Grid, Paper } from "@mui/material";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { formatDate } from "../utils/common";

ChartJS.register(ArcElement, Tooltip, Legend);

export function Financing() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [Labels, setLabels] = useState([]);
  const [TotalCount, setTotalCount] = useState([]);

  const onDatesChange = (dates) => {
    const [start, end] = dates;
    setStartDate(start);
    setEndDate(end);
  };

  const queryStatsData = async () => {
    const queryParams = {
      from_datetime: formatDate(startDate) + "T00:00:00",
      to_datetime: formatDate(endDate) + "T23:59:59",
    };
    const response = await axios.get("/financing_sources/", {
      params: queryParams,
      headers: getAuthHeader(),
    });
    setLabels(response.data.map((el) => el.name));
    setTotalCount(response.data.map((el) => el.total_count));
  };

  const data = {
    labels: Labels,
    datasets: [
      {
        data: TotalCount,
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <Grid align="center" sx={{ mb: "1rem" }}>
      <Paper elevation="10" style={{ padding: 20, width: 450 }}>
        <Typography variant="h5" sx={{ mb: "1rem" }}>
          Типы финансирования
        </Typography>
        <Typography>Выберите необходимый временной промежуток</Typography>
        <DatePicker
          selected={startDate}
          onChange={onDatesChange}
          startDate={startDate}
          endDate={endDate}
          selectsRange
        />
        <Button
          variant="contained"
          sx={{ mt: "1rem" }}
          onClick={() => {
            queryStatsData();
          }}
        >
          Поиск
        </Button>
      </Paper>
      <Box style={{ width: 600 }} sx={{ mt: "1rem" }}>
        <Pie data={data} />
      </Box>
    </Grid>
  );
}

export default Financing;
