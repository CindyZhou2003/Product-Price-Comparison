// src/components/pages/ProductComparison.js
import React, { useState } from 'react';
import {
    Typography, Box, Button, TextField, Card, CardContent, CardMedia,
    Link, Tooltip, IconButton, Divider, FormControl, MenuItem, Select, InputLabel
} from '@mui/material';
import { useNavigate } from "react-router-dom";
import Grid from '@mui/material/Grid2';
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import axios from "axios"; // 导入 FavoriteBorder 图标

function ProductComparison() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState({});

  const [sortOption, setSortOption] = useState('relevance'); // State for sorting option
  const [platformFilter, setPlatformFilter] = useState('All'); // State for platform filter

  const [products, setProducts] = useState([]);

  // 处理搜索请求的函数
  const handleSearch = async (event) => {
    event.preventDefault();

    try {
      // 使用 axios 发起 GET 请求，并将搜索关键词放入 `params` 中
      const response = await axios.get('http://127.0.0.1:8000/backend/search_products', {
        params: { search: searchQuery },  // 通过 params 传递查询参数
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // 处理响应结果
      if (response.data.status === 'ok') {
        alert('查询成功！');
        // 将查询到的商品列表更新到 products 状态中
        setProducts(response.data.products);  // 更新 products 状态
      } else {
        alert(`查询失败：${response.data.message}`);
      }
    } catch (error) {
      console.error('查询失败:', error);
      alert('查询失败，请稍后重试！');
    }
  };

  // 处理关注按钮点击事件
 const handleFavoriteClick = (index) => {
    setFavorites((prev) => ({
      ...prev,
      [index]: !prev[index] // 切换关注状态
    }));
  };

 // Handle sorting option change
  const handleSortChange = (option) => {
    setSortOption(option);
    let sortedProducts;
    if (option === 'priceAsc') {
      sortedProducts = [...products].sort((a, b) => a.price - b.price);
    } else if (option === 'priceDesc') {
      sortedProducts = [...products].sort((a, b) => b.price - a.price);
    } else {
      sortedProducts = [...products].sort((a, b) => a.id - b.id); // Default: relevance (no change)
    }
    setProducts(sortedProducts);
  };

   // Handle platform filter change
  const handlePlatformFilterChange = (event) => {
    const platform = event.target.value;
    setPlatformFilter(platform);
    if (platform === 'All') {
      setProducts(products);
    } else {
      setProducts(products.filter(product => product.platform === platform));
    }
  };

  // const sampleProducts = [
  //   {
  //     title: 'iPhone 14 - 超长标题测试 - Apple 最好的智能手机 - 最新技术和强大性能',
  //     price: '¥5999',
  //     store: 'Apple Store',
  //     platform: '京东',
  //     reviews: '1234条评论',
  //     image: 'https://img13.360buyimg.com/n7/jfs/t1/199925/14/35495/50518/66ec00cfF6e3d1772/100ef8d744a7985e.jpg.avif',
  //     link: 'https://item.jd.com/100014576703.html'
  //   },
  //   {
  //     title: '三星 Galaxy S21',
  //     price: '¥4999',
  //     store: 'Samsung Store',
  //     platform: '天猫',
  //     reviews: '876条评论',
  //     image: 'https://example.com/samsung.jpg',
  //     link: 'https://tmall.com/samsung'
  //   },
  //   {
  //     title: '华为 Mate 40',
  //     price: '¥4299',
  //     store: 'Huawei Store',
  //     platform: '京东',
  //     reviews: '3200条评论',
  //     image: 'https://example.com/huawei.jpg',
  //     link: 'https://jd.com/huawei'
  //   },
  //   {
  //     title: '小米 11',
  //     price: '¥3999',
  //     store: 'Xiaomi Store',
  //     platform: '天猫',
  //     reviews: '2100条评论',
  //     image: 'https://example.com/xiaomi.jpg',
  //     link: 'https://tmall.com/xiaomi'
  //   },
  //   {
  //     title: 'OPPO Find X3',
  //     price: '¥4500',
  //     store: 'OPPO Store',
  //     platform: '京东',
  //     reviews: '1500条评论',
  //     image: 'https://example.com/oppo.jpg',
  //     link: 'https://jd.com/oppo'
  //   }
  // ];



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
          onChange={(e) => setSearchQuery(e.target.value)} // 更新搜索关键词状态
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
        {products.length > 0 ? (
          products.map((product, index) => (
            <Grid item key={index} size={{ xs: 2, sm: 4, md: 3 }}>
              <Card sx={{ height: 420, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <CardMedia
                  component="img"
                  sx={{ width: 180, height: 180, objectFit: 'contain', mx: 'auto', mt: 2 }}
                  image={product.img}
                  alt={product.title}
                />
                <CardContent>
                  {/* 使用 Tooltip 包裹标题，并限制标题只显示一行 */}
                  <Tooltip title={product.title} arrow>
                    <Typography
                      gutterBottom
                      variant="h6"
                      component="div"
                      sx={{
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
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
                  <IconButton onClick={() => handleFavoriteClick(index)}>
                    {favorites[index] ? (
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
            请进行搜索或未找到匹配的商品
          </Typography>
        )}
      </Grid>
    </Box>
  );
}

export default ProductComparison;



