from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.db import store
from app.schemas import ProductInput, ProductRecord
from app.services.compliance import run_compliance_checks
from app.services.content_generator import generate_content_asset
from app.services.market_collector import collect_market_data

app = FastAPI(title="E-commerce Automation Workflow API", version="0.1.0")


class ProductInputResponse(BaseModel):
    product_id: str
    message: str


class FeedbackPayload(BaseModel):
    ctr: float | None = None
    conversion_rate: float | None = None
    favorites: int | None = None
    return_rate: float | None = None
    bad_review_keywords: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/product/input", response_model=ProductInputResponse)
def product_input(payload: ProductInput) -> ProductInputResponse:
    product_id = str(uuid4())
    record = ProductRecord(product_id=product_id, input_data=payload)
    store.put(record)
    return ProductInputResponse(product_id=product_id, message="产品信息已录入")


@app.post("/market-data/{product_id}/collect")
def market_data_collect(product_id: str) -> dict:
    record = store.get(product_id)
    if not record:
        raise HTTPException(status_code=404, detail="产品不存在")

    record.market_data = collect_market_data(record.input_data)
    store.update(product_id, record)
    return {"product_id": product_id, "market_data": record.market_data}


@app.post("/content/{product_id}/generate")
def content_generate(product_id: str) -> dict:
    record = store.get(product_id)
    if not record:
        raise HTTPException(status_code=404, detail="产品不存在")

    if not record.market_data:
        record.market_data = collect_market_data(record.input_data)

    record.content_asset = generate_content_asset(record.input_data, record.market_data)
    store.update(product_id, record)
    return {
        "product_id": product_id,
        "content_asset": record.content_asset.model_dump(),
    }


@app.post("/content/{product_id}/validate")
def content_validate(product_id: str) -> dict:
    record = store.get(product_id)
    if not record or not record.content_asset:
        raise HTTPException(status_code=404, detail="内容资产不存在")

    report = run_compliance_checks(record.content_asset)
    record.compliance_report = report
    store.update(product_id, record)
    return {"product_id": product_id, "compliance": report}


@app.get("/content/{product_id}")
def get_content(product_id: str) -> dict:
    record = store.get(product_id)
    if not record:
        raise HTTPException(status_code=404, detail="产品不存在")

    return record.model_dump()


@app.post("/feedback/{product_id}")
def collect_feedback(product_id: str, payload: FeedbackPayload) -> dict:
    record = store.get(product_id)
    if not record or not record.content_asset:
        raise HTTPException(status_code=404, detail="内容资产不存在")

    record.content_asset.data_feedback = payload.model_dump()
    store.update(product_id, record)
    return {"product_id": product_id, "data_feedback": record.content_asset.data_feedback}
