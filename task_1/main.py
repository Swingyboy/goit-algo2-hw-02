from typing import List, Dict, Union
from models import PrintJob, PrinterConstraints

# Define the main function
def optimize_printing(print_jobs: List[Union[PrintJob, Dict]], printer_constraints: Union[PrinterConstraints, Dict]) -> Dict:
    # Convert dictionaries to objects
    if isinstance(printer_constraints, Dict):
        printer_constraints = PrinterConstraints(**printer_constraints)
    for i, job in enumerate(print_jobs):
        if isinstance(job, Dict):
            print_jobs[i] = PrintJob(**job)
        # Sort jobs by priority and maintain original order for same priority
        print_jobs = sorted(print_jobs, key=lambda job: (job.priority, print_jobs.index(job)))

        print_order = []
        total_time = 0
        current_volume = 0
        current_items = 0
        batch_times = []

        for job in print_jobs:
            if (current_volume + job.volume <= printer_constraints.max_volume and
                    current_items + 1 <= printer_constraints.max_items):
                # Add the job to the current batch
                print_order.append(job.id)
                current_volume += job.volume
                current_items += 1
                batch_times.append(job.print_time)
            else:
                # Finalize the current batch and reset for the next one
                total_time += max(batch_times, default=0)
                batch_times = []
                current_volume = 0
                current_items = 0

                # Add the job to the new batch
                print_order.append(job.id)
                current_volume = job.volume
                current_items = 1
                batch_times.append(job.print_time)

        # Add the time for the last batch
        if batch_times:
            total_time += max(batch_times)

        return {
            "print_order": print_order,
            "total_time": total_time
        }


# Test cases
def test_printing_optimization():
    # Test 1: Same priority models
    test1_jobs = [
        PrintJob(id="M1", volume=100, priority=1, print_time=120),
        PrintJob(id="M2", volume=150, priority=1, print_time=90),
        PrintJob(id="M3", volume=120, priority=1, print_time=150)
    ]

    # Test 2: Different priority models
    test2_jobs = [
        PrintJob(id="M1", volume=100, priority=2, print_time=120),  # Lab work
        PrintJob(id="M2", volume=150, priority=1, print_time=90),  # Diploma work
        PrintJob(id="M3", volume=120, priority=3, print_time=150)  # Personal project
    ]

    # Test 3: Exceeding volume constraints
    test3_jobs = [
        PrintJob(id="M1", volume=250, priority=1, print_time=180),
        PrintJob(id="M2", volume=200, priority=1, print_time=150),
        PrintJob(id="M3", volume=180, priority=2, print_time=120)
    ]

    constraints = PrinterConstraints(
        max_volume=300,
        max_items=2
    )

    print("Test 1 (Same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")
    assert result1['print_order'] == ['M1', 'M2', 'M3'], f"Test 1 failed: incorrect print order, calculated: {result1['print_order']}"
    assert result1['total_time'] == 270, "Test 1 failed: incorrect total time"

    print("\nTest 2 (Different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")
    assert result2['print_order'] == ['M2', 'M1', 'M3'], f"Test 2 failed: incorrect print order, calculated: {result1['print_order']}"
    assert result2['total_time'] == 270, "Test 2 failed: incorrect total time"

    print("\nTest 3 (Exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")
    assert result3['print_order'] == ['M1', 'M2', 'M3'], f"Test 3 failed: incorrect print order, calculated: {result1['print_order']}"
    assert result3['total_time'] == 450, "Test 3 failed: incorrect total time"


if __name__ == "__main__":
    test_printing_optimization()
