use sqlx::{postgres::PgPoolOptions, PgPool};
use std::time::Duration;

pub async fn init_pool(
    url: &str,
    pool_size: u32,
    max_overflow: u32,
    timeout_secs: u64,
    recycle_secs: u64,
    pre_ping: bool,
) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(pool_size + max_overflow)
        .min_connections(pool_size)
        .acquire_timeout(Duration::from_secs(timeout_secs))
        .max_lifetime(Some(Duration::from_secs(recycle_secs)))
        .test_before_acquire(pre_ping)
        .connect(url)
        .await
}
