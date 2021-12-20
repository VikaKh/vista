import React, { useState } from "react";
import Search from "./Search";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "../utils/axios-config";
import { getAuthHeader } from "../utils/user";
import { getPersonFullName, formatDate } from "../utils/common";
import Select from "react-select";
import { Box, Stepper, Step, StepLabel, Button, Typography, Grid, Paper } from "@mui/material";
import { TableCell, TableRow, TableContainer, Table, TableHead, TableBody, TablePagination } from "@mui/material";

const StatsPatient = () => {
  const steps = ["Выберите дату", "Выберите пациента", "Выберите тип приема"];

  const [selectedPatient, setSelectedPatient] = useState(null);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [statsRawData, setStatsRawData] = useState([]);
  const [selectedType, setSelectedType] = useState({ label: "Любой", value: "any" });
  const [activeStep, setActiveStep] = React.useState(0);
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const onDatesChange = (dates) => {
    const [start, end] = dates;
    setStartDate(start);
    setEndDate(end);
  };

  const queryStatsData = async () => {
    const queryParams = { from_date: formatDate(startDate), to_date: formatDate(endDate) };
    if (selectedPatient) {
      queryParams.patient = selectedPatient?.value;
    }
    // http://127.0.0.1:8000/api/patient_appointments/?status=visited&from_date=2021-06-21&to_date=2021-06-21&patient=775332
    const response = await axios.get("/patient_appointments/", {
      params: queryParams,
      headers: getAuthHeader(),
    });
    setStatsRawData(response.data);
    handleNext();
  };

  const stringifyPatientOption = (option) => {
    const { first_name: firstName, last_name: lastName, patr_name: patrName, birth_date: birthDate } = option;
    return `${lastName} ${firstName} ${patrName}, ${birthDate}`;
  };

  const filterType = (statsRawData) => {
    if (selectedType.value === "any") return statsRawData;
    return Object.values(statsRawData).filter((element) => element.status === selectedType.value);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setSelectedPatient(null);
  };

  function NormalStatus(stat) {
    const statuses = {
      'visited': 'посещен',
      'missed': 'пропущен',
      'scheduled': 'запланирован',
    };
    return statuses[stat.toLowerCase()] ?? "not found";
  }
  var options = {weekday: 'short', year:'numeric', month:'long', day:'numeric', hour:'numeric', minute:'numeric', second:'numeric'};

  return (
    <div>
      <Grid align="center" sx={{ mb: "1rem" }}>
        <Paper elevation="10" style={{ padding: 20 }}>
          <Typography variant="h5" sx={{ mb: "1rem" }}>
            Отображение информации о пациентах
          </Typography>
          <Stepper activeStep={activeStep} sx={{ mb: "1rem" }}>
            {steps.map((label, index) => {
              const stepProps = {};
              const labelProps = {};
              return (
                <Step key={label} {...stepProps}>
                  <StepLabel {...labelProps}>{label}</StepLabel>
                </Step>
              );
            })}
          </Stepper>
          {activeStep === 0 && (
            <Box style={{ width: 800 }}>
              <Typography>Выберите необходимые даты</Typography>
              <DatePicker
                selected={startDate}
                onChange={onDatesChange}
                startDate={startDate}
                endDate={endDate}
                selectsRange
              />
            </Box>
          )}
          {activeStep === 1 && (
            <Box style={{ width: 800 }}>
              <Search
                resourceName="patients"
                stringifyOption={stringifyPatientOption}
                onOptionSelect={setSelectedPatient}
                placeholder="Введите ФИО пацента"
              />
            </Box>
          )}
          {activeStep === 2 && (
            <Box style={{ width: 800 }}>
              <Select
                options={[
                  { value: "missed", label: "Пропущен" },
                  { value: "visited", label: "Посещен" },
                  { value: "any", label: "Любой" },
                  { value: "scheduled", label: "Запланирован" },
                ]}
                placeholder="Выберите тип приема"
                value={selectedType}
                onChange={(selectedType) => setSelectedType(selectedType)}
                isClearable
                sx={{ mb: "1rem" }}
              />
            </Box>
          )}
          {activeStep === steps.length && (
            <div>
              <Typography> По вашему запросу найдено {filterType(statsRawData).length} результатов</Typography>
              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Пациент</TableCell>
                      <TableCell align="right">Дата приема</TableCell>
                      <TableCell align="right">Врач</TableCell>
                      <TableCell align="right">Тип приема</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {" "}
                    {filterType(statsRawData)
                      .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                      .map((data) => (
                        <TableRow key={data.type} sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
                          <TableCell component="th" scope="row">
                            {getPersonFullName(data.patient)}
                          </TableCell>
                          <TableCell align="right">{(new Date(data.start_at)).toLocaleDateString("ru-ru", options)}</TableCell>
                          <TableCell align="right">{getPersonFullName(data.employee)}</TableCell>
                          <TableCell align="right">{NormalStatus(data.status)}</TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </TableContainer>
              <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={filterType(statsRawData).length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </div>
          )}
          {activeStep === steps.length ? (
            <Box style={{ width: 800 }} sx={{ flexDirection: "center" }}>
              <Button onClick={handleReset}>Заново</Button>
            </Box>
          ) : (
            <Box style={{ width: 800 }} sx={{ display: "flex", flexDirection: "row", pt: 2 }}>
              <Button color="inherit" disabled={activeStep === 0} onClick={handleBack} sx={{ mr: 1 }}>
                {" "}
                Назад{" "}
              </Button>
              <Box sx={{ flex: "1 1 auto" }} />
              {activeStep === 0 && (
                <Button variant="contained" disabled={!endDate} onClick={handleNext}>
                  Дальше
                </Button>
              )}
              {activeStep === 1 && (
                <Button variant="contained" disabled={!setSelectedPatient} onClick={handleNext}>
                  Дальше
                </Button>
              )}
              {activeStep === 2 && (
                <Button
                  variant="contained"
                  onClick={() => {
                    queryStatsData();
                  }}
                >
                  Поиск
                </Button>
              )}
            </Box>
          )}
        </Paper>
      </Grid>
    </div>
  );
};

export default StatsPatient;
