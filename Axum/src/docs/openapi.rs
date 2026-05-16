use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(paths(crate::handlers::products::get_products))]
pub struct ApiDoc;
