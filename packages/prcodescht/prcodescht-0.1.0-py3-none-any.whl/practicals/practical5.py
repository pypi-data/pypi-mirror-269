from mrjob.job import MRJob

class MRCharCount(MRJob):
    def mapper(self, _, line):
        for char in line.strip():
            yield char, 1
    def reducer(self, char, counts):
        yield char, sum(counts)
if __name__ == '__main__':
    MRCharCount.run()

from mrjob.job import MRJob
import re

WORD_REGEXP = re.compile(r"[\w']+")
class MRWordCount(MRJob):
    def mapper(self, _, line):
        for word in WORD_REGEXP.findall(line):
            yield word.lower(), 1
    def reducer(self, word, counts):
        yield word, sum(counts)
if __name__ == '__main__':
    MRWordCount.run()
