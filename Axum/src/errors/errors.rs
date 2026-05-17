// src/errors/errors.rs
use axum::{
    // extract::MatchedPath,
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
// use serde_json::json;

use crate::response::api_response::ApiResponse;

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("resource not found")]
    NotFound {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },

    #[error("bad request")]
    BadRequest {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },

    #[error("validation error")]
    Validation {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },

    #[error("database error")]
    Db {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },

    #[error("cache error")]
    Cache {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },

    #[error("internal server error")]
    Internal {
        message: String,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: Option<String>,
    },
}

impl AppError {
    pub fn with_path(mut self, req_path: impl Into<String>) -> Self {
        let p = Some(req_path.into());
        match &mut self {
            AppError::NotFound { path, .. }
            | AppError::BadRequest { path, .. }
            | AppError::Validation { path, .. }
            | AppError::Db { path, .. }
            | AppError::Cache { path, .. }
            | AppError::Internal { path, .. } => {
                *path = p;
            }
        }
        self
    }

    pub fn not_found(message: impl Into<String>) -> Self {
        Self::NotFound {
            message: message.into(),
            code: None,
            details: None,
            path: None,
        }
    }

    pub fn bad_request(message: impl Into<String>) -> Self {
        Self::BadRequest {
            message: message.into(),
            code: None,
            details: None,
            path: None,
        }
    }

    pub fn validation(message: impl Into<String>, details: Option<serde_json::Value>) -> Self {
        Self::Validation {
            message: message.into(),
            code: None,
            details,
            path: None,
        }
    }

    pub fn internal(message: impl Into<String>) -> Self {
        Self::Internal {
            message: message.into(),
            code: None,
            details: None,
            path: None,
        }
    }

    pub fn db(message: impl Into<String>) -> Self {
        Self::Db {
            message: message.into(),
            code: None,
            details: None,
            path: None,
        }
    }

    pub fn cache(message: impl Into<String>) -> Self {
        Self::Cache {
            message: message.into(),
            code: None,
            details: None,
            path: None,
        }
    }

    fn status_and_type(&self) -> (StatusCode, &'static str) {
        match self {
            AppError::NotFound { .. } => (StatusCode::NOT_FOUND, "NotFound"),
            AppError::BadRequest { .. } => (StatusCode::BAD_REQUEST, "BadRequest"),
            AppError::Validation { .. } => (StatusCode::UNPROCESSABLE_ENTITY, "Validation"),
            AppError::Db { .. } => (StatusCode::INTERNAL_SERVER_ERROR, "DatabaseError"),
            AppError::Cache { .. } => (StatusCode::INTERNAL_SERVER_ERROR, "CacheError"),
            AppError::Internal { .. } => (StatusCode::INTERNAL_SERVER_ERROR, "InternalServerError"),
        }
    }

    fn split_fields(
        self,
    ) -> (
        String,
        Option<String>,
        Option<serde_json::Value>,
        Option<String>,
    ) {
        match self {
            AppError::NotFound {
                message,
                code,
                details,
                path,
            }
            | AppError::BadRequest {
                message,
                code,
                details,
                path,
            }
            | AppError::Validation {
                message,
                code,
                details,
                path,
            }
            | AppError::Db {
                message,
                code,
                details,
                path,
            }
            | AppError::Cache {
                message,
                code,
                details,
                path,
            }
            | AppError::Internal {
                message,
                code,
                details,
                path,
            } => (message, code, details, path),
        }
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, err_type) = self.status_and_type();
        let (message, code, details, path) = self.split_fields();

        let body = ApiResponse::<serde_json::Value>::error(
            status,
            err_type,
            message,
            code,
            details,
            path.unwrap_or_else(|| "unknown".to_string()),
        );

        (status, Json(body)).into_response()
    }
}
