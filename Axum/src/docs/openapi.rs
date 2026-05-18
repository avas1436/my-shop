#![cfg(feature = "openapi")]
// src/docs/openapi.rs 
use utoipa::OpenApi;



#[derive(OpenApi)]
#[openapi(
    paths(
        crate::handlers::product::get_products,
        crate::handlers::product::get_product_detail,
    ),
    components(
        schemas(
            crate::dto::product::ProductDetailDto,
        )
    )
)]
pub struct ApiDoc;
