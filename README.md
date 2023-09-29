# Convenient multiprocessing with Message Queues
[pypi](https://pypi.org/project/multiprocessing-mq/) \
[中文](./README-cn.md)
## Features
- Lightning-fast startup: New processes launch in just 10ms.
- Lightning-fast execution: Sending code (with parameters) takes only 0.8ms.
- Easy to use: Thanks to `interactivity.py`, minimal modifications are required.
- Automatically suspends when idle, conserving resources.

## Usage
(We recommend referring to `example.py` for guidance)
### Creating Processes
```python
import multiprocessing_mq as mq
my_pro = mq.Process(init=init_code, suspend=True, rest_time=0)
```
#### Parameters
- `init`: Initialization code.
- `suspend`: Whether to suspend.
- `rest_time`: Sleep time.
- `process_events`: Performs event loop while waiting for process to resume, preventing UI from freezing.

### Usage
There are multiple ways to send tasks to child processes. Among them, using `inter` is the simplest.
#### inter
Create a virtual class to simulate the environment of a child process. For example, to retrieve the value of `a` inside the child process, you only need `my_pro.inter.a`. Running a function only requires `my_pro.inter.a()`.
#### run_com
Run a function and wait for a return value.
```python
run_com(self, code: str, args: dict = {}, process_events=None)
```
- `code`: The code to execute.
- `args`: Arguments (**Note:** `args` won't automatically pass parameters; you need to pass them yourself within `code`).
- `process_events`: Performs an event loop while waiting for the process result, preventing the UI from freezing.

**Note:** `run_com` uses `eval` to execute functions, so you cannot use it to modify variable values (you can use `run_without_return` instead).
#### run_without_return
```python
run_without_return(self, code: str, args: dict = {})
```
Run a function without waiting for a return value; internally uses `exec`.