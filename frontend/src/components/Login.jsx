import React, { useState } from "react";
import Input from "../utils/Input";
import axios from "../utils/axios-config";
import { Grid, Paper, Avatar, Button, Typography, Link, Alert } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { setDataToLocalstorage } from "../utils/user";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const paperStyle = { padding: 20, width: 350, margin: "20px auto" };

  const login = async () => {
    try {
      const response = await axios.post(`login/`, {
        username,
        password,
      });
      setDataToLocalstorage(response.data);
      window.location.href = "/employee_stats";
    } catch (e) {
      setError("Заполните все поля");
      e.response.data.non_field_errors && setError(e.response.data.non_field_errors);
    }
  };

  return (
    <Grid>
      <Paper elevation="10" style={paperStyle}>
        <Grid align="center">
          <Typography variant="h5" sx={{ mb: "1rem" }}>
            Войти
          </Typography>
          <Avatar sx={{ bgcolor: "#566885" }}>
            <PersonIcon />
          </Avatar>
        </Grid>
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
          onClick={() => login()}
          fullWidth
          size="large"
          sx={{ mb: "1rem" }}
        >
          Войти
        </Button>
        <Grid align="center">
          <Typography> Нет аккаунта?</Typography>
          <Typography>
            <Link href="/registration">Зарегистрироваться</Link>
          </Typography>
        </Grid>
      </Paper>
    </Grid>
  );
};

export default Login;
