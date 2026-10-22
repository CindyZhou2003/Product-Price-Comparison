// src/api.js
import axios from 'axios';

// 通过开发服务器代理访问后端（见 setupProxy.js），同源请求可以直接携带 Session Cookie
const api = axios.create({
  baseURL: '/backend',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

// 第一次发送 POST 前先向后端领取 CSRF Cookie
api.interceptors.request.use(async (config) => {
  if (config.method !== 'get' && !document.cookie.includes('csrftoken=')) {
    await api.get('/csrf');
  }
  return config;
});

// Session 失效时回到登录页
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('isAuthenticated');
      window.location.href = `${process.env.PUBLIC_URL}/login`;
    }
    return Promise.reject(error);
  }
);

export default api;
