import multiprocessing, concurrent.futures
import time, copy

# Sample callback function
def callback_sample(id: int, config=None, task=None):
    if id == 1:
        print("Runing sample task function, please customize yours according to the actual usage.")
    result = {
        'taskId': id
    }
    return result

# Sample result callback function
def result_callback_sample(id: int, config=None, result=None, log: dict=None):
    if id == 1:
        print("Runing sample result function, please customize yours according to the actual usage.")
    return result

# Default configuration
default_config = {
    'debug': False,
    'task': {
        'list': [],                     # Support list and integer. Integer represent the number of tasks to be generated.
        'callback': callback_sample,
        'config': {},
        'result_callback': False
    },
    'worker': {
        'number': multiprocessing.cpu_count(),
        'per_second': 0,                # If greater than 0, the specified number of workers run at set intervals.
        'multiprocessing': False
    }
}

results = []
logs = []

# Start function
def start(userConfig: dict):

    global results, logs
    results = []
    logs = []

    # Merge config with 2 level
    config = copy.deepcopy(default_config)
    for level1_key in config.keys():
        if level1_key in userConfig:
            if isinstance(config[level1_key], dict):
                config[level1_key].update(userConfig[level1_key])
            else:
                config[level1_key] = userConfig[level1_key]

    # Multi-processing handler
    use_multiprocessing = config['worker']['multiprocessing']
    if use_multiprocessing:
        in_child_process = (multiprocessing.current_process().name != 'MainProcess')
        # Return False if is in worker process to let caller handle
        if in_child_process:
            # print("Exit procedure due to the child process")
            return False
        
    # Debug mode
    if config['debug']:
        print("Configuration:")
        print(config)

    # Callback check
    if not callable(config['task']['callback']):
        exit("Callback function is invalied")

    # Task list to queue
    task_list = []
    user_task_list = config['task']['list']
    if isinstance(user_task_list, list):
        id = 1
        for task in user_task_list:
            data = {
                'id': id,
                'task': task
            }
            task_list.append(data)
            id += 1
    elif isinstance(user_task_list, int):
        for i in range(user_task_list):
            id = i + 1
            data = {
                'id': id,
                'task': {}
            }
            task_list.append(data)

    # Worker dispatch
    worker_num = config['worker']['number']
    worker_num = worker_num if isinstance(worker_num, int) else 1
    worker_per_second = config['worker']['per_second'] if config['worker']['per_second'] else 0
    max_workers = len(task_list) if worker_per_second else worker_num
    # result_queue = multiprocessing.Queue() if use_multiprocessing else queue.Queue()
    pool_executor_class = concurrent.futures.ProcessPoolExecutor if use_multiprocessing else concurrent.futures.ThreadPoolExecutor
    print("Start to dispatch workers ---\n")

    # Pool Executor
    with pool_executor_class(max_workers=max_workers) as executor:
        pool_results = []
        # Task dispatch
        for task in task_list:
            pool_result = executor.submit(consume_task, task, config)
            pool_results.append(pool_result)
            # Worker per_second setting
            if worker_per_second and task['id'] % worker_num == 0:
                time.sleep(float(worker_per_second))
        # Get results from the async results
        for pool_result in concurrent.futures.as_completed(pool_results):
            log = pool_result.result()
            result = log['result']
            if callable(config['task']['result_callback']):
                result = config['task']['result_callback'](config=config['task']['config'], id=log['task_id'], result=log['result'], log=log)
            logs.append(log)
            results.append(result)
        # results = [result.result() for result in concurrent.futures.as_completed(pool_results)]

    print("End of worker dispatch ---\n")
    return results

# Worker function
def consume_task(data, config):
    started_at = time.time()
    return_value = config['task']['callback'](config=config['task']['config'], id=data['id'], task=data['task'])
    ended_at = time.time()
    duration = ended_at - started_at
    log = {
        'task_id': data['id'],
        'started_at': started_at,
        'ended_at': ended_at,
        'duration': duration,
        'result': return_value
    }
    return log

def get_results():
    return results

def get_logs():
    return logs