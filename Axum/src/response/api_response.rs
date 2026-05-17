// src/response/api_response.rs
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use chrono::{DateTime, Utc};
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct ErrorDetail {
    pub message: String,
    pub code: Option<String>,
    pub details: Option<serde_json::Value>,
}

#[derive(Debug, Serialize)]
pub struct ApiResponse<T>
where
    T: Serialize,
{
    pub success: bool,
    pub status_code: u16,
    pub error_type: Option<String>,
    pub detail: Option<ErrorDetail>,
    pub data: Option<T>,
    pub path: String,
    pub timestamp: DateTime<Utc>,
}

impl<T> ApiResponse<T>
where
    T: Serialize,
{
    pub fn success(status: StatusCode, data: T, path: String) -> Self {
        Self {
            success: true,
            status_code: status.as_u16(),
            error_type: None,
            detail: None,
            data: Some(data),
            path,
            timestamp: Utc::now(),
        }
    }

    pub fn error(
        status: StatusCode,
        error_type: impl Into<String>,
        message: impl Into<String>,
        code: Option<String>,
        details: Option<serde_json::Value>,
        path: String,
    ) -> ApiResponse<serde_json::Value> {
        ApiResponse {
            success: false,
            status_code: status.as_u16(),
            error_type: Some(error_type.into()),
            detail: Some(ErrorDetail {
                message: message.into(),
                code,
                details,
            }),
            data: None,
            path,
            timestamp: Utc::now(),
        }
    }
}

impl<T> IntoResponse for ApiResponse<T>
where
    T: Serialize,
{
    fn into_response(self) -> Response {
        let status =
            StatusCode::from_u16(self.status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR);
        (status, Json(self)).into_response()
    }
}
