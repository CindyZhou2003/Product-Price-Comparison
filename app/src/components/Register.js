// src/components/Register.js
import { useState } from 'react';
import { TextField, Button, Box, Typography, Container, Link } from '@mui/material';
import Grid from '@mui/material/Grid2';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import { useNavigate } from 'react-router-dom';
import BgImg from '../img/background.jpg'
import PIcon2 from "../img/picon2.png";
import axios from "axios";
import theme from './style'
import {ThemeProvider } from '@mui/material/styles';


function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  // 注册提交处理函数
  const handleSubmit = async (event) => {
    event.preventDefault();
    // 检查密码是否一致
    if (password !== confirmPassword) {
      alert("两次输入的密码不一致!");
      return;
    }
    // 检查表单字段是否为空
    if (!username || !email || !password) {
      alert("请填写所有必填字段！");
      return;
    }

    // 构建请求数据
    const requestData = {
      username: username,
      email: email,
      password: password,
    };

    // 使用axios发送POST请求到后端注册接口
    try {
      const response = await axios.post('http://127.0.0.1:8000/backend/register', requestData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // 处理响应结果
      if (response.data.status === 'ok') {
        alert('注册成功！');
        navigate('/login');  // 注册成功后跳转到登录页面
      } else {
        alert(`注册失败：${response.data.message}`);
      }
    } catch (error) {
      console.error('注册请求失败:', error);
      alert('注册失败，请稍后重试！');
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
              backdropFilter: 'blur(10px)',
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              borderRadius: 2,
              padding: 4,
              boxShadow: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main', width: 80, height: 80 }}>
                <img src={PIcon2} alt="Login Icon" style={{ width: '100%', height: '100%' }} />
              </Avatar>
            <Typography component="h1" variant="h5">
              注册界面
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
                id="email"
                label="请输入邮件地址"
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                helperText="我们不会将您的邮件泄露给其他人"
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
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                helperText="密码必须包含至少6个字符，字母和数字都要有"
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="confirmPassword"
                label="确认密码"
                type="password"
                id="confirmPassword"
                autoComplete="new-password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                helperText="请重新输入密码"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                注册
              </Button>
              <Grid container justifyContent="flex-end">
                <Grid item>
                  <Link href="#" variant="body2" onClick={() => navigate('/')}>
                      {"已经有账号？直接登录"}
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

export default Register;
