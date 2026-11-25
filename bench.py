#!/usr/bin/env python3

import os
import sys
import argparse
import json
import subprocess
import shutil
import time
import csv

BENCH_TIMEOUT = 30


def input_file(benchmark):
    pre, _ = os.path.splitext(benchmark)
    return pre + ".in"


def parse_time_ns(stderr_bytes):
    for line in stderr_bytes.decode(errors="replace").splitlines():
        if line.startswith("TIME_NS:"):
            return int(line.split(":")[1])
    return None


def pass_args_for(passes):
    if passes is None:
        return ""
    if passes == []:
        return "-noopt"
    return " ".join("-p {}".format(p) for p in passes)


def install_bench_runtime():
    bench_runtime = os.path.join(os.path.dirname(__file__), "bench_runtime.c")
    student_runtime = os.path.abspath("../lib/runtime/runtime.c")
    student_runtime_dir = os.path.abspath("../lib/runtime")

    shutil.copy2(bench_runtime, student_runtime)
    subprocess.run("make", cwd=student_runtime_dir, check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run("dune build", shell=True, cwd="..", check=True)


def bench(config, repetitions):
    use_bench_timing = False
    bench_runtime = os.path.join(os.path.dirname(__file__), "bench_runtime.c")
    if os.path.exists(bench_runtime):
        try:
            install_bench_runtime()
            use_bench_timing = True
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"Warning: could not install bench runtime ({e}), falling back to wall-clock timing")
            subprocess.run("dune build", shell=True, cwd="..", check=True)
    else:
        subprocess.run("dune build", shell=True, cwd="..", check=True)

    compile_exe = os.path.abspath("../_build/default/bin/compile.exe")

    base_output = "compiled_benchmarks"
    if not os.path.exists(base_output):
        os.mkdir(base_output)

    examples = sorted(f for f in os.listdir("benchmarks") if f.endswith(".lisp"))
    configs = list(enumerate(config.items()))

    for i, (name, passes) in configs:
        output_dir = os.path.join(base_output, str(i + 1))
        for example in examples:
            print(f"Compiling: {example} [{name}]")
            src = os.path.join("benchmarks", example)
            subprocess.run(
                f"{compile_exe} {pass_args_for(passes)} {src} {output_dir}",
                shell=True,
                check=True,
            )

    results = {}
    for example in examples:
        print(f"Running: {example}")
        results[example] = {}

        input_path = os.path.join("benchmarks", input_file(example))
        stdin = open(input_path).read() if os.path.exists(input_path) else ""

        captured_stdout = None
        for i, (name, passes) in configs:
            run_cmd = os.path.abspath(
                os.path.join(base_output, str(i + 1), f"{example}.exe")
            )

            try:
                result = subprocess.run(
                    run_cmd, input=stdin.encode(), capture_output=True,
                    timeout=BENCH_TIMEOUT,
                )
            except subprocess.TimeoutExpired:
                print(f"Error: '{example}' with configuration '{name}' timed out")
                results[example][name] = None
                continue

            if result.returncode != 0:
                print(f"Error: '{example}' with configuration '{name}' exited with error")
                results[example][name] = None
                continue

            if captured_stdout is None:
                captured_stdout = result.stdout
            elif captured_stdout != result.stdout:
                print(f"Error: output of '{example}' changes when using different optimizations")
                exit(1)

            times = []
            for _ in range(repetitions):
                try:
                    start = time.perf_counter()
                    r = subprocess.run(
                        run_cmd, input=stdin.encode(), capture_output=True,
                        timeout=BENCH_TIMEOUT,
                    )
                    elapsed_ns = (time.perf_counter() - start) * 10**9
                except subprocess.TimeoutExpired:
                    continue
                if r.returncode != 0:
                    continue
                if use_bench_timing:
                    ns = parse_time_ns(r.stderr)
                    if ns is not None:
                        times.append(ns)
                else:
                    times.append(elapsed_ns)

            if len(times) == 0:
                print(f"Warning: all runs of '{example}' [{name}] failed or timed out")
                results[example][name] = None
            else:
                if len(times) < repetitions:
                    print(f"Warning: only {len(times)}/{repetitions} runs of '{example}' [{name}] succeeded")
                results[example][name] = sum(times) / len(times)

    return results


def main():
    if not os.path.exists("benchmarks"):
        print(
            "Benchmark script should be run from the root of the benchmarks repository"
        )
        sys.exit(1)
    parser = argparse.ArgumentParser(
        description="CSCI 1260 final homework benchmark script"
    )
    parser.add_argument("--config", type=argparse.FileType("r"), default="config.json")
    parser.add_argument("--output", type=argparse.FileType("w"), default="results.csv")
    parser.add_argument("--repeat", type=int, default=100)
    args = parser.parse_args()
    try:
        config = json.load(args.config)
    except json.decoder.JSONDecodeError as e:
        print("Error reading config file {}: {}".format(args.config.name, e))
        sys.exit(1)
    results = bench(config, args.repeat)
    writer = csv.writer(args.output)
    for example in sorted(results.keys()):
        config_times = results[example]
        for config_name in sorted(config_times.keys()):
            val = config_times[config_name]
            writer.writerow((example, config_name, val if val is not None else "FAILED"))

    print(f"BENCH_JSON:{json.dumps(results)}")


if __name__ == "__main__":
    main()
