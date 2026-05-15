// src/cache/redis.rs
use deadpool_redis::{Config, Pool, Runtime};

pub fn init_redis_pool(
    url: &str,
    max_connections: usize,
) -> Result<Pool, deadpool_redis::CreatePoolError> {
    let mut cfg = Config::from_url(url);

    cfg.pool.max_size = max_connections;

    cfg.create_pool(Some(Runtime::Tokio1))
}
