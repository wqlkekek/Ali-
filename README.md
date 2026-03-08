# 电商自动化工作流软件（Codex 开发版 MVP）

基于你提供的方案实现了一个可运行的 FastAPI MVP，覆盖：

- 产品输入与标准化（`POST /product/input`）
- 市场数据抓取（MVP mock）（`POST /market-data/{product_id}/collect`）
- AI 内容生成（规则+模板版，可替换 GPT API）（`POST /content/{product_id}/generate`）
- 审核与合规校验（`POST /content/{product_id}/validate`）
- 内容中台查询（`GET /content/{product_id}`）
- 数据回流（`POST /feedback/{product_id}`）

## 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开：`http://127.0.0.1:8000/docs`

## 数据结构

核心数据结构位于 `app/schemas.py`，与需求文档中的 JSON 对齐。

## 后续接入建议

1. 将 `app/services/content_generator.py` 替换为真实 GPT-5 mini API 调用。
2. 将 `app/services/market_collector.py` 替换为官方 API 或爬虫聚合。
3. 将 `app/db.py` 内存存储替换为 MongoDB/PostgreSQL。
4. 在 `app/services/compliance.py` 增加规则引擎与人工审核工作流。
