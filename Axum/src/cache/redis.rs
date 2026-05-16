// src/cache/redis.rs
use deadpool_redis::{Config, CreatePoolError, Pool, Runtime};
use std::time::Duration;

pub fn init_redis_pool(
    url: &str,
    max_connections: usize,
    timeout_secs: u64,
) -> Result<Pool, Box<dyn std::error::Error>> {
    let cfg = Config::from_url(url);

    // تنظیم pool با builder pattern
    let pool = cfg
        .builder()?
        .max_size(max_connections)
        .wait_timeout(Some(Duration::from_secs(5)))
        .create_timeout(Some(Duration::from_secs(timeout_secs)))
        .recycle_timeout(Some(Duration::from_secs(timeout_secs)))
        .runtime(Runtime::Tokio1)
        .build()
        .map_err(CreatePoolError::Build)?;

    Ok(pool)
}
