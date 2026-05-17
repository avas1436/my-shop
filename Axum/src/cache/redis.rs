// src/cache/redis.rs
use std::time::Duration;

use deadpool_redis::{
    redis::AsyncCommands,
    Config, Pool, Runtime,
};

use crate::errors::errors::AppError;

pub fn init_redis_pool(
    url: &str,
    max_connections: usize,
    timeout_secs: u64,
) -> Result<Pool, AppError> {
    let cfg = Config::from_url(url);

    // تنظیم pool با builder pattern
    let pool = cfg
        .builder()
        .map_err(|e| AppError::Cache {
            message: format!("failed to create redis pool builder: {e}"),
            code: Some("REDIS_POOL_BUILDER_ERROR".to_string()),
            details: None,
            path: None,
        })?
        .max_size(max_connections)
        .wait_timeout(Some(Duration::from_secs(5)))
        .create_timeout(Some(Duration::from_secs(timeout_secs)))
        .recycle_timeout(Some(Duration::from_secs(timeout_secs)))
        .runtime(Runtime::Tokio1)
        .build()
        .map_err(|e| AppError::Cache {
            message: format!("failed to build redis pool: {e}"),
            code: Some("REDIS_POOL_BUILD_ERROR".to_string()),
            details: None,
            path: None,
        })?;

    Ok(pool)
}

#[derive(Clone)]
pub struct RedisClient {
    pub pool: Pool,
}

impl RedisClient {
    pub fn new(pool: Pool) -> Self {
        Self { pool }
    }

    pub async fn get(&self, key: &str) -> Result<Option<String>, AppError> {
        let mut conn = self.pool.get().await.map_err(|e| AppError::Cache {
            message: format!("failed to get redis connection from pool: {e}"),
            code: Some("REDIS_POOL_GET_ERROR".to_string()),
            details: None,
            path: None,
        })?;

        let value: Option<String> = conn.get(key).await.map_err(|e| AppError::Cache {
            message: format!("redis GET error for key `{key}`: {e}"),
            code: Some("REDIS_GET_ERROR".to_string()),
            details: None,
            path: None,
        })?;

        Ok(value)
    }

    pub async fn set_ex(&self, key: &str, value: String, ttl: u64) -> Result<(), AppError> {
        let mut conn = self.pool.get().await.map_err(|e| AppError::Cache {
            message: format!("failed to get redis connection from pool: {e}"),
            code: Some("REDIS_POOL_GET_ERROR".to_string()),
            details: None,
            path: None,
        })?;

        let _: () = conn.set_ex(key, value, ttl).await.map_err(|e| AppError::Cache {
            message: format!("redis SETEX error for key `{key}`: {e}"),
            code: Some("REDIS_SETEX_ERROR".to_string()),
            details: None,
            path: None,
        })?;

        Ok(())
    }

    // pub async fn del(&self, key: &str) -> Result<(), AppError> {
    //     let mut conn = self.pool.get().await.map_err(|e| AppError::Cache {
    //         message: format!("failed to get redis connection from pool: {e}"),
    //         code: Some("REDIS_POOL_GET_ERROR".to_string()),
    //         details: None,
    //         path: None,
    //     })?;

    //     let _: usize = conn.del(key).await.map_err(|e| AppError::Cache {
    //         message: format!("redis DEL error for key `{key}`: {e}"),
    //         code: Some("REDIS_DEL_ERROR".to_string()),
    //         details: None,
    //         path: None,
    //     })?;

    //     Ok(())
    // }
}

