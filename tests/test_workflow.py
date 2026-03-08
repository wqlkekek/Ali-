from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_end_to_end_workflow() -> None:
    payload = {
        "product_name": "智能保温杯",
        "category": "杯壶",
        "core_features": ["长效保温", "温度显示", "食品级材质"],
        "audience": ["上班族", "学生"],
        "usage_scenes": ["通勤", "办公室"],
        "price_range": "99-149",
        "brand_tone": "专业温暖",
        "platform": ["taobao", "jd"],
    }

    created = client.post("/product/input", json=payload)
    assert created.status_code == 200
    product_id = created.json()["product_id"]

    market = client.post(f"/market-data/{product_id}/collect")
    assert market.status_code == 200
    assert "search_trends" in market.json()["market_data"]

    generated = client.post(f"/content/{product_id}/generate")
    assert generated.status_code == 200
    content = generated.json()["content_asset"]
    assert content["primary_selling_point"]

    validated = client.post(f"/content/{product_id}/validate")
    assert validated.status_code == 200
    assert "passed" in validated.json()["compliance"]

    feedback = client.post(
        f"/feedback/{product_id}",
        json={"ctr": 0.12, "conversion_rate": 0.03, "bad_review_keywords": ["太重"]},
    )
    assert feedback.status_code == 200
    assert feedback.json()["data_feedback"]["ctr"] == 0.12
