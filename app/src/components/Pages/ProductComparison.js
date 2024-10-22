// src/components/pages/ProductComparison.js
import React, { useState } from 'react';
import {
    Typography, Box, Button, TextField, Card, CardContent, CardMedia,
    Link, Tooltip, IconButton, Divider, FormControl, MenuItem, Select, InputLabel, Pagination
} from '@mui/material';
import { useNavigate } from "react-router-dom";
import Grid from '@mui/material/Grid2';
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import axios from "axios";

function ProductComparison() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState({});
  const [sortOption, setSortOption] = useState('relevance');
  const [platformFilter, setPlatformFilter] = useState('All');
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const PRODUCTS_PER_PAGE = 48;
  //搜索函数
  const handleSearch = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.get('http://127.0.0.1:8000/backend/search_products', {
        params: { search: searchQuery },
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.data.status === 'ok') {
        alert('查询成功！');
        setProducts(response.data.products);
        setTotalPages(Math.ceil(response.data.products.length / PRODUCTS_PER_PAGE));
        setCurrentPage(1);
      } else {
        alert(`查询失败：${response.data.message}`);
      }
    } catch (error) {
      console.error('查询失败:', error);
      alert('查询失败，请稍后重试！');
    }
  };

  //关注函数
  const handleFavoriteClick = async (productId) => {
  const userId = localStorage.getItem('user_id');  // 从 localStorage 获取 user_id

  if (!userId) {
    alert('请先登录后再进行关注操作。');
    return;
  }

  // 判断当前商品是否已被关注
  const isLiked = favorites[productId];

  try {
    // 根据当前状态决定请求类型：喜欢或者取消喜欢
    const url = isLiked ? 'http://127.0.0.1:8000/backend/unlike' : 'http://127.0.0.1:8000/backend/like';

    const response = await axios.post(url, {
      id: productId,   // 商品 ID
      user_id: userId  // 用户 ID
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.data.status === 'ok') {
      if (isLiked) {
        alert('取消关注成功！');
      } else {
        alert('关注成功！');
      }

      // 更新本地的状态，切换商品的关注状态
      setFavorites((prev) => ({
        ...prev,
        [productId]: !isLiked  // 切换状态：如果已喜欢则取消，未喜欢则添加
      }));
    } else {
      alert(`操作失败：${response.data.message}`);
    }
  } catch (error) {
    console.error('操作请求失败:', error);
    alert('操作失败，请稍后重试！');
  }
};


  const handleSortChange = (option) => {
    setSortOption(option);
    let sortedProducts;
    if (option === 'priceAsc') {
      sortedProducts = [...products].sort((a, b) => a.price - b.price);
    } else if (option === 'priceDesc') {
      sortedProducts = [...products].sort((a, b) => b.price - a.price);
    } else {
      sortedProducts = [...products].sort((a, b) => a.id - b.id);
    }
    setProducts(sortedProducts);
  };

  const handlePlatformFilterChange = (event) => {
    const platform = event.target.value;
    setPlatformFilter(platform);
    if (platform === 'All') {
      setProducts(products);
    } else {
      setProducts(products.filter(product => product.platform === platform));
    }
  };

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
    window.scrollTo(0, 0);  // Automatically scroll to the top when the page changes
  };

  const paginatedProducts = products.slice(
    (currentPage - 1) * PRODUCTS_PER_PAGE,
    currentPage * PRODUCTS_PER_PAGE
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          商品比价
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}>
          返回首页
        </Button>
      </Box>
      <Typography variant="body1" gutterBottom>
        比较不同平台的商品价格，以找到最优惠的价格。
      </Typography>
      <Divider>Start Search</Divider>

      {/* 搜索框 */}
      <Box sx={{ display: 'flex', mb: 3 }}>
        <TextField
          label="搜索商品"
          variant="outlined"
          fullWidth
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          sx={{ mr: 2 }}
        />
        <Button variant="contained" color="primary" onClick={handleSearch}>
          搜索
        </Button>
      </Box>

      {/* Sorting and Filtering Controls */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Box>
          <Button variant="outlined" onClick={() => handleSortChange('relevance')}>
            默认排序
          </Button>
          <Button variant="outlined" onClick={() => handleSortChange('priceAsc')} sx={{ ml: 2 }}>
            价格从低到高
          </Button>
          <Button variant="outlined" onClick={() => handleSortChange('priceDesc')} sx={{ ml: 2 }}>
            价格从高到低
          </Button>
        </Box>
        <FormControl variant="outlined" sx={{ minWidth: 120 }}>
          <InputLabel>平台筛选</InputLabel>
          <Select
            value={platformFilter}
            onChange={handlePlatformFilterChange}
            label="平台筛选"
          >
            <MenuItem value="All">全部平台</MenuItem>
            <MenuItem value="JD">京东</MenuItem>
            <MenuItem value="Tmall">天猫</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* 商品展示卡片 */}
      <Grid container rowSpacing={4} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        {paginatedProducts.length > 0 ? (
          paginatedProducts.map((product, index) => (
            <Grid item key={index} size={{ xs: 2, sm: 4, md: 3 }}>
              <Card sx={{ height: 460, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <CardMedia
                  component="img"
                  sx={{ width: 180, height: 180, objectFit: 'contain', mx: 'auto', mt: 2 }}
                  image={product.img}
                  alt={product.title}
                />
                <CardContent>
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
                  <Typography variant="body2" color="text.secondary">
                    评论: {product.comments}
                  </Typography>
                </CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', pl: 2, pb: 2 }}>
                  <Link href={product.link} target="_blank" rel="noopener" underline="hover" sx={{ mr: 2 }}>
                    查看详情
                  </Link>
                  <IconButton onClick={() => handleFavoriteClick(product.id)}>
                    {favorites[product.id] ? (
                      <FavoriteIcon color="error" />
                    ) : (
                      <FavoriteBorderIcon />
                    )}
                  </IconButton>
                </Box>
              </Card>
            </Grid>
          ))
        ) : (
          <Typography variant="body1" sx={{ mt: 2 }}>
            请先进行搜索；如搜索成功，则未找到对应的商品，请尝试更换关键词进行搜索
          </Typography>
        )}
      </Grid>

      {/* 分页控制 */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={totalPages}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
}

export default ProductComparison;





