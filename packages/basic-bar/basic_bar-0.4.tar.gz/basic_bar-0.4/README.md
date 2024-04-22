# Basic Bar

A basic and efficient progress bar in Python

```python
from basic_bar import bar

for _ in bar(range(1000000)):
    pass

# ▕█████████████████████████████████▏ 100.00% 3.14s
```