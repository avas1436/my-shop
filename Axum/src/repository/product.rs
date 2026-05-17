// src/repository/product.rs
use crate::models::enums::ProductStatus;
use crate::models::product::Product;
use sqlx::PgPool;

#[derive(Clone)]
pub struct ProductRepository {
    pub pool: PgPool,
}

impl ProductRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn find_by_id(&self, id: i32) -> Result<Option<Product>, sqlx::Error> {
        let product = sqlx::query_as!(
            Product,
            r#"
            SELECT
            id,
            sku,
            slug,
            name,
            description,
            price,
            discount_price,
            cost_price,
            tax_rate,
            currency_code,
            status as "status: ProductStatus",
            is_featured,
            is_digital,
            weight,
            width,
            height,
            depth,
            meta_title,
            meta_description,
            gtin,
            brand_id,
            created_at,
            updated_at,
            published_at,
            deleted_at
            FROM products
            WHERE id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(product)
    }
}
