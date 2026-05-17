// src/docs/openapi.rs 
use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(paths(crate::handlers::product::get_products))]
pub struct ApiDoc;
