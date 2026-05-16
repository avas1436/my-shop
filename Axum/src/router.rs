// src/router.rs

use crate::docs::openapi::ApiDoc;
use crate::handlers::products::get_products;
use crate::state::app_state::AppState;
use axum::{routing::get, Router};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

pub fn routes() -> Router<AppState> {
    Router::new()
        .merge(SwaggerUi::new("/swagger").url("/api-doc/openapi.json", ApiDoc::openapi()))
        .route("/products", get(get_products))
}
