import React, { useEffect, useState } from "react";
import Logo from "../assets/img/navbar-logo.png";
import { NavLink } from "react-router-dom";
import { logout, getCurrentUser } from "../utils/user";
import { Typography, AppBar, Toolbar, Button, Link } from "@mui/material";
import AccountCircle from "@mui/icons-material/AccountCircle";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";

const Navbar = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const getFullName = () => {
    const first = localStorage.getItem("firstName");
    const last = localStorage.getItem("lastName");
    const patr = localStorage.getItem("patronymic");
    return `${last} ${first} ${patr}`;
  };

  useEffect(() => {
    const user = getCurrentUser();
    if (user) setCurrentUser(user);
  }, []);

  return (
    <AppBar position="static" color="transparent" elevation="0">
      <Toolbar>
        <Link href="/">
          <img src={Logo} alt="" />
        </Link>
        <Typography variant="h5" component="div" sx={{ flexGrow: 1, color: "#566885" }}>
          Смарт Клиника
        </Typography>
        {!currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/loginet">
              Войти через
            </NavLink>
          </Button>
        )}
        {!currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/login">
              Войти
            </NavLink>
          </Button>
        )}
        {!currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/registration">
              Регистрация
            </NavLink>
          </Button>
        )}
        {currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/financing">
              Финансирование
            </NavLink>
          </Button>
        )}
        {currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/reviews">
              Отзывы
            </NavLink>
          </Button>
        )}
        {currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/employee_stats">
              О врачах
            </NavLink>
          </Button>
        )}
        {currentUser && (
          <Button>
            <NavLink style={{ color: "#566885" }} to="/patient_stats">
              О пациентах
            </NavLink>
          </Button>
        )}
        {currentUser && (
          <div>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              style={{ color: "#566885" }}
            >
              <AccountCircle />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem>{getFullName()}</MenuItem>
              <MenuItem>{localStorage.getItem("orgName")}</MenuItem>
              <MenuItem onClick={logout}>Выйти</MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
