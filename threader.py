import threading

class ThreadResult:
    not_started = 0
    success = 1
    timeout = 2
    error = 3

def init_result():
    return {
        'status': ThreadResult.not_started,
        'retval': None
    }

def wrapper(task, result):
    def wrapped_task():
        try:
            val = task()
            result['retval'] = val
            result['status'] = ThreadResult.success
        except Exception as e:
            result['retval'] = e
            result['status'] = ThreadResult.error
    return wrapped_task

def run_on_other_threads(tasks, timeout):
    thread_data = []
    found_problem = False
    results = []
    for task in tasks:
        this_result = init_result()
        thread = threading.Thread(target=wrapper(task, this_result))
        thread_data.append((thread, this_result))
        thread.start()

    for data in thread_data:
        (thread, result) = data
        thread.join(timeout)
        if thread.isAlive():
            found_problem = True
        else:
            if result['status'] == ThreadResult.success:
                results.append(result['retval'])
            else:
                found_problem = True
    return (not found_problem, results)
