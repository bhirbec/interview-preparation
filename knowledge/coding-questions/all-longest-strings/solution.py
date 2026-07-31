def all_longest_strings(input_array):
  max_len = max(len(s) for s in input_array)
  return [s for s in input_array if len(s) == max_len]


def all_longest_strings_1(input_array):
  current_max = len(input_array[0])
  output = [input_array[0]]

  for item in input_array[1:]:
    candidate_max = len(item)
    if candidate_max > current_max:
      current_max = candidate_max
      output = [item]
    elif candidate_max == current_max:
      output.append(item)

  return output
