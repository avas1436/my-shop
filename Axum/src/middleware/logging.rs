// src/middleware/logging.rs
use std::time::Instant;

use axum::{
    body::Body,
    extract::MatchedPath,
    // http::{Request, Response},
    http::Request,
    middleware::Next,
};
use tracing::{error, info};

pub async fn logging_middleware(req: Request<Body>, next: Next) -> axum::response::Response {
    let start = Instant::now();

    let method = req.method().clone();

    // مسیر matched را بگیر (اگر وجود داشت)
    let matched_path = req
        .extensions()
        .get::<MatchedPath>()
        .map(|m| m.as_str().to_string());

    // اگر matched نبود، از uri استفاده کن
    let path = matched_path.unwrap_or_else(|| req.uri().path().to_string());

    // path را در extensions نگه می‌داریم
    let mut req = req;
    req.extensions_mut().insert(path.clone());

    let res = next.run(req).await;

    let status = res.status();
    let latency = start.elapsed().as_millis();

    if status.is_server_error() {
        error!(%method, %path, %status, latency_ms = latency, "request failed");
    } else {
        info!(%method, %path, %status, latency_ms = latency, "request served");
    }

    res
}
