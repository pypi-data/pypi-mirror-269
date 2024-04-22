import time, sys


def progress(iterable, length=33):
    total, start = len(iterable), time.monotonic()
    for count, it in enumerate(iterable, 1):
        yield it
        if count % max(1, total // 10000) == 0 or count == total:
            percent = count / total
            sys.stdout.write(
                f'\r▕{"█" * int(length * percent) + " " * (length - int(length * percent))}▏ '
                f"{percent * 100:.2f}% "
                f"{(time.monotonic() - start) / count * (total - count):.2f}s"
            ), sys.stdout.flush()
    sys.stdout.write(f'\r▕{"█" * length}▏ 100.00% {time.monotonic() - start:.2f}s\n')
