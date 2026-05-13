# Traffic Jam 3D - 游戏落地页

现代化响应式游戏落地页，专注游戏体验的极简设计。

**演示地址**: [https://traffic-jam-3d.org]

## ✨ 特色

- 🎯 **极简设计** - 无导航栏，专注游戏体验
- 📱 **响应式** - 完美适配所有设备
- 🎮 **智能缩放** - iframe 16:9 比例自适应
- 🚀 **高性能** - 快速加载，流畅动画

## 🚀 快速开始

```bash
# 本地预览
python -m http.server 8008
# 访问 http://localhost:8008
```

**部署**: 上传到任何静态托管服务即可

## 📁 文件结构

```
├── index.html    # 主页面
├── style.css     # 样式文件
└── README.md     # 说明文档
```

## 🎨 自定义

### 更换游戏
修改 `index.html` 中的 iframe src 属性

### 更新信息
修改 `<title>` 和 meta 标签

### 自定义颜色
在 `style.css` 中搜索替换颜色值：
- `#FFD700` - 金色主题
- `#1a1a1a` - 深色背景



## 🌐 部署

- **GitHub Pages**: 上传到仓库，启用 Pages
- **Netlify**: 拖拽文件夹到 netlify.com/drop
- **Vercel**: 运行 `vercel` 命令
- **传统托管**: FTP 上传到服务器根目录

## 📱 响应式

- 桌面端: 1024px 最大宽度
- 平板端: 768px 断点
- 移动端: 480px 断点
- iframe: 16:9 比例自适应



## 🐛 常见问题

- **游戏不显示**: 检查 iframe URL 和 CORS 策略
- **样式异常**: 清除缓存，检查 CSS 加载
- **移动端问题**: 验证 viewport 和 aspect-ratio 支持

## 📄 许可

免费使用，无需署名。


