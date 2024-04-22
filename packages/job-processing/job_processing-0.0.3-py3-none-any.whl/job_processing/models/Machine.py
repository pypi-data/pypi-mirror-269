class Machine:
    def __init__(self, capacity, processing_time_of_jobs):
        self.machine_capacity = capacity
        self.processing_time_of_jobs = processing_time_of_jobs

    def job_processing_time(self, job):
        return self.processing_time_of_jobs[job.job_size]
