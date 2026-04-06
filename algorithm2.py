# algorithm will calculate wich processor a process will be assigned to, 
# in what order the processes will go in, and for how long
# also what the average turnaround time is

# processes should have cycle amounts between 1 and 1000000 (in ten millions, 10 million to 10 trillion)
# processes should have cycle amounts between 1 and 16000 (in MB, 1 megabyte to 16 gigabites)
def min_turnaround(processes: list) -> tuple:
    n = len(processes)
    slow = {'A': [[], False, 0], 'B': [[], False, 0], 'C': [[], False, 0]} # format: [list of assigned processes (pid, cycles, mem), currently in use by last process, cycles left for curr process]
    fast = {'D': [[], False, 0], 'E': [[], False, 0], 'F': [[], False, 0]}
    time = 0.0
    num_assigned_slow = 0 # how many the slow processors have been assigned (index of smallest not completed)
    num_assigned_fast = -1 # how many the fast processors have been assigned (neg index of largest not completed)
    num_completed = 0 # to keep track of while loop
    num_assigned = 0 # to keep track of how many processes are available to assign


    # first, sort processes in order of ascending burst time
    processes = merge_sort_proc(processes)

    # turnaround time for whole set is time it takes to complete all processes
    # assumes processes = list of tuples w/ format (pid, cycles, memory)
    while num_completed < n:
        # decrement cycles in currently assigned slow procs and
        # assign smallest non-assigned process to a slow processor
        for p in ['A', 'B', 'C']:
            if slow[p][1]: # if there is a process in this core
                slow[p][2] -= 2 * 0.25 # decrement the amount completed
                # check if the process is now complete, remove if it is
                if slow[p][2] <= 0:
                    slow[p][1] = False
                    slow[p][2] = 0
                    num_completed += 1
            # check if processor is available and set it up if it is
            if not(slow[p][1]) and num_assigned != n:
                slow[p][0].append(processes[num_assigned_slow])
                slow[p][1] = True
                slow[p][2] = slow[p][0][-1][1]
                num_assigned += 1
                num_assigned_slow += 1

        # decrement cycles in currently assigned fast procs and
        # assign largest non-assigned process to a fast processor
        for p in ['D', 'E', 'F']:
            if fast[p][1]: # if there is a process in this core
                fast[p][2] -= 4 * 0.25 # decrement the amount completed
                # check if the process is now complete, remove if it is
                if fast[p][2] <= 0:
                    fast[p][1] = False
                    fast[p][2] = 0
                    num_completed += 1
            # check if processor is available and set it up if it is
            if not(fast[p][1]) and num_assigned != n:
                fast[p][0].append(processes[num_assigned_fast])
                fast[p][1] = True
                fast[p][2] = fast[p][0][-1][1]
                num_assigned += 1
                num_assigned_fast -= 1
        
        if num_assigned != num_completed:
            time += 0.25 # time is moving; time increments by 0.25 since fastest speed = 4 and 4 * 0.25 = 1 = smallest val of cycles
    return (time, slow, fast)
        

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

    sorted_left = merge_sort_proc(left)
    sorted_right = merge_sort_proc(right)
    return merge (sorted_left, sorted_right)

if __name__ == '__main__':
    # test data if we are not actively using the 250 generated processes
    test_data = [(1, 6000, 10), (2, 40000, 200), (3, 20, 1200),
                 (4, 80000, 8120), (5, 1, 400), (6, 1000000, 1000), 
                 (7, 800, 230), (8, 12, 7821), (9, 612, 10000),
                 (10, 9820, 812), (11, 15, 4082), (12, 170000, 1190), 
                 (13, 720, 82), (14, 1509, 482), (15, 184200, 1), 
                 (16, 10, 2), (17, 34, 4122), (18, 170, 16000)]
    results = min_turnaround(test_data)
    print(f'Turnaround: {results[0]}')
    print(results[1])
    print(results[2])