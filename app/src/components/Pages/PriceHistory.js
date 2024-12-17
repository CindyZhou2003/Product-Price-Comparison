// src/components/pages/PriceHistory.js
import React, { useState } from 'react';
import { Typography, Box, Button, TextField, Snackbar, Alert } from '@mui/material';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Line } from 'react-chartjs-2';  // 导入 Line 图表
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend} from 'chart.js';

// 注册Chart.js所需的组件
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function PriceHistory() {
  const navigate = useNavigate(); // Use navigate for navigation
  const [searchQuery, setSearchQuery] = useState('');
  const [priceHistoryData, setPriceHistoryData] = useState(null); // 用于存储价格历史数据
  const [loading, setLoading] = useState(false);  // 显示加载状态
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: '' });

  // 打开 Snackbar
  const handleSnackbarOpen = (message, severity) => {
    setSnackbar({ open: true, message, severity });
  };

  // 关闭 Snackbar
  const handleSnackbarClose = () => {
    setSnackbar({ open: false, message: '', severity: '' });
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    setLoading(true);  // 开始查询时设置为加载中

    try {
      const response = await axios.get('http://127.0.0.1:8000/backend/update_and_show_price', {
        params: { search: searchQuery },
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.data.status === 'success') {
        // 假设返回的数据中包含价格历史数据
        const { priceHistory } = response.data;

        setPriceHistoryData({
          labels: priceHistory.map(entry => entry.date),
          datasets: [
            {
              label: '价格 (元)',
              data: priceHistory.map(entry => entry.price),
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderWidth: 4,
              pointRadius: 4,
              pointBackgroundColor: 'rgba(75, 192, 192, 1)',
              pointBorderWidth: 4,
              tension: 0.4,
            },
          ],
        });

        handleSnackbarOpen(`查询成功！`, 'success');
      } else {
        handleSnackbarOpen(`查询失败：${response.data.message}`, 'error');
      }
    } catch (error) {
      console.error('查询失败:', error);
      handleSnackbarOpen(`查询失败，请稍后重试！`, 'error');
    } finally {
      setLoading(false);  // 无论成功还是失败，关闭加载状态
    }
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false, // 允许自定义大小
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 16, // 调整图例字体大小
          },
        },
      },
      title: {
        display: true,
        text: '商品价格历史趋势',
        font: {
          size: 18, // 设置标题字体大小
        },
      },
    },
    scales: {
      x: {
        ticks: {
          font: {
            size: 16, // 调整 X 轴刻度字体大小
          },
        },
      },
      y: {
        ticks: {
          font: {
            size: 16, // 调整 Y 轴刻度字体大小
          },
        },
        beginAtZero: false,
      },
    },
  };


  return (
    <div>
    <Box>
      {/* 包含标题和按钮的行容器 */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          历史价格
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}
          sx={{xs: 10, sm: 15, lg:18}}>
          返回首页
        </Button>
      </Box>

      <Typography variant="body1" gutterBottom>
        查看商品的历史价格趋势，并了解它们在不同时间段的价格波动情况。
      </Typography>
      <div style={{ height: '16px' }} />  {/* 手动插入一行空白 */}
      {/* 搜索框 */}
      <Box sx={{ display: 'flex', mb: 3 }}>
        <TextField
          label="请输入想要搜索商品的url"
          variant="outlined"
          fullWidth
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          sx={{ mr: 2 }}
        />
        <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading}
        >
          {loading ? '查询中...' : '搜索'}
        </Button>
      </Box>

      {/* 显示价格历史图表 */}
    {priceHistoryData && (
      <Box
        sx={{
          mt: 4,
          display: 'flex',         // 使用 Flexbox 布局
          justifyContent: 'center', // 水平居中
          width: '80%',            // 让容器占满宽度
          mb: 2,
        }}
      >
        <Box sx={{ width: '80%', height: 400 }}> {/* 图表容器 */}
          <Typography variant="h6" gutterBottom>
          </Typography>
          <Line data={priceHistoryData} options={chartOptions} />
        </Box>
      </Box>
    )}
    </Box>
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

export default PriceHistory;
