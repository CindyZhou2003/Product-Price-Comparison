import React, { useState } from 'react';
import {
    Box,
    TextField,
    Button,
    Typography,
    InputAdornment,
    IconButton,
    Container,
    CssBaseline,
    Link
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import theme from "./style";
import BgImg from "../asserts/img/bc2.png";
import MobileBgImg from '../asserts/img/phonebc.png'
import {ThemeProvider } from '@mui/material/styles';
import Grid from "@mui/material/Grid2";

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isCodeSent, setIsCodeSent] = useState(false);
  const [isCodeVerified, setIsCodeVerified] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [codeCountdown, setCodeCountdown] = useState(60);
  const navigate = useNavigate();

  // 发送验证码
  const handleSendCode = async () => {
    if (!email) {
      alert('请输入邮箱地址');
      return;
    }

    try {
      // 调用后端发送验证码
      const response = await axios.post('http://127.0.0.1:8000/backend/send_verification_code', { email });
      if (response.data.status === 'success') {
        alert('验证码已发送，请检查您的邮箱');
        setIsCodeSent(true);
        // 倒计时逻辑
        let countdown = 60;
        const timer = setInterval(() => {
          countdown -= 1;
          setCodeCountdown(countdown);
          if (countdown === 0) {
            clearInterval(timer);
            setIsCodeSent(false);
            setCodeCountdown(60);
          }
        }, 1000);
      } else {
        alert(`发送验证码失败：${response.data.message}`);
      }
    } catch (error) {
      alert('发送验证码失败，请稍后重试');
      console.error(error);
    }
  };

  // 验证验证码
  const handleVerifyCode = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/backend/verify_code', { email, verification_code: verificationCode });
      if (response.data.status === 'success') {
        alert('验证码验证成功');
        setIsCodeVerified(true);
      } else {
        alert('验证码验证失败，请检查验证码');
      }
    } catch (error) {
      alert('验证验证码失败，请稍后重试');
      console.error(error);
    }
  };

  // 重置密码
  const handleResetPassword = async () => {
    if (newPassword !== confirmPassword) {
      alert('两次输入的密码不一致');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/backend/reset_password', {
        email,
        password: newPassword,
      });
      if (response.data.status === 'success') {
        alert('密码重置成功，请使用新密码登录');
        navigate('/login');
      } else {
        alert(`密码重置失败：${response.data.message}`);
      }
    } catch (error) {
      alert('密码重置失败，请稍后重试');
      console.error(error);
    }
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
            flexDirection: { xs: 'column', md: 'row' },
            padding: 2, // 添加内边距以适应小屏幕
          }}
        >
        <Box
            sx={{
            position: 'relative', // 或 absolute
            top: { xs: '0px', sm: '-120px' }, // 小屏幕时调整位置
            left: { xs: '0px', sm: '150px' },
            display: 'inline-block',
            background: 'linear-gradient(to right, purple, orange)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            // lineHeight: 2, // 设置行高，避免文字被截断
            overflow: 'visible', // 确保内容可见
            marginBottom: { xs: 4, md: 0 },
            }}
            >
            <Typography
              component="h1"
              variant="h1"
              sx={{
                lineHeight: 2, // 设置文字的行高
                // color: 'primary.main', // 使用主题的 primary 颜色
                fontSize: { xs: '2rem', sm: '3rem', md: '4rem' },
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
            <Typography component="h1" variant="h5">
              忘记密码
            </Typography>

            {/* 邮箱输入和验证码发送 */}
            {!isCodeVerified && (
              <>
                <Box sx={{ mt: 2, display: 'flex', gap: 2, alignItems: 'center' }}>
                  <TextField
                    fullWidth
                    required
                    label="请输入您的邮箱地址"
                    name="email"
                    autoComplete="email"
                    variant="outlined"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <Button
                    onClick={handleSendCode}
                    disabled={isCodeSent}
                    variant="contained"
                  >
                    {isCodeSent ? `重新发送(${codeCountdown}s)` : '发送验证码'}
                  </Button>

                </Box>

                <TextField
                  fullWidth
                  required
                  label="请输入验证码"
                  variant="outlined"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  sx={{ mt: 2 }}
                />
                <Button
                  fullWidth
                  variant="contained"
                  sx={{ mt: 2 }}
                  onClick={handleVerifyCode}
                >
                  验证验证码
                </Button>

              <Grid container justifyContent="flex-end" sx={{mt:2}}>
                <Grid item>
                  <Link href="#" variant="body2" onClick={() => navigate('/')}>
                      {"返回登录"}
                  </Link>
                </Grid>
              </Grid>
              </>
            )}

            {/* 密码重置 */}
            {isCodeVerified && (
              <>
                <TextField
                  fullWidth
                  label="请输入新密码"
                  variant="outlined"
                  type={showPassword ? 'text' : 'password'}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  sx={{ mt: 2 }}
                  slotProps={{
                    input: {
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={() => setShowPassword(!showPassword)}>
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  },
                  }}
                />
                <TextField
                  fullWidth
                  label="确认新密码"
                  variant="outlined"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  sx={{ mt: 2 }}
                />
                <Button
                  fullWidth
                  variant="contained"
                  sx={{ mt: 2 }}
                  onClick={handleResetPassword}
                >
                  重置密码
                </Button>
              </>
            )}
          </Box>
        </Container>
        </Box>
    </ThemeProvider>
  );
}

export default ForgotPassword;
