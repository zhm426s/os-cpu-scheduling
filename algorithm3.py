import csv
# algorithm will calculate wich processor a process will be assigned to, 
# in what order the processes will go in, and for how long
# also what the average turnaround time is.
# NEW ADDITION (According to assignment): Take into account memory availibility

# processes should have cycle amounts between 1 and 1000000 (in ten millions, 10 million to 10 trillion)
# processes should have memory amounts between 1 and 16000 (in MB, 1 megabyte to 16 gigabites)

def min_turnaround(processes: list) -> tuple:
    n = len(processes)

    # format for each process: 
    # [0]: list of assigned processes (pid, cycles, mem)
    # [1]: bool for if currently in use by last process
    # [2]: cycles left for current process
    # [3]: memory capacity for process

    # slow processors: PA, PB, PC -> 8GB = 8000MB
    slow = {
        'A': [[], False, 0, 8000], 
        'B': [[], False, 0, 8000], 
        'C': [[], False, 0, 8000]
    } 

    # fast processors: PD, PE, PF -> 16GB = 16000MB
    fast = {
        'D': [[], False, 0, 16000], 
        'E': [[], False, 0, 16000], 
        'F': [[], False, 0, 16000]
    }

    time = 0.0

    # pointers to track which processes have been assigned
    num_assigned_slow = 0       # slow => index of smallest not completed (front of list)
    num_assigned_fast = -1      # fast => neg index of largest not completed (back of list)

    num_completed = 0           # to keep track of while loop
    num_assigned = 0            # to keep track of how many processes are available to assign

    used = [False] * n          # track which processes have already been assigned

    completion_times = {}       # track completion time of each process for average turnaround

    # first, sort processes in order of ascending burst time
    # assumption: Program knows all processes and is able to adjust accordingly
    processes = merge_sort_proc(processes)

    # turnaround time for whole set is time it takes to complete all processes
    # assumes processes = list of tuples w/ format (pid, cycles, memory)
    while num_completed < n:

        # ---------------- SLOW PROCESSORS ----------------
        # decrement cycles in currently assigned slow procs and
        # assign smallest non-assigned process to a slow processor
        for p in ['A', 'B', 'C']:
            if slow[p][1]:      # if there is a process in this core
                slow[p][2] -= 2 * 0.25      # decrement the amount completed

                # check if the process is now complete, remove if it is
                if slow[p][2] <= 0:
                    slow[p][1] = False
                    slow[p][2] = 0

                    # record completion time
                    finished_proc = slow[p][0][-1]
                    completion_times[finished_proc[0]] = time

                    num_completed += 1

            # if processor is idle then assign new process
            if not slow[p][1]:
                # find next process that fits memory constraint
                while num_assigned_slow < n:
                    if used[num_assigned_slow]:
                        num_assigned_slow += 1
                        continue

                    proc = processes[num_assigned_slow]

                    # check if process memory fits this processor
                    if proc[2] <= slow[p][3]:
                        slow[p][0].append(proc)
                        slow[p][1] = True
                        slow[p][2] = proc[1]

                        used[num_assigned_slow] = True
                        num_assigned_slow += 1      # move pointer only when a process is assigned
                        num_assigned += 1
                        break
                    else:
                        num_assigned_slow += 1

        # ---------------- FAST PROCESSORS ----------------
        # decrement cycles in currently assigned fast procs and
        # assign largest non-assigned process to a fast processor
        for p in ['D', 'E', 'F']:
            if fast[p][1]:      # if there is a process in this core
                fast[p][2] -= 4 * 0.25      # decrement the amount completed

                # check if the process is now complete, remove if it is
                if fast[p][2] <= 0:
                    fast[p][1] = False
                    fast[p][2] = 0

                    # record completion time
                    finished_proc = fast[p][0][-1]
                    completion_times[finished_proc[0]] = time

                    num_completed += 1

            # if processor is idle  assign new process
            if not fast[p][1]:
                # traverse from largest jobs backward
                while abs(num_assigned_fast) <= n:
                    if used[num_assigned_fast]:
                        num_assigned_fast -= 1
                        continue

                    proc = processes[num_assigned_fast]

                    # check memory constraint
                    if proc[2] <= fast[p][3]:
                        fast[p][0].append(proc)
                        fast[p][1] = True
                        fast[p][2] = proc[1]

                        used[num_assigned_fast] = True
                        num_assigned_fast -= 1      # move pointer only when a process is assigned
                        num_assigned += 1
                        break
                    else:
                        num_assigned_fast -= 1

        if num_assigned != num_completed:
            time += 0.25        # time is moving; time increments by 0.25 since fastest speed = 4 and 4 * 0.25 = 1 = smallest val of cycles

    time /= 1000000000
    avg_time = (sum(completion_times.values()) / n) / 1000000000

    # ---------------- CLEAN OUTPUT FORMATTING ----------------
    slow_stats = {}
    fast_stats = {}

    for p in slow:
        slow_stats[p] = {
            "processes": slow[p][0],
            "count": len(slow[p][0]),
            "memory": slow[p][3]
        }

    for p in fast:
        fast_stats[p] = {
            "processes": fast[p][0],
            "count": len(fast[p][0]),
            "memory": fast[p][3]
        }

    return (time, avg_time, slow_stats, fast_stats)


# ---------------- MERGE SORT ----------------
def merge_sort_proc(processes):
    if len(processes) < 2:
        return processes

    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i][1] < right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(processes) // 2
    left = processes[:mid]
    right = processes[mid:]

    return merge(merge_sort_proc(left), merge_sort_proc(right))


# ---------------- MAIN ----------------
if __name__ == '__main__':
    process_list = []

    with open("processes.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            pid = int(row[0])
            burst = int(row[1])
            memory = int(row[2])
            process_list.append([pid, burst, memory])

    results = min_turnaround(process_list)

    slow_stats = results[2]
    fast_stats = results[3]

    print("\n================ RESULTS ================\n")

    print(f"TOTAL TURNAROUND TIME: {results[0]} seconds")
    print(f"AVERAGE TURNAROUND TIME: {results[1]} seconds\n")

    print("=========== SLOW PROCESSORS (A, B, C) ===========")
    for p in slow_stats:
        s = slow_stats[p]
        print(f"\nProcessor {p}:")
        print(f"  Total Runtime: {sum(proc[1] for proc in s['processes'])}")
        print(f"  Average Runtime: {(sum(proc[1] for proc in s['processes']) / s['count']) if s['count'] > 0 else 0}")
        print(f"  Process Count: {s['count']}")

    print("\n=========== FAST PROCESSORS (D, E, F) ===========")
    for p in fast_stats:
        f = fast_stats[p]
        print(f"\nProcessor {p}:")
        print(f"  Total Runtime: {sum(proc[1] for proc in f['processes'])}")
        print(f"  Average Runtime: {(sum(proc[1] for proc in f['processes']) / f['count']) if f['count'] > 0 else 0}")
        print(f"  Process Count: {f['count']}")