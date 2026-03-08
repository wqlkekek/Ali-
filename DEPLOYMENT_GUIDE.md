# 电商自动化工作流系统：超详细傻瓜式部署与使用教程

> 适合完全没有后端经验的同学。你只需要照着步骤点、复制、粘贴即可。

---

## 0. 你将获得什么

部署完成后，你会有：

1. 一个后端 API 服务（FastAPI）
2. 一个可视化前端页面（浏览器打开即可操作）
3. 一条完整流程：
   - 录入产品
   - 抓取市场数据
   - 生成内容资产
   - 合规校验
   - 数据回流

---

## 1. 准备环境（Linux / macOS）

### 1.1 检查 Python 版本

在项目根目录执行：

```bash
python --version
```

如果输出是 `Python 3.10+` 即可。

### 1.2 进入项目目录

```bash
cd /workspace/Ali-
```

---

## 2. 创建虚拟环境（强烈推荐）

### 2.1 创建

```bash
python -m venv .venv
```

### 2.2 激活

```bash
source .venv/bin/activate
```

激活后，终端前面通常会出现 `(.venv)`。

---

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

如果你网络受限（例如公司代理），可能安装失败。你可以：

1. 使用可联网环境安装；
2. 配置 pip 镜像源（如阿里云镜像）；
3. 让运维开放 PyPI 出口。

---

## 4. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

你看到以下类似信息说明成功：

- `Application startup complete`
- `Uvicorn running on http://0.0.0.0:8000`

---


## 4.1 macOS 一键启动（最省事）

如果你是 macOS 用户，推荐直接执行：

```bash
bash scripts/start_macos.sh
```

或者双击 `scripts/start_macos.command`。

脚本会自动做这些事：

1. 检查 Python3 是否存在且版本 >= 3.10
2. 自动创建 `.venv`（若不存在）
3. 自动升级 pip 并安装 `requirements.txt`
4. 默认使用 8000 端口，若占用则自动切换到 8010
5. 自动启动 Uvicorn 并尝试打开浏览器

## 5. 打开页面

浏览器访问：

- 前端控制台：`http://127.0.0.1:8000/`
- API 文档（Swagger）：`http://127.0.0.1:8000/docs`

---

## 6. 前端页面怎么用（一步一步）

打开前端后按下面顺序点击：

### 步骤 A：提交产品信息

1. 在「1) 产品输入」中填写字段（已预置示例）。
2. 点击 **提交产品信息**。
3. 页面会显示一个 `product_id`。

### 步骤 B：抓取市场数据

1. 点击 **抓取市场数据**。
2. 下方响应会出现 `competitor_summary / review_keywords / search_trends`。

### 步骤 C：生成内容资产

1. 点击 **生成内容资产**。
2. 响应里会出现：
   - `primary_selling_point`
   - `packaging_copy`
   - `detail_page_copy`
   - `platform_versions`

### 步骤 D：合规校验

1. 点击 **执行合规校验**。
2. 响应会给出：
   - `passed`（是否通过）
   - `hit_words`（命中词）

### 步骤 E：提交数据回流

1. 填写 CTR、转化率、收藏数、退货率、差评词。
2. 点击 **提交反馈数据**。
3. 系统会把这些数据写入 `data_feedback`，用于后续自动优化。

### 步骤 F：查询完整记录

1. 点击 **查询完整记录**。
2. 可一次性查看该商品全生命周期数据。

---

## 7. 用 API 文档手工调试（可选）

进入 `http://127.0.0.1:8000/docs`：

1. 找到 `POST /product/input`，点 `Try it out`
2. 填 JSON 并执行
3. 把返回的 `product_id` 用到后续接口

推荐顺序：

1. `/product/input`
2. `/market-data/{product_id}/collect`
3. `/content/{product_id}/generate`
4. `/content/{product_id}/validate`
5. `/feedback/{product_id}`
6. `/content/{product_id}`

---

## 8. 常见报错与解决方案

### 报错：`ModuleNotFoundError: fastapi`

原因：依赖未安装。重新执行：

```bash
pip install -r requirements.txt
```

### 报错：`Address already in use`

原因：8000 端口被占用。

解决：换端口启动，例如：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```

然后访问 `http://127.0.0.1:8010/`。

### 报错：接口 404

原因：可能 `product_id` 不存在，或者顺序没走完。

解决：先重新提交产品信息，得到新 `product_id`，再依顺序操作。

---

## 9. 生产部署建议（上线前必须做）

1. 把 `app/db.py` 的内存存储替换成 MongoDB / PostgreSQL。
2. 在 `app/services/content_generator.py` 接入真实 GPT-5 mini API。
3. 在 `app/services/market_collector.py` 接入真实爬虫/API。
4. 增加鉴权（JWT/API Key）、限流、日志、审计。
5. 用 Nginx + Gunicorn/Uvicorn 多进程部署。
6. 使用 HTTPS 与安全组白名单。

---

## 10. 一条命令快速体验（仅本地）

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

运行后直接打开 `http://127.0.0.1:8000/`。
