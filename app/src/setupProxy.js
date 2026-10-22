// src/setupProxy.js
const { createProxyMiddleware } = require('http-proxy-middleware');

// 把 /backend 请求转发到 Django；Docker 中通过 BACKEND_URL 指向 backend 服务
module.exports = function (app) {
  app.use(createProxyMiddleware({
    target: process.env.BACKEND_URL || 'http://localhost:8000',
    pathFilter: '/backend',
  }));
};
