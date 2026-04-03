# home.baizx.cool

一个基于 Hugo 的单页学术主页，包含：

- 自我介绍、研究兴趣、联系方式与论文列表同页展示
- 系统深浅色自动同步
- 基于 ORCID 数据生成的动态图表
- GitHub Actions 定期同步 ORCID 论文
- GitHub Pages 与 Vercel 双部署

## 本地开发

```bash
hugo server
```

## 手动同步 ORCID

```bash
python scripts/fetch_orcid.py --orcid-id 0009-0005-5135-5594
```

## 部署说明

- GitHub Pages: 使用 `.github/workflows/deploy.yml`
- ORCID 定时同步: 使用 `.github/workflows/update-orcid.yml`
- 自定义域名: `home.baizx.cool`
- Vercel: 直接导入该仓库，Framework Preset 选择 `Hugo`
