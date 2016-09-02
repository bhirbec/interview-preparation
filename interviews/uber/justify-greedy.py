# https://www.glassdoor.com/Interview/Given-a-message-one-two-three-four-five-six-seven-eight-nine-chop-it-in-chunks-no-exceed-the-give-buffer-size-and-print-QTN_1438219.htm

def main():
    text = '''
        Measurements of "the hit ratio" are typically performed on benchmark applications.
        The actual hit ratio varies widely from one application to another. In particular,
        video and audio streaming applications often have a hit ratio close to zero, because
        each bit of data in the stream is read once for the first time (a compulsory miss),
        used, and then never read or written again. Even worse, many cache algorithms (in particular,
        LRU) allow this streaming data to fill the cache, pushing out of the cache information
        that will be used again soon (cache pollution).[2]
    '''

    text = text[1:].replace('\n', ' ').replace('    ', '')
    for line in justify(text, 60):
        print line

def justify(text, buff_size):
    words = text.split(' ')
    n = len(words)
    line = []
    i = 0
    line_size = 0

    while i < n:
        word = words[i]

        new_size = line_size + len(word)
        if line_size > 0:
            new_size += 1

        if new_size <= buff_size:
            line.append(word)
            line_size = new_size
            i += 1
        else:
            yield ' '.join(line)
            line = []
            line_size = 0

    if line:
        yield ' '.join(line)


main()
