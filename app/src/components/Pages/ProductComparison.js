// src/components/pages/ProductComparison.js
import React, { useState } from 'react';
import {
  Typography, Box, Button, TextField, Card, CardContent, CardMedia, Link, Tooltip,
  IconButton, Divider, FormControl, MenuItem, Select, InputLabel, Pagination,
  CircularProgress,
  ListItemIcon
} from '@mui/material';
import { useNavigate } from "react-router-dom";
import Grid from '@mui/material/Grid2';
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import axios from "axios";
import { ReactComponent as JDLogo } from '../../asserts/img/JD.svg'; // 替换为京东 logo 的 SVG 文件
import { ReactComponent as TaobaoLogo } from '../../asserts/img/TB.svg'; // 替换为淘宝 logo 的 SVG 文件

function ProductComparison() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState({});
  const [sortOption, setSortOption] = useState('relevance');
  const [platformFilter, setPlatformFilter] = useState('All');
  const [originalProducts, setOriginalProducts] = useState([]); // 原始搜索结果
  const [products, setProducts] = useState([]); // 筛选后的结果
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [platformSearchQuery, setPlatformSearchQuery] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('JD');
  const [loading, setLoading] = useState(false);

  const PRODUCTS_PER_PAGE = 48;

  const paginatedProducts = products.slice(
    (currentPage - 1) * PRODUCTS_PER_PAGE,
    currentPage * PRODUCTS_PER_PAGE
  );
  //搜索函数
  const handleSearch = async (event) => {
    event.preventDefault();
    if (!searchQuery.trim()) {
      alert('请输入搜索关键词！');
      return;
    }
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:8000/backend/search_products', {
        params: { search: searchQuery },
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.data.status === 'success') {
        alert('查询成功！');
        setOriginalProducts(response.data.products); // 存储原始结果
        setProducts(response.data.products); // 初始化筛选结果
        setTotalPages(Math.ceil(response.data.products.length / PRODUCTS_PER_PAGE));
        setCurrentPage(1);
      } else {
        alert(`查询失败：${response.data.message}`);
        setOriginalProducts([]); // 清空原始结果
        setProducts([]); // 清空筛选结果
      }
    } catch (error) {
      console.error('查询失败:', error);
      setOriginalProducts([]);
      setProducts([]);
    } finally {
      setLoading(false);
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

      if (response.data.status === 'success') {
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
      console.log('全部商品:', originalProducts);
      setProducts(originalProducts);
    } else {
      const filteredProducts = originalProducts.filter(
        product => product.platform.trim() === platform
      );
      setProducts(filteredProducts);
      setTotalPages(Math.ceil(filteredProducts.length / PRODUCTS_PER_PAGE)); // 更新总页数
    }
    setCurrentPage(1);
  };

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
    window.scrollTo(0, 0);  // Automatically scroll to the top when the page changes
  };

  const handlePlatformSearch = () => {
    if (!platformSearchQuery.trim()) {
      alert('请输入关键词！');
      return;
    }
    // 假设你有 API 调用或跳转逻辑
    console.log(`搜索平台: ${selectedPlatform}, 关键词: ${platformSearchQuery}`);
    // 示例：跳转到平台搜索结果页面
    window.open(`https://${selectedPlatform.toLowerCase()}.com/s?keyword=${platformSearchQuery}`);
  };

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
            <MenuItem value="All">
              全部平台
            </MenuItem>
            <MenuItem value="京东">
              <ListItemIcon>
                <JDLogo style={{ width: 24, height: 24 }} />
              </ListItemIcon>
              京东
            </MenuItem>
            <MenuItem value="淘宝">
              <ListItemIcon>
                <TaobaoLogo style={{ width: 24, height: 24 }} />
              </ListItemIcon>
              淘宝
            </MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* 商品展示卡片 */}
      <Grid container rowSpacing={4} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>)?
        (
          <Typography variant="body1" sx={{ mt: 2 }}>
            正在搜索，请稍候...
          </Typography>
        ) :searchQuery.trim() && paginatedProducts.length > 0 ? (
            <>
          {paginatedProducts.map((product, index) => (
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
                    信息: {product.info}
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
          ))}
        {/* 添加平台内搜索部分 */}
        <Grid item xs={12}>
          <Box sx={{ mt: 3 }}>
            <Typography variant="body1" sx={{ mb: 2 }}>
              不满意搜索结果？试试平台内搜索：
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <FormControl sx={{ minWidth: 120, mr: 2 }}>
                <InputLabel>选择平台</InputLabel>
                <Select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value)}
                  label="选择平台"
                >
                  <MenuItem value="JD">京东</MenuItem>
                  <MenuItem value="Taobao">淘宝</MenuItem>
                </Select>
              </FormControl>
              <TextField
                label="输入关键词"
                variant="outlined"
                fullWidth
                value={platformSearchQuery}
                onChange={(e) => setPlatformSearchQuery(e.target.value)}
                sx={{ mr: 2 }}
              />
              <Button variant="contained" color="primary" onClick={handlePlatformSearch}>
                平台搜索
              </Button>
            </Box>
          </Box>
        </Grid>
          </>
        ) : searchQuery.trim() && paginatedProducts.length === 0 ? (
          <>
            <Typography variant="body1" sx={{ mt: 2 }}>
              没有找到相关商品，请尝试其他关键词。
            </Typography>
          </>
        ) : null}
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





