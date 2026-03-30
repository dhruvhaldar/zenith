## 2024-05-24 - Vectorizing Python Loops in Physical Models
**Learning:** In academic/scientific code, physics formulas are often written as direct ports of mathematical equations using standard Python `for` loops. These are massive bottlenecks when generating hundreds or thousands of data points (e.g., generating light curves or sampling points across an array).
**Action:** Always check loop constructs in scientific code operating on arrays. Replacing a pure Python loop with NumPy vectorized operations (like boolean indexing and `np.where`/`np.ones_like`) can provide a ~50x speedup with minimal effort and without sacrificing accuracy.
## 2026-10-27 - Optimizing `scipy.integrate.quad` Integrands
**Learning:** Using `numpy` functions (like `np.sqrt`) for scalar operations inside `scipy.integrate.quad` integrands introduces significant overhead because `quad` calls the integrand repeatedly with scalar float values, triggering NumPy's scalar dispatch overhead.
**Action:** Use standard Python `math` module functions (like `math.sqrt`) instead of NumPy functions when writing integrands for `scipy.integrate.quad` where possible, for faster integration.

## 2024-05-14 - Replace numpy with math module for scalar math
**Learning:** Replacing `numpy` with the standard Python `math` module for trigonometric operations yields significant performance gains for scalar operations by avoiding scalar dispatch overhead. However, when switching to `math.asin` or `math.acos`, explicitly clamp inputs to `[-1.0, 1.0]` to prevent `ValueError: math domain error` caused by microscopic floating-point inaccuracies, which `numpy` typically handles with warnings rather than fatal errors.
**Action:** When replacing `numpy` with `math` for scalar trig operations, ensure inputs are clamped to their valid mathematical domains before calling the function.
## 2026-10-27 - Caching Expensive Integrations
**Learning:** `scipy.integrate.quad` is computationally expensive and only accepts scalar inputs. Standard performance tweaks like vectorization don't work natively here. However, since the function is pure math, it's highly repetitive (e.g., standard parameters, common redshift grids).
**Action:** Use Python's built-in `@lru_cache` from `functools` on wrapper functions around `scipy.integrate.quad` to bypass redundant numerical integration overhead.

## 2026-03-30 - Negligible Speedups vs Downstream Overhead
**Learning:** Avoid micro-optimizations that yield negligible absolute speedups (e.g., vectorizing a very small array of 50 elements) if the calculation time is immediately dwarfed by massive downstream overhead (e.g., synchronous `matplotlib.pyplot` calls). While technically "faster", the real-world impact is zero.
**Action:** When finding a slow function, profile the ENTIRE function end-to-end to understand where the real time is spent. Do not optimize a 0.1ms computation if the 1.5s rendering step right next to it is the true bottleneck.
