import argparse

ROCK, PAPER, SCISSORS = 1, 2, 3
MOVE_SCORES = {ROCK: 1, PAPER: 2, SCISSORS: 3}
WINNING_MOVE = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
LOSING_MOVE = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
ENEMY_MOVE_CODE = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
PLAYER_MOVE_CODE = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    turns = [(t[0], t[2]) for t in open(args.input_file_path)]
    return turns


def main():
    encoded_turns = read_input()

    part_1_turns = [(ENEMY_MOVE_CODE[a], PLAYER_MOVE_CODE[b]) for a, b in encoded_turns]
    print(f"Part 1: {calculate_final_score(part_1_turns)}")

    part_2_turns = [(ENEMY_MOVE_CODE[a], decode_move_from_outcome(b, ENEMY_MOVE_CODE[a])) for a, b in encoded_turns]
    print(f"Part 2: {calculate_final_score(part_2_turns)}")


def decode_move_from_outcome(code, enemy_move):
    if code == 'X':
        return LOSING_MOVE[enemy_move]
    if code == 'Y':
        return enemy_move
    if code == 'Z':
        return WINNING_MOVE[enemy_move]
    raise Exception(f"{code} isn't a valid outcome code")


def calculate_final_score(turns):
    score = 0
    for enemy_move, player_move in turns:
        if player_move == enemy_move:
            score += 3
        if player_move == WINNING_MOVE[enemy_move]:
            score += 6
        score += MOVE_SCORES[player_move]
    return score


if __name__ == "__main__":
    main()
