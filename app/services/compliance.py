from __future__ import annotations

from app.schemas import ContentAsset


BANNED_WORDS = ["最", "国家级", "100%治愈", "绝对"]


def run_compliance_checks(asset: ContentAsset) -> dict:
    text_blob = " ".join(
        [
            asset.primary_selling_point,
            *asset.secondary_selling_points,
            *asset.ad_copy,
            asset.packaging_copy.front_title,
            asset.packaging_copy.subtitle,
            asset.detail_page_copy.first_screen_slogan,
        ]
    )

    hits = [w for w in BANNED_WORDS if w in text_blob]
    return {
        "passed": len(hits) == 0,
        "hit_words": hits,
        "message": "合规检查通过" if not hits else "存在潜在违规词，请人工复审",
    }
