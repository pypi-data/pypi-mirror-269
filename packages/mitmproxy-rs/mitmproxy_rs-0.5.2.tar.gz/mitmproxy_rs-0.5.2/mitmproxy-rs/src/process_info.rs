use std::path::{Path, PathBuf};

use anyhow::Result;
use pyo3::prelude::*;

#[allow(unused_imports)]
use mitmproxy::processes::{image, ProcessList};
#[cfg(windows)]
use mitmproxy::windows;

#[pyclass(module = "mitmproxy_rs", frozen)]
pub struct Process(mitmproxy::processes::ProcessInfo);

#[pymethods]
impl Process {
    #[getter]
    fn executable(&self) -> &Path {
        &self.0.executable
    }
    #[getter]
    fn display_name(&self) -> &str {
        &self.0.display_name
    }
    #[getter]
    fn is_visible(&self) -> bool {
        self.0.is_visible
    }
    #[getter]
    fn is_system(&self) -> bool {
        self.0.is_system
    }
    fn __repr__(&self) -> String {
        format!(
            "Process(executable={:?}, display_name={:?}, is_visible={}, is_windows={})",
            self.executable(),
            self.display_name(),
            self.is_visible(),
            self.is_system(),
        )
    }
}

/// Return a list of all running executables.
/// Note that this groups multiple processes by executable name.
///
/// *Availability: Windows*
#[pyfunction]
pub fn active_executables() -> PyResult<Vec<Process>> {
    #[cfg(windows)]
    {
        windows::processes::active_executables()
            .map(|p| p.into_iter().map(Process).collect())
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{}", e)))
    }
    #[cfg(not(windows))]
    Err(pyo3::exceptions::PyNotImplementedError::new_err(
        "active_executables is only available on Windows",
    ))
}

#[pyfunction]
#[allow(unused_variables)]
pub fn executable_icon(path: PathBuf) -> Result<PyObject> {
    #[cfg(windows)]
    {
        let mut icon_cache = windows::icons::ICON_CACHE.lock().unwrap();
        let png_bytes = icon_cache.get_png(path)?;
        Ok(Python::with_gil(|py| {
            pyo3::types::PyBytes::new(py, png_bytes).to_object(py)
        }))
    }
    #[cfg(not(windows))]
    Err(pyo3::exceptions::PyNotImplementedError::new_err(
        "executable_icon is only available on Windows",
    )
    .into())
}
