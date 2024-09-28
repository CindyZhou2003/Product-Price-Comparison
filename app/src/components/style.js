import { createTheme } from '@mui/material/styles';
import Register from "./Register";

const theme = createTheme({
  palette: {
    secondary: {
      light: '#ffd7db',
      main: '#ffcdd2',
      dark: '#b28f93',
      contrastText: '#000',
    },
    primary: {
      light: '#f27573',
      main: '#ef5350',
      dark: '#a73a38',
      contrastText: '#fff',
    },
  },
});

export default theme;