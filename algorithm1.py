import csv 
from collections import deque  # deque is used in Round Robin

# ---------------- PROCESS CLASS ----------------
# represents a single process/job in the system
class Process:
    def __init__(self, pid, burst_time, memory_bytes):
        self.pid = pid                          # unique process ID
        self.burst_time = burst_time            # total CPU time required
        self.remaining_time = burst_time        # used for RR scheduling (decreases over time)
        self.memory_bytes = memory_bytes        # memory requirement (not used in scheduling here)
        self.completion_time = 0                # time when process finishes execution

# ---------------- PROCESSOR CLASS ----------------
# represents a CPU/core that executes processes
class Processor:
    def __init__(self, name):
        self.name = name                        # processor identifier (pa, pb, etc.)
        self.available_time = 0                 # next time this processor becomes free

# initialize processors
processors = [
    Processor("pa"), Processor("pb"), Processor("pc"),
    Processor("pd"), Processor("pe"), Processor("pf")
]

# ---------------- HELPER FUNCTIONS ----------------
# creates a deep copy of process list
# ensures each scheduling algorithm runs independently
def clone_processes(process_list):
    out = []
    for p in process_list:
        # create a new Process object with same values
        out.append(Process(p.pid, p.burst_time, p.memory_bytes))
    return out

# finds the processor that becomes available the earliest
# this simulates assigning the next job to the least busy processor
def get_next_processor():
    earliest = processors[0]

    for p in processors:
        # choose processor with smallest available_time
        if p.available_time < earliest.available_time:
            earliest = p

    return earliest

# resets all processors before running a new scheduling algorithm
def reset_processors():
    for p in processors:
        p.available_time = 0    # all processors start idle at time 0

# ---------------- FIFO SCHEDULING ----------------
# First-In-First-Out: processes executed in order of arrival
def fifo(process_list):
    reset_processors()  # ensure clean state

    # assign each process in given order
    for p in process_list:
        proc = get_next_processor()  # pick earliest available processor

        finish = proc.available_time + p.burst_time  # when process will finish
        proc.available_time = finish                 # update processor availability
        p.completion_time = finish                   # record process completion

    # compute average waiting and turnaround times
    wait = 0
    turn = 0

    for p in process_list:
        wait += p.completion_time - p.burst_time  # waiting = turnaround - burst
        turn += p.completion_time                 # turnaround = completion time

    return wait / len(process_list), turn / len(process_list)


# ---------------- SJF SCHEDULING ----------------
# Shortest Job First: execute smallest burst jobs first
def sjf(process_list):
    reset_processors()

    # sort processes by burst time (ascending)
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


# ---------------- ROUND ROBIN SCHEDULING ----------------
# each process gets a fixed time slice (quantum)
def rr(process_list):
    reset_processors()

    time_quantum = 10**2        # fixed time slice (100 CPU cycles)
    queue = deque(process_list) # queue for RR scheduling

    # continue until all processes are completed
    while queue:
        p = queue.popleft()         # get next process in queue
        proc = get_next_processor() # assign to earliest available processor

        # determine how long this process will run in this cycle
        if p.remaining_time <= time_quantum:
            run = p.remaining_time   # finish process
        else:
            run = time_quantum       # only run for quantum

        finish = proc.available_time + run  # compute finish time
        proc.available_time = finish        # update processor availability
        p.remaining_time -= run             # reduce remaining work

        # if process finished, record completion
        if p.remaining_time == 0:
            p.completion_time = finish
        else:
            queue.append(p)  # otherwise requeue it for another turn

    wait = 0
    turn = 0

    for p in process_list:
        wait += p.completion_time - p.burst_time
        turn += p.completion_time

    # multiplied by 10 (scaling adjustment for time quantum effects)
    return 10 * wait / len(process_list), 10 * turn / len(process_list)


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    process_list = []

    # read process data from CSV file
    with open("processes.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row

        for row in reader:
            pid = int(row[0])      # process ID
            burst = int(row[1])    # CPU burst time
            memory = int(row[2])   # memory requirement

            # create Process object and add to list
            process_list.append(Process(pid, burst, memory))

    # run all scheduling algorithms on separate copies of process list
    fifo_result = fifo(clone_processes(process_list))
    sjf_result = sjf(clone_processes(process_list)) 
    rr_result = rr(clone_processes(process_list))

    # output results
    print("\noutput: (avg_wait, avg_turnaround) in millions of cpu cycles")
    print("FIFO:", fifo_result)
    print("SJF:", sjf_result)
    print("RR:", rr_result)