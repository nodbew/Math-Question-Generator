use pyo3::prelude::*;

#[pymodule]
fn rust_core(m: &Bound<PyModule>) -> PyResult<()> {
    Ok(())
}
