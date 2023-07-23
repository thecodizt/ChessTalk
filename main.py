import speech_recognition as sr

import subprocess
import chess
import chess.engine
from tqdm import tqdm
import time
from colorama import init, Fore, Style

r = sr.Recognizer()
mic = sr.Microphone()

engine = chess.engine.SimpleEngine.popen_uci("./Stockfish/src/Stockfish")

board = chess.Board()
player_color = chess.WHITE


word_dict = {
    'apple': 'a',
    'ball': 'b',
    'cat': 'c',
    'dog': 'd',
    'elephant': 'e',
    'frog': 'f',
    'guitar': 'g',
    'hat': 'h',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'to': '2'
}



# Initialize colorama
init()

def say(text):
    subprocess.call(['say', text])


while not board.is_game_over():
    time.sleep(1)
    if board.turn == player_color:
        # Player's turn
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Adjusted for noise")
            say("Your move:")
            player_move = None
            
            audio = r.listen(source)
            transcript = r.recognize_google(audio)
            transcript = transcript.lower()
            # transcript = ''.join(word_dict[x] for x in transcript.split(' ') if x in word_dict.keys() else x)
            transcript = ''.join(word_dict[x.lower()] if x.lower() in word_dict else x[0] for x in transcript.split())
            transcript = transcript.lower()
            print("Your move: " + transcript)
            player_move = transcript
            # player_move = input()
            try:
                move = chess.Move.from_uci(player_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print(Fore.RED + "Invalid move! Try again.")
                    say("Illegal move")
                    continue
            except:
                print(Fore.RED + "Invalid move format! Try again.")
                say("Tell again please")
                continue
    else:
        # Engine's turn
        result = engine.play(board, chess.engine.Limit(time=1))
        move = result.move
        if move is not None:
            board.push(move)
            say(str(move))

    # Clear the previous output
    print('\033c', end='')

    # Print the current board state with color
    print(Fore.GREEN + str(board) + Style.RESET_ALL)

# Call the say function with SAN move

engine.quit()
