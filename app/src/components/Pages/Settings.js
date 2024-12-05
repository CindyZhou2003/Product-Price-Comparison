// src/components/pages/Settings.js
import React, { useState } from 'react';
import {
    Typography,
    Box,
    Button,
    TextField,
    Divider,
    FormControlLabel,
    Switch,
    IconButton,
    InputAdornment
} from '@mui/material';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Visibility, VisibilityOff } from '@mui/icons-material';

function Settings() {
  const navigate = useNavigate();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [emailNotifications, setEmailNotifications] = useState(true);
  const userId = localStorage.getItem('user_id'); // 获取当前用户 ID
  const [showPassword, setShowPassword] = useState(false); // 控制密码可见性

  const handlePasswordChange = async () => {
      // 在此处理更改密码逻辑，例如调用后端 API
      if (newPassword !== confirmPassword) {
          alert('新密码与确认密码不匹配');
          return;
      }
      if (!newPassword || !oldPassword || !confirmPassword) {
          alert("请填写所有必填字段！")
          return;
      }
      // 构建请求数据
      const requestData = {
          new_password: newPassword,
          old_password: oldPassword,
          user_id: userId,
      };

      // 使用axios发送POST请求到后端注册接口
      try {
          const response = await axios.post('http://127.0.0.1:8000/backend/change_password', requestData, {
              headers: {
                  'Content-Type': 'application/json',
              },
          });
          // 处理响应结果
          if (response.data.status === 'success') {
              alert('修改密码成功！');
              window.location.reload(); // 刷新当前页面
          } else {
              alert(`修改密码失败：${response.data.message}`);
          }
      } catch (error) {
          console.error('修改密码请求失败:', error);
          alert('修改密码失败，请稍后重试！');
      }
  };
  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };
  const handleSavePreferences = async() => {
    // 在此处理保存偏好设置的逻辑，例如调用后端 API
      const requestData = {
          user_id: userId,
          state: emailNotifications,
      }
      try {
          const response = await axios.post('http://127.0.0.1:8000/backend/change_email_service_state',
              requestData, {
              headers: {
                  'Content-Type': 'application/json',
              },
          });
          // 处理响应结果
          if (response.data.status === 'success') {
              alert('偏好设置已保存');
              // window.location.reload(); // 刷新当前页面
          } else {
              alert(`偏好设置保存失败：${response.data.message}`);
          }
      } catch (error) {
          console.error('偏好设置更改请求失败:', error);
          alert('偏好设置更改失败，请稍后重试！');
      }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          设置
        </Typography>
        <Button variant="contained" color="primary" onClick={() => navigate('/home')}>
          返回首页
        </Button>
      </Box>
      <Typography variant="body1" gutterBottom>
        自定义您的偏好设置和账户选项。
      </Typography>
      <Divider sx={{ my: 3 }}>更改密码</Divider>

      {/* 更改密码部分 */}
      <Box sx={{ maxWidth: 400, mb: 3 }}>
        <TextField
          label="旧密码"
          type={showPassword ? "text" : "password"}
          variant="outlined"
          required
          fullWidth
          value={oldPassword}
          onChange={(e) => setOldPassword(e.target.value)}
          helperText="请输入您之前的密码"
          sx={{ mb: 2 }}
          slotProps={{
            input: {
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={toggleShowPassword} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            },
          }}
        />
        <TextField
          label="新密码"
          type={showPassword ? "text" : "password"}
          variant="outlined"
          required
          fullWidth
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          helperText="新密码必须包含至少6个字符，字母和数字都要有"
          sx={{ mb: 2 }}
          slotProps={{
            input: {
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={toggleShowPassword} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            },
          }}
        />
        <TextField
          label="确认新密码"
          type="password"
          variant="outlined"
          required
          fullWidth
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          helperText="请重新输入新密码"
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="secondary" onClick={handlePasswordChange}>
          保存更改
        </Button>
      </Box>

      <Divider sx={{ my: 3 }}>通知设置</Divider>

      {/* 通知设置部分 */}
      <Box sx={{ maxWidth: 400, mb: 3 }}>
        <FormControlLabel
          control={
            <Switch
              checked={emailNotifications}
              onChange={(e) => setEmailNotifications(e.target.checked)}
            />
          }
          label="电子邮件通知"
        />
        <Button variant="contained" color="secondary" onClick={handleSavePreferences}>
          保存偏好设置
        </Button>
      </Box>
    </Box>
  );
}

export default Settings;
