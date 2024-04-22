# Basic Bar

Basic Bar is a simple and effective text-based progress bar for Python applications. It's lightweight and easy to integrate, making it perfect for monitoring the progress of iterable operations with visual feedback and estimated completion times.

## Installation

You can install Basic Bar directly from PyPI:

```bash
pip install basic-bar
```

## Usage

To use Basic Bar, simply wrap any iterable in the `bar()` function. This function will yield from the iterable and display a progress bar in the terminal.

### Example

Here's a basic example of how to use Basic Bar:

```python
from basic_bar import bar
import time

# Example iterable
data = range(100)

# Wrapping the iterable with the bar function
for item in bar(data):
    time.sleep(0.01)  # Simulate some work
```

This will display a progress bar in your terminal, updating with each iteration.

### Customization

You can customize the length of the progress bar by providing a `length` parameter:

```python
for item in bar(data, length=50):
    time.sleep(0.01)  # Simulate some work
```

## Features

- **Simple Integration**: Just wrap your iterable with `bar()`.
- **Customizable Bar Length**: Adjust the length of the progress bar to fit your needs.
- **Real-Time Updates**: Provides real-time feedback on progress with percentage completion and estimated time remaining.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
