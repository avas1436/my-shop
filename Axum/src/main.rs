pub mod cache {
    pub mod redis;
}
pub mod config;
pub mod db {
    pub mod postgres;
}
pub mod router;
pub mod state {
    pub mod app_state;
}
pub mod docs {
    pub mod openapi;
}
pub mod handlers {
    pub mod products;
}
pub mod services {
    pub mod product_service;
}
use config::Settings;
use state::app_state::AppState;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt::init();

    let cfg = Settings::from_env();

    let db = db::postgres::init_pool(
        &cfg.database_url,
        cfg.db_pool_size,
        cfg.db_max_overflow,
        cfg.db_pool_timeout,
        cfg.db_pool_recycle,
        cfg.db_pool_pre_ping,
    )
    .await
    .expect("Failed to create database pool");

    let redis = cache::redis::init_redis_pool(
        &cfg.redis_url,
        cfg.redis_max_connections,
        cfg.redis_socket_timeout,
    )
    .expect("Failed to create Redis pool");

    let state = AppState {
        db,
        redis,
        session_prefix: cfg.session_prefix.clone(),
    };

    let app = router::routes().with_state(state);

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    let serve_future = axum::serve(listener, app.into_make_service());

    if let Err(e) = serve_future.await {
        eprintln!("Server error: {}", e);
    }
}
