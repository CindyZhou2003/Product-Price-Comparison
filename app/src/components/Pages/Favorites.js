// src/components/pages/Favorites.js
import React, { useState, useEffect } from 'react';
import { Typography, Box, Button, Card, CardContent, CardMedia, IconButton,CircularProgress,
  Dialog, DialogTitle, DialogContent, Snackbar, Alert} from '@mui/material';
import { useNavigate } from "react-router-dom";
import Grid from '@mui/material/Grid2';
import axios from 'axios';
import DeleteIcon from '@mui/icons-material/Delete';
import Tooltip from '@mui/material/Tooltip'
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip as ChartTooltip, Legend } from 'chart.js';
// 注册 Chart.js 组件
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ChartTooltip, Legend);

function Favorites() {
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const userId = localStorage.getItem('user_id'); // 获取当前用户 ID
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false); // 控制加载状态
  const [priceHistory, setPriceHistory] = useState(null); // 存储历史价格数据
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: '' });

  // 打开 Snackbar
  const handleSnackbarOpen = (message, severity) => {
    setSnackbar({ open: true, message, severity });
  };

  // 关闭 Snackbar
  const handleSnackbarClose = () => {
    setSnackbar({ open: false, message: '', severity: '' });
  };

  const handleClickOpen = async (productId) => {
    setOpen(true);
    setLoading(true); // 开始加载

    try {
      // 向后端 API 请求历史价格数据
      const response = await axios.get(`http://127.0.0.1:8000/backend/show_price`, {
        params: { id: productId }, // 传递商品 ID 参数
      });

      const { priceHistory } = response.data;

      const dates = priceHistory.map(entry => entry.date); // 提取所有日期
      const prices = priceHistory.map(entry => entry.price); // 提取所有价格

      // 设置价格数据
      setPriceHistory({
        labels: dates, // x轴 - 日期
        datasets: [
          {
            label: '价格 (元)',
            data: prices, // y轴 - 价格
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 4, // 调整线条宽度
            pointRadius: 4, // 调整数据点的半径
            pointBackgroundColor: 'rgba(75, 192, 192, 1)', // 数据点颜色
            pointBorderWidth: 4, // 数据点边框宽度
            tension: 0.4,
          },
        ],
      });
    } catch (error) {
      console.error('获取历史价格数据失败:', error);
    } finally {
      setLoading(false); // 加载完成
    }
  };

  const handleClose = () => {
    setOpen(false);
    setPriceHistory(null); // 关闭弹窗时重置数据
  };

  // 从后端获取用户关注的商品列表
  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/backend/get_favorites', {
          params: { user_id: userId },
        });

        if (response.data.status === 'success') {
          setFavorites(response.data.favorites);
          handleSnackbarOpen(`获取关注列表成功`, 'success');
        } else {
          handleSnackbarOpen(`获取关注列表失败：${response.data.message}`, 'error');
        }
      } catch (error) {
        console.error('获取关注商品列表失败:', error);
        handleSnackbarOpen('获取关注商品列表失败，请稍后重试！', 'error');
      }
    };
    fetchFavorites();
  }, [userId]);

  // 移除商品关注
  const handleRemoveFavorite = async (productId) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/backend/unlike', {
        user_id: userId,
        id: productId,
      });

      if (response.data.status === 'success') {
        handleSnackbarOpen('取消关注成功', 'success');
        // 更新本地列表，移除该商品
        setFavorites(favorites.filter(product => product.id !== productId));
      } else {
        handleSnackbarOpen(`取消关注失败：${response.data.message}`, 'error');
      }
    } catch (error) {
      console.error('取消关注请求失败:', error);
      handleSnackbarOpen('取消关注失败，请稍后重试！', 'error');
    }
  };

  return (
  <div>
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          我的关注
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}
          sx={{
              fontSize: { xs: 10, sm: 15, lg:18 }, // 调整按钮大小
            }}>
          返回首页
        </Button>
      </Box>
      <Typography variant="body1" gutterBottom>
        管理您关注的商品，并接收降价通知。
      </Typography>

      {/* 如果没有关注的商品，显示提示信息 */}
      {favorites.length === 0 ? (
        <Typography variant="body1" sx={{ mt: 2 }}>
          您还没有关注任何商品。
        </Typography>
      ) : (
          <Grid container rowSpacing={4} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          {favorites.map((product) => (
            <Grid item key={product.id} size={{ xs: 6, sm: 4, md: 3 ,lg:2.4 }}>
              <Card sx={{ height: 410, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <CardMedia
                  component="img"
                  sx={{ width: 150, height: 150, objectFit: 'contain', mx: 'auto', mt: 2 }}
                  image={product.img}
                  alt={product.title}
                />
                <CardContent>
                  {/* Tooltip 在鼠标悬停时显示完整标题 */}
                  <Tooltip title={product.title} arrow>
                    <Typography
                      gutterBottom
                      variant="h6"
                      component="div"
                      sx={{
                        display: '-webkit-box',
                        WebkitLineClamp: 2,      // 限制文本行数为 2 行
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',      // 隐藏溢出部分
                        textOverflow: 'ellipsis',// 使用省略号表示溢出
                        whiteSpace: 'normal',    // 允许换行
                        fontSize: { xs: 15, sm: 18, lg:20 },
                      }}
                    >
                      {product.title}
                    </Typography>
                  </Tooltip>
                  <Typography variant="body2" color="text.secondary">
                    价格: {product.price}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                      display: 'block',       // 必须使用 block 或 inline-block
                      overflow: 'hidden',     // 隐藏溢出的文本
                      textOverflow: 'ellipsis', // 使用省略号表示溢出
                      whiteSpace: 'nowrap',   // 禁止换行
                    }}
                  >
                    店铺: {product.shop}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    平台: {product.platform}
                  </Typography>
                </CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    p: 2,
                    gap: 1, // 按钮之间的间距
                  }}
                >
                  <Button
                    variant="outlined"
                    color="primary"
                    href={product.link}
                    target="_blank"
                    sx={{
                      fontSize: { xs: '0.7rem', sm: '0.875rem' }, // 字体大小
                      padding: { xs: '4px 6px', sm: '6px 12px' }, // 内边距
                      minWidth: { xs: 'auto', sm: '80px' }, // 最小宽度
                    }}
                  >
                    查看详情
                  </Button>

                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={() => handleClickOpen(product.id)}
                    sx={{
                      fontSize: { xs: '0.7rem', sm: '0.875rem' }, // 字体大小
                      padding: { xs: '4px 6px', sm: '6px 12px' }, // 内边距
                      minWidth: { xs: 'auto', sm: '80px' }, // 最小宽度
                    }}
                  >
                    历史价格
                  </Button>

                  <IconButton
                    color="secondary"
                    onClick={() => handleRemoveFavorite(product.id)}
                    sx={{
                      fontSize: { xs: '1rem', sm: '1.25rem' }, // 调整 IconButton 的大小
                    }}
                  >
                    <DeleteIcon fontSize="inherit" />
                  </IconButton>
                </Box>
              </Card>
              {/* 弹出框 - 显示历史价格 */}
            <Dialog open={open} onClose={handleClose} fullWidth maxWidth="md">
              <DialogTitle>商品历史价格</DialogTitle>
              <DialogContent sx={{ minHeight: 300, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                {loading ? (
                  <CircularProgress /> // 显示加载状态
                ) : priceHistory ? (
                  <Line data={priceHistory} />
                ) : (
                  <Typography color="error">暂无数据</Typography>
                )}
              </DialogContent>
            </Dialog>
            </Grid>
          ))}
        </Grid>
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

export default Favorites;
