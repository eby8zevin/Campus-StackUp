const HEADER: &str = "application/json";

use std::error::Error;

use crate::rust::RustSingleCycle;
use reqwest::{ self, blocking::Client, header::ACCEPT };

pub fn api_request_single_rust_cycle(
    rust_version: &str
) -> Result<RustSingleCycle, Box<dyn Error>> {
    let request_string: String = format!("https://endoflife.date/api/rust/{}.json", rust_version);
    
    let client = Client::new();
    
    let body = client
        .get(request_string)
        .header(ACCEPT, HEADER)
        .send()?
        .bytes()?
        .to_vec();

    let response = unsafe { String::from_utf8_unchecked(body) };
    let deserialised_response = serde_json::from_str::<RustSingleCycle>(&response)?;
    Ok(deserialised_response)
}