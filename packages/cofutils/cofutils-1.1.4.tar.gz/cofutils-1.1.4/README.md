# Introduction for Cof utils
There're several useful tools for experiments, such as cofrun, coftimer, cofmem, cofwriter. 
The Overview of `Cofutils`
![overview](images/cofutils-overview.svg)

## Install
#### By Pypi
`pip install cofutils`

#### By Source
```
git clone https://gitee.com/haiqwa/cofutils.git
pip install .
```
## Usage
### Cof Writer
#### Cof Logger
Cof logger can print user message according to print-level.
In *.py:
```
from cofutils import coflogger
coflogger.debug("this is debug")
coflogger.info("this is info")
coflogger.warn("this is warn")
coflogger.error("this is error")
```
Print-level is determined by environment variable `COF_DEBUG`:
```
COF_DEBUG=WARN python main.py
```
The default print-level is `INFO`. By the way, only the node of 'rank=0' can output log in distributed environment

#### Cof CSV
Dump data into csv format.

* Get a unique csv writer by calling cofcsv
* Write data in dict type. You can append data at anywhere and anytime
* Save data as `[name].csv` under the `root_dir`. After that cofcsv will clear data in default
```python
from cofutils import cofcsv

data = {'a':1, 'b':2, 'c':3}
test_csv = cofcsv('test')
test_csv.write(data)
data = {'a':4, 'b':5, 'c':6}
test_csv.write(data)

# remember to save data by calling cofcsv.save
cofcsv.save(root_dir='csv_output')
```

#### Cof Tb
Write data into tensorboard. 
```python
from cofutils import coftb
coftb('test')
coftb.write({'a': 10})
coftb.write({'a': 20})
coftb.write({'a': 30})
coftb.close()
```


By default, `events.out.tfevents.xxx` would be dump to `coftb` directory.
```bash
tensorboard --logdir coftb/
```
---

### Cof Timer
Cof timer is similar to the `Timer` in `Megatron-LM`. By default, the timer achieves the duration time of operations on the host side. If you want to profile cuda programme, please set `cuda_timer=True`, which obtains execution time by cuda events.

It support two log modes which can be set by the keyword `timedict`:
* Organize the result into a string and output it into `STDOUT` which is easy to view for users 
* Directly return the result time table as `Dict` format

Users can also customize their time log writer by setting `writer`. Currently, cof timer supports `csv`, `tb`, `info`, `debug`, `warn`, `error` as writer function.

Note: if you call `.log` to print time, then **the timer will reset automatically** 
```python
from cofutils import coftimer, coflogger
import time
import torch
coftimer.set_writer(writer = "warn,csv,tb", name="loop_sleep")
test_1 = coftimer('test1')
test_2 = coftimer('test2')
test_3 = coftimer('test3', cuda_timer=True)


for _ in range(3):
    test_1.start()
    time.sleep(1)
    test_1.stop()

coftimer.log(normalizer=3, timedict=False)

with test_2:
    for _ in range(3):
        time.sleep(1)

coftimer.log(normalizer=3, timedict=False)

m1 = torch.randn(1024,1024,16,device="cuda:0")
m2 = torch.randn(1024,1024,16,device="cuda:0")
with test_3:
    for _ in range(3):
        m1 = m1+m2
        m1.div_(20)
        m2.div_(10)
time_dict = coftimer.log(normalizer=3, timedict=True)
coflogger.info(time_dict)
coftimer.save()
```

```bash
[2024-04-19 08:35:38.241]  [Cof WARNING]: time (ms) | test1: 1001.09 | test2: 0.00 | test3: 0.00
[2024-04-19 08:35:41.247]  [Cof WARNING]: time (ms) | test1: 0.00 | test2: 1001.09 | test3: 0.00
[2024-04-19 08:35:42.000]  [Cof INFO]: {'test1': 0.0, 'test2': 0.0, 'test3': 10.247509638468424}
```

### Cof Memory Report
Print GPU memory states by pytorch cuda API. And it supports to dump memory states into tensorboard of csv, except for printing out to the terminal.
* `MA`: memory current allocated
* `MM`: max memory allocated
* `MR`: memory reserved by pytorch

`cofmem` is a time-cost API. Please remember to remove it if you want to profiling the performance of program. Similarly, you can set writer for `cofmem`. `cofmem` would do nothing if you set writer as `None`.

The latency of `cofmem`:
|writer|latency|
|:-|:-:|
|None|0ms|
|logger.info|0.8ms|
|tensorboard|2.8ms|
|csv|0.5ms|

```python
from cofutils import cofmem, cofcsv, coftimer
import torch
cofmem.set_writer('tb,csv', name="test-1")
coftimer.set_writer('tb,csv', name="test-1")
timer = coftimer(name='test-1')
cofmem("Before Init Random Tensor")
tensor1 = torch.rand((1024, 1024, 128), dtype=torch.float32, device='cuda:0')
tensor2 = torch.rand((1024, 1024, 128), dtype=torch.float32, device='cuda:0')


with timer:
    cofmem("After Init Random Tensor")
    add_result = tensor1 + tensor2
    cofmem("After Addition")

    subtract_result = tensor1 - tensor2
    cofmem("After Subtraction")

    multiply_result = tensor1 * tensor2
    cofmem("After Multiplication")

    divide_result = tensor1 / tensor2
    cofmem("After Division")

coftimer.log()
cofcsv.save()

```
Note that `cofmem` would return a dict which contains memory report.
```bash
(deepspeed) haiqwa@gpu9:~/documents/cofutils$ python ~/test.py 
[2023-11-11 15:32:46.873]  [Cof INFO]: before xxx GPU Memory Report (GB): MA = 0.00 | MM = 0.00 | MR = 0.00
[2023-11-11 15:32:46.873]  [Cof INFO]: after xxx GPU Memory Report (GB): MA = 0.00 | MM = 0.00 | MR = 0.00
```
---

### Cofrun is all you need!
User can easily launch distributed task by `cofrun`. What users need to do is to provide a template bash file and configuration json file.

You can see the examples in `example/`

```bash
usage: cofrun [-h] [--file FILE] [--input_dir INPUT_DIR] [--template-file TEMPLATE_FILE]
              [--output_dir OUTPUT_DIR] [--test] [--nsys] [--list] [--range RANGE]
              [--summary SUMMARY]

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  configuration file path
  --input_dir INPUT_DIR, -i INPUT_DIR
                        run experiments in batch mode. all config files are placed in input
                        directory
  --template-file TEMPLATE_FILE, -T TEMPLATE_FILE
                        provide the path of template .sh file
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        write execution output to specific path
  --test, -t            use cofrun in test mode -> just generate bash script
  --nsys, -n            use nsys to profile your cuda programme
  --list, -l            list id of all input files, only available when input dir is provided
  --range RANGE, -r RANGE
                        support 3 formats: [int | int,int,int... | int-int], and int value must be
                        > 0; for example, --range 0,1-3,6
  --summary SUMMARY, -s SUMMARY
                        provide your directory path which contains output files and cofrun would
                        give the experiment summary in csv format
```

Let's run the example:

```bash
cofrun -f demo_config.json -T demo_template.sh
```

If you use batch mode, there're some tips which maybe helpful for you:

```bash
Cofrun is ready to execute multiple tasks in batch mode. There're maybe some useful suggestions: 
    1. install and launch tmux. the following are some necessary related instructions: 
        * create a new tmux window: tmux new -s cof
        * detach from the current session: Ctrl+b d
        * attach to an existing session: tmux attach -t cof
    2. the process would hang up if distributed task crashes. we strongly recommand you to: 
        * add "export TORCH_NCCL_ASYNC_ERROR_HANDLING=1, pkill python" to your template script
        * if process hangs up, you can input "pkill python" command or Ctrl+C to skip the current task
```

And the execution history of cofrun will be written into `history.cof`
