// src/router.rs
use crate::docs::openapi::ApiDoc;
use crate::handlers::product::{get_product_detail, get_products};
use crate::state::app_state::AppState;
use axum::{routing::get, Router, middleware};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

pub fn routes() -> Router<AppState> {
    Router::new()
        .merge(SwaggerUi::new("/swagger").url("/api-doc/openapi.json", ApiDoc::openapi()))
        .route("/products", get(get_products))
        .route("/product/{id}", get(get_product_detail))
        .layer(middleware::from_fn(crate::middleware::logging::logging_middleware)) 
}
