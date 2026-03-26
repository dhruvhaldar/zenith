## 2024-05-24 - Vectorizing Python Loops in Physical Models
**Learning:** In academic/scientific code, physics formulas are often written as direct ports of mathematical equations using standard Python `for` loops. These are massive bottlenecks when generating hundreds or thousands of data points (e.g., generating light curves or sampling points across an array).
**Action:** Always check loop constructs in scientific code operating on arrays. Replacing a pure Python loop with NumPy vectorized operations (like boolean indexing and `np.where`/`np.ones_like`) can provide a ~50x speedup with minimal effort and without sacrificing accuracy.
## 2026-10-27 - Optimizing `scipy.integrate.quad` Integrands
**Learning:** Using `numpy` functions (like `np.sqrt`) for scalar operations inside `scipy.integrate.quad` integrands introduces significant overhead because `quad` calls the integrand repeatedly with scalar float values, triggering NumPy's scalar dispatch overhead.
**Action:** Use standard Python `math` module functions (like `math.sqrt`) instead of NumPy functions when writing integrands for `scipy.integrate.quad` where possible, for faster integration.
## 2026-03-26 - Optimizing Python scalar mathematical operations
**Learning:** Using `numpy` mathematical functions (e.g., `np.sin`, `np.cos`, `np.arcsin`) on scalar values introduces significant dispatch overhead compared to the standard `math` module (e.g., `math.sin`, `math.cos`, `math.asin`), making the code substantially slower when called repeatedly, like inside loops processing many coordinates.
**Action:** Always use the standard Python `math` module instead of `numpy` for operations strictly dealing with scalar floating-point values to achieve significant performance improvements.
