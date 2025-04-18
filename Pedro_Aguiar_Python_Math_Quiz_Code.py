import random
import time
import math

# Leaderboard file
LEADERBOARD_FILE = "leaderboard.txt"

def mathQuizGame():
    """
    Main function to start the Math Quiz Game.
    This function handles the main menu and decides whether to play in single-player or multiplayer mode.
    """
    print("Welcome to the Math Quiz Game!")
    print("You can play solo or compete with another player in multiplayer mode.")
    
    # Ask if the user wants to play multiplayer mode
    multiplayer_mode = input("Do you want to play multiplayer mode? (yes/no): ").lower()
    if multiplayer_mode == "yes":
        multiplayer_game()  # Start multiplayer mode
    else:
        single_player_game()  # Start single-player mode


def single_player_game():
    """
    Single-player mode of the game.
    The player answers math questions, and their score is tracked.
    Adaptive difficulty increases or decreases based on performance.
    """
    score_points = 0  # Tracks the player's score
    consecutive_correct = 0  # Tracks consecutive correct answers
    consecutive_incorrect = 0  # Tracks consecutive incorrect answers
    attempts_number = 3  # Number of attempts per question
    difficulty_levels = ["easy", "medium", "hard"]  # Available difficulty levels
    current_difficulty_index = 0  # Current difficulty level index

    while True:
        # Display the main menu
        menu = input("Please select one of the following options: 1 - Play | 2 - Exit ----> ").lower()

        if menu == "1" or menu == "play":
            level_selected = difficulty_levels[current_difficulty_index]
            print(f"You have {attempts_number} attempts to answer the question.")

            while attempts_number > 0:
                # Generate a math problem based on the current difficulty
                problem, correct_answer = generate_problem(level_selected)
                print(problem)

                # Start the timer for the question
                start_time = time.time()
                answer = input("Enter your answer: ")
                elapsed_time = time.time() - start_time

                # Check if the user answered within the time limit (10 seconds)
                if elapsed_time > 10:
                    print("Time's up! You took too long to answer.")
                    attempts_number -= 1
                    consecutive_incorrect += 1
                    continue

                try:
                    answer = float(answer)  # Convert the input to a float
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    attempts_number -= 1
                    consecutive_incorrect += 1
                    continue

                # Check if the answer is correct
                if round(answer, 2) == round(correct_answer, 2):
                    print("Correct! You earned a point.")
                    score_points += 1
                    consecutive_correct += 1
                    consecutive_incorrect = 0
                else:
                    print(f"Incorrect. The correct answer was {round(correct_answer, 2)}.")
                    attempts_number -= 1
                    consecutive_incorrect += 1
                    consecutive_correct = 0

                # Adaptive difficulty adjustment
                if consecutive_correct >= 3 and current_difficulty_index < len(difficulty_levels) - 1:
                    current_difficulty_index += 1
                    print(f"Great job! Moving to the next difficulty level: {difficulty_levels[current_difficulty_index]}")
                    consecutive_correct = 0
                elif consecutive_incorrect >= 2 and current_difficulty_index > 0:
                    current_difficulty_index -= 1
                    print(f"Difficulty decreased to: {difficulty_levels[current_difficulty_index]}")
                    consecutive_incorrect = 0

            # Display the final score and update the leaderboard
            print(f"Your final score is {score_points}.")
            save_score(score_points)
            display_leaderboard()
            break

        elif menu == "2" or menu == "exit":
            print("Thank you for playing!")
            break

        else:
            print("Invalid option. Please try again.")


