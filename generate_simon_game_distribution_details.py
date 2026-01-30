
FIRST_LEVEL_SUBSTRING_LENGTH = 3
RANGE = 8

SIMON_GAME_DISTRIBUTION = [
    ["1 2 3 4 5 6"], 
    ["2 4 6 1 3 5"],
    ["3 6 2 5 1 4"],
    ["4 1 5 2 6 3"],
    ["5 3 1 6 4 2"],
    ["6 5 4 3 2 1"]
]

def get_number_of_appearances():
    appearances = [0]*RANGE
    for sequence in SIMON_GAME_DISTRIBUTION:
        length = len(sequence[0].split())
        for index, value in enumerate(sequence[0].split()):
            if index <= FIRST_LEVEL_SUBSTRING_LENGTH -1:
                appearances[int(value)-1] += (length - FIRST_LEVEL_SUBSTRING_LENGTH)
            elif index > FIRST_LEVEL_SUBSTRING_LENGTH -1:
                appearances[int(value)-1] += (length-index+1)
    return appearances


print(get_number_of_appearances())