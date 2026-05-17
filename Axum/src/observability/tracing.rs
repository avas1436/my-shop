// src/observability/tracing.rs


use tracing_subscriber::{EnvFilter, fmt, prelude::*};

pub fn init() {

    let filter = EnvFilter::try_from_default_env()

    .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::registry()

    .with(fmt::layer())

    .with(filter)

    .init();

}

// use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

// pub fn init() {
//     tracing_subscriber::registry()
//         .with(tracing_subscriber::EnvFilter::new("info"))
//         .with(tracing_subscriber::fmt::layer())
//         .init();
// }