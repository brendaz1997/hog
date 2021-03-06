"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0
    pig_out = 0
    for i in range (1, num_rolls+1):
        roll = dice()
        total += roll
        if roll == 1:
            pig_out = 1
    if pig_out == 1:
        return 1
    else:
        return total
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    lst = [int(opponent_score) for opponent_score in str(opponent_score)]
    return 1 + max(lst)
    # END PROBLEM 2


# Write your prime functions here! 
def is_prime(n):
    if n == 1:
        return False
    if n == 2:
        return True
    for i in range (2,n):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    if is_prime(n) == True:
        n += 1
        while is_prime(n) == False:
            n += 1
    return n

def hogtimus_prime(player_score):
    return (next_prime(player_score))



def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:
        points = free_bacon(opponent_score)
        if is_prime(points) == True:
            return(hogtimus_prime(points))
        return (points)
    a = roll_dice(num_rolls, dice)
    if is_prime(a) == True:
        return(hogtimus_prime(a))
    else:
        return a
    # END PROBLEM 2


def select_dice(dice_swapped):
    """Return a six-sided dice unless four-sided dice have been swapped in due
    to Perfect Piggy. DICE_SWAPPED is True if and only if four-sided dice are in
    play.
    """
    # BEGIN PROBLEM 3
    if dice_swapped == True:
        return four_sided
    if dice_swapped == False:
        return six_sided
    # END PROBLEM 3


# Write additional helper functions here!
from math import sqrt

def is_perf_square(n):
    if n == 1:
        return False
    if n % sqrt(n) == 0:
        return True
    else:
        return False

def is_perf_cube(n):
    if n == 1:
        return False
    if n % ((n)**(1/3)) == 0:
        return True
    else:
        return False

# If a player's score for the turn is not a 1, but is a perfect square or a perfect cube, 
#the player scores the turn score but swaps the normal six-sided dice with four-sided dice for all subsequent turns. 
#The next time either player activates Perfect Piggy, the six-sided dice will be swapped back.
def is_perfect_piggy(turn_score):
    """Returns whether the Perfect Piggy dice-swapping rule should occur."""
    # BEGIN PROBLEM 4
    if is_perf_square(turn_score) or is_perf_cube(turn_score) == True:
        return True
    else:
        return False
    # END PROBLEM 4


def is_swap(score0, score1):
    """Returns whether one of the scores is double the other."""
    # BEGIN PROBLEM 5
    if score0 == score1 * 2:
        return True
    elif score1 == score0 *2:
        return True
    else:
        return False
    # END PROBLEM 5

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0:     The starting score for Player 0
    score1:     The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 6
    dice = select_dice(dice_swapped)

    while score0 < goal or score1 < goal:

        if player == 0:
            turn_total0 = take_turn(strategy0(score0,score1), score1, dice)
            score0 += turn_total0
            if is_perfect_piggy(turn_total0) == True:
                dice_swapped = not dice_swapped

        if player == 1:
            turn_total1 = take_turn(strategy1(score1,score0), score0, dice)
            score1 += turn_total1
            if is_perfect_piggy(turn_total1) == True:
                dice_swapped = not dice_swapped

        if is_swap(score0, score1) == True:
            score0, score1 = score1, score0

        dice = select_dice(dice_swapped)

        if score0 >= goal or score1 >= goal:
            return score0, score1

        player = other(player)
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the strategy
    returns a valid input. Use `check_strategy_roll` to raise an error with a
    helpful message if the strategy returns an invalid output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 7
    for i in range (goal):
        for n in range (goal):
            if check_strategy_roll(i, n, strategy(i, n)) != None:
                return check_strategy_roll(i, n, strategy(i, n))
    # END PROBLEM 7


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def a(*args):
        total = 0
        #func = fn(*args)
        for i in range(num_samples):
            total += fn(*args)
        return total/num_samples
    return a

    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    high_score_roll_avg = 0
    average = make_averaged(roll_dice, num_samples)
    for n in range(1, 11):
        if n == 1:
            score_roll_avg = average(n, dice)
        else:
            score_roll_avg = average(n, dice)
            high_score_roll_avg = average(n - 1, dice)
        if score_roll_avg > high_score_roll_avg:
            number1 = n
        if score_roll_avg == high_score_roll_avg:
            number2 = n
            if number2 < number1:
                number1 = number2
    return number1 
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    hog_bacon = hogtimus_prime(free_bacon(opponent_score))
    c = free_bacon(opponent_score) + score
    score1 = hogtimus_prime(c)
    diff = score1 - score
    if hog_bacon >= margin or diff >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    hog_bacon = hogtimus_prime(free_bacon(opponent_score))
    score1 = hog_bacon + score
    if is_swap(score1, opponent_score) == True and opponent_score > score1:
        return 0
    elif bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
        return 0
    else:
        return num_rolls
    # END PROBLEM 11
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** Use swap_strategy as a base for strategy since it already has 
    a .71 chance of winning. Then if score is less than or equal to 30 points away from 100, 
    change margin to 5 to make less risky choices. Similarly, if score is between 30 and 70 points 
    away from 100, change margin to 7. And if score is greater than or equal to 70 points away
    from 100, margin is 8 (make riskier choices to get higher turn score). Using the new margin, use swap_strategy 
    to determine if rolling 0 dice is beneficial for swapping or scoring more than the margin. 
    If it is (returns 0), set num_roll to 0. However, check to see if opponent score is less 
    than your score for a potential swap. If it is, then set num_roll back to what is was before 
    to avoid rolling 0 dice and swapping to a lower score.  ***
    """
    # BEGIN PROBLEM 11
    hog_bacon = hogtimus_prime(free_bacon(opponent_score))
    score1 = hog_bacon + score
    margin = 8
    num_roll = 4
    if 100 - score <= 30:
        margin = 5
    elif 100 - score > 30 and 100 - score < 70:
        margin = 7
    elif 100 - score >= 70:
        margin = 8
    if swap_strategy(score, opponent_score, margin, num_roll) == 0:
        b = num_roll
        num_roll = 0
        if is_swap(score1, opponent_score) == True and opponent_score < score1:
            num_roll = b
    return num_roll
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()