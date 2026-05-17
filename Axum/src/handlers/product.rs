// src/handlers/product.rs
use crate::{
    errors::errors::AppError, response::api_response::ApiResponse, services::product,
    state::app_state::AppState,
};
use axum::{extract::Path, extract::State, http::StatusCode};

#[utoipa::path(
    get,
    path = "/products",
    responses(
        (status = 200, description = "List of products")
    )
)]
pub async fn get_products() -> Result<ApiResponse<()>, AppError> {
    Ok(ApiResponse::success(StatusCode::OK, (), "/products".to_string()))
}


#[utoipa::path(
    get,
    path = "/product/{id}",
    responses(
        (status = 200, description = "Product Detail")
    )
)]
pub async fn get_product_detail(
    Path(id): Path<i32>,
    State(state): State<AppState>,
    uri: axum::http::Uri,
) -> Result<ApiResponse<crate::dto::product::ProductDetailDto>, AppError> {
    let product = product::get_product_by_id(&state, id).await?;

    Ok(ApiResponse::success(
        StatusCode::OK,
        product,
        uri.path().to_string(),
    ))
}
