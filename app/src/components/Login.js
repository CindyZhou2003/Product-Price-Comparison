// Login.js
import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container, Link, Snackbar, Alert } from '@mui/material';
import Grid from '@mui/material/Grid2';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import PIcon from '../asserts/Picon.png'
import BgImg from '../asserts/bc.png'
import MobileBgImg from '../asserts/phonebc.png'
import { useNavigate } from 'react-router-dom';
import api from '../api';
import theme from './style'
import {ThemeProvider } from '@mui/material/styles';
// import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: '' });

  // 打开 Snackbar
  const handleSnackbarOpen = (message, severity) => {
    setSnackbar({ open: true, message, severity });
  };

  // 关闭 Snackbar
  const handleSnackbarClose = () => {
    setSnackbar({ open: false, message: '', severity: '' });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // 构建请求数据
    const requestData = {
      username: username,
      password: password,
    };
    // 在这里处理表单提交逻辑，比如表单验证或登录请求
     try {
      const response = await api.post('/login', requestData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
        console.log("Response received:", response);

        if (response.data.status === 'success') {
          // 登录成功（后端已建立 Session），更新登录状态并跳转到主页
          handleSnackbarOpen(`登录成功！`, 'success');
          setIsAuthenticated(true);
          navigate('/home');
        } else {
          handleSnackbarOpen(`登录失败：${response.data.message}`, 'error');
        }
      }catch (error) {
          console.error('登录请求失败:', error);
          handleSnackbarOpen(`登录失败，请稍后重试！`, 'error');
        }

  };

  return (
  <div>
      <ThemeProvider theme={theme}>
        <Box
          sx={{
            backgroundImage: {
              xs: `url(${MobileBgImg})`, // 手机端背景图片
              md: `url(${BgImg})` // 桌面端背景图片
            },
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            width: '100vw',
            minHeight: '100vh',
            display: 'flex',
            flexDirection: { xs: 'column', md: 'row' }, // 改为列布局在小屏幕，行布局在大屏幕
            alignItems: 'center',
            justifyContent: 'center',
            padding: 2, // 添加内边距以适应小屏幕
          }}
        >
        <Box
            sx={{
            position: 'relative', // 或 absolute
            top: { xs: '0px', sm: '-120px' }, // 小屏幕时调整位置
            left: { xs: '0px', sm: '150px' },
            textAlign: 'center', // 小屏幕居中
            display: 'inline-block',
            background: 'linear-gradient(to right, purple, orange)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            // lineHeight: 2, // 设置行高，避免文字被截断
            overflow: 'visible', // 确保内容可见
            marginBottom: { xs: 4, md: 0 }, // 小屏幕标题与输入框之间增加间距
            }}
            >
            <Typography
              component="h1"
              variant="h1"
              sx={{
                lineHeight: 2, // 设置文字的行高
                // color: 'primary.main', // 使用主题的 primary 颜色
                  fontSize: { xs: '2rem', sm: '3rem', md: '4rem' }, // 响应式字号
              }}
            >
              Price Pilot
            </Typography>
        </Box>
          <Container component="main" maxWidth="xs" sx={{ padding: { xs: 2, sm: 4 } }}>
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
              <Avatar sx={{ m: 1, bgcolor: 'transparent',
                  width: { xs: 80, sm: 120 },
                  height: { xs: 80, sm: 120 } }}>
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
                <Grid container sx={{ mt: 2 }} justifyContent="space-between">
                  <Grid item xs={6} sx={{ textAlign: 'left' }}>
                    <Link href="#" variant="body2" onClick={() => navigate('/forgot_password')} sx={{ fontSize: { xs: '0.8rem', sm: '0.9rem' } }}>
                      {"忘记密码?"}
                    </Link>
                  </Grid>
                  <Grid item xs={6} sx={{ textAlign: 'right' }}>
                    <Link href="#" variant="body2" onClick={() => navigate('/register')} sx={{ fontSize: { xs: '0.8rem', sm: '0.9rem' } }}>
                      {"还没有账号？注册新账号"}
                    </Link>
                  </Grid>
                </Grid>
              </Box>
            </Box>
          </Container>
        </Box>
      </ThemeProvider>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000} // 3秒后自动关闭
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }} // 提示位置
      >
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
  </div>
  );
}

export default Login;
