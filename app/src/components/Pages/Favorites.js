// src/components/pages/Favorites.js
import React, { useState, useEffect } from 'react';
import { Typography, Box, Button, Card, CardContent, CardMedia, IconButton } from '@mui/material';
import { useNavigate } from "react-router-dom";
import Grid from '@mui/material/Grid2';
import axios from 'axios';
import DeleteIcon from '@mui/icons-material/Delete';
import Tooltip from '@mui/material/Tooltip'

function Favorites() {
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const userId = localStorage.getItem('user_id'); // 获取当前用户 ID

  // 从后端获取用户关注的商品列表
  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/backend/get_favorites', {
          params: { user_id: userId },
        });

        if (response.data.status === 'ok') {
          setFavorites(response.data.favorites);
        } else {
          alert(`获取关注列表失败：${response.data.message}`);
        }
      } catch (error) {
        console.error('获取关注商品列表失败:', error);
        alert('获取关注商品列表失败，请稍后重试！');
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

      if (response.data.status === 'ok') {
        alert('取消关注成功');
        // 更新本地列表，移除该商品
        setFavorites(favorites.filter(product => product.id !== productId));
      } else {
        alert(`取消关注失败：${response.data.message}`);
      }
    } catch (error) {
      console.error('取消关注请求失败:', error);
      alert('取消关注失败，请稍后重试！');
    }
  };

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

      {/* 如果没有关注的商品，显示提示信息 */}
      {favorites.length === 0 ? (
        <Typography variant="body1" sx={{ mt: 2 }}>
          您还没有关注任何商品。
        </Typography>
      ) : (
          <Grid container rowSpacing={4} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          {favorites.map((product) => (
            <Grid item key={product.id} size={{ xs: 2, sm: 4, md: 3 }}>
              <Card sx={{ height: 440, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <CardMedia
                  component="img"
                  sx={{ width: 180, height: 180, objectFit: 'contain', mx: 'auto', mt: 2 }}
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
                      }}
                    >
                      {product.title}
                    </Typography>
                  </Tooltip>
                  <Typography variant="body2" color="text.secondary">
                    价格: {product.price}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    店铺: {product.shop}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    平台: {product.platform}
                  </Typography>
                </CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', p: 2 }}>
                  <Button variant="outlined" color="primary" href={product.link} target="_blank">
                    查看详情
                  </Button>
                  <IconButton
                    color="secondary"
                    onClick={() => handleRemoveFavorite(product.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

export default Favorites;
