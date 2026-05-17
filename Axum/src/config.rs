// src/config.rs
use std::env;

#[derive(Clone, Debug)]
pub struct Settings {
    pub database_url: String,
    // pub sql_echo: bool,
    pub db_pool_size: u32,
    pub db_max_overflow: u32,
    pub db_pool_timeout: u64,
    pub db_pool_recycle: u64,
    pub db_pool_pre_ping: bool,

    pub redis_url: String,
    pub redis_max_connections: usize,
    pub redis_socket_timeout: u64,
    pub session_prefix: String,
}

impl Settings {
    pub fn from_env() -> Self {
        Self {
            database_url: env::var("DATABASE_URL").unwrap(),

            //  در این قسمت اگر مقدار در فایل محیطی صحیح باشد این مقدار هم صحیح میشود در غیر این صورت همیشه غلط است
            // sql_echo: env::var("SQL_ECHO").unwrap_or("false".into()) == "true",

            db_pool_size: env::var("DB_POOL_SIZE")
                .unwrap_or("5".into())
                .parse()
                .unwrap(),

            db_max_overflow: env::var("DB_MAX_OVERFLOW")
                .unwrap_or("10".into())
                .parse()
                .unwrap(),

            db_pool_timeout: env::var("DB_POOL_TIMEOUT")
                .unwrap_or("15".into())
                .parse()
                .unwrap(),

            db_pool_recycle: env::var("DB_POOL_RECYCLE")
                .unwrap_or("1800".into())
                .parse()
                .unwrap(),

            db_pool_pre_ping: env::var("DB_POOL_PRE_PING").unwrap_or("true".into()) == "true",

            redis_url: env::var("REDIS_URL").unwrap(),

            redis_max_connections: env::var("REDIS_MAX_CONNECTIONS")
                .unwrap_or("10".into())
                .parse()
                .unwrap(),

            redis_socket_timeout: env::var("REDIS_SOCKET_TIMEOUT")
                .unwrap_or("5".into())
                .parse()
                .unwrap(),

            session_prefix: env::var("SESSION_PREFIX").unwrap_or("shop:".into()),
        }
    }
}
