# GMS Instagram Stories Archive

自动化下载和归档 Gian Marco Schiaretti Instagram 故事的完整解决方案。

## 🎯 功能特性

- 🤖 **自动下载**: 每日自动下载 Instagram 故事
- 🖼️ **智能截图**: 仅截取故事媒体框架，避免界面元素
- 🌐 **网页展示**: 美观的图片画廊界面
- 📦 **自动同步**: 推送到 GitHub 仓库
- 🔒 **安全认证**: 使用 Personal Access Token，保护隐私

## 📁 项目结构

```
gms/
├── complete_workflow_console.py  # 完整工作流脚本
├── run_workflow.bat              # 一键运行批处理
├── .gitignore                    # Git 忽略规则
├── chrome_profile/               # 浏览器配置目录
└── webpage/                      # 主要代码目录
    ├── auto_story_downloader.py  # 核心下载脚本
    ├── scan.py                   # 图库数据更新
    ├── push_to_github_token.py   # GitHub 推送脚本
    ├── index.html                # 网页主界面
    ├── gallery.js                # 画廊交互逻辑
    ├── style.css                 # 网页样式
    ├── gallery-data.json         # 图库数据文件
    ├── pics/                     # 图片存储目录
    ├── requirements.txt          # Python 依赖
    └── *.bat                     # 各种批处理脚本
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd webpage
pip install playwright
python -m playwright install chromium
```

### 2. 配置 GitHub Token

首次运行时会提示输入 GitHub Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 创建新的 Token，选择 `repo` 权限
3. 运行脚本时输入 Token
4. Token 会安全保存在本地，后续无需重复输入

### 3. 运行完整工作流

**方法一：双击运行**
```
双击 run_workflow.bat
```

**方法二：命令行运行**
```bash
cd gms
python complete_workflow_console.py
```

## 🔄 工作流程

### Step 1: 下载故事
- 自动打开 Chromium 浏览器
- 等待手动登录 Instagram（首次需要）
- 导航到目标故事页面
- 智能截取每个故事媒体框架
- 保存到 `pics/YYYY-MM-DD/` 目录

### Step 2: 更新图库
- 扫描图片目录
- 更新 `gallery-data.json` 数据
- 按日期组织图片信息

### Step 3: 推送到 GitHub
- 提交所有更改
- 推送到指定仓库
- 自动处理分支和冲突

## 🌐 本地预览

启动本地服务器查看网页：

```bash
cd webpage
python -m http.server 8000
```

访问 http://localhost:8000 查看图库界面。

## ⏰ 定时任务

设置每日自动运行：

1. 打开 Windows 任务计划程序
2. 创建基本任务
3. 设置每日触发器
4. 操作：运行 `run_workflow.bat`

## 🔧 单独功能脚本

### 仅下载故事
```bash
cd webpage
python auto_story_downloader.py
# 或双击 run_downloader.bat
```

### 仅更新图库
```bash
cd webpage
python scan.py
```

### 仅推送到 GitHub
```bash
cd webpage
python push_to_github_token.py
# 或双击 push_to_github_token.bat
```

### 清除保存的 Token
```bash
cd webpage
python clear_token.py
```

## 🔒 安全特性

- **Token 本地存储**: 保存在项目根目录外，不会被推送
- **Git 忽略保护**: 多层 .gitignore 确保敏感文件不被提交
- **会话持久化**: Chrome 配置保存，避免重复登录

## 📊 网页功能

- **响应式设计**: 适配各种屏幕尺寸
- **图片灯箱**: 点击查看大图，支持键盘导航
- **搜索过滤**: 按日期快速查找
- **排序功能**: 最新/最旧排序切换
- **统计信息**: 显示日期数、故事数、最新日期

## 🛠️ 技术栈

- **后端**: Python 3.14+, Playwright
- **前端**: HTML5, CSS3, Vanilla JavaScript
- **版本控制**: Git
- **部署**: GitHub Pages

## 📝 注意事项

- 首次运行需要手动登录 Instagram
- 确保 Chrome 浏览器已安装
- Token 需要包含 `repo` 权限
- 建议在稳定的网络环境下运行

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供个人学习使用，请遵守 Instagram 的使用条款。

---

**所有内容属于 [@gianmarcoschiaretti](https://www.instagram.com/gianmarcoschiaretti/)，仅作个人归档使用。**
