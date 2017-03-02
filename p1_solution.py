# 2016-07-10

# problem #1 - currency arbitrage

# first line is n, the number of lines that follow

# each line that follows has USD -> euro rate, euro -> GBP rate, GBP -> USD rate

# for each rate line, output profit for changing $100,000 to euros, then to GBP, then to dollars; 
# return zero if no profit resulted

# print values in dollars truncated to whole dollars

import sys
import string
stream = sys.stdin
# stream = open("tests/input0.txt")
line = stream.readline()
line = line.rstrip("\n")
args = line.split(" ")
args = [string.atol(x) for x in args]
N = int(args[0])
# print N
quote_tuple_list = []
for i in xrange(N):
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  args = [string.atof(x) for x in args]
  # print args
  quote_tuple = tuple(args)
  quote_tuple_list.append(quote_tuple)
def trunc(num, digits):
  sp = str(num).split('.')
  result = None
  if digits == 0:
    result = sp[0]
  else:
    result = '.'.join([sp[0], sp[1][ : digits]])
  next_result = float(result)
  return next_result
# print trunc(114.12, 0)
results = []
for quote_tuple in quote_tuple_list:
  usd_to_euro_rate, euro_to_gbp_rate, gbp_to_usd_rate = quote_tuple
  final_amount = 100000 * (1.0 / usd_to_euro_rate) * (1.0 / euro_to_gbp_rate) * (1.0 / gbp_to_usd_rate)
  result = None
  if final_amount >= 100000:
    profit = final_amount - 100000
    result = trunc(profit, 0)
  else:
    result = 0
  results.append(result)
for result in results:
  result_str = str(result)
  print result_str
# three quotes
# USD -> EUR, EUR -> GBP, GBP -> USD
# start with 100,000 USD
# USD -> EUR -> GBP -> USD


