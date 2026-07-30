def highlight_symbols(names, symbols):
  result = []
  for name in names:
    best_index = -1
    best_symbol = None
    for symbol in symbols:
      index = name.find(symbol)
      if index == -1:
        continue
      if best_symbol is None:
        better = True
      elif len(symbol) != len(best_symbol):
        better = len(symbol) > len(best_symbol)
      else:
        better = index < best_index
      if better:
        best_index = index
        best_symbol = symbol
    if best_symbol is None:
      result.append(name)
    else:
      i = best_index
      j = i + len(best_symbol)
      result.append('{0}[{1}]{2}'.format(name[:i], name[i:j], name[j:]))
  return result
