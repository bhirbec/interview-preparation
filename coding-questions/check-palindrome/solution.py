def check_palindrome(input_string):
  n = len(input_string) // 2
  for i in range(n):
    if input_string[i] != input_string[-(i+1)]:
      return False
  return True
