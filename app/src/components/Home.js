// Home.js
import { AppBar, Toolbar, Typography, CssBaseline, Box, IconButton, Drawer, List, ListItem, ListItemText, Divider, InputBase, Card, CardContent, CardMedia, Button } from '@mui/material';
import Grid from '@mui/material/Grid2';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import AccountCircle from '@mui/icons-material/AccountCircle';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import HistoryIcon from '@mui/icons-material/History';
import FavoriteIcon from '@mui/icons-material/Favorite';
import SettingsIcon from '@mui/icons-material/Settings';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import theme from './style';
import { ThemeProvider } from '@mui/material/styles';
import pic1 from '../img/pic1.jpg';
import pic2 from '../img/pic2.jpg';
import pic3 from '../img/pic3.jpg';

const drawerWidth = 240;

function Home({ setIsAuthenticated }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate('/login');
  };

  const menuItems = [
    { text: '商品比价', icon: <CompareArrowsIcon /> },
    { text: '历史价格', icon: <HistoryIcon /> },
    { text: '关注', icon: <FavoriteIcon /> },
    { text: '设置', icon: <SettingsIcon /> }
  ];

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text}>
            <IconButton color="inherit">
              {item.icon}
            </IconButton>
            <ListItemText primary={item.text} sx={{ color: '#ffffff' }} />
          </ListItem>
        ))}
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
            <Typography variant="h5" noWrap component="div" sx={{ flexGrow: 1 }}>
              商品比价网站
            </Typography>
            <Box sx={{ position: 'relative', display: 'flex' }}>
              <IconButton color="inherit">
                <SearchIcon />
              </IconButton>
              <InputBase
                placeholder="Search for products..."
                inputProps={{ 'aria-label': 'search' }}
                sx={{ color: 'inherit', ml: 1, flex: 1, borderBottom: '1px solid white' }}
              />
            </Box>
            <IconButton
              size="large"
              edge="end"
              color="inherit"
              aria-label="account of current user"
              onClick={handleLogout}
            >
              <AccountCircle />
            </IconButton>
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
                color: '#ffa8ab',
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
          <Typography variant="h4" gutterBottom>
            Welcome to the Price Comparison Website!
          </Typography>
          <Typography variant="body1" gutterBottom>
            Here you can compare prices for different products from various online marketplaces.
          </Typography>
          <Typography variant="body1" gutterBottom>
            Use the search bar at the top to find products, or navigate using the side menu to view your comparison history, favorite products, and more.
          </Typography>

          {/* Content Grid Section */}
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
                    Compare Products
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Get detailed comparisons between products from multiple sources to find the best deals.
                  </Typography>
                </CardContent>
                <Button size="small" color="primary">Explore</Button>
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
                    Track Price History
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Check the historical price trends of your favorite products.
                  </Typography>
                </CardContent>
                <Button size="small" color="primary">View History</Button>
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
                    Manage Favorites
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Keep track of your favorite items and get notified of price drops.
                  </Typography>
                </CardContent>
                <Button size="small" color="primary">Manage</Button>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default Home;
