use crate::state::app_state::AppState;

pub async fn get_products(state: &AppState) -> Vec<String> {
    vec!["product1".into(), "product2".into()]
}
