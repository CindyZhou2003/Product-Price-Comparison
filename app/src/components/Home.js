// Home.js
import { AppBar, Toolbar, Typography, CssBaseline, Box, IconButton, Drawer, List, ListItem, ListItemText, Divider, InputBase } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import AccountCircle from '@mui/icons-material/AccountCircle';
import { useState } from 'react';
import {useNavigate} from "react-router-dom";

const drawerWidth = 240;

function Home({ setIsAuthenticated }) {
  // 定义侧边栏的状态和切换处理函数
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // 退出登录功能
  const handleLogout = () => {
    // 更新状态为未登录并跳转回登录页面
    setIsAuthenticated(false);
    navigate('/login');
  };

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {['商品比价', '历史价格', '关注', '设置'].map((text) => (
          <ListItem button key={text}>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      {/* 顶部操作栏 */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle} // 切换侧边栏的显示状态
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Price Comparison
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
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        {/* 固定在桌面上的侧边栏 */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
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
          mt: 8
        }}
      >
        <Typography variant="h4" gutterBottom>
          Welcome to the Price Comparison Website!
        </Typography>
        <Typography>
          Here you can compare prices for different products from various online marketplaces.
        </Typography>
        <Typography>
          Use the search bar at the top to find products, or navigate using the side menu to view your comparison history, favorite products, and more.
        </Typography>
      </Box>
    </Box>
  );
};

export default Home;
