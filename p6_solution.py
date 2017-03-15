# 2017-03-15

# problem #6 - audit sale

# takes O(n * log(n)) time

# inspired by anh duc le

# sort using a unary "distinguisher" metric non-increasing from left to right

# post-sort, we have two regions - help asked for at left, no help asked for at right

# knowing that we have a divider, use dynamic programming to find optimal divider location

# we need two heaps instead of just sorting because we have interaction between left and right

# we always sell exactly M securities as we are seeking highest profit

# treat prefix and suffix separately; 
# add items until we have no room, 
# at which point we remove weakest items; 
# prefix and suffix are always disjoint

# typo in sandeep mohanty's explanation; 
# help asked is at left, no help asked is at right

# push() and pop() are bottlenecks; 
# use pushpop() for significant speed-up 
# as we spend more time in C this way

import sys
import string

import heapq

class PriorityQueue:
  # pop() retrieves low-priority items
  def  __init__(self):
    self.heap = []
  def push(self, item, priority):
    pair = (priority, item)
    heapq.heappush(self.heap, pair)
  def pop(self):
    (priority, item) = heapq.heappop(self.heap)
    return item
  def pushPop(self, item, priority):
    pair = (priority, item)
    (prev_priority, prev_item) = heapq.heappushpop(self.heap, pair)
    return prev_item
  def isEmpty(self):
    return len(self.heap) == 0
  def getSize(self):
    return len(self.heap)
  def peek(self):
    heap = self.heap
    pair = heap[0]
    item = pair[1]
    return item

class Security:
  # confidence is a value in [0, 100]
  def __init__(self, price, confidence):
    self.price = price
    self.confidence = confidence
  def getPrice(self):
    return self.price
  def getConfidence(self):
    return self.confidence
  def getDistinguisher(self):
    return self.getPrice() * (100 - self.getConfidence())
  # for guaranteed expected profit
  def getLeftProfit(self):
    return 100 * self.getPrice()
  # for un-guaranteed expected profit
  def getRightProfit(self):
    return self.getConfidence() * self.getPrice()
  def toString(self):
    return str((self.getPrice(), self.getConfidence()))

def main():
  stream = sys.stdin
  # stream = open("tests/official/input19.txt")
  # stream = open("tests/official/input01.txt")
  # stream = open("tests/official/input17.txt")
  line = stream.readline()
  line = line.rstrip("\n\r\t ")
  args = line.split(" ")
  args = [string.atoi(x) for x in args]
  N = args[0]
  M = args[1]
  K = args[2]
  securities = []
  for i in xrange(N):
    line = stream.readline()
    line = line.rstrip("\n\r\t ")
    args = line.split(" ")
    args = [string.atoi(x) for x in args]
    price = args[0]
    confidence = args[1]
    security = Security(price, confidence)
    securities.append(security)

  ordered_securities = sorted(securities, key = lambda x: x.getDistinguisher(), reverse = True)

  # sum of K largest left profits in [0, i]-index elements
  prefix = [0] * N
  # sum of (M - K) largest right profits in [i + 1, N)-index elements
  suffix = [0] * N

  # use order from distinguisher when deciding to move from right to left

  # for best K items at left, 
  # based on with-help (left) profit
  prefix_pq = PriorityQueue()

  curr_left_sum = 0
  for i in xrange(N):
    security = ordered_securities[i]
    curr_left_sum += security.getLeftProfit()
    if ((prefix_pq.getSize() + 1) > K) == False:
      prefix_pq.push(security, security.getLeftProfit())
    else:
      security_to_remove = prefix_pq.pushPop(security, security.getLeftProfit())
      # security_to_remove = prefix_pq.pop()
      curr_left_sum -= security_to_remove.getLeftProfit()
    prefix[i] = curr_left_sum

  # for best (M - K) items at right, 
  # based on not-with-help (right) profit
  suffix_pq = PriorityQueue()

  curr_right_sum = 0
  indices = reversed(xrange(N))
  for i in indices:
    security = ordered_securities[i]
    curr_right_sum += security.getRightProfit()
    if ((suffix_pq.getSize() + 1) > (M - K)) == False:
      suffix_pq.push(security, security.getRightProfit())
    else:
      security_to_remove = suffix_pq.pushPop(security, security.getRightProfit())
      # security_to_remove = suffix_pq.pop()
      curr_right_sum -= security_to_remove.getRightProfit()
    suffix[i] = curr_right_sum

  max_profit = 0 if N == 0 else suffix[0]

  # assume we always have K help and (M - K) no help
  for i in xrange(N):
    curr_prefix_value = prefix[i]
    curr_suffix_value = 0 if (i + 1) >= N else suffix[i + 1]
    max_profit = max(max_profit, curr_prefix_value + curr_suffix_value)

  print max_profit

if __name__ == "__main__":
  main()


