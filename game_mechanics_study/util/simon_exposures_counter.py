from typing import List


SIMON_GAME_DISTRIBUTION = [
        [[1, 2, 3],
        [1, 2, 3, 4], 
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6]], 
        [[2, 4, 6],
        [2, 4, 6, 1],
        [2, 4, 6, 1, 3],
        [2, 4, 6, 1, 3, 5]], 
        [[3, 6, 2],
        [3, 6, 2, 5],
        [3, 6, 2, 5, 1],
        [3, 6, 2, 5, 1, 4]], 
        [[4, 1, 5],
        [4, 1, 5, 2],
        [4, 1, 5, 2, 6],
        [4, 1, 5, 2, 6, 3]],
        [[5, 3, 1],
        [5, 3, 1, 6],
        [5, 3, 1, 6, 4],
        [5, 3, 1, 6, 4, 2]],
        [[6, 5, 4],
        [6, 5, 4, 3],
        [6, 5, 4, 3, 2],
        [6, 5, 4, 3, 2, 1]]
    ]

def _getTargetIndex(targetID: str) -> int:
    mapping = {
        '81': 1,
        '138': 2,
        '71': 3,
        '105': 4,
        '108': 5,
        '44': 6 
    }
    return mapping[targetID]


def simon_exposures_counter(sequenceLength: int, targetID: str, gameIndex: int):
    targetIndex = _getTargetIndex(targetID)
    count = 0
    for i in range(len(SIMON_GAME_DISTRIBUTION)):
        if i <= gameIndex:
            sequences_for_game = SIMON_GAME_DISTRIBUTION[i] 
            # further reduce it based on the length of the sequence
            if i < gameIndex:
                possible_sequences = sequences_for_game
            else:
                possible_sequences = [seq for seq in sequences_for_game if len(seq) <= sequenceLength]
            for sequence in possible_sequences:
                if targetIndex in sequence:
                    count += 1
    return count


def _getBlockOrder(block: int) -> List:
    mapping = {
        1: [1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 6, 4, 5],
        2: [2, 1, 4, 2, 6, 3, 4, 1, 2, 6, 4, 3, 1, 2, 6, 4, 6, 5],
        3: [3, 1, 6, 2, 5, 3, 6, 2, 3, 5, 6, 2, 3, 6, 5, 2, 1, 4],
        4: [4, 1, 5, 4, 1, 6, 2, 5, 4, 1, 5, 4, 1, 5, 2, 6, 2, 3],
    }
    return mapping[block]

def baseline_exposures_counter(block:int, trial, targetID:str):
    counter = 0
    target = _getTargetIndex(targetID)
    blockIndex = 1

    while blockIndex <= block:
        block_order = _getBlockOrder(blockIndex)
        trialIndex = 0
        while trialIndex < len(block_order) and (trialIndex <= trial or blockIndex < block):
            if block_order[trialIndex] == target:
                counter+=1
            trialIndex+=1
        blockIndex+=1
    return counter

print(baseline_exposures_counter(4, 18, '71'))

# for i in range(1, 6):
    # print(simon_exposures_counter(6, '14', i))  # Expected output: 8
    # print(simon_exposures_counter(6, '105', i))  # Expected output: 8