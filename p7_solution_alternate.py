# 2017-03-06

# problem #7 - trade analysis

# O(n * log(n) ^ 2)-time solution; not fast enough as it takes ~25 seconds for test #13 in python

# FFT is O(n * log(n))-time

# balanced polynomial multiplication and overflow-avoiding multiplication inspired by maciek gawron

# we build up operand polynomials in a balanced manner

# express problem in terms of a product of monomials

# perform FFT to find coefficients for result polynomial

# by turning problem into one about a polynomial, we have off-by-one error and break combinations into size groups; we take coefficients and multiply by sizes and sum and we get our desired weighted product sum result

# P = (x + a_1) * (x + a_2) * ... * (x + a_(n / 2)) * (x + a_(n / 2 + 1)) * ... * (x + a_n)

#   = [(x + a_1) * (x + a_2) * ... * (x + a_(n / 2))] * [(x + a_(n / 2 + 1)) * ... * (x + a_n)]

#   = (degree-O(n / 2) polynomial) * (degree-O(n / 2) polynomial)

# ought to weight

# size for problem for a node s.t. there are O(n) nodes:
# sum over d from 0 to (log base two of n) of (2 ^ d * 2 ^ ((log base two of n) - d))
# = sum over d from 0 to (log base two of n) of (2 ^ (log base two of n))
# = sum over d from 0 to (log base two of n) of n
# = O(n * log(n))

# average size for problem for a node, i.e. when there is one node:
# O(log(n))

# a quirk of the problem is that signal size is at worst in O(n) 
# and number of multiplications is in O(n); 
# n is largest degree for a polynomial encountered; 
# n is the variable "n" from the problem statement

# double is ~17 significant digits

# loss of precision for built-in complex type can cause strange time-varying signals

"""

(x + a_1) * (x + a_2) * (x + a_3) = (x ^ 2 + (a_1 + a_2) * x + a_1 * a_2) * (x + a_3)
 = x ^ 3 + (a_1 + a_2) * x ^ 2 + (a_1 * a_2) * x + a_3 * x ^ 2 + ((a_1 * a_3) + (a_2 * a_3)) * x + (a_1 * a_2 * a_3)
 = x ^ 3 + (a_1 + a_2 + a_3) * x ^ 2 + (a_1 * a_2 + a_1 * a_3 + a_2 * a_3) * x + (a_1 * a_2 * a_3)

power 3 -> size (3 - 3) = size 0
power 2 -> size (3 - 2) = size 1
power 1 -> size (3 - 1) = size 2
power 0 -> size (3 - 0) = size 3

"""

# FFT approach inspired by jeremy kun

modulus = 10 ** 9 + 7
import cmath
import math
def omega(p, q):
  return cmath.exp((2.0 * cmath.pi * 1j * q) / p)
def fft(signal):
  n_s = len(signal)
  if n_s == 1:
    return signal
  else:
    F_even = fft([signal[i] for i in xrange(0, n_s, 2)])
    F_odd = fft([signal[i] for i in xrange(1, n_s, 2)])
    combined = [0] * n_s
    for m in xrange(n_s / 2):
      combined[m] = F_even[m] + omega(n_s, -m) * F_odd[m]
      combined[m + n_s / 2] = F_even[m] - omega(n_s, -m) * F_odd[m]
    return combined
def ifft(signal):
  timeSignal = fft([x.conjugate() for x in signal])
  return [x.conjugate() / len(signal) for x in timeSignal]
