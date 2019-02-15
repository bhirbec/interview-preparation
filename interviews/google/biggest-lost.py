# Given the daily values of a stock, find how you can lose the most
# with one buy-sell trading.


def find_biggest_loss(prices):
  buy = 0
  sell = 0
  max_loss = 0
  output = buy, sell, max_loss
  n = len(prices)

  for i in range(1, n):
    price = prices[i]
    if price > prices[buy]:
      buy = i
      sell = i
    elif price < prices[sell]:
      sell = i
      loss = prices[buy] - prices[sell]
      if loss > max_loss:
        max_loss = loss
        output = buy, sell, max_loss

  return output


prices = [23, 24, 27, 532, 14, 12, 17, 121, 24, 1344, 0]
print(find_biggest_loss(prices))
