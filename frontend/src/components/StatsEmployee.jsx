import React, { useState } from "react";
import Search from "./Search";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "../utils/axios-config";
import { getAuthHeader } from "../utils/user";
import Select from "react-select";
import { getPersonFullName, formatDate } from "../utils/common";
import { Box, Stepper, Step, StepLabel, Button, Typography, Grid, Paper } from "@mui/material";
import { TableCell, TableRow, TableContainer, Table, TableHead, TableBody, TablePagination } from "@mui/material";

const StatsEmployee = () => {
  const steps = ["Выберите дату", "Выберите отделение", "Выберите врача", "Выберите тип приема"];

  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [statsRawData, setStatsRawData] = useState([]);
  const [selectedStructure, setSelectedStructure] = useState(null);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [selectedType, setSelectedType] = useState({ label: "Любой", value: "any" });
  const [activeStep, setActiveStep] = React.useState(0);
  const [skipped, setSkipped] = React.useState(new Set());
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const onDatesChange = (dates) => {
    const [start, end] = dates;
    setStartDate(start);
    setEndDate(end);
  };

  const queryStatsData = async () => {
    const queryParams = {
      from_date: formatDate(startDate),
      to_date: formatDate(endDate),
      employee: selectedEmployee?.value,
      status: selectedType.value,
    };

    if (selectedStructure) {
      queryParams.organisation_structure = selectedStructure?.value;
    }

    // http://127.0.0.1:8000/api/patient_appointments/?status=visited&from_date=2021-06-21&to_date=2021-06-21&patient=775332
    const response = await axios.get("/patient_appointments/", {
      params: queryParams,
      headers: getAuthHeader(),
    });
    setStatsRawData(response.data);
    handleNext();
  };

  const onOptionChange = (type, option) => {
    let fn = null;
    switch (type) {
      case "structure":
        fn = setSelectedStructure;
        setSelectedEmployee(null);
        break;
      case "employee":
        fn = setSelectedEmployee;
        break;
      case "type":
        fn = setSelectedType;
        break;
      default:
        throw Error("Unexpected option type");
    }
    fn(option);
  };

  const stringifyEmployeeOption = (option) => {
    const {
      first_name: firstName,
      last_name: lastName,
      patr_name: patrName,
      organisation_structure: { name: orgName },
    } = option;
    return `${lastName} ${firstName} ${patrName}, ${orgName}`;
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const filterType = (statsRawData) => {
    if (selectedType.value === "any") return statsRawData;
    return statsRawData.filter((element) => element.status === selectedType.value);
  };

  const isStepOptional = (step) => {
    return step === 1 || step === 2;
  };

  const isStepSkipped = (step) => {
    return skipped.has(step);
  };

  const handleNext = () => {
    let newSkipped = skipped;
    if (isStepSkipped(activeStep)) {
      newSkipped = new Set(newSkipped.values());
      newSkipped.delete(activeStep);
    }

    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    setSkipped(newSkipped);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleSkip = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    setSkipped((prevSkipped) => {
      const newSkipped = new Set(prevSkipped.values());
      newSkipped.add(activeStep);
      return newSkipped;
    });
  };

  const handleReset = () => {
    setActiveStep(0);
    setSelectedEmployee(null);
    setSelectedStructure(null);
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
            Отображение работы врачей
          </Typography>
          <Stepper activeStep={activeStep} sx={{ mb: "1rem" }}>
            {steps.map((label, index) => {
              const stepProps = {};
              const labelProps = {};
              if (isStepOptional(index)) {
                labelProps.optional = <Typography variant="caption">Опционально</Typography>;
              }
              if (isStepSkipped(index)) {
                stepProps.completed = false;
              }
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
                resourceName="organisation_structures"
                stringifyOption={(o) => o.name}
                onOptionSelect={(option) => onOptionChange("structure", option)}
                value={selectedStructure}
                placeholder="Введите название отделения"
                queryParam="search"
                isClearable={true}
                sendInitialRequest={true}
              />
            </Box>
          )}
          {activeStep === 2 && (
            <Box style={{ width: 800 }}>
              <Search
                resourceName="employees"
                stringifyOption={stringifyEmployeeOption}
                onOptionSelect={(option) => onOptionChange("employee", option)}
                value={selectedEmployee}
                placeholder="Введите ФИО врача"
                extraQueryParams={{ organisation_structure: selectedStructure?.value }}
                isClearable={true}
                sendInitialRequest={!!selectedStructure?.value}
              />
            </Box>
          )}
          {activeStep === 3 && (
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
                onChange={(option) => onOptionChange("type", option)}
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
              {isStepOptional(activeStep) && (
                <Button color="inherit" onClick={handleSkip} sx={{ mr: 1 }}>
                  Пропустить
                </Button>
              )}
              {activeStep === 0 && (
                <Button variant="contained" disabled={!endDate} onClick={handleNext}>
                  Дальше
                </Button>
              )}
              {activeStep === 1 && (
                <Button variant="contained" disabled={!selectedStructure} onClick={handleNext}>
                  Дальше
                </Button>
              )}
              {activeStep === 2 && (
                <Button variant="contained" disabled={!selectedEmployee} onClick={handleNext}>
                  Дальше
                </Button>
              )}
              {activeStep === 3 && (
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

export default StatsEmployee;
