// Home.js
import {
    AppBar, Toolbar, Typography, CssBaseline, Box, IconButton, Drawer, List, ListItem,
    ListItemText, Divider, InputBase, Card, CardContent, CardMedia, Button, Tooltip, CircularProgress, Link
} from '@mui/material';

import Grid from '@mui/material/Grid2';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import AccountCircle from '@mui/icons-material/AccountCircle';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import HistoryIcon from '@mui/icons-material/History';
import FavoriteIcon from '@mui/icons-material/Favorite';
import SettingsIcon from '@mui/icons-material/Settings';
import {Outlet, useLocation, useNavigate} from "react-router-dom";
import theme from './style';
import { ThemeProvider } from '@mui/material/styles';
import pic1 from '../asserts/img/pic1.jpg';
import pic2 from '../asserts/img/pic2.jpg';
import pic3 from '../asserts/img/pic3.jpg';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import HomeIcon from '@mui/icons-material/Home';
import PIcon from "../asserts/img/Picon.png";
import Avatar from "@mui/material/Avatar";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import favorites from "./Pages/Favorites"; // 用于发送 HTTP 请求
import handleFavoriteClick from "./Pages/ProductComparison"
const drawerWidth = 240;

function Home({ setIsAuthenticated }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); // Get the current route location
  const [allProducts, setAllProducts] = useState([]); // 存储从后端获取的商品数据
  const [loadingProducts, setLoadingProducts] = useState(false); // 控制加载状态

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem("isAuthenticated"); // Clear the persistent state
    navigate('/login');

  };
    // 获取所有商品的函数
  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await axios.get("http://localhost:8000/backend/get_random_products");
        if (response.data && response.data.products) {
          setAllProducts(response.data.products); // 这里确保提取到的 products 是数组
        } else {
          console.error("Unexpected API response structure:", response.data);
          setAllProducts([]); // 如果数据格式错误，设置为空数组
        }
      } catch (error) {
        console.error("Error fetching products:", error);
        setAllProducts([]); // 如果请求失败，设置为空数组
      }
    }
    fetchProducts();
  }, []);

 const menuItems = [
     { text: '主页', icon: <HomeIcon />, path: '/home' },
    { text: '商品比价', icon: <CompareArrowsIcon />, path: '/home/product-comparison' },
    { text: '历史价格', icon: <HistoryIcon />, path: '/home/price-history' },
    { text: '关注', icon: <FavoriteIcon />, path: '/home/favorites' },
    { text: '设置', icon: <SettingsIcon />, path: '/home/settings' }
  ];

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} onClick={() => navigate(item.path)}>
            <IconButton color="inherit">
              {item.icon}
            </IconButton>
            <ListItemText primary={item.text} sx={{ color: '#ffffff' }} />
          </ListItem>
        ))}
          <Divider component="li" />
      </List>
    </div>
  );

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />

        {/* 顶部操作栏 */}
        <AppBar
          position="fixed"
          sx={{
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            ml: { sm: `${drawerWidth}px` },
            bgcolor: 'primary'
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
              <Avatar sx={{ m: 1, bgcolor: 'transparent', width: 60, height: 60 }}>
                <img src={PIcon} alt="Login Icon" style={{ width: '100%', height: '100%' }} />
              </Avatar>
            <Typography
              variant="h4"
              noWrap
              component="div"
              sx={{ flexGrow: 1 }}
            >
              <span style={{ fontFamily: `'Ma Shan Zheng', cursive` }}>商品比价网站</span>{' '}
              <span style={{ fontFamily: `'Arizonia-Regular-OTF'`,fontWeight:600 }}>Price Pilot</span>
            </Typography>

            <Box sx={{ position: 'relative', display: 'flex' }}>
              <IconButton color="inherit">
                <SearchIcon fontSize="large"/>
              </IconButton>
              <InputBase
                placeholder="搜索商品..."
                inputProps={{ 'aria-label': 'search' }}
                sx={{ color: 'inherit', ml: 1, flex: 1, borderBottom: '1px solid white' }}
              />
            </Box>
            <Tooltip title="退出登录" arrow placement="bottom">
              <IconButton
                size="large"
                edge="end"
                color="inherit"
                aria-label="account of current user"
                onClick={handleLogout}
              >
                <AccountCircle fontSize="large" />
              </IconButton>
            </Tooltip>
          </Toolbar>
        </AppBar>

        {/* 侧边栏 */}
        <Box
          component="nav"
          sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
          aria-label="mailbox folders"
        >
          {/* 对于移动设备上的侧边栏 */}
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{ keepMounted: true }}
            sx={{
              display: { xs: 'block', sm: 'none' },
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: drawerWidth,
                backgroundColor: '#ba4e5c', // 设置背景颜色为深灰色
                color: '#ffd9d9',
                transition: 'background-color 0.5s ease-in-out' // 添加过渡效果
              },
            }}
          >
            {drawer}
          </Drawer>
          {/* 固定在桌面上的侧边栏 */}
          <Drawer
            variant="permanent"
            sx={{
              display: { xs: 'none', sm: 'block' },
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: drawerWidth,
                background: 'linear-gradient(180deg, #d36775 30%, #e9b3ba 90%)',
                color: '#f8b1b4',
                boxShadow: '3px 0 5px rgba(0,0,0,0.2)' // 添加阴影效果
              },
            }}
            open
          >
            {drawer}
          </Drawer>
        </Box>

        {/* 主页内容 */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            mt: 8,
            borderRadius: '8px',
            boxShadow: '1px 1px 10px rgba(0,0,0,0.1)', // 为主内容区添加阴影效果
          }}
        >
            <Outlet />
             {/* Only show these elements when on the /home path */}
          {location.pathname === '/home' && (
            <>
              <Typography variant="h4" gutterBottom>
                  <ShoppingCartIcon sx={{mr: 1.5}} fontSize="large"/>
                欢迎来到商品比价网站！
              </Typography>
              <Typography variant="body1" gutterBottom>
                在这里，您可以比较不同在线市场的不同产品的价格。
              </Typography>
              <Typography variant="body1" gutterBottom>
                使用顶部的搜索栏查找产品，或使用侧面菜单导航查看比较历史记录、最喜欢的产品等。
              </Typography>
               {/*Content Grid Section */}
              <Grid container spacing={4} sx={{ mt: 4 }}>
                {/* Product Comparison */}
                <Grid item xs={8} md={4}>
                  <Card sx={{ maxWidth: 300 }}>
                    <CardMedia
                      component="img"
                      height="300"
                      image={pic1}
                      alt="Product Comparison"
                    />
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="div">
                        比较商品
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        获取来自多个来源的产品之间的详细比较以找到最优惠的价格。
                      </Typography>
                    </CardContent>
                    <Button size="small" color="primary">探索</Button>
                  </Card>
                </Grid>

                {/* Price History */}
                <Grid item xs={8} md={4}>
                  <Card sx={{ maxWidth: 300 }}>
                    <CardMedia
                      component="img"
                      height="300"
                      image={pic3}
                      alt="Price History"
                    />
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="div">
                        追踪历史价格
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        查看您最喜爱的产品的历史价格趋势。
                      </Typography>
                    </CardContent>
                    <Button size="small" color="primary">查看</Button>
                  </Card>
                </Grid>

                {/* Favorites */}
                <Grid item xs={8} md={4}>
                  <Card sx={{ maxWidth: 300 }}>
                    <CardMedia
                      component="img"
                      height="300"
                      image={pic2}
                      alt="Favorites"
                    />
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="div">
                        管理喜爱
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        追踪您喜爱的商品并获取降价通知。
                      </Typography>
                    </CardContent>
                    <Button size="small" color="primary">管理</Button>
                  </Card>
                </Grid>
              </Grid>
              <Box sx={{ width: '100%', mt: 6, mb: 2, textAlign: 'center' }}>
                  <Typography
                    variant="h4"
                    component="div"
                    sx={{
                      fontWeight: 'bold',
                      textAlign: 'center',
                      borderBottom: '2px solid #ddd',
                      width: 'fit-content',
                      mx: 'auto',
                      px: 2,
                    }}
                  >
                    每日推荐
                  </Typography>
                </Box>
                  {/* 商品展示部分 */}
             <Grid container spacing={3} justifyContent="center">
                  {loadingProducts ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  allProducts.map((product, index) => (
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
                  ))
                )}
             </Grid>
            </>
          )}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default Home;