def multiplayer_game():
    """
    Multiplayer mode of the game.
    Two players take turns answering math questions, and their scores are compared at the end.
    """
    print("\n--- Multiplayer Mode ---")
    player1_name = input("Enter Player 1's name: ")  # Get Player 1's name
    player2_name = input("Enter Player 2's name: ")  # Get Player 2's name

    player1_score = 0  # Track Player 1's score
    player2_score = 0  # Track Player 2's score
    rounds = 5  # Number of rounds per player

    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num} ---")

        # Player 1's turn
        print(f"{player1_name}'s turn:")
        problem, correct_answer = generate_problem("easy")  # Generate a problem for Player 1
        print(problem)
        start_time = time.time()
        answer = input("Enter your answer: ")
        elapsed_time = time.time() - start_time

        # Check if Player 1 answered correctly and within the time limit
        if elapsed_time > 10:
            print("Time's up! No points awarded.")
        else:
            try:
                answer = float(answer)
                if round(answer, 2) == round(correct_answer, 2):
                    print("Correct! You earned a point.")
                    player1_score += 1
                else:
                    print(f"Incorrect. The correct answer was {round(correct_answer, 2)}.")
            except ValueError:
                print("Invalid input. No points awarded.")

        # Player 2's turn
        print(f"\n{player2_name}'s turn:")
        problem, correct_answer = generate_problem("easy")  # Generate a problem for Player 2
        print(problem)
        start_time = time.time()
        answer = input("Enter your answer: ")
        elapsed_time = time.time() - start_time

        # Check if Player 2 answered correctly and within the time limit
        if elapsed_time > 10:
            print("Time's up! No points awarded.")
        else:
            try:
                answer = float(answer)
                if round(answer, 2) == round(correct_answer, 2):
                    print("Correct! You earned a point.")
                    player2_score += 1
                else:
                    print(f"Incorrect. The correct answer was {round(correct_answer, 2)}.")
            except ValueError:
                print("Invalid input. No points awarded.")

    # Display the final scores and determine the winner
    print("\n--- Final Scores ---")
    print(f"{player1_name}: {player1_score}")
    print(f"{player2_name}: {player2_score}")

    if player1_score > player2_score:
        print(f"{player1_name} wins!")
    elif player2_score > player1_score:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie!")

    # Save scores to the leaderboard
    save_score(player1_score, player1_name)
    save_score(player2_score, player2_name)
    display_leaderboard()


def generate_problem(difficulty):
    """
    Generates a math problem based on the specified difficulty level.
    Args:
        difficulty (str): The difficulty level ("easy", "medium", or "hard").
    Returns:
        tuple: A tuple containing the problem string and the correct answer.
    """
    if difficulty == "easy":
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        operation = random.choice(["+", "-", "*", "/"])
        if operation == "+":
            return f"What is {x} + {y}?", x + y
        elif operation == "-":
            return f"What is {x} - {y}?", x - y
        elif operation == "*":
            return f"What is {x} * {y}?", x * y
        elif operation == "/":
            return f"What is {x} / {y}?", x / y

    elif difficulty == "medium":
        x = random.randint(1, 20)
        y = random.randint(1, 20)
        z = random.randint(1, 10)
        operation = random.choice(["algebra", "fraction"])
        if operation == "algebra":
            return f"Solve for x: 2x + {y} = {z}", (z - y) / 2
        elif operation == "fraction":
            return f"What is ({x}/{y}) + ({z}/{y})?", (x + z) / y

    elif difficulty == "hard":
        x = random.randint(1, 10)
        operation = random.choice(["calculus", "trigonometry"])
        if operation == "calculus":
            return f"What is the derivative of x^{x}?", x * (x ** (x - 1))
        elif operation == "trigonometry":
            angle = random.randint(0, 90)
            return f"What is sin({angle})?", round(math.sin(math.radians(angle)), 2)


def save_score(score, name="Player"):
    """
    Saves the player's score to the leaderboard file.
    Args:
        score (int): The player's score.
        name (str): The player's name.
    """
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{name}: {score}\n")


def display_leaderboard():
    """
    Displays the leaderboard by reading from the leaderboard file.
    Handles errors such as missing or malformed entries gracefully.
    """
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            scores = []
            for line in file.readlines():
                # Remove whitespace and ignore empty lines
                line = line.strip()
                if not line:
                    continue

                # Split the line into name and score
                parts = line.split(": ")
                if len(parts) == 2:  # Ensure there are exactly two elements
                    name, score = parts
                    try:
                        scores.append((name, int(score)))  # Convert score to integer
                    except ValueError:
                        print(f"Ignoring invalid score in line: {line}")
                else:
                    print(f"Invalid format in line: {line}")

        # Sort scores in descending order
        scores.sort(key=lambda x: x[1], reverse=True)

        # Display the leaderboard
        print("\n--- Leaderboard ---")
        for i, (name, score) in enumerate(scores[:5], 1):
            print(f"{i}. {name}: {score}")
        print("-------------------")

    except FileNotFoundError:
        print("No score records found.")


if __name__ == "__main__":
    mathQuizGame()
