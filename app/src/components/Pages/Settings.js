// src/components/pages/Settings.js
import React from 'react';
import {Typography, Box, Button} from '@mui/material';
import {useNavigate} from "react-router-dom";

function Settings() {
    const navigate = useNavigate(); // Use navigate for navigation
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          设置
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}>
          返回首页
        </Button>
      </Box>
      <Typography variant="body1" gutterBottom>
        自定义您的偏好设置和账户选项。
      </Typography>
      {/* 添加设置页面的其他内容，比如更改密码、主题设置等 */}

    </Box>
  );
}

export default Settings;
