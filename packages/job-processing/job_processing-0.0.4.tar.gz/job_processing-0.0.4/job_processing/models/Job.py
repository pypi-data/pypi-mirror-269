class Job:
    def __init__(self, release_time, due_date, processing_time, job_size):
        self.release_time = release_time
        self.due_date = due_date
        self.processing_time = processing_time
        self.job_size = job_size

    def printJob(self):
        print("release_time: ", self.release_time, "due_date: ", self.due_date,
              "processing_time: ", self.processing_time, "job_size: ", self.job_size)
