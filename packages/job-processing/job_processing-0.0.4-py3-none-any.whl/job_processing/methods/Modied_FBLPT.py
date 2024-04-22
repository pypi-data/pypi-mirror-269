def modied_FBLPT(jobs, machines):
    # Sort jobs in decreasing order of the average processing time for all machines
    avg_processing_time_per_job = []
    for job in jobs:
        avg_processing_time_per_job.append(sum(
            machines[job.job_size].processing_time_of_jobs) / len(machines[job.job_size].processing_time_of_jobs))
    return avg_processing_time_per_job
