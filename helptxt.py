text = ['Welcome to Digital Othello!', 'On the main page you are given 3 options:',
        '1: To play against a fellow, human friend. Both players will input their moves through the terminal.',
        '2: To play against the computer itself. The computer follows the minimax algorithm, so it will make optimal decisions looking several turns ahead.',
        '3: To watch two minimax AI players play against one another. ',
        'The rules of Othello are simple:',
        '1. Black moves first',
        '2. You can only place a piece on a square if that square is empty, and next to (above, below, left, right, and diagonal to) an enemy\'s piece',
        '3. If you have no valid moves to make, your turn is skipped until you do',
        '4. The game ends when no more valid moves can be made by either player.',
        'On the board, you will see the rows and columns, denoted with the numbers 1-8.',
        'To place a piece on a particular square, you must input the row and column of the square side-by-side, with no spaces.',
        'E.g, to place a piece on the square in row 3 column 4, you would input 34. For row 5 and column 6, you would input 56.',
        'If you run the game with an integer argument, you can change the number of turns that the computer will look ahead. Do this if you want to change the difficulty.',
        'Be warned: Setting the number too high may cause the game to run extremely slowly.']
def printmsg():
    for i in range(len(text)):
        if i == 0 or i == 5:
            print(text[i].center(180, ' '))
        elif (i > 1 and i<5) or i > 5 and i < 10:
            print('\t'+text[i])
            if i == 9:
                print()
        else:
            print(text[i])
    print('\n\n')
    input('Press Enter to return to the main menu...')
