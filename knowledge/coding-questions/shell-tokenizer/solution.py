def tokenize(command):
  tokens = []
  current = []
  has_token = False   # a quote pair starts a token even if it stays empty
  in_quotes = False

  for ch in command:
    if ch == '"':
      in_quotes = not in_quotes
      has_token = True
    elif ch == " " and not in_quotes:
      if has_token:
        tokens.append("".join(current))
        current = []
        has_token = False
    else:
      current.append(ch)
      has_token = True

  if has_token:
    tokens.append("".join(current))
  return tokens
