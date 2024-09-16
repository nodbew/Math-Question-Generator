use pyo3::prelude::*;

#[pymodule]
/// The base module
fn rust_core(m: &Bound<PyModule>) -> PyResult<()> {
    Ok(())
}
