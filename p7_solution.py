# 2017-03-12

# problem #7 - trade analysis

# O(n)-time solution

import sys
import string

def getGOfS():
  stream = sys.stdin
  # stream = open("tests/official/input00.txt")
  # stream = open("tests/official/input01.txt")
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  n = int(args[0])
  if n == 0:
    return 0
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  args = [string.atoi(x) for x in args]
  a = args
  t = [0] * n
  P_prime_1 = [0] * n
  t[0] = a[0]
  P_prime_1[0] = 1
  mod = 10 ** 9 + 7
  for i in xrange(1, n):
    t[i] = (t[i - 1] * (1 + a[i]) + a[i]) % mod
    # f[i] = (f[i - 1] * (1 + a[i]) + (1 + t[i - 1]) * a[i]) % mod
  P_final_1 = reduce(lambda x, y: (x * y) % mod, [1 + x for x in a])
  # instead of calculating P_prime_final_1 using closed-form formula, 
  # use recursive formula with dynamic programming; 
  # this is desirable because using modulus disrupts division 
  # by a factor in the polynomial
  for i in xrange(1, n):
    P_prime_1[i] = ((((1 + a[i]) * P_prime_1[i - 1])) % mod + t[i - 1] + 1) % mod
  P_prime_final_1 = P_prime_1[n - 1]
  G_s = ((n * (t[n - 1] + 1)) % mod - P_prime_final_1) % mod
  return G_s
  # there is a special case where i == 0 for t[i] and f[i]

def main():
  result = getGOfS()
  print result

if __name__ == "__main__":
  main()


