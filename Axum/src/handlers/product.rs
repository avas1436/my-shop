// src/handlers/product.rs
use crate::{
    errors::errors::AppError, response::api_response::ApiResponse, services::product,
    state::app_state::AppState, dto::product::ProductDetailDto
};
use axum::{extract::Path, extract::State, http::StatusCode};

#[cfg_attr(feature = "openapi", utoipa::path(
    get,
    path = "/products",
    responses(
        (status = 200, description = "List of products")
    )
))]
pub async fn get_products() -> Result<ApiResponse<()>, AppError> {
    Ok(ApiResponse::success(StatusCode::OK, (), "/products".to_string()))
}


#[cfg_attr(feature = "openapi", utoipa::path(
    get,
    path = "/product/{id}",
    responses(
        (status = 200, description = "Product Detail", body = ProductDetailDto)
    )
))]
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
