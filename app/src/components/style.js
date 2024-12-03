import { createTheme } from '@mui/material/styles';
/*字体：Roboto  Lato  Oswald  Ma Shan Zheng  Noto Serif SC  ZCOOL XiaoWei*/
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
    fontFamily: `'Noto Serif SC', serif`, // 默认字体

    h1:{
      fontFamily:'Perfect',
      fontWeight:400,

    },
    h2:{
      fontFamily:'Arizonia-Regular-OTF',
    },
    h3:{
      fontFamily: `'Elrotex',serif`,
      fontWeight:400
    },

    h4:{
      fontFamily:`'Ma Shan Zheng', cursive`,
      fontWeight: 500,
    },

    h5:{
      fontFamily:`'ZCOOL XiaoWei',sans-serif`,
      fontWeight:400
    },

    h6:{
      fontFamily:'TanukiMagic',
      fontWeight:400,
      fontSize:35,
    },

    body1:{
      fontFamily: `'Noto Serif SC', serif`,
      fontSize: '1.2rem'
    },

    body2:{
      fontFamily:`'Noto Serif SC', serif`,
      fontSize: '1rem'
    },
    subtitle1:{

    },
    subtitle2:{

    },
  },
});

export default theme;