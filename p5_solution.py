# 2017-03-14

# problem #5 - employee stock grants

# use directed acyclic graph, edge constraints, topological ordering

# break into dependencies by treating nodes with min. rating earliest

# nodes with minimum rating have zero active dependencies and we always have a node with a minimum rating, so there is a safe order; this is also same reasoning for saying graph is acyclic

# can avoid sorting for topological ordering by taking advantage of rating domain; 
# we won't do that here because the rating domain can be quite large

# takes O(n * log(n) + 10 * n) = O(n * log(n)) time

class Employee:
  def __init__(self, index, rating, min_shares):
    self.index = index
    self.rating = rating
    self.min_shares = min_shares
    self.inferior_neighbors = []
    self.num_granted_shares = 0
  def getIndex(self):
    return self.index
  def getRating(self):
    return self.rating
  def getMinShares(self):
    return self.min_shares
  def addInferiorNeighbor(self, employee):
    self.inferior_neighbors.append(employee)
  def getInferiorNeighbors(self):
    return self.inferior_neighbors
  def getNumGrantedShares(self):
    return self.num_granted_shares
  def setNumGrantedShares(self, num_shares):
    self.num_granted_shares = num_shares
  def toString(self):
    return str(len(self.getInferiorNeighbors()))

import sys
import string

def main():
  stream = sys.stdin
  # stream = open("tests/official/input00.txt")
  # stream = open("tests/official/input01.txt")
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  N = int(args[0])
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  args = [string.atoi(x) for x in args]
  r = args
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  args = [string.atoi(x) for x in args]
  m = args
  # print N, r, m
  employees = [Employee(i, r[i], m[i]) for i in xrange(N)]
  for employee in employees:
    i = employee.getIndex()
    rating = employee.getRating()
    close_employees = employees[max(0, i - 10) : min(N - 1 + 1, i + 10 + 1)]
    if employee in close_employees:
      close_employees.remove(employee)
    inferior_neighbors = [x for x in close_employees if x.getRating() < rating]
    for inferior_neighbor in inferior_neighbors:
      employee.addInferiorNeighbor(inferior_neighbor)
  for employee in employees:
    min_shares = employee.getMinShares()
    employee.setNumGrantedShares(min_shares)
  """
  print employees
  print [x.getRating() for x in employees]
  print [x.getMinShares() for x in employees]
  print [x.toString() for x in employees]
  """
  # we don't have explicit topological sort
  rating_sorted_employees = sorted(employees, key = lambda x: x.getRating())
  # print [x.getRating() for x in rating_sorted_employees]
  for employee in rating_sorted_employees:
    curr_num_granted_shares = employee.getNumGrantedShares()
    for inferior_neighbor in employee.getInferiorNeighbors():
      neighbor_num_granted_shares = inferior_neighbor.getNumGrantedShares()
      curr_num_granted_shares = max(curr_num_granted_shares, neighbor_num_granted_shares + 1)
    employee.setNumGrantedShares(curr_num_granted_shares)
  total_num_granted_shares = sum([x.getNumGrantedShares() for x in employees])
  print total_num_granted_shares
  # print [x.getNumGrantedShares() for x in employees]

if __name__ == "__main__":
  main()


