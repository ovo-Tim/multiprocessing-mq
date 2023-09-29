# 带有消息队列的方便多进程
[pypi](https://pypi.org/project/multiprocessing-mq/) \
[English](./README.md)
## 特性
- 极速启动: 启动新进程仅需 10ms
- 极速运行: 发送代码(带参数)，仅需 0.8ms
- 简单使用: 得益于 `interactivity.py` 只需要少量修改即可完成
- 无任务时自动挂起，节省资源

## 使用
(建议参照 `example.py`)
### 创建进程
``` python
import multiprocessing_mq as mq
my_pro = mq.Process(init=init_code, suspend=True, rest_time=0)
```
#### 参数
- `init`: 初始化代码
- `suspend`: 是否挂起
- `rest_time`: 休眠时间
- `process_events`: 等待进程恢复时进行事件循环，防止界面卡死

### 使用
有多种方式可以向子进程发送任务。其中，使用 `inter` 是最简单的方式
#### inter
通过创建一个虚拟类来模拟子进程的环境
例如获取子进程内 `a` 的值只需要 `my_pro.inter.a` \
运行函数只需要 `my_pro.inter.a()`

#### run_com
运行函数并等待返回值
``` python
run_com(self, code:str,args:dict = {}, process_events = None)
```
- `code`: 要执行的代码
- `args`: 参数 (**注意：** `args`不会自动帮你把参数传进去，你需要在 `code` 自己传进去)
- `process_events`: 等待进程结果时进行事件循环，防止界面卡死

**注意：** `run_com` 使用 `eval` 来执行函数，因此你不能用它来修改变量值(你可以使用 `run_without_return`)

#### run_without_return
``` python
run_without_return(self, code:str, args:dict = {})
```
运行函数，不等待函数值，内部使用 `exec`


