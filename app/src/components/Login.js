// src/components/Login.js
import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container, Link } from '@mui/material';
import Grid from '@mui/material/Grid2';
// import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import PIcon from '../img/picon.png'
import BgImg from '../img/background.jpg'
import { useNavigate } from 'react-router-dom';


function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    // 在这里处理表单提交逻辑，比如表单验证或登录请求
    console.log('Email:', email);
    console.log('Password:', password);

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
              id="email"
              label="请输入邮件地址"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
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
                <Link href="#" variant="body2" onClick={() => navigate('/signup')}>
                  {"还没有账号？注册新账号"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}

export default Login;
