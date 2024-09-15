use pyo3::prelude::*;

#[pymodule]
fn rust_core(m: &Bound<_, PyModule>) -> PyResult<()> {
    Ok(())
}
