# 2016-07-10

# problem #2 - fixed-income security trade allocation

# remember to not leave an un-tradeable number of units for a portfolio after allocating

# also, if gap is un-tradeable, we maximize allocated value while still leaving tradeable gap; for this, we brute force values between 0 and allocated_value, endpoints included and visited in order from large to small

def trunc(num, digits):
  sp = str(num).split('.')
  result = None
  if digits == 0:
    result = sp[0]
  else:
    result = '.'.join([sp[0], sp[1][ : digits]])
  next_result = float(result)
  return next_result
import sys
import string
stream = sys.stdin
# stream = open("tests/input0.txt")
# stream = open("tests/input1.txt")
line = stream.readline()
line = line.rstrip("\n")
args = line.split(" ")
args = [string.atol(x) for x in args]
T = int(args[0])
# print T
line = stream.readline()
line = line.rstrip("\n")
args = line.split(" ")
args = [string.atol(x) for x in args]
min_trade_size = int(args[0])
increment = int(args[1])
available_units = int(args[2])
# print min_trade_size, increment, available_units
portfolios = []
class Portfolio:
  def __init__(self, portfolio_identifier, portfolio_order, units_allocated = 0):
    self.portfolio_identifier = portfolio_identifier
    self.portfolio_order = portfolio_order
    self.units_allocated = units_allocated
  def getIdentifier(self):
    return self.portfolio_identifier
  def getOrder(self):
    return self.portfolio_order
  def getUnitsAllocated(self):
    return self.units_allocated
  def setUnitsAllocated(self, units_allocated):
    self.units_allocated = units_allocated
  def __repr__(self):
    result_tuple = (self.getIdentifier(), self.getOrder())
    result_str = str(result_tuple)
    return result_str
for i in xrange(T):
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split(" ")
  # args = [string.atof(x) for x in args]
  # print args
  portfolio_identifier = args[0]
  portfolio_order = int(args[1])
  # print portfolio_identifier, portfolio_order
  portfolio = Portfolio(portfolio_identifier, portfolio_order)
  portfolios.append(portfolio)
ordered_portfolios = sorted(portfolios, key = lambda x: (x.getOrder(), x.getIdentifier()))
# print ordered_portfolios
def getProportionalAllocation(portfolio_order, total_order, available_units):
  result = portfolio_order / (1.0 * total_order) * available_units
  return result
total_order = sum([x.getOrder() for x in portfolios])
curr_available_units = available_units
def getValueIsTradeable(allocated_amount, min_trade_size, increment):
  if allocated_amount == 0:
    # value is zero, which is tradeable
    return True
  if allocated_amount < min_trade_size:
    return False
  # print portfolio_order, allocated_amount, min_trade_size, increment
  n = (allocated_amount - min_trade_size) / (1.0 * increment)
  # print trunc(n, 0)
  have_integer_n = (n - trunc(n, 0)) == 0
  # print n, trunc(n, 0), have_integer_n
  gap_is_tradeable = have_integer_n
  return gap_is_tradeable
# print getValueIsTradeable(0, 1, 2)
# print getValueIsTradeable(3, 1, 2)
# print getValueIsTradeable(3, 2, 2)
def getGapIsUntradeable(portfolio_order, allocated_amount, min_trade_size, increment):
  return getValueIsTradeable(portfolio_order - allocated_amount, min_trade_size, increment) == False
# print getGapIsUntradeable(6, 4, 2, 3)
# print getGapIsUntradeable(6, 3, 1, 2)
# print getGapIsUntradeable(6, 4, 4, 3)
def getAllocationThatIsTradeable(proportional_allocation, min_trade_size, increment, round_down = False):
  # if discretizeable, err in favor of too much
  n = (proportional_allocation - min_trade_size) / (1.0 * increment)
  # print "n:", n, "min. trade size:", min_trade_size
  if round_down == False:
    # round up
    n = round(n)
  else:
    # round down
    n = int(n)
  next_allocation = min_trade_size + increment * n
  next_allocation = int(next_allocation)
  return next_allocation
seen_portfolios = set([])
for portfolio in ordered_portfolios:
  # print curr_available_units, portfolio.getOrder()
  if True:
    proportional_allocation = getProportionalAllocation(portfolio.getOrder(), total_order, curr_available_units)
    # print "proportional allocation:", proportional_allocation
    # print min_trade_size
    # print portfolio.getIdentifier()
    if proportional_allocation < min_trade_size:
      if (proportional_allocation > min_trade_size / 2.0) == False:
        pass
        # print "hello"
      else:
        # still try to satisfy customer, by rounding up their desire
        tentative_amount_allocated = min_trade_size
        # print amount_allocated
        portfolio.setUnitsAllocated(tentative_amount_allocated)
    elif proportional_allocation >= min_trade_size:
      # print proportional_allocation, min_trade_size, portfolio.getOrder()
      if proportional_allocation >= portfolio.getOrder():
        portfolio.setUnitsAllocated(portfolio.getOrder())
      elif proportional_allocation < portfolio.getOrder():
        tentative_amount_allocated = getAllocationThatIsTradeable(proportional_allocation, min_trade_size, increment, round_down = True)
        if tentative_amount_allocated < min_trade_size:
          tentative_amount_allocated = 0
        portfolio.setUnitsAllocated(tentative_amount_allocated)
    # portfolio gap can't be an untradeable value
    gap_is_untradeable = getGapIsUntradeable(portfolio.getOrder(), portfolio.getUnitsAllocated(), min_trade_size, increment)
    if gap_is_untradeable == True:
      portfolio.setUnitsAllocated(0)
    seen_portfolios |= set([portfolio])
    total_order = sum([x.getOrder() for x in portfolios if x not in seen_portfolios])
    curr_available_units = curr_available_units - portfolio.getUnitsAllocated()
  next_sorted_portfolios = sorted(portfolios, key = lambda x: x.getIdentifier())
for portfolio in next_sorted_portfolios:
  portfolio_identifier = portfolio.getIdentifier()
  portfolio_order = portfolio.getUnitsAllocated()
  print portfolio_identifier, portfolio_order


