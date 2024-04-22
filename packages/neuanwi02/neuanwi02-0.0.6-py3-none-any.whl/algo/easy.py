import heapq
from bisect import bisect_left, bisect_right

def heapsort(iterable):
  h = []
  result = []
  for value in iterable:
    heapq.heappush(h, value)
  for i in range(len(h)):
    result.append(heapq.heappop(h))
  return result

def calCountsByRange(nums, left_value, right_value):
    r_i = bisect_right(nums, right_value)
    l_i = bisect_left(nums, left_value)
    return r_i - l_i
# 출처: https://programming119.tistory.com/196 [개발자 아저씨들 힘을모아:티스토리]
