// Home.js
import {
    AppBar, Toolbar, Typography, CssBaseline, Box, IconButton, Drawer, List, ListItem,
    ListItemText, Divider, Card, CardContent, CardMedia, Button, Tooltip,
    CircularProgress, Link, Snackbar, Alert
} from '@mui/material';
import { SimpleTreeView, TreeItem } from '@mui/x-tree-view';
import Grid from '@mui/material/Grid2';
import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';
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
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import axios from "axios";
const drawerWidth = 240;
const phonedrawerWidth = 180;
function Home({ setIsAuthenticated }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); // Get the current route location
  const [allProducts, setAllProducts] = useState([]); // 存储从后端获取的商品数据
  const [loadingProducts, setLoadingProducts] = useState(false); // 控制加载状态
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [favorites, setFavorites] = useState({}); // 商品收藏状态
  const [drawerOpen, setDrawerOpen] = useState(false); // 控制分类树抽屉
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: '' });

  // 打开 Snackbar
  const handleSnackbarOpen = (message, severity) => {
    setSnackbar({ open: true, message, severity });
  };

  // 关闭 Snackbar
  const handleSnackbarClose = () => {
    setSnackbar({ open: false, message: '', severity: '' });
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem("isAuthenticated"); // Clear the persistent state
    navigate('/login');

  };
  // 获取分类树
  useEffect(() => {
    fetch('http://localhost:8000/backend/get_categories') // 替换为你的分类接口
      .then((response) => response.json())
      .then((data) => {
        setCategories(data.categories); // 假设返回的 JSON 包含 categories 列表
      })
      .catch((err) => console.error('获取分类失败', err));
  }, []);

    const fetchProducts = (categoryId) => {
    setLoadingProducts(true);
    fetch(`http://localhost:8000/backend/search_through_categories?category=${categoryId}`) // 替换为你的商品接口
      .then((response) => response.json())
      .then((data) => {
        handleSnackbarOpen(`获取分类商品成功`, 'success');
        setAllProducts(data.products || []);
      })
      .catch((err) => {
          console.error('获取商品失败', err);
          handleSnackbarOpen(`获取分类商品失败！`, 'error');
      })
      .finally(() => setLoadingProducts(false));
  };

  // 点击分类时处理
  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId);
    fetchProducts(categoryId);
  };

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
          <ListItem button key={item.text} onClick={() => navigate(item.path)}
            sx={{xs: '1.1rem', sm: '1.5rem', lg:'2.5rem'}}
          >
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

  // 渲染分类树
  const renderCategoryTree = (categories) =>
    categories.map((category) => (
      <TreeItem
        key={category.id}
        nodeId={String(category.id)}
        label={category.name}
        onClick={() => handleCategoryClick(category.id)}
       itemId={category.id}>
        {category.subcategories && renderCategoryTree(category.subcategories)}
      </TreeItem>
    ));

  //关注函数
  const handleFavoriteClick = async (productId) => {
    const userId = localStorage.getItem('user_id');  // 从 localStorage 获取 user_id
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
          handleSnackbarOpen(`取消关注成功！`, 'success');
        } else {
          handleSnackbarOpen(`关注成功！`, 'success');
        }
        // 更新本地的状态，切换商品的关注状态
        setFavorites((prev) => ({
          ...prev,
          [productId]: !isLiked  // 切换状态：如果已喜欢则取消，未喜欢则添加
        }));
      } else {
        handleSnackbarOpen(`操作失败：${response.data.message}`, 'error');
      }
    } catch (error) {
      console.error('操作请求失败:', error);
      handleSnackbarOpen(`操作失败，请稍后重试！`, 'error');
    }
  };

  return (
  <div>
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />

        {/* 顶部操作栏 */}
        <AppBar
          position="fixed"
          sx={{
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            ml: { sm: `${drawerWidth}px` },
            bgcolor: 'primary.main',
          }}
        >
          <Toolbar sx={{ minHeight: { xs: 50, sm: 64 } }}> {/* 调整Toolbar高度 */}
            {/* 菜单按钮 */}
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{
                mr: 1,
                display: { sm: 'none' },
                fontSize: { xs: '1.25rem', sm: '1.5rem' } // 按钮大小
              }}
            >
              <MenuIcon fontSize="medium" />
            </IconButton>

        {/* 图标 */}
        <Avatar
          sx={{
            m: 0.5,
            bgcolor: 'transparent',
            width: { xs: 40, sm: 60 },
            height: { xs: 40, sm: 60 } // 头像大小
          }}
        >
          <img src={PIcon} alt="Login Icon" style={{ width: '100%', height: '100%' }} />
        </Avatar>

        {/* 标题 */}
        <Typography
          variant="h6"
          noWrap
          component="div"
          sx={{
            flexGrow: 1,
            fontSize: { xs: '1.3rem', sm: '1.5rem', lg:'2.5rem' }, // 字体大小
          }}
        >
          <span style={{ fontFamily: `'Ma Shan Zheng', cursive` }}>商品比价网站</span>{' '}
          <span style={{ fontFamily: `'Arizonia-Regular-OTF'`, fontWeight: 600 }}>Price Pilot</span>
        </Typography>

        {/* 退出登录按钮 */}
        <Tooltip title="退出登录" arrow placement="bottom">
          <IconButton
            edge="end"
            color="inherit"
            aria-label="account of current user"
            onClick={handleLogout}
          >
            <LogoutIcon sx={{
              fontSize: { xs: '1.2rem', sm: '1.5rem', lg:'2rem' }, // 调整按钮大小
            }}/>
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
                width: phonedrawerWidth,
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
              {/*Content Grid Section */}
            <Grid container spacing={4} sx={{ mt: 4 }}>
              {/* Product Comparison */}
              <Grid item xs={12} sm={6} md={4}>
                <Card
                  sx={{
                    maxWidth: { xs: 250, sm: 300 }, // 手机端小一点
                    mx: 'auto', // 水平居中
                  }}
                >
                  <CardMedia
                    component="img"
                    sx={{
                      height: { xs: 150, sm: 300 }, // 手机端图片高度减小
                      objectFit: "contain",         // 保证图片等比例缩放且完整显示
                    }}
                    image={pic1}
                    alt="Product Comparison"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="div" sx={{ fontSize: { xs: '1rem', sm: '1.25rem' } }}>
                      比较商品
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}>
                      获取来自多个来源的产品之间的详细比较以找到最优惠的价格。
                    </Typography>
                  </CardContent>
                  <Button size="small" color="primary" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
                   onClick={() => navigate('/home/product-comparison')}
                  >探索</Button>
                </Card>
              </Grid>

              {/* Price History */}
              <Grid item xs={12} sm={6} md={4}>
                <Card
                  sx={{
                    maxWidth: { xs: 250, sm: 300 },
                    mx: 'auto',
                  }}
                >
                  <CardMedia
                    component="img"
                    sx={{
                      height: { xs: 150, sm: 300 },
                      objectFit: "contain",         // 保证图片等比例缩放且完整显示
                    }}
                    image={pic3}
                    alt="Price History"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="div" sx={{ fontSize: { xs: '1rem', sm: '1.25rem' } }}>
                      追踪历史价格
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}>
                      查看您最喜爱的产品的历史价格趋势。
                    </Typography>
                  </CardContent>
                  <Button size="small" color="primary" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
                    onClick={() => navigate('/home/price-history')}
                  >查看</Button>
                </Card>
              </Grid>

              {/* Favorites */}
              <Grid item xs={12} sm={6} md={4}>
                <Card
                  sx={{
                    maxWidth: { xs: 250, sm: 300 },
                    mx: 'auto',
                  }}
                >
                  <CardMedia
                    component="img"
                    sx={{
                      height: { xs: 150, sm: 300 },
                      objectFit: "contain",         // 保证图片等比例缩放且完整显示
                    }}
                    image={pic2}
                    alt="Favorites"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="div" sx={{ fontSize: { xs: '1rem', sm: '1.25rem' } }}>
                      管理喜爱
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}>
                      追踪您喜爱的商品并获取降价通知。
                    </Typography>
                  </CardContent>
                  <Button size="small" color="primary" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
                    onClick={() => navigate('/home/favorites')}
                  >管理</Button>
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
                    分类查询
                  </Typography>
                </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 4 }}>
            {/* 分类树抽屉 */}
              <Drawer
                anchor="right"
                open={drawerOpen}
                onClose={() => setDrawerOpen(false)}
              >
                <Box sx={{ width: 250, p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    分类浏览
                  </Typography>
                  <SimpleTreeView
                    defaultCollapseIcon={<ExpandMoreIcon />}
                    defaultExpandIcon={<ChevronRightIcon />}
                    onNodeSelect={handleCategoryClick}
                  >
                    {renderCategoryTree(categories)}
                  </SimpleTreeView>
                </Box>
              </Drawer>

                  {/* 商品展示部分 */}
            <Box sx={{ width: '100%', flex:1}}>
                <Button
                  variant="outlined"
                  startIcon={<MenuIcon />}
                  onClick={() => setDrawerOpen(true)}
                  sx={{ mb: 2 }}
                >
                  分类浏览
                </Button>
                {selectedCategory && (
                  <Typography variant="h6" gutterBottom>
                    当前分类: {selectedCategory}
                  </Typography>
                )}
             <Grid container spacing={3} justifyContent="center">
                  {loadingProducts ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  allProducts.map((product, index) => (
                    <Grid item key={index} size={{xs:6, // 手机两列
                          sm:4,// 小屏展示三列
                          md:3, // 中屏展示四列
                          lg:2.4, // 大屏展示五列
                          }}
                        >
                    <Card sx={{ height: 410, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        <CardMedia
                          component="img"
                          sx={{ width: 150, height: 150, objectFit: 'contain', mx: 'auto', mt: 2 }}
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
                          <Typography variant="body2" color="text.secondary">
                            信息: {product.info}
                          </Typography>
                        </CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', pl: 2, pb: 4 }}>
                          <Link href={product.link} target="_blank" rel="noopener" underline="hover" sx={{ mr: 1 }}>
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
            </Box>
            </Box>

            </>
          )}
          </Box>
      </Box>
    </ThemeProvider>
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

export default Home;
