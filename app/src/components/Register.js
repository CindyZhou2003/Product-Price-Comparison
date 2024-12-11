// src/components/Register.js
import React, { useState } from 'react';
import {TextField, Button, Box, Typography, Container, Link, InputAdornment, IconButton} from '@mui/material';
import Grid from '@mui/material/Grid2';
import CssBaseline from '@mui/material/CssBaseline';
import { useNavigate } from 'react-router-dom';
import BgImg from '../asserts/img/bc2.png'
import MobileBgImg from '../asserts/img/phonebc.png'
import axios from "axios";
import theme from './style'
import {ThemeProvider } from '@mui/material/styles';
import { Visibility, VisibilityOff } from '@mui/icons-material';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false); // 控制密码可见性
  const [verificationCode, setVerificationCode] = useState('');
  const [isCodeSent, setIsCodeSent] = useState(false); // 是否已发送验证码
  const [codeCountdown, setCodeCountdown] = useState(0); // 倒计时

  // 注册提交处理函数
  const handleSubmit = async (event) => {
    event.preventDefault();
    // 检查密码是否一致
    if (password !== confirmPassword) {
      alert("两次输入的密码不一致!");
      return;
    }
    // 检查表单字段是否为空
    if (!username || !email || !password || !verificationCode) {
      alert("请填写所有必填字段并输入验证码！");
      return;
    }

    try {
      // 发送请求验证验证码
      const verifyResponse = await axios.post('http://127.0.0.1:8000/backend/verify_code', {
        email,
        verification_code: verificationCode,
      });

      if (verifyResponse.data.status !== 'success') {
        alert(`验证码错误：${verifyResponse.data.message}`);
        return;
      }

      // 验证成功后发送注册请求
      const registerResponse = await axios.post('http://127.0.0.1:8000/backend/register', {
        username,
        email,
        password,
      });

      if (registerResponse.data.status === 'success') {
        alert('注册成功！');
        navigate('/login'); // 注册成功后跳转到登录页面
      } else {
        alert(`注册失败：${registerResponse.data.message}`);
      }
    } catch (error) {
      console.error('注册请求失败:', error);
      alert('注册失败，请稍后重试！');
    }
  };

  // 发送验证码
  const sendVerificationCode = async () => {
    if (!email) {
      alert("请先填写邮箱地址！");
      return;
    }
    if (isCodeSent) return; // 防止重复发送

    try {
      const response = await axios.post('http://127.0.0.1:8000/backend/send_verification_code', { email });
      if (response.data.status === 'success') {
        alert('验证码已发送到您的邮箱！');
        setIsCodeSent(true);
        setCodeCountdown(60); // 开启倒计时
        const interval = setInterval(() => {
          setCodeCountdown((prev) => {
            if (prev === 1) {
              clearInterval(interval);
              setIsCodeSent(false);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);
      } else {
        alert(`发送验证码失败：${response.data.message}`);
      }
    } catch (error) {
      console.error('发送验证码失败:', error);
      alert('发送验证码失败，请稍后重试！');
    }
  };

  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
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
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: { xs: 'column', md: 'row' }, // 改为列布局在小屏幕，行布局在大屏幕
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
            {/*<Avatar sx={{ m: 1, bgcolor: 'transparent', width: 80, height: 80 }}>*/}
            {/*    <img src={PIcon} alt="Login Icon" style={{ width: '100%', height: '100%' }} />*/}
            {/*  </Avatar>*/}
            <Typography component="h1" variant="h5">
              注册
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
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2, // 设置控件之间的间距
                  mt: 2,
                }}
              >
                <TextField
                  variant="outlined"
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
                <Button
                  onClick={sendVerificationCode}
                  disabled={isCodeSent}
                  variant="contained"
                >
                  {isCodeSent ? `重新发送 (${codeCountdown}s)` : '发送验证码'}
                </Button>
              </Box>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="verificationCode"
                label="请输入验证码"
                name="verificationCode"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="请输入密码"
                type={showPassword ? "text" : "password"}
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                helperText="密码必须包含至少6个字符，字母和数字都要有"
                slotProps={{
                input: {
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={toggleShowPassword} edge="end">
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
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
