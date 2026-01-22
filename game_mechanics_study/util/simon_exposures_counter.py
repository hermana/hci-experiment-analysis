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
        '16': 3,
        '105': 4,
        '71': 5,
        '14': 6  # 81, 138, 16, 105, 71, 14
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


# print(simon_exposures_counter(5, '81', 2))  # Expected output: 8