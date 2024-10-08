// src/components/pages/PriceHistory.js
import React from 'react';
import {Typography, Box, Button} from '@mui/material';
import {useNavigate} from "react-router-dom";

function PriceHistory() {
    const navigate = useNavigate(); // Use navigate for navigation
  return (
    <Box>
      {/* 包含标题和按钮的行容器 */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          历史价格
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}>
          返回首页
        </Button>
      </Box>
      {/* 其他内容 */}
      <Typography variant="body1" gutterBottom>
        查看商品的历史价格趋势，并了解它们在不同时间段的价格波动情况。
      </Typography>
    </Box>
  );
}

export default PriceHistory;
