import csv
from collections import deque

class Process:
    def __init__(self, pid, burst_time, memory_bytes):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_bytes = memory_bytes
        self.completion_time = 0

class Processor:
    def __init__(self, name):
        self.name = name
        self.available_time = 0

processors = [
    Processor("pa"), Processor("pb"), Processor("pc"),
    Processor("pd"), Processor("pe"), Processor("pf")
]
###################################################################
def clone_processes(process_list):
    out = []
    for p in process_list:
        out.append(Process(p.pid, p.burst_time, p.memory_bytes))
    return out

def get_next_processor():
    earliest = processors[0]
    for p in processors:
        if p.available_time < earliest.available_time:
            earliest = p
    return earliest

def reset_processors():
    for p in processors:
        p.available_time = 0

###################################################################
def fifo(process_list):
    reset_processors()

    for p in process_list:
        proc = get_next_processor()
        finish = proc.available_time + p.burst_time
        proc.available_time = finish
        p.completion_time = finish

    wait = 0
    turn = 0

    for p in process_list:
        wait += p.completion_time - p.burst_time
        turn += p.completion_time

    return wait / len(process_list), turn / len(process_list)


def sjf(process_list):
    reset_processors()

    process_list.sort(key=lambda p: p.burst_time)

    for p in process_list:
        proc = get_next_processor()
        finish = proc.available_time + p.burst_time
        proc.available_time = finish
        p.completion_time = finish

    wait = 0
    turn = 0

    for p in process_list:
        wait += p.completion_time - p.burst_time
        turn += p.completion_time

    return wait / len(process_list), turn / len(process_list)

def rr(process_list):
    reset_processors()

    time_quantum = 10**6
    queue = deque(process_list)

    while queue:
        p = queue.popleft()
        proc = get_next_processor()

        if p.remaining_time <= time_quantum:
            run = p.remaining_time
        else:
            run = time_quantum

        finish = proc.available_time + run
        proc.available_time = finish
        p.remaining_time -= run

        if p.remaining_time == 0:
            p.completion_time = finish
        else:
            queue.append(p)

    wait = 0
    turn = 0

    for p in process_list:
        wait += p.completion_time - p.burst_time
        turn += p.completion_time

    return wait / len(process_list), turn / len(process_list)


if __name__ == "__main__":
    process_list = []

    with open("processes.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            pid = int(row[0])
            burst = int(row[1])
            memory = int(row[2])
            process_list.append(Process(pid, burst, memory))

    fifo_result = fifo(clone_processes(process_list))
    sjf_result = sjf(clone_processes(process_list))
    rr_result = rr(clone_processes(process_list))

    print("\noutput: (avg_wait, avg_turnaround) in cpu cycles\n")
    print("fifo:", fifo_result)
    print("sjf :", sjf_result)
    print("rr  :", rr_result)