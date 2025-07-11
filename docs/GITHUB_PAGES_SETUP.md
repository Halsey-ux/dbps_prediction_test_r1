# GitHub Pages 部署指南

## 🌐 将消毒副产物预测系统部署到GitHub Pages

本指南将帮助您在GitHub Pages上部署项目的静态展示页面。

### 📋 前提条件

- 已将项目推送到GitHub仓库
- 拥有GitHub账户
- 仓库是公开的（GitHub Pages免费版要求）

### 🚀 部署步骤

#### 1. 访问仓库设置

1. 打开您的GitHub仓库: `https://github.com/Halsey-ux/dbps_prediction_test_r1`
2. 点击仓库页面上方的 **Settings** 选项卡
3. 在左侧菜单中找到 **Pages** 选项

#### 2. 配置GitHub Pages

1. 在 **Source** 部分，选择 **Deploy from a branch**
2. 在 **Branch** 下拉菜单中选择 **main**
3. 在 **Folder** 下拉菜单中选择 **/ (root)** 或 **/docs**
4. 点击 **Save** 按钮

#### 3. 验证部署

- GitHub会自动构建您的网站
- 几分钟后，您会看到一个绿色的勾号和网站URL
- 访问URL: `https://halsey-ux.github.io/dbps_prediction_test_r1/`

### 🎯 方法选择

#### 选项A: 使用docs文件夹（推荐）

```bash
# 如果选择docs文件夹，GitHub Pages会自动使用 docs/index.html
# 网站地址: https://halsey-ux.github.io/dbps_prediction_test_r1/
```

#### 选项B: 使用根目录

```bash
# 如果选择根目录，需要在根目录创建index.html
cp docs/index.html index.html
git add index.html
git commit -m "Add index.html for GitHub Pages"
git push test_R1 main
```

### 📁 文件结构

```
项目根目录/
├── docs/
│   ├── index.html          # 主页面（已创建）
│   └── GITHUB_PAGES_SETUP.md  # 本指南
├── README.md               # 项目说明
└── 其他项目文件...
```

### 🔧 自定义域名（可选）

如果您有自定义域名：

1. 在 **Custom domain** 输入框中输入您的域名
2. 勾选 **Enforce HTTPS**
3. 在您的域名DNS设置中添加CNAME记录指向 `halsey-ux.github.io`

### 🛠️ 故障排除

#### 常见问题及解决方案

**Q: 网站显示404错误**
- 确保选择了正确的分支和文件夹
- 检查 `docs/index.html` 文件是否存在
- 等待几分钟让GitHub完成构建

**Q: CSS样式不显示**
- 检查HTML中的CSS链接是否正确
- 确保使用了CDN链接而不是本地文件

**Q: 构建失败**
- 检查HTML文件的语法是否正确
- 查看Actions标签页中的构建日志

### 📊 访问统计

GitHub Pages部署完成后，您可以：
- 通过GitHub Insights查看访问统计
- 使用Google Analytics进行详细分析
- 监控网站性能

### 🔗 相关链接

- [GitHub Pages官方文档](https://docs.github.com/en/pages)
- [自定义域名设置](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages限制](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#usage-limits)

---

### 📝 部署检查清单

- [ ] 代码已推送到GitHub
- [ ] 在Settings中启用了GitHub Pages
- [ ] 选择了正确的分支和文件夹
- [ ] 等待构建完成
- [ ] 验证网站可以正常访问
- [ ] 检查所有链接和资源是否正常

完成上述步骤后，您的消毒副产物预测系统展示页面将在以下地址可用：
🌐 **https://halsey-ux.github.io/dbps_prediction_test_r1/**

### 🎉 成功部署后

您的静态展示页面将包含：
- 项目介绍和功能特点
- 技术架构说明
- 使用指南和快速开始
- 下载链接和文档
- 联系方式和GitHub链接

这个页面将成为您项目的对外展示窗口，方便用户了解和使用您的消毒副产物预测系统！ 