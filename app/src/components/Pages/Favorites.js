// src/components/pages/Favorites.js
import React from 'react';
import {Typography, Box, Button} from '@mui/material';
import {useNavigate} from "react-router-dom";

function Favorites() {
    const navigate = useNavigate(); // Use navigate for navigation
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          我的关注
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}>
          返回首页
        </Button>
      </Box>
      <Typography variant="body1" gutterBottom>
        管理您关注的商品，并接收降价通知。
      </Typography>
      {/* 添加关注商品页面的其他内容，比如商品列表、移除关注等操作 */}

    </Box>
  );
}

export default Favorites;
