// src/dto/product.rs
use crate::models::enums::ProductStatus;
use crate::models::product::Product;
use bigdecimal::BigDecimal;
use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};
use utoipa::ToSchema;

#[derive(Debug, Serialize, Deserialize, ToSchema)] 
pub struct ProductDetailDto {
    pub id: i32,
    pub sku: String,
    pub slug: Option<String>,
    pub name: String,
    pub description: Option<String>,
    pub price: i32,
    pub discount_price: Option<i32>,
    pub cost_price: Option<i32>,
    pub tax_rate: i32,
    pub currency_code: String,
    pub status: ProductStatus,
    pub is_featured: bool,
    pub is_digital: bool,
    #[schema(value_type = String)]
    pub weight: Option<BigDecimal>,
    #[schema(value_type = String)]
    pub width: Option<BigDecimal>,
    #[schema(value_type = String)]
    pub height: Option<BigDecimal>,
    #[schema(value_type = String)]
    pub depth: Option<BigDecimal>,
    pub meta_title: Option<String>,
    pub meta_description: Option<String>,
    pub gtin: Option<String>,
    pub brand_id: Option<i32>,
    #[schema(value_type = String, format = DateTime)]
    pub created_at: DateTime<Utc>,
    #[schema(value_type = String, format = DateTime)]
    pub updated_at: Option<DateTime<Utc>>,
    #[schema(value_type = String, format = DateTime)]
    pub published_at: Option<DateTime<Utc>>,
}

impl From<Product> for ProductDetailDto {
    fn from(p: Product) -> Self {
        Self {
            id: p.id,
            sku: p.sku,
            slug: p.slug,
            name: p.name,
            description: p.description,
            price: p.price,
            discount_price: p.discount_price,
            cost_price: p.cost_price,
            tax_rate: p.tax_rate,
            currency_code: p.currency_code,
            status: p.status,
            is_featured: p.is_featured,
            is_digital: p.is_digital,
            weight: p.weight,
            width: p.width,
            height: p.height,
            depth: p.depth,
            meta_title: p.meta_title,
            meta_description: p.meta_description,
            gtin: p.gtin,
            brand_id: p.brand_id,
            created_at: p.created_at,
            updated_at: p.updated_at,
            published_at: p.published_at,
        }
    }
}
