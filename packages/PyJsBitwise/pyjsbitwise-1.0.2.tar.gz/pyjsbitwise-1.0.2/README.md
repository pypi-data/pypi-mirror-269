# PyJsShift
JavaScript-flavored bitwise operations.

# Usage
Import Module:
```python
from pyjsbitwise import *
```

Cast int or float to 32-bit signed value:
```python
i32cast(-2**31) # 2147483648
i32cast(2**53 / 3) # -1431655766
```

Bitwise not, and, or, xor like JavaScript's ~, &, |, ^:
```python
bwnot(float("NaN")) # -1
bwand(2**32-1, 2**32-1) # -1
bwor(2**31, 2**53) # -2147483648
bwxor(2**31, 2**31-1) # -1
```

Shift left, right and unsigned right like JavaScript's <<, >>, >>>:
```python
lshift(1, 32) # 1
rshift(-2, -31) # -1
urshift(-1, 0) # 4294967295
```
