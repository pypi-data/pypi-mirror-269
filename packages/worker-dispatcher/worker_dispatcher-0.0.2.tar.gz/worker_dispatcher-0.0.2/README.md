<p align="center">
    <a href="https://www.python.org/psf-landing/" target="_blank">
        <img src="https://www.python.org/static/community_logos/python-logo.png" height="60px">
    </a>
    <h1 align="center">Python Worker Dispatcher</h1>
    <br>
</p>

A flexible task dispatcher for Python with multiple threading or processing control

Features
--------

- ***Tasks Dispatching** to managed worker*

- ***Elegant Interface** for setup and use*

---

OUTLINE
-------

- [Demonstration](#demonstration)
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
    - [Option](#option)
        - [callbacks.process](#callbacksprocess)
        - [callbacks.task](#callbackstask)

---

DEMONSTRATION
-------------

Use 20 theads concurrently to dispatch tasks for HTTP reqeusts

```python
import worker_dispatcher
import requests

def each_task(config, task_id: int, task_data):
    response = requests.get(config['my_endpoint'] + task_data)
    return response

responses = worker_dispatcher.start({
    'task': {
        'list': ['ORD_AH001', 'ORD_KL502', '...' , 'ORD_GR393'],
        'callback': each_task,
        'config': {
            'my_endpoint': 'https://your.name/order-handler/'
        },
    },
    'worker': {
        'number': 20,
    }
})
```

Utilizes all CPU cores on the machine to compute tasks.

```python
import worker_dispatcher

def each_task(config, task_id: int, task_data):
    result = sum(task_id * i for i in range(10**9))
    return result

if __name__ == '__main__':
    results = worker_dispatcher.start({
        'task': {
            'list': 10,
            'callback': each_task,
        },
        'worker': {   
            'multiprocessing': True
        }
    })
```

---
