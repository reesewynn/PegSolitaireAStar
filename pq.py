import itertools
from heapq import heappush, heappop

REMOVED = '<removed_task>'
class PQ():
    def __init__(self, init_item = None, init_priority = 0):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()
        self._size = 0
        if init_item:
            self.add(init_item, init_priority)

    def add(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
        self._size += 1

    def remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = REMOVED
        self._size -= 1

    def contains(self, task):
        return task in self.entry_finder
    
    def is_empty(self):
        return self._size == 0
    
    def size(self):
        return self._size

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not REMOVED:
                del self.entry_finder[task]
                self._size -= 1
                return task
        raise KeyError('pop from an empty priority queue')
