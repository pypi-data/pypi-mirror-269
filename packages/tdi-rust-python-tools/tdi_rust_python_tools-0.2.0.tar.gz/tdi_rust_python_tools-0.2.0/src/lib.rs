

use pyo3::prelude::*;
use std::collections::HashSet;
use html_escape::decode_html_entities;


use regex::Regex;
use lazy_static::lazy_static;


lazy_static! {
    static ref LT_GT_PATTERN: Regex = Regex::new(
        r"(?x)
        (?P<start>^|\s|>)
        (?P<symbol>[<>])
        (?P<matched_char>[^\s/>])
        "
    ).unwrap();
}

#[pyfunction]
fn combine_dedupe_values(values: Vec<&str>, separator: &str) -> String {
    let mut output: HashSet<&str> = HashSet::new();

    for value in values {
        let terms: HashSet<&str> = value.split(separator).collect();
        output.extend(terms);
    }

    let mut sorted_output: Vec<&str> = output.into_iter().collect();
    sorted_output.sort();

    sorted_output.join(", ")
}


#[pyfunction]
fn fix_lt_gt(value: &str) -> PyResult<String> {
    Ok(LT_GT_PATTERN.replace_all(value, "$start$symbol $matched_char").into_owned())
}

#[pyfunction]
fn unescape_html_chars(value: &str) -> PyResult<String> {
    Ok(decode_html_entities(value).into_owned())
}


lazy_static! {
    static ref TEMPERATURE_PATTERN: Regex = Regex::new(
        r"(?i)(-?\d+\.?\d*)(\s*[^°]C)"
    ).unwrap();
}


#[pyfunction]
fn clean_temperature(value: &str) -> PyResult<String> {
    let value = TEMPERATURE_PATTERN.replace_all(value, "$1°C");
    Ok(value.replace("℃", "°C"))
}

lazy_static! {
    static ref CHINESE_CHARS: Regex = Regex::new(r"[\p{Script=Han}]").unwrap();
}

#[pyfunction]
fn remove_chinese_chars(value: &str) -> PyResult<String> {
    Ok(CHINESE_CHARS.replace_all(value, "").to_string())
}

lazy_static! {
    static ref HTML_PATTERN: Regex = Regex::new(r"<.*?>").unwrap();
}

#[pyfunction]
fn strip_html_tags(value: &str) -> PyResult<String> {
    let result = HTML_PATTERN.replace_all(value, "");
    Ok(result.to_string())
}

#[pyfunction]
fn correct_spaces(value: &str) -> PyResult<String> {
    let result = value.replace(" ", " ").split_whitespace().collect::<String>();
    Ok(result)
}


/// A Python module implemented in Rust.
#[pymodule]
fn tdi_rust_python_tools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(combine_dedupe_values, m)?)?;
    m.add_function(wrap_pyfunction!(fix_lt_gt, m)?)?;
    m.add_function(wrap_pyfunction!(unescape_html_chars, m)?)?;
    m.add_function(wrap_pyfunction!(clean_temperature, m)?)?;
    m.add_function(wrap_pyfunction!(remove_chinese_chars, m)?)?;
    m.add_function(wrap_pyfunction!(strip_html_tags, m)?)?;
    m.add_function(wrap_pyfunction!(correct_spaces, m)?)?;
    Ok(())
}
