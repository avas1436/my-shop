// src/services/product.rs
use crate::{dto::product::ProductDetailDto, errors::errors::AppError, state::app_state::AppState, repository::product::ProductRepository};
use tracing::error;

pub async fn get_product_by_id(
    state: &AppState,
    product_id: i32,
) -> Result<ProductDetailDto, AppError> {
    let cache_key = format!("product:detail:{product_id}");

    // check redis
    if let Some(cached) = state
        .redis
        .get(&cache_key)
        .await
        .map_err(|_| AppError::cache("redis get failed"))?
    {
        let product: ProductDetailDto = serde_json::from_str(&cached)
            .map_err(|_| AppError::internal("failed to decode cached product"))?;
        return Ok(product);
    }

    // build repo from shared app pool 
    let repo = ProductRepository::new(state.db.clone());

    // fetch from db
    let product = repo
        .find_by_id(product_id)
        .await
        .map_err(|e| {
            error!(
                product_id = %product_id,
                ?e,
                "db error while fetching product"
            );
            AppError::db("db error while fetching product")
        })?
        .ok_or_else(|| AppError::not_found("product not found"))?;

    let dto = ProductDetailDto::from(product);

    // cache result
    let json =
        serde_json::to_string(&dto).map_err(|_| AppError::internal("failed to encode product"))?;
    state
        .redis
        .set_ex(&cache_key, json, 3600)
        .await
        .map_err(|_| AppError::cache("redis set failed"))?;

    Ok(dto)
}
