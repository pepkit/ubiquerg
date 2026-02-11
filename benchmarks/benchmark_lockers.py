#!/usr/bin/env python3
"""Benchmark: OneLocker vs ThreeLocker.

Run: python benchmark_lockers.py
"""

import multiprocessing
import os
import sys
import tempfile
import time

multiprocessing.set_start_method("spawn", force=True)

from ubiquerg import OneLocker, ThreeLocker


def benchmark_exclusive_access(filepath, iterations=100):
    """Measure lock/unlock cycle speed for exclusive access."""
    one = OneLocker(filepath)
    start = time.perf_counter()
    for _ in range(iterations):
        one.write_lock()
        one.write_unlock()
    one_time = time.perf_counter() - start

    three = ThreeLocker(filepath)
    start = time.perf_counter()
    for _ in range(iterations):
        three.write_lock()
        three.write_unlock()
    three_time = time.perf_counter() - start

    return one_time, three_time


def reader_process(filepath, locker_type, hold_time, barrier, timestamps, idx):
    """Subprocess: wait for barrier, acquire read lock, hold it, record times."""
    if locker_type == "three":
        locker = ThreeLocker(filepath)
    else:
        locker = OneLocker(filepath)

    barrier.wait()
    t_start = time.perf_counter()
    locker.read_lock()
    t_acquired = time.perf_counter()
    time.sleep(hold_time)
    locker.read_unlock()
    t_done = time.perf_counter()

    timestamps[idx] = (t_start, t_acquired, t_done)


def benchmark_concurrent_reads(filepath, n_readers=4, hold_time=0.5):
    """Spawn n_readers behind a barrier, measure overlap behavior."""
    results = {}

    for locker_type in ["one", "three"]:
        barrier = multiprocessing.Barrier(n_readers)
        manager = multiprocessing.Manager()
        timestamps = manager.dict()

        processes = []
        for i in range(n_readers):
            p = multiprocessing.Process(
                target=reader_process,
                args=(filepath, locker_type, hold_time, barrier, timestamps, i),
            )
            processes.append(p)

        for p in processes:
            p.start()
        for p in processes:
            p.join(timeout=60)

        starts = [timestamps[i][0] for i in range(n_readers)]
        acquireds = [timestamps[i][1] for i in range(n_readers)]
        dones = [timestamps[i][2] for i in range(n_readers)]

        wall = max(dones) - min(starts)
        avg_wait = sum(a - s for s, a in zip(starts, acquireds)) / n_readers

        results[locker_type] = {"wall": wall, "avg_wait": avg_wait}

    return results


def main():
    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "benchmark.txt")
    with open(filepath, "w") as f:
        f.write("benchmark data")

    iterations = 100
    n_readers = 4
    hold_times = [0.5, 3.0]

    print("ubiquerg locker benchmark")
    print("=" * 50)

    # Benchmark 1: Exclusive access speed
    print(f"\n1. Exclusive lock/unlock ({iterations} iterations)")
    print("-" * 50)
    one_time, three_time = benchmark_exclusive_access(filepath, iterations)
    speedup = three_time / one_time
    print(f"   OneLocker:   {one_time:.4f}s  ({one_time / iterations * 1000:.2f}ms/cycle)")
    print(f"   ThreeLocker: {three_time:.4f}s  ({three_time / iterations * 1000:.2f}ms/cycle)")
    print(f"   OneLocker {speedup:.1f}x faster")

    # Benchmark 2: Concurrent readers at different hold times
    for hold_time in hold_times:
        print(f"\n2. Concurrent readers ({n_readers} readers, {hold_time}s hold each)")
        print("-" * 50)
        # Suppress wait_for_lock stdout dots (fd-level for child processes)
        sys.stdout.flush()
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_fd = os.dup(1)
        os.dup2(devnull, 1)
        os.close(devnull)
        results = benchmark_concurrent_reads(filepath, n_readers, hold_time)
        os.dup2(old_fd, 1)
        os.close(old_fd)

        one = results["one"]
        three = results["three"]
        print(f"   OneLocker:   {one['wall']:.2f}s wall  (avg {one['avg_wait']:.2f}s wait)")
        print(f"   ThreeLocker: {three['wall']:.2f}s wall  (avg {three['avg_wait']:.2f}s wait)")

    os.unlink(filepath)
    os.rmdir(tmpdir)


if __name__ == "__main__":
    main()
