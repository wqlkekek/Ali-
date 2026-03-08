from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PackagingCopy(BaseModel):
    front_title: str = ""
    subtitle: str = ""
    three_short_points: list[str] = Field(default_factory=list)
    back_description: str = ""
    instructions: str = ""
    precautions: str = ""
    brand_story: str = ""


class DetailPageCopy(BaseModel):
    first_screen_slogan: str = ""
    pain_point_intro: str = ""
    feature_modules: list[dict[str, Any]] = Field(default_factory=list)
    usage_scenes_display: list[str] = Field(default_factory=list)
    parameters_display: list[dict[str, Any]] = Field(default_factory=list)
    comparison_module: list[dict[str, Any]] = Field(default_factory=list)
    faq: list[dict[str, str]] = Field(default_factory=list)
    after_sales_commitment: str = ""


class ProductInput(BaseModel):
    product_name: str
    category: str
    core_features: list[str] = Field(default_factory=list)
    audience: list[str] = Field(default_factory=list)
    usage_scenes: list[str] = Field(default_factory=list)
    price_range: str
    brand_tone: str
    platform: list[str] = Field(default_factory=list)


class ContentAsset(BaseModel):
    product_name: str
    category: str
    core_features: list[str] = Field(default_factory=list)
    audience: list[str] = Field(default_factory=list)
    usage_scenes: list[str] = Field(default_factory=list)
    price_range: str = ""
    brand_tone: str = ""
    primary_selling_point: str = ""
    secondary_selling_points: list[str] = Field(default_factory=list)
    packaging_copy: PackagingCopy = Field(default_factory=PackagingCopy)
    detail_page_copy: DetailPageCopy = Field(default_factory=DetailPageCopy)
    platform_versions: dict[str, dict[str, Any]] = Field(default_factory=dict)
    ad_copy: list[str] = Field(default_factory=list)
    data_feedback: dict[str, Any] = Field(default_factory=dict)


class ProductRecord(BaseModel):
    product_id: str
    input_data: ProductInput
    market_data: dict[str, Any] = Field(default_factory=dict)
    content_asset: ContentAsset | None = None
    compliance_report: dict[str, Any] = Field(default_factory=dict)
