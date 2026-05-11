# 🚀 PriceScout 部署指南

## 📋 快速部署到 GitHub Pages

### 步骤 1: 安装 Git

如果还没有安装 Git，请下载并安装：

**Windows:**
- 官网下载：https://git-scm.com/download/win
- 或使用 Chocolatey: `choco install git`

**安装后重启终端，然后验证：**
```bash
git --version
```

### 步骤 2: 创建 GitHub 仓库

1. 访问 https://github.com 并登录
2. 点击右上角 **"+"** → **"New repository"**
3. 填写信息：
   - **Repository name:** `pricescout`
   - **Description:** 智能电商价格采集与对比工具
   - **选择 Public**（公开仓库才能用 Pages）
   - ✅ **不要勾选** "Add a README file"（我们已经有了）
4. 点击 **"Create repository"**

### 步骤 3: 初始化本地 Git 并推送

在项目目录下执行以下命令（替换 `YOUR_USERNAME` 为您的 GitHub 用户名）：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件到暂存区
git add .

# 3. 提交代码
git commit -m "✨ PriceScout v1.0.0 - 智能电商价格采集与对比工具"

# 4. 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/pricescout.git

# 5. 推送代码到 GitHub
git branch -M main
git push -u origin main
```

### 步骤 4: 启用 GitHub Pages

1. 在 GitHub 仓库页面，点击 **Settings**（设置）
2. 左侧菜单找到 **"Pages"**
3. 配置：
   - **Source:** Select `Deploy from a branch`
   - **Branch:** 选择 `main`，文件夹选择 `/ (root)`
   - 点击 **Save**
4. 等待 1-2 分钟，页面会显示：
   > Your site is live at https://YOUR_USERNAME.github.io/pricescout/

### 步骤 5: 访问您的网站

恭喜！您的 PriceScout 网站已经上线了！🎉

访问地址：`https://YOUR_USERNAME.github.io/pricescout/`

---

## 🔄 后续更新代码

修改代码后，执行以下命令更新网站：

```bash
git add .
git commit -m "更新说明"
git push
```

GitHub Pages 会自动重新部署（通常 1-2 分钟内生效）。

---

## 🛠️ 常用 Git 命令

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 创建新分支
git branch feature-name

# 切换分支
git checkout feature-name

# 合并分支
git merge feature-name

# 拉取最新代码
git pull origin main
```

---

## 📚 额外资源

- **Git 官方文档**: https://git-scm.com/doc
- **GitHub Pages 文档**: https://docs.github.com/en/pages
- **GitHub 桌面客户端**: https://desktop.github.com/ （可视化操作，无需记忆命令）

---

## ⚠️ 注意事项

1. **公开仓库**: GitHub Pages 需要公开仓库才能免费使用
2. **部署时间**: 推送代码后可能需要 1-2 分钟才能看到更新
3. **示例数据**: 网页演示依赖 `sample_data.json`，请确保它随网页一起部署
4. **自定义域名**: 可以在 Pages 设置中添加自定义域名

---

**祝部署顺利！有问题随时提问。** 🚀
