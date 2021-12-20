import React, { useState } from "react";
import Input from "../utils/Input";
import axios from "../utils/axios-config";
import { Grid, Paper, Avatar, Button, Typography, Link, Alert } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { setDataToLocalstorage } from "../utils/user";

const Registration = () => {
  const [first_name, setFirstname] = useState("");
  const [patronymic, setPatronymic] = useState("");
  const [last_name, setLast_name] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const paperStyle = { padding: 40, width: 400, margin: "40px auto" };

  const register = async () => {
    try {
      const response = await axios.post(`register/`, {
        first_name,
        patronymic,
        last_name,
        username,
        password,
      });
      setDataToLocalstorage(response.data);

      window.location.href = "/login";
    } catch (e) {
      setError("Заполните все поля");
      e.response.data.password && setError(e.response.data.password);
      e.response.data.username && setError(e.response.data.username);
      console.log(error);
    }
  };

  return (
    <Grid>
      <Paper elevation="10" style={paperStyle}>
        <Grid align="center">
          <Typography variant="h5" sx={{ mb: "1rem" }}>
            Регистрация
          </Typography>
          <Avatar sx={{ bgcolor: "#566885" }}>
            <PersonIcon />
          </Avatar>
        </Grid>
        <Input value={last_name} setValue={setLast_name} label="Фамилия" placeholder="Введите фамилию" />
        <Input value={first_name} setValue={setFirstname} label="Имя" placeholder="Введите имя" />
        <Input value={patronymic} setValue={setPatronymic} label="Отчество" placeholder="Введите отчество" />
        <Input value={username} setValue={setUsername} label="Логин" placeholder="Введите логин" />
        <Input value={password} setValue={setPassword} label="Пароль" placeholder="Введите пароль" type="password" />
        {error && (
          <Alert severity="error" sx={{ mb: "1rem" }}>
            {error}
          </Alert>
        )}
        <Button
          type="submit"
          color="primary"
          variant="contained"
          onClick={() => register()}
          fullWidth
          size="large"
          sx={{ mb: "1rem" }}
        >
          Зарегистрироваться{" "}
        </Button>
        <Grid align="center">
          <Typography> Уже есть аккаунт?</Typography>
          <Typography>
            {" "}
            <Link href="/login">Войдите</Link>
          </Typography>
        </Grid>
      </Paper>
    </Grid>
  );
};

export default Registration;
