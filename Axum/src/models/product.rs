// src/models/product.rs
use crate::models::enums::ProductStatus;
use bigdecimal::BigDecimal;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Product {
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
    pub weight: Option<BigDecimal>,
    pub width: Option<BigDecimal>,
    pub height: Option<BigDecimal>,
    pub depth: Option<BigDecimal>,
    pub meta_title: Option<String>,
    pub meta_description: Option<String>,
    pub gtin: Option<String>,
    pub brand_id: Option<i32>,
    pub created_at: DateTime<Utc>,
    pub updated_at: Option<DateTime<Utc>>,
    pub published_at: Option<DateTime<Utc>>,
    pub deleted_at: Option<DateTime<Utc>>,
}
