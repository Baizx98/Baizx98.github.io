# home.baizx.cool

一个基于 Hugo 的单页学术主页模板，包含：

- 个人介绍、研究兴趣、联系方式与论文列表同页展示
- 自动适配系统深浅色
- 基于 ORCID 数据生成的论文趋势图
- GitHub Actions 定期同步 ORCID 论文
- 可部署到 GitHub Pages 或 Vercel

## 项目结构

- `hugo.toml`: 站点配置与个人信息
- `layouts/index.html`: 单页首页模板
- `static/styles/main.css`: 页面样式
- `static/scripts/site.js`: 前端图表逻辑
- `data/orcid.json`: ORCID 同步后的论文数据
- `scripts/fetch_orcid.py`: 拉取 ORCID 数据的脚本
- `.github/workflows/deploy.yml`: GitHub Pages 部署工作流
- `.github/workflows/update-orcid.yml`: ORCID 定时同步工作流
- `vercel.json`: Vercel 构建配置

## 前置要求

- Hugo Extended `0.147.2` 或更高
- Python `3.12` 或更高
- 一个公开可访问的 ORCID 账号
- 一个 GitHub 仓库
- 可选：一个 Vercel 账号

## 本地开发

安装 Hugo 和 Python 后，执行：

```bash
hugo server
```

默认本地预览地址：

```text
http://localhost:1313
```

如果你修改了 ORCID 相关信息，先手动更新数据：

```bash
python3 scripts/fetch_orcid.py --orcid-id 0009-0005-5135-5594
```

## 修改个人信息

主要修改这些文件：

- `hugo.toml`
  - 姓名、研究方向、简介、链接
- `data/orcid.json`
  - 不建议手改，通常由脚本自动生成
- `layouts/index.html`
  - 页面结构
- `static/styles/main.css`
  - 页面样式

如果你要替换成自己的 ORCID：

1. 修改 `hugo.toml` 中的：
   - `orcid`
   - `orcid_id`
2. 修改 `.github/workflows/update-orcid.yml` 中的：
   - `ORCID_ID`
3. 运行一次：

```bash
python3 scripts/fetch_orcid.py --orcid-id 你的_ORCID_ID
```

## 部署到 GitHub Pages

这个仓库已经内置了 GitHub Pages 工作流：`.github/workflows/deploy.yml`

### 步骤

1. 将仓库推送到 GitHub。
2. 打开 GitHub 仓库设置。
3. 进入 `Settings -> Pages`。
4. 在 `Source` 里选择 `GitHub Actions`。
5. 确保默认分支是你实际使用的分支，例如 `master` 或 `main`。
6. 推送代码后，GitHub 会自动执行部署。

### 触发方式

- 推送到 `master`
- 推送到 `main`
- 手动执行 `Deploy Hugo Site`

## ORCID 自动同步

这个仓库已经内置了 ORCID 同步工作流：`.github/workflows/update-orcid.yml`

### 功能

- 每周自动从 ORCID 拉取最新论文
- 有变更时自动提交 `data/orcid.json`

### 触发方式

- 推送到 `master`
- 推送到 `main`
- 手动执行 `Sync ORCID Publications`
- 定时任务：每周一 `03:17 UTC`

### 本地手动同步

```bash
python3 scripts/fetch_orcid.py --orcid-id 0009-0005-5135-5594
```

## 部署到 Vercel

这个仓库同样可以直接部署到 Vercel。

### 步骤

1. 在 Vercel 中导入这个 GitHub 仓库。
2. Framework 可以选择 `Other` 或 `Hugo`。
3. 确认项目根目录是仓库根目录。
4. 确认构建配置：

```text
Build Command: hugo --gc --minify
Output Directory: public
```

5. 在 Vercel 项目环境变量中显式添加：

```text
HUGO_VERSION=0.147.2
HUGO_ENV=production
```

建议同时勾选：

- Production
- Preview

### 为什么要手动设置 `HUGO_VERSION`

某些情况下，Vercel 可能不会正确使用仓库里的 Hugo 配置，导致：

- 页面信息显示不完整
- `hugo.toml` 中的参数不生效
- 构建日志出现 taxonomy 相关 warning

手动设置 `HUGO_VERSION=0.147.2` 后通常就会恢复正常。

## 自定义域名

当前配置中自定义域名是：

```text
home.baizx.cool
```

如果你要使用自己的域名：

1. 修改 `hugo.toml` 中的 `baseURL`
2. 修改 `static/CNAME`
3. 在 GitHub Pages 或 Vercel 中绑定对应域名
4. 配置 DNS

## GitHub Pages 和 Vercel 如何同时使用

推荐只让一个平台作为正式生产站点，另一个作为备用镜像。

建议做法：

- `home.baizx.cool` 指向 Vercel
- GitHub Pages 使用默认域名作为备用

或者：

- `home.baizx.cool` 指向 GitHub Pages
- Vercel 只保留预览部署

不建议让同一个正式域名同时承担两个平台的生产入口。

## 常见问题

### 1. Vercel 页面和本地 / GitHub Pages 不一致

优先检查：

- Vercel 项目绑定的分支是否正确
- 是否使用了最新提交
- `HUGO_VERSION` 是否在 Vercel 中显式设置
- 是否触发过 `Redeploy without cache`

### 2. GitHub Actions 没有自动执行

检查工作流监听的分支是否和你的默认分支一致。

当前仓库已经监听：

- `master`
- `main`

### 3. ORCID 数据没有更新

先手动执行：

```bash
python3 scripts/fetch_orcid.py --orcid-id 你的_ORCID_ID
```

再检查：

- ORCID 资料是否公开
- `ORCID_ID` 是否填写正确
- GitHub Actions 是否成功运行

## 一键上手建议

如果你是第一次使用这个模板，推荐按下面顺序操作：

1. 修改 `hugo.toml` 中的个人信息
2. 修改 ORCID 账号信息
3. 本地执行：

```bash
python3 scripts/fetch_orcid.py --orcid-id 你的_ORCID_ID
hugo server
```

4. 推送到 GitHub
5. 打开 GitHub Pages
6. 如果需要，再接入 Vercel

