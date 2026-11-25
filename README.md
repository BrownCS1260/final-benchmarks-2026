Benchmarks for the CSCI 1260 final project
------------------------------------------

Open up a pull request on this repository to add a benchmark to the
`benchmarks/` directory.

You should add tests in pairs, a .lisp file with a matching .out file.

Your tests should be named with your GitHub username:
`<username>-<testname>.lisp` and `<username>-<testname>.out`.


Benchmarking the final homework
-------------------------------

Here's how to get started running benchmarks for the final homework:

1. Clone this respository into your final homework repository:

```shell
git clone https://github.com/BrownCS1260/final-benchmarks-2026.git benchmarks
```

2. In the new benchmarks directory, make a `config.json` file. This file should
   be a JSON-formatted dictionary where the keys are configuration names and the
   values are lists of pass names. Use an empty list `[]` for no optimizations,
   or `null` to run all optimizations (equivalent to invoking the compiler with
   no `-p` flags). For example:

```json
{
  "No optimizations": [],
  "All optimizations": null,
  "Inlining": ["uniquify-variables", "inline"],
  "Constant propagation and inlining": ["uniquify-variables", "inline", "propagate-constants"]
}
```

 3. Run the benchmark script. It will run each benchmark using each
    specified configuration and write the results to `results.csv`.

 ```shell
 python3 bench.py
 ```

 You can control the number of repetitions with `--repeat` (default 100):

 ```shell
 python3 bench.py --repeat 50
 ```
 
Have fun!
