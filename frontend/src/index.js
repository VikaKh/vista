import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import { Auth0Provider } from "@auth0/auth0-react";
import {ThemeProvider, createTheme} from "@mui/material"

const theme = createTheme({
  palette : {
    primary: {
        main: '#566885'
  }},
  secondary: {
    main: '#00ff00'
}
});

ReactDOM.render(
    <ThemeProvider theme={theme}>
      <Auth0Provider
    domain="dev-r3x70wdq.us.auth0.com"
    clientId="stLY9t6TsYxnE60u6Z05KZmMieP68YMD"
    redirectUri={window.location.origin}
  >
    <App />
    </Auth0Provider>
    </ThemeProvider>,
  document.getElementById('root')
);


