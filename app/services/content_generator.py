from __future__ import annotations

from app.schemas import ContentAsset, DetailPageCopy, PackagingCopy, ProductInput


def generate_content_asset(product: ProductInput, market_data: dict) -> ContentAsset:
    primary = product.core_features[0] if product.core_features else "高品质体验"
    secondary = product.core_features[1:4] if len(product.core_features) > 1 else ["高性价比", "易上手"]

    packaging = PackagingCopy(
        front_title=f"{product.product_name} · {primary}",
        subtitle=f"为{','.join(product.audience) or '目标人群'}打造",
        three_short_points=secondary[:3],
        back_description=f"聚焦{product.usage_scenes[0] if product.usage_scenes else '日常使用'}场景，兼顾性能与体验。",
        instructions="开箱后按说明安装并进行首次调试。",
        precautions="避免高温潮湿环境，远离火源。",
        brand_story=f"我们坚持{product.brand_tone}风格，持续打磨用户体验。",
    )

    detail_page = DetailPageCopy(
        first_screen_slogan=f"{product.product_name}：{primary}，一步到位",
        pain_point_intro="你是否也遇到功能复杂、效果不稳定、选择成本高的问题？",
        feature_modules=[
            {"title": feat, "description": f"围绕{feat}进行专项优化，提升转化。"}
            for feat in product.core_features[:4]
        ],
        usage_scenes_display=product.usage_scenes,
        parameters_display=[
            {"name": "价格带", "value": product.price_range},
            {"name": "目标人群", "value": " / ".join(product.audience)},
        ],
        comparison_module=[
            {"dimension": "核心卖点", "ours": primary, "others": "泛化描述"},
            {"dimension": "品牌语调", "ours": product.brand_tone, "others": "无明显调性"},
        ],
        faq=[
            {"q": "是否适合新手？", "a": "是，开箱即可按图文快速上手。"},
            {"q": "是否支持售后？", "a": "支持7天无忧退换和在线客服。"},
        ],
        after_sales_commitment="7天无忧退换，1对1客服支持。",
    )

    platform_versions = {
        p: {
            "title": f"[{p.upper()}] {product.product_name}",
            "highlights": [primary, *secondary],
            "description": f"结合市场反馈：{','.join(market_data.get('review_keywords', []))}",
        }
        for p in (product.platform or ["taobao", "jd", "douyin"])
    }

    return ContentAsset(
        product_name=product.product_name,
        category=product.category,
        core_features=product.core_features,
        audience=product.audience,
        usage_scenes=product.usage_scenes,
        price_range=product.price_range,
        brand_tone=product.brand_tone,
        primary_selling_point=primary,
        secondary_selling_points=secondary,
        packaging_copy=packaging,
        detail_page_copy=detail_page,
        platform_versions=platform_versions,
        ad_copy=[
            f"{product.product_name}，{primary}，现在入手更划算！",
            f"{product.product_name}：{product.brand_tone}风格爆款，限时抢购。",
        ],
    )
