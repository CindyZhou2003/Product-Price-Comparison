import { createTheme } from '@mui/material/styles';

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
      main: '#c84153',
      dark: '#a03442',
      contrastText: '#fff',
    },
    background: {
      default: '#f8d3c9'  // 设置全局背景颜色
    }
  },

  typography: {
    fontFamily: `'Noto Serif SC', serif`,

    h5:{
      fontFamily:`'ZCOOL XiaoWei',sans-serif`,
      fontWeight:500
    },

    h4:{
      fontFamily:`'Ma Shan Zheng', cursive`,
      fontWeight: 600,
    },

    body1:{
      fontFamily: `'Noto Serif SC', serif`,
      fontSize: '1rem'
    },

    body2:{
      fontFamily:`'ZCOOL XiaoWei',sans-serif`,
      fontSize: '1rem'
    },
  },
});

export default theme;