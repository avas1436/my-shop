// src/router.rs
#[cfg(feature = "openapi")]
use crate::docs::openapi::ApiDoc;
use crate::handlers::product::{get_product_detail, get_products};
use crate::state::app_state::AppState;
use axum::{routing::get, Router, middleware};

#[cfg(feature = "openapi")]
use utoipa::OpenApi;
#[cfg(feature = "openapi")]
use utoipa_swagger_ui::SwaggerUi;

pub fn routes() -> Router<AppState> {
    let app = Router::new()
        .route("/products", get(get_products))
        .route("/product/{id}", get(get_product_detail))
        .layer(middleware::from_fn(crate::middleware::logging::logging_middleware));

    #[cfg(feature = "openapi")]
    let app = app.merge(SwaggerUi::new("/swagger").url("/api-doc/openapi.json", ApiDoc::openapi()));

    app
    }
