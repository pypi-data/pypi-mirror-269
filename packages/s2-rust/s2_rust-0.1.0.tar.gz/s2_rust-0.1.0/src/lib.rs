use pyo3::prelude::*;
// use s2::cell

mod s2_functions;
use s2_functions::{lat_lon_to_cell_id_one_point, cell_id_to_lat_lon_one_point};

#[pyfunction]
fn lat_lon_to_cell_id(lat_vec: Vec<f64>, lon_vec: Vec<f64>, level: u64) -> PyResult<Vec<u64>> {
    Ok(
        lat_vec.iter().zip(lon_vec.iter()).map(|(lat, lon)| {
            lat_lon_to_cell_id_one_point(*lat, *lon, level)
        }
    ).collect())
}

#[pyfunction]
fn cell_id_to_lat_lon(cell_id_vec: Vec<u64>) -> PyResult<Vec<(f64, f64)>> {
    Ok(
        cell_id_vec.iter().map(|cell_id| {
            cell_id_to_lat_lon_one_point(*cell_id)
        }).collect()
    )
}


/// A Python module implemented in Rust.
#[pymodule]
fn s2_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(lat_lon_to_cell_id, m)?)?;
    m.add_function(wrap_pyfunction!(cell_id_to_lat_lon, m)?)?;
    Ok(())
}
