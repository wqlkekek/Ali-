# 电商自动化工作流软件（Codex 开发版 MVP）

该项目已包含：

- FastAPI 后端 API
- 可视化前端页面（`/`）
- 端到端流程测试样例
- 超详细部署使用教程（见 `DEPLOYMENT_GUIDE.md`）

## 主要能力

- 产品输入与标准化（`POST /product/input`）
- 市场数据抓取（MVP mock）（`POST /market-data/{product_id}/collect`）
- AI 内容生成（模板版，可替换 GPT-5 mini API）（`POST /content/{product_id}/generate`）
- 审核与合规校验（`POST /content/{product_id}/validate`）
- 内容中台查询（`GET /content/{product_id}`）
- 数据回流（`POST /feedback/{product_id}`）

## 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后：

- 前端页面：`http://127.0.0.1:8000/`
- Swagger 文档：`http://127.0.0.1:8000/docs`


## macOS 一键启动

已提供一键启动脚本：

```bash
bash scripts/start_macos.sh
```

或在 Finder 中双击：`scripts/start_macos.command`。

脚本会自动完成：Python 版本检查、虚拟环境创建、依赖安装、端口检测、启动服务并尝试打开浏览器。

## 文档入口

- 傻瓜式部署教程：[`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md)

## 后续接入建议

1. 将 `app/services/content_generator.py` 替换为真实 GPT-5 mini API 调用。
2. 将 `app/services/market_collector.py` 替换为官方 API 或爬虫聚合。
3. 将 `app/db.py` 内存存储替换为 MongoDB/PostgreSQL。
4. 在 `app/services/compliance.py` 增加规则引擎与人工审核工作流。