root = 3 * 10 ** 4
# assume that degree_to_coefficient_dict has a key-value pair for all degrees in [0, max_degree]
class Polynomial:
  def __init__(self, degree_to_coefficient_dict, max_degree):
    self.degree_to_coefficient_dict = degree_to_coefficient_dict
    highest_non_zero_degree = float("-inf")
    if len(degree_to_coefficient_dict) != 0:
      highest_non_zero_degree = 0
    for i in xrange(len(degree_to_coefficient_dict)):
      coefficient = degree_to_coefficient_dict[i]
      degree = i
      if coefficient != 0:
        highest_non_zero_degree = max(highest_non_zero_degree, degree)
    max_degree = highest_non_zero_degree
    self.max_degree = max_degree
  def getDegreeToCoefficientDict(self):
    return self.degree_to_coefficient_dict
  def getMaxDegree(self):
    return self.max_degree
  def toSignal(self):
    degree_to_coefficient_dict = self.getDegreeToCoefficientDict()
    max_degree = self.getMaxDegree()
    signal = []
    for i in xrange(max_degree + 1):
      coefficient = degree_to_coefficient_dict[i]
      signal.append(coefficient)
    return signal
  @staticmethod
  def fromSignal(signal):
    degree_to_coefficient_dict = {}
    max_degree = len(signal) - 1
    for i in xrange(max_degree + 1):
      coefficient = signal[i]
      degree = i
      degree_to_coefficient_dict[degree] = coefficient
    polynomial = Polynomial(degree_to_coefficient_dict, max_degree)
    return polynomial
  # don't assume that two input signals are of exact equal length
  # assume that signals are composed of integers
  def multiply(self, polynomial):
    p = self.toSignal()
    q = polynomial.toSignal()
    p_num_terms = self.getMaxDegree() + 1
    q_num_terms = polynomial.getMaxDegree() + 1
    r_num_terms = (p_num_terms - 1) + (q_num_terms - 1) + 1
    next_r_num_terms = int(2 ** math.ceil(math.log(r_num_terms, 2)))
    P = fft(p + ([0] * (next_r_num_terms - p_num_terms)))
    Q = fft(q + ([0] * (next_r_num_terms - q_num_terms)))
    R = [P[i] * Q[i] for i in xrange(next_r_num_terms)]
    r = ifft(R)
    r_real = [x.real for x in r]
    r_real_rounded = [int(round(x)) for x in r_real]
    degree_to_coefficient_dict = {}
    max_degree = None
    for i in xrange(next_r_num_terms):
      degree = i
      # hopefully taking modulus here will alleviate pressure on precision
      coefficient = r_real_rounded[i] % modulus
      degree_to_coefficient_dict[degree] = coefficient
    max_degree = next_r_num_terms - 1
    result_polynomial = Polynomial(degree_to_coefficient_dict, max_degree)
    return result_polynomial
  # remember to take care of case where polynomials are of unequal size; 
  # make sure we don't overflow by making sure product of two coefficients of size "root" = 3 * 10 ^ 4 is around "modulus" = 10 ^ 9 + 7; 
  # decompose using "root" (or "secondary modulus") into floor of quotient and remainder
  def multiplyWithoutOverflow(self, polynomial):
    v1 = self.toSignal()
    v2 = polynomial.toSignal()
    # key is that degree possibly increases
    w1 = [v1[i] % root for i in xrange(len(v1))]
    w2 = [v2[i] % root for i in xrange(len(v2))]
    w3 = [int(math.floor(v1[i] / root)) for i in xrange(len(v1))]
    w4 = [int(math.floor(v2[i] / root)) for i in xrange(len(v2))]
    p1 = Polynomial.fromSignal(w1)
    p2 = Polynomial.fromSignal(w2)
    p3 = Polynomial.fromSignal(w3)
    p4 = Polynomial.fromSignal(w4)
    ans1 = p1.multiply(p2)
    ans2 = p1.multiply(p4)
    ans3 = p3.multiply(p2)
    ans4 = p3.multiply(p4)
    d1 = ans1.getDegreeToCoefficientDict()
    d2 = ans2.getDegreeToCoefficientDict()
    d3 = ans3.getDegreeToCoefficientDict()
    d4 = ans4.getDegreeToCoefficientDict()
    signal = []
    max_signal_size = max(len(d1), len(d2), len(d3), len(d4))
    for i in xrange(max_signal_size):
      term1 = d1[i] if i < len(d1) else 0
      term2 = d2[i] * root if i < len(d2) else 0
      term3 = d3[i] * root if i < len(d3) else 0
      term4 = d4[i] * root * root if i < len(d4) else 0
      coefficient = (term1 + term2 + term3 + term4) % modulus
      signal.append(coefficient)
    result = Polynomial.fromSignal(signal)
    return result
  def toString(self):
    return self.getDegreeToCoefficientDict()
import sys
import string
stream = sys.stdin
# stream = open("tests/official/input01.txt")
line = stream.readline()
line = line.rstrip("\n")
args = line.split(" ")
args = [string.atoi(x) for x in args]
n = args[0]
line = stream.readline()
line = line.rstrip("\n")
args = line.split(" ")
args = [string.atoi(x) for x in args]
S = args
# print n, S, modulus
a_i_values = S
# print a_i_values
def balancedPolynomialMultiply(S, a, b):
  if a == b:
    polynomial = Polynomial({0 : S[a], 1 : 1}, 1)
    return polynomial
  else:
    mid = int(math.floor((a + b) / 2.0))
    p1 = balancedPolynomialMultiply(S, a, mid)
    p2 = balancedPolynomialMultiply(S, mid + 1, b)
    result = p1.multiplyWithoutOverflow(p2)
    return result
result_polynomial = balancedPolynomialMultiply(S, 0, n - 1)
degree_to_coefficient_dict = result_polynomial.getDegreeToCoefficientDict()
num_terms = result_polynomial.getMaxDegree() + 1
result = 0
for i in xrange(num_terms):
  coefficient = degree_to_coefficient_dict[i]
  size = n - i
  result = (result + size * coefficient) % modulus
print result,
