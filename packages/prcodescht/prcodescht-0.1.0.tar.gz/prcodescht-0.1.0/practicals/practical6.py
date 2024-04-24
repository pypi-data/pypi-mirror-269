from mrjob.job import MRJob
import re

class SentenceCountJob(MRJob):
    
    def mapper(self, _, line):
        sentences = re.split(r'[.!?]', line)
        for sentence in sentences:
            if sentence.strip():
                yield sentence.strip(), 1
    
    def reducer(self, key, values):
        yield key, sum(values)
if __name__ == '__main__':
    SentenceCountJob.run()
