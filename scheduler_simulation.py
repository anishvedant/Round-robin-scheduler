import threading
import time

class Thread:
    def _init_(self, thread_id, priority):
        self.thread_id = thread_id
        self.priority = priority
        self.state = "READY"
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0  # Track waiting time for each thread

class Scheduler:
    def _init_(self):
        self.threads = []
        self.current_thread_index = -1
        self.last_scheduling_time = time.time()  # Keep track of the last scheduling time

    def add_thread(self, thread):
        self.threads.append(thread)

    def schedule_rr_with_priority(self):
        if not self.threads:
            return None
        
        current_time = time.time()
        self.current_thread_index = (self.current_thread_index + 1) % len(self.threads)
        next_thread = self.threads[self.current_thread_index]

        # Update waiting time for the current thread
        if next_thread.state == "READY":
            next_thread.waiting_time += current_time - self.last_scheduling_time

        # Update last scheduling time
        self.last_scheduling_time = current_time

        return next_thread

    def suspend_thread(self, thread_id):
        for thread in self.threads:
            if thread.thread_id == thread_id and thread.state == "READY":
                thread.state = "SUSPENDED"
                return True
        return False

    def resume_thread(self, thread_id):
        for thread in self.threads:
            if thread.thread_id == thread_id and thread.state == "SUSPENDED":
                thread.state = "READY"
                return True
        return False

def thread_function(thread_id, state):
    print(f"Thread {thread_id} is {state}...")
    time.sleep(1)  # Simulating thread execution time

def simulate_execution(scheduler, scheduling_algorithm, num_iterations=5):
    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    start_time = time.time()

    for i in range(num_iterations):
        num_threads = len(scheduler.threads)
        print(f"\nIteration {i + 1}:")  # Print iteration message before each iteration
        if num_threads == 0:
            print("No threads to execute.")
            continue  # Skip to the next iteration if there are no threads available
        
        for thread in list(scheduler.threads):  # Create a copy of the list to iterate over
            next_thread = scheduling_algorithm()
            if next_thread:
                if next_thread.state == "READY":
                    next_thread.state = "RUNNING"
                    print(f"Thread {next_thread.thread_id} transitioned from READY to RUNNING")
                thread_function(next_thread.thread_id, next_thread.state)
                next_thread.state = "FINISHED"
                print(f"Thread {next_thread.thread_id} transitioned from RUNNING to FINISHED")

                total_turnaround_time += 1  # Assuming each thread takes 1 unit of time
                total_waiting_time += next_thread.waiting_time
                total_response_time += time.time() - start_time  # Update response time here
                time.sleep(0.1)  # Introduce a small delay between scheduling threads

    end_time = time.time()

    num_threads = len(scheduler.threads)
    throughput = num_iterations / (end_time - start_time) if num_threads > 0 else 0
    cpu_utilization = (total_turnaround_time / (end_time - start_time)) * 100 if num_threads > 0 else 0
    avg_turnaround_time = total_turnaround_time / (num_iterations * num_threads) if num_threads > 0 else 0
    avg_waiting_time = total_waiting_time / num_threads if num_threads > 0 else 0
    avg_response_time = total_response_time / (num_iterations * num_threads) if num_threads > 0 else 0

    print(f"\nnum_threads: {num_threads}")
    print(f"Throughput: {throughput} threads/second")
    print(f"CPU Utilization: {cpu_utilization}%")
    print(f"Average Turnaround Time: {avg_turnaround_time} seconds")
    print(f"Average Waiting Time: {avg_waiting_time} seconds")
    print(f"Average Response Time: {avg_response_time} seconds")

def main():
    scheduler = Scheduler()

    # Create some threads with different priorities
    for i in range(5):
        priority = i % 3  # Assign priority based on the remainder of i divided by 3
        thread = Thread(thread_id=i, priority=priority)
        scheduler.add_thread(thread)

    # Resume all threads
    print("Resuming all threads...")
    for thread in scheduler.threads:
        scheduler.resume_thread(thread.thread_id)

    # Simulate execution for Round Robin scheduling with priority
    print("\nRound Robin scheduling with priority:")
    simulate_execution(scheduler, scheduler.schedule_rr_with_priority)

    # Suspend all threads
    print("\nSuspending all threads...")
    for thread in scheduler.threads:
        scheduler.suspend_thread(thread.thread_id)

    # Simulate execution for Round Robin scheduling with priority after suspension
    print("\nRound Robin scheduling with priority after suspension:")
    simulate_execution(scheduler, scheduler.schedule_rr_with_priority)

if __name__ == "_main_":
    main()
