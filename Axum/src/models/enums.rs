// src/models/enums.rs 
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, sqlx::Type)]
#[sqlx(type_name = "inventorystatus", rename_all = "UPPERCASE")]
pub enum InventoryStatus {
    InStock,
    LowStock,
    OutOfStock,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, sqlx::Type)]
#[sqlx(type_name = "productstatus", rename_all = "UPPERCASE")]
pub enum ProductStatus {
    Active,
    Inactive,
    Draft,
    Archived,
}

// #[derive(Debug, Clone, PartialEq, Eq, Type, Serialize, Deserialize)]
// #[sqlx(type_name = "cartstatus", rename_all = "lowercase")]
// pub enum CartStatus {
//     Active,
//     Abandoned,
//     Converted,
// }

// #[derive(Debug, Clone, PartialEq, Eq, Type, Serialize, Deserialize)]
// #[sqlx(type_name = "userrole", rename_all = "lowercase")]
// pub enum UserRole {
//     Admin,
//     Customer,
// }

// #[derive(Debug, Clone, PartialEq, Eq, Type, Serialize, Deserialize)]
// #[sqlx(type_name = "purposeotp", rename_all = "lowercase")]
// pub enum PurposeOtp {
//     Login,
//     Register,
//     Reset,
// }
