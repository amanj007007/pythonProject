from collections import Counter, defaultdict
from contextlib import contextmanager


LOGS = [
    "2026-09-09 10:01:22 INFO /home 200 0.031",
    "2026-09-09 10:01:25 ERROR /api/users 500 1.202",
    "2026-09-09 10:02:01 INFO /login 200 0.089",
    "2026-09-09 10:02:14 WARN /admin 403 0.011",
    "2026-09-09 10:02:20 ERROR /api/users 500 0.977",
    "2026-09-09 10:03:05 INFO /home 200 0.025",
    "bad line that should not crash the parser",
    "2026-09-09 10:03:40 INFO /api/orders 201 0.310",
]


class ParseError(Exception):
    pass


def parse_log(line):
    try:
        date, clock, level, path, status, seconds = line.split()

        return {
            "time": f"{date} {clock}",
            "level": level,
            "path": path,
            "status": int(status),
            "seconds": float(seconds),
        }

    except (ValueError, TypeError) as error:
        raise ParseError(f"Could not parse line: {line}") from error


@contextmanager
def banner(title):
    print(f"=== {title} ===")

    try:
        yield
    finally:
        print("=== end ===")


def main():
    level_counts = Counter()
    times = defaultdict(list)
    error_paths = set()
    bad_lines = 0

    for line in LOGS:
        try:
            log = parse_log(line)

        except ParseError:
            bad_lines += 1
            continue

        level_counts[log["level"]] += 1
        times[log["path"]].append(log["seconds"])

        if 500 <= log["status"] < 600:
            error_paths.add(log["path"])

    averages = {
        path: sum(seconds) / len(seconds)
        for path, seconds in times.items()
    }

    sorted_averages = sorted(
        averages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    with banner("Log Analysis"):
        print("\nRequests per level:")

        for level, count in level_counts.items():
            print(f"{level}: {count}")

        print("\nAverage response time per path:")

        for path, average in sorted_averages:
            print(f"{path}: {average:.3f}s")

        print("\nPaths with 5xx responses:")
        print(error_paths)

        print(f"\nBad lines: {bad_lines}")


if __name__ == "__main__":
    main()