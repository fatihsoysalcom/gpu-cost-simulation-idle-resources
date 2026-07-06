import time

class GPUTask:
    def __init__(self, name, cost_per_second=0.0001): # Example cost: $0.36/hour
        self.name = name
        self.cost_per_second = cost_per_second
        self.start_time = None
        self.stop_time = None
        self.is_running = False

    def start(self):
        if not self.is_running:
            print(f"[{self.name}] Starting GPU instance...")
            self.start_time = time.time()
            self.is_running = True
        else:
            print(f"[{self.name}] Instance is already running.")

    def stop(self):
        if self.is_running:
            print(f"[{self.name}] Stopping GPU instance...")
            self.stop_time = time.time()
            self.is_running = False
        else:
            print(f"[{self.name}] Instance is not running.")

    def get_actual_duration(self):
        if self.start_time is None:
            return 0
        if self.is_running: # If still running, calculate up to the current moment
            return time.time() - self.start_time
        return self.stop_time - self.start_time

    def calculate_cost(self):
        duration = self.get_actual_duration()
        return duration * self.cost_per_second

def simulate_work(task_name, duration_seconds):
    print(f"[{task_name}] Simulating work for {duration_seconds:.1f} seconds...")
    time.sleep(duration_seconds)
    print(f"[{task_name}] Work completed.")

# --- Main Simulation ---
if __name__ == "__main__":
    print("--- GPU Cost Simulation: Identifying Idle Resource Charges ---")
    print("This simulation demonstrates how forgetting to stop a cloud GPU instance")
    print("can lead to unexpected 'hidden' costs due to idle time.")
    print("-" * 70)

    # Scenario 1: Properly managed task
    print("\nScenario 1: 'Training Model A' - Properly stopped after use.")
    model_a_task = GPUTask("Training Model A", cost_per_second=0.0002) # Example cost rate
    model_a_task.start()
    simulate_work(model_a_task.name, 3) # Simulate 3 seconds of training
    model_a_task.stop() # Task is stopped immediately after work
    cost_a = model_a_task.calculate_cost()
    print(f"[{model_a_task.name}] Actual duration: {model_a_task.get_actual_duration():.2f} seconds")
    print(f"[{model_a_task.name}] Total cost: ${cost_a:.4f}")
    print("-" * 70)

    # Scenario 2: Task forgotten to be stopped (the 'hidden cost')
    print("\nScenario 2: 'Data Preprocessing B' - Forgotten to be stopped.")
    model_b_task = GPUTask("Data Preprocessing B", cost_per_second=0.00015) # Another example cost rate
    model_b_task.start()
    simulate_work(model_b_task.name, 2) # Simulate 2 seconds of preprocessing
    # --- IMPORTANT: The 'model_b_task.stop()' call is intentionally omitted here ---
    print(f"[{model_b_task.name}] Work finished, but the instance was *forgotten* to be stopped.")

    # Simulate some time passing while the instance is still running idly
    idle_time_simulated = 5 # seconds
    print(f"[{model_b_task.name}] Instance runs idly for an additional {idle_time_simulated} seconds...")
    time.sleep(idle_time_simulated)

    # Now, calculate the cost as if the bill arrived and the instance was still running or stopped much later.
    # For demonstration, we'll stop it now to get a final cost.
    model_b_task.stop()

    # Calculate what the cost *should* have been if stopped immediately after work
    cost_b_expected_work = 2 * model_b_task.cost_per_second
    # Calculate the actual total cost incurred
    cost_b_actual = model_b_task.calculate_cost()
    # The difference is the hidden cost from idle time
    hidden_idle_cost = cost_b_actual - cost_b_expected_work

    print(f"[{model_b_task.name}] Expected cost (if stopped immediately after work): ${cost_b_expected_work:.4f}")
    print(f"[{model_b_task.name}] Actual duration: {model_b_task.get_actual_duration():.2f} seconds")
    print(f"[{model_b_task.name}] Actual total cost: ${cost_b_actual:.4f}")
    print(f"[{model_b_task.name}] Hidden idle cost: ${hidden_idle_cost:.4f} (from {idle_time_simulated}s of idle time)") # Illustrates the hidden charge
    print("-" * 70)

    print("\nSummary:")
    print(f"Total cost for properly managed task: ${cost_a:.4f}")
    print(f"Total cost for forgotten task (including hidden idle cost): ${cost_b_actual:.4f}")
    print("This simulation highlights how idle cloud resources can significantly inflate your GPU bill.")
