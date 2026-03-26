import time
import tracemalloc


def handle_event(value):
    if value > 50:
        return "ALERT"
    if value < 0:
        return "ERROR"
    return "OK"


def test_load_testing():
    start = time.perf_counter()

    results = []
    for i in range(10000):
        results.append(handle_event(i % 100))

    duration = time.perf_counter() - start

    assert len(results) == 10000
    assert duration < 1.5


def test_stress_testing():
    start = time.perf_counter()

    counter = 0
    for i in range(50000):
        result = handle_event(i % 120)
        if result:
            counter += 1

    duration = time.perf_counter() - start

    assert counter == 50000
    assert duration < 3.0


def test_response_time_measurement():
    start = time.perf_counter()
    result = handle_event(75)
    duration = time.perf_counter() - start

    assert result == "ALERT"
    assert duration < 0.01


def test_resource_utilization():
    tracemalloc.start()

    data = [handle_event(i % 100) for i in range(20000)]

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert len(data) == 20000
    assert peak < 10 * 1024 * 1024  # < 10 MB