// Login.js
import { useState } from 'react';
import { TextField, Button, Box, Typography, Container, Link } from '@mui/material';
import Grid from '@mui/material/Grid2';
// import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import PIcon from '../img/picon2.png'
import BgImg from '../img/background.jpg'
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import theme from './style'
import {ThemeProvider } from '@mui/material/styles';


function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();


  const handleSubmit = async (event) => {
    event.preventDefault();
    // 构建请求数据
    const requestData = {
      username: username,
      password: password,
    };
    console.log("Submitting request with:", requestData);
    // 在这里处理表单提交逻辑，比如表单验证或登录请求
     try {
      const response = await axios.post('http://127.0.0.1:8000/backend/login', requestData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
        console.log("Response received:", response);

        if (response.data.status === 'ok') {
          // 登录成功，更新登录状态并跳转到主页
          const userId = response.data.user_id;
          console.log("User ID received:", userId);

          // 将 user_id 存储在 localStorage 中
          localStorage.setItem('user_id', userId);

          alert('登录成功！');
          setIsAuthenticated(true);
          navigate('/home');
        } else {
          alert(`登录失败：${response.data.message}`);
        }
      }catch (error) {
          console.error('登录请求失败:', error);
          alert('登录失败，请稍后重试！');
        }

  };

  return (
      <ThemeProvider theme={theme}>
        <Box
          sx={{
            backgroundImage: `url(${BgImg})`,
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            width: '100vw',
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
              sx={{
                backdropFilter: 'blur(10px)', // Blurred background effect
                backgroundColor: 'rgba(255, 255, 255, 0.8)', // Semi-transparent white background
                borderRadius: 2,
                padding: 4,
                boxShadow: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Avatar sx={{ m: 1, bgcolor: 'secondary.main', width: 120, height: 120 }}>
                <img src={PIcon} alt="Login Icon" style={{ width: '100%', height: '100%' }} />
              </Avatar>
              <Typography component="h1" variant="h4">
                商品比价网站
              </Typography>
              <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  id="username"
                  label="请输入用户名"
                  name="username"
                  autoComplete="username"
                  autoFocus
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="请输入密码"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                  type="submit"
                  fullWidth
                  sx={{ mt: 3, mb: 2 }}
                  variant="contained" color="primary"
                >
                  登录
                </Button>
                <Grid container>
                  <Grid item xs>
                    <Link href="#" variant="body2">
                      {"忘记密码?"}
                    </Link>
                  </Grid>
                  <Grid item offset={{ md: 'auto' }}>
                    <Link href="#" variant="body2" onClick={() => navigate('/register')}>
                      {"还没有账号？注册新账号"}
                    </Link>
                  </Grid>
                </Grid>
              </Box>
            </Box>
          </Container>
        </Box>
      </ThemeProvider>
  );
}

export default Login;
