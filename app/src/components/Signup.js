// src/components/SignUp.js
import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container, Link } from '@mui/material';
import Grid from '@mui/material/Grid2';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import { useNavigate } from 'react-router-dom';
import BgImg from '../img/background.jpg'
import PIcon from "../img/picon.png";

function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    // 在这里处理表单提交逻辑，比如表单验证或注册请求
    if (password !== confirmPassword) {
      alert("两次输入的密码不一致!");
      return;
    }
    console.log('Username:', username);
    console.log('Email:', email);
    console.log('Password:', password);
    // 进一步处理注册逻辑，例如调用API
  };

  return (
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
            <img src={PIcon} alt="Login Icon" style={{ width: '100%', height: '100%' }} />
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
            helperText="密码必须包含至少6个字符"
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
            登录
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
  );
}

export default SignUp;
