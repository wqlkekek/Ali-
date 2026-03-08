from __future__ import annotations

from datetime import datetime

from app.schemas import ProductInput


def collect_market_data(product: ProductInput) -> dict:
    """MVP mock collector: in production replace with crawler/API integrations."""
    return {
        "competitor_summary": [
            f"同类{product.category}头部商品强调{feature}" for feature in product.core_features[:3]
        ],
        "review_keywords": ["性价比", "耐用", "体验好"],
        "search_trends": [f"{product.product_name} 推荐", f"{product.category} 哪个好"],
        "social_trends": ["开箱测评", "真实使用场景"],
        "collected_at": datetime.utcnow().isoformat(),
    }
