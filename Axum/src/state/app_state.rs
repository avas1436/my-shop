// src/state/app_state.rs 
use crate::{cache::redis::RedisClient, repository::product::ProductRepository};
use sqlx::PgPool;

#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
    pub redis: RedisClient,
    pub product_repo: ProductRepository,
    pub session_prefix: String,
}
