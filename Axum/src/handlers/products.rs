use crate::services::product_service;
use crate::state::app_state::AppState;
use axum::{extract::State, Json};

#[utoipa::path(
    get,
    path = "/products",
    responses(
        (status = 200, description = "List products")
    )
)]
pub async fn get_products(State(state): State<AppState>) -> Json<Vec<String>> {
    let products = product_service::get_products(&state).await;

    Json(products)
}
