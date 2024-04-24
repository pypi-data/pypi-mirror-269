from mrjob.job import MRJob
import re

WORD_REGEXP = re.compile(r"[\w']+")
class MRWordCount(MRJob):
    def mapper(self, _, line):
        for word in WORD_REGEXP.findall(line):
            yield word, 1
    def reducer(self, word, counts):
        yield word, sum(counts)
if __name__ == '__main__':
    MRWordCount.run()
