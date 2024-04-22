import time
import unittest
from unittest.mock import patch
from io import StringIO
from basic_bar import bar


class TestProgressBar(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_yield_items(self, mock_stdout):
        iterable = range(5)
        result = list(bar(iterable))
        self.assertEqual(result, [0, 1, 2, 3, 4])

    @patch("sys.stdout", new_callable=StringIO)
    def test_accurate_display(self, mock_stdout):
        list(bar(range(100)))
        output = mock_stdout.getvalue()
        self.assertIn("100.00%", output)
        self.assertTrue(output.endswith("\n"))

    @patch("sys.stdout", new_callable=StringIO)
    def test_customizable_length(self, mock_stdout):
        list(bar(range(100), length=50))
        output = mock_stdout.getvalue()
        self.assertTrue("█" * 50 in output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_handles_different_iterables(self, mock_stdout):
        iterables = [list(range(10)), set(range(10)), tuple(range(10))]
        for iterable in iterables:
            with self.subTest(iterable=iterable):
                result = list(bar(iterable))
                self.assertEqual(result, list(iterable))

    @patch("sys.stdout", new_callable=StringIO)
    def test_handles_empty_iterables(self, mock_stdout):
        result = list(bar([]))
        self.assertEqual(result, [])
        self.assertIn("100.00%", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_total_time_at_completion(self, mock_stdout):
        list(bar(range(1)))  # Simple case with almost immediate completion
        output = mock_stdout.getvalue()
        self.assertTrue(output.strip().endswith("s"))

    @patch("sys.stdout", new_callable=StringIO)
    def test_timing_estimations_accuracy(self, mock_stdout):
        iterable = range(100)
        start_time = time.monotonic()
        for _ in bar(iterable):
            time.sleep(0.01)  # Simulating work
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        output = mock_stdout.getvalue()
        last_line = output.strip().split("\n")[-1]
        reported_time = float(last_line.split()[-1][:-1])
        self.assertAlmostEqual(elapsed_time, reported_time, delta=1.0)

    @patch("sys.stdout", new_callable=StringIO)
    def test_progress_bar_scaling(self, mock_stdout):
        list(bar(range(3), length=10))
        output = mock_stdout.getvalue()
        self.assertIn(
            "█" * 3 + " " * 7, output
        )  # Check if bar scales correctly for 33%

    @patch("sys.stdout", new_callable=StringIO)
    def test_progress_bar_update_frequency(self, mock_stdout):
        # Testing with a large number to ensure updates at less than 1% increments
        list(bar(range(200000), length=50))
        output = mock_stdout.getvalue()
        updates = output.count("\r")
        self.assertTrue(updates > 100)  # More than 100 updates for 200000 items
