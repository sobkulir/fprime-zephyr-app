# LedBlinker benchmarks

The code in this folder is a mess.

_Note: Internally, numerous files in the project are replaced for each benchmark, but the originals are kept under `backups/` and are restored after `run_bench.py` finishes._

## RAM and Flash
To run all benchmarks, simply run:
```sh
python3 run_bench.py
```

It will generate results under `report/` directory.

## Performance
First bring in the necessary templated files:
```sh
python3 run_bench.py -p
```

Then compile the LedBlinker, flash it and run it. Try uplinking/downlinking files to see the performance measurements.

Then restore the backups:
```sh
python3 run_bench.py -r
```