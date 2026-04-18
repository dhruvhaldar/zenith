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

## 2026-11-06 - Bounded Array Maths vs Boolean Masking
**Learning:** In NumPy array processing, calculating boundaries continuously and applying `np.clip()` to bound physical values (like overlap fractions) is significantly faster (up to ~30%) and cleaner than creating large boolean arrays (like `full_transit` or `ingress_egress`), performing `np.any()`, and assigning conditionally. It minimizes array allocation overhead.
**Action:** Replace multiple boolean mask conditions with continuous mathematical boundaries bounded by `np.clip()` when calculating piecewise functions in physics models.
## 2024-05-30 - Fast Integer Exponentiation in NumPy
**Learning:** Using the generic power operator `**` on NumPy arrays (e.g., `array**5`) invokes NumPy's generic power function, which has significant overhead for small integer powers.
**Action:** Replace small integer power calculations on arrays with explicit mathematical multiplication (e.g., `x2 = x * x; x5 = x2 * x2 * x`). This can be up to 4x faster for large arrays and avoids unnecessary overhead while maintaining readability.

## 2024-05-30 - Numerical Stability with np.expm1
**Learning:** When calculating `exp(x) - 1.0` for arrays, using NumPy's `np.expm1(x)` is slightly faster (combines operations) and provides significantly better numerical stability, particularly avoiding overflow/underflow warnings that `np.exp` might trigger before the subtraction.
**Action:** Always replace `np.exp(x) - 1.0` with `np.expm1(x)` when writing scientific calculations in NumPy.
## 2024-05-30 - Fast Base-10 Exponentiation in NumPy
**Learning:** Using `10**x` on NumPy arrays triggers a slower, generic arbitrary-base exponentiation routine.
**Action:** Replace `10**x` with its natural logarithm equivalent: `np.exp(np.log(10) * x)` (where `np.log(10) ≈ 2.302585092994046`). This maps down to a much faster C-level implementation for `np.exp`, often providing a ~2x performance speedup.

## 2024-05-30 - Fast Base-10 Logarithm in NumPy
**Learning:** Using `np.log10(x)` on NumPy arrays is slower than using the natural logarithm `np.log(x)` multiplied by a constant factor, because `np.log` maps directly to highly-optimized C-level routines.
**Action:** Replace `np.log10(x)` with its natural logarithm equivalent: `np.log(x) / np.log(10)`. When calculating `C * np.log10(x)`, precalculate `C / np.log(10)` (where `np.log(10) ≈ 2.302585092994046`). This provides roughly a 30% speedup for array calculations.

## 2026-11-12 - Fast Integer Exponentiation inside quad Integrands
**Learning:** Python's generic power operator (`**`) carries overhead even for small integer powers. When used inside tight numerical integration loops (like `scipy.integrate.quad` integrands), this overhead multiplies drastically.
**Action:** Unroll small integer powers (e.g., `x**3`) to explicit multiplication (e.g., `x * x * x`) inside performance-critical functions and loops, especially `quad` integrands.

## 2026-12-05 - Array-Scalar Addition Optimization
**Learning:** When performing multiple additions on a NumPy array with scalar values inside a loop or function (e.g., `array + scalar1 + scalar2 + scalar3`), each operation creates a new intermediate array. This requires multiple passes of memory allocation and iteration over the array.
**Action:** Combine all scalar terms into a single constant before adding them to the array (e.g., `constant = scalar1 + scalar2 + scalar3; result = array + constant`). This reduces the number of array additions to just one, saving memory bandwidth and execution time.
## 2024-05-30 - Array-Scalar Multiplication Optimization
**Learning:** When multiplying a NumPy array by multiple scalar values (e.g., `array * scalar1 * scalar2 * scalar3`), executing it left-to-right creates multiple intermediate array allocations. This requires redundant passes of memory allocation and iteration over the array.
**Action:** Combine all scalar terms into a single constant with parentheses before multiplying with the array (e.g., `array * (scalar1 * scalar2 * scalar3)`). This reduces the number of array multiplications to just one, saving memory bandwidth and execution time.
## 2024-05-30 - Mathematical Simplification to Minimize Array Allocation
**Learning:** When performing mathematical operations involving multiple scalar constants and an array (e.g., `C1 * ((array + C2) / C3)`), evaluating it sequentially creates multiple intermediate array allocations.
**Action:** Mathematically expand and combine all scalar terms into a single constant where possible before applying them to the array (e.g., `(C1 / C3) * (array + C2)`). This significantly reduces intermediate array creation overhead, saving execution time and memory bandwidth.
## 2024-05-30 - Inline `np.clip` vs Separate Reassignment
**Learning:** In NumPy array processing, evaluating a mathematical expression and applying `np.clip()` simultaneously inline (e.g., `overlap = np.clip((A - B) * C, min, max)`) is substantially faster (roughly 2x) than evaluating the array, assigning it to a variable, and then reassigning it with a separate `np.clip` call (e.g., `overlap = (A - B) * C; overlap = np.clip(overlap, min, max)`). The separate reassignment introduces redundant intermediate array allocation and iteration overhead.
**Action:** When bounding an array expression, apply `np.clip()` inline directly around the expression rather than in a separate reassignment step to minimize array allocation overhead.
