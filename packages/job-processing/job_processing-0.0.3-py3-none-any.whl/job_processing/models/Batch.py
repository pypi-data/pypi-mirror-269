class Batch:
    def __init__(self, batch_size):
        self.jobs = []
        self.processing_time = 0
        self.batch_size = batch_size

    def add_job(self, job):
        self.jobs.append(job)
        self.processing_time += job.processing_time

    def remove_job(self, job):
        self.jobs.remove(job)
        self.processing_time -= job.processing_time

    def total_size(self):
        return sum(job.job_size for job in self.jobs)
