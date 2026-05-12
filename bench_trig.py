import timeit
import math
from zenith.utils import deg_to_rad

print("math.radians:", timeit.timeit("math.radians(123.45)", setup="import math", number=10000000))
print("deg_to_rad:", timeit.timeit("deg_to_rad(123.45)", setup="from zenith.utils import deg_to_rad", number=10000000))
