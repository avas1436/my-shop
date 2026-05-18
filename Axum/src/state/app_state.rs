// src/state/app_state.rs 
use crate::{cache::redis::RedisClient};
use sqlx::PgPool;

#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
    pub redis: RedisClient,
    pub session_prefix: String,
}
