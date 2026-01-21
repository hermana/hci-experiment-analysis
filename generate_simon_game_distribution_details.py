# SIMON_GAME_DISTRIBUTION = [
#     # ["1 2 3 4 5 6"], 
#     # ["2 4 6 1 3 5"],
#     # ["3 6 2 5 1 4"],
#     # ["4 1 5 2 6 3"],
#     # ["5 3 1 6 4 2"],
#     # ["6 5 4 3 2 1"]
# ]


# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 3 4"], 
#     ["2 4 6 1"],
#     ["3 6 2 5"],
#     ["4 1 5 2"],
#     ["5 3 1 6"],
#     ["6 5 4 3"]
# ]


# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 6"], 
#     ["2 4 3 5"],
#     ["3 6 2 1 4"],
#     ["4 1 5 2 3"],
#     ["5 3 1 6 4 2"],
#     ["6 5 4 3 2 1"]
# ]

# 12 blocks, with 6 "targets" instead! 
# Talk to Morgan tomorrow 
# However, end of the sequence could mean end of the subsequence? or not?

# SIMON_GAME_DISTRIBUTION = [
#     ["1 3 5 8"],
#     ["2 4 6 1 7"],
#     ["3 2 7"],
#     ["4 5 3 6 2"],
#     ["5 7 4"],
#     ["6 1 5 8 3"],
#     ["7 6 2 4"],
#     ["8 2 7 1"]
# ]

# SIMON_GAME_DISTRIBUTION = [
#     ["1 3 5 8"],
#     ["2 4 6 1 7"],
#     ["3 2 7"],
#     ["4 5 3 6 2"],
#     ["5 7 4"],
#     ["6 1 5 8 3"],
#     ["7 6 2 4"],
#     ["8 2 7 1"]
# ]

# SIMON_GAME_DISTRIBUTION = [
#     ["1 5 3 6 2"],
#     ["4 6 2 3 1"],
#     ["5 4 1 6 3"],
#     ["2 1 5 4"],
#     ["3 4 1 2 5 6"],
#     ["6 2 3 5"],
# ]


FIRST_LEVEL_SUBSTRING_LENGTH = 3
RANGE = 8
# It could be easier to analyze on a per target basis. We need the above structure to have the same beginning, middle, end. 

# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 3 4 5"],
#     ["2 4 1 5 3"],
#     ["3 1 4 2 5"],
#     ["4 5 2 3 1"],
#     ["5 3 1 2 4"]
# ]

# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 3 4"],
#     ["2 4 1 3"],
#     ["3 1 4 2"],
#     ["4 3 2 1"]
# ]


# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 3 4 2"],
#     ["2 4 1 3 4"],
#     ["3 1 4 2 1"],
#     ["4 3 2 1 3"]
# ]

# The other idea: vary the sequence lengths. 
# SIMON_GAME_DISTRIBUTION = [
#     ["1 2 3 4 5 6"], 
#     ["2 4 6 1 3 5"],
#     ["3 6 2 5 1 4"],
#     ["4 1 5 2 6 3"],
#     ["5 3 1 6 4 2"],
#     ["6 5 4 3 2 1"]
# ]

# Start with a substring of 3 

# we also had it so that they don't learn up to 6 every time

def get_number_of_appearances():
    appearances = [0]*RANGE
    for sequence in SIMON_GAME_DISTRIBUTION:
        length = len(sequence[0].split())
        for index, value in enumerate(sequence[0].split()):
            if index <= FIRST_LEVEL_SUBSTRING_LENGTH -1:
                appearances[int(value)-1] += (length - FIRST_LEVEL_SUBSTRING_LENGTH)
            elif index > FIRST_LEVEL_SUBSTRING_LENGTH -1:
                appearances[int(value)-1] += (length-index)
    return appearances


print(get_number_of_appearances())