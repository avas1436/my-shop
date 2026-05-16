use deadpool_redis::Pool;
use sqlx::PgPool;

#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
    pub redis: Pool,
    pub session_prefix: String,
}
