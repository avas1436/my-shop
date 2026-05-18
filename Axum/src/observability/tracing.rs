// src/observability/tracing.rs
use tracing_subscriber::{fmt, EnvFilter, prelude::*};

pub fn init() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    let fmt_layer = fmt::layer()
        .compact()
        .with_target(false)
        .with_file(true)
        .with_line_number(true);

    tracing_subscriber::registry()
        .with(filter)
        .with(fmt_layer)
        .init();
}




// use tracing_subscriber::{EnvFilter, fmt, prelude::*};

// pub fn init() {

//     let filter = EnvFilter::try_from_default_env()

//     .unwrap_or_else(|_| EnvFilter::new("info"));

//     tracing_subscriber::registry()

//     .with(fmt::layer())

//     .with(filter)

//     .init();

// }