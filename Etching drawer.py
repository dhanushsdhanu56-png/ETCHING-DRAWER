import shutil
import sys

# Set up the line characters
UP_DOWN_CHAR = chr(9474)          # │
LEFT_RIGHT_CHAR = chr(9472)       # ─
DOWN_RIGHT_CHAR = chr(9484)       # ┌
DOWN_LEFT_CHAR = chr(9488)        # ┐
UP_RIGHT_CHAR = chr(9492)         # └
UP_LEFT_CHAR = chr(9496)          # ┘
UP_DOWN_RIGHT_CHAR = chr(9500)    # ├
UP_DOWN_LEFT_CHAR = chr(9508)     # ┤
DOWN_LEFT_RIGHT_CHAR = chr(9516)  # ┬
UP_LEFT_RIGHT_CHAR = chr(9524)    # ┴
CROSS_CHAR = chr(9532)            # ┼


# Get the size of the terminal window
CANVAS_WIDTH, CANVAS_HEIGHT = shutil.get_terminal_size()

# Leave room for command information
CANVAS_WIDTH -= 1
CANVAS_HEIGHT -= 5


# Canvas stores (x, y) coordinates and their connected directions
canvas = {}

# Starting cursor position
cursorX = 0
cursorY = 0


def getCanvasString(canvasData, cx, cy):
    """Return a string representing the drawing."""

    canvasStr = ''

    for rowNum in range(CANVAS_HEIGHT):
        for columnNum in range(CANVAS_WIDTH):

            # Display cursor
            if columnNum == cx and rowNum == cy:
                canvasStr += '#'
                continue

            # Get the cell information
            cell = canvasData.get((columnNum, rowNum))

            if cell in ({'W', 'S'}, {'W'}, {'S'}):
                canvasStr += UP_DOWN_CHAR

            elif cell in ({'A', 'D'}, {'A'}, {'D'}):
                canvasStr += LEFT_RIGHT_CHAR

            elif cell == {'S', 'D'}:
                canvasStr += DOWN_RIGHT_CHAR

            elif cell == {'A', 'S'}:
                canvasStr += DOWN_LEFT_CHAR

            elif cell == {'W', 'D'}:
                canvasStr += UP_RIGHT_CHAR

            elif cell == {'W', 'A'}:
                canvasStr += UP_LEFT_CHAR

            elif cell == {'W', 'S', 'D'}:
                canvasStr += UP_DOWN_RIGHT_CHAR

            elif cell == {'W', 'S', 'A'}:
                canvasStr += UP_DOWN_LEFT_CHAR

            elif cell == {'A', 'S', 'D'}:
                canvasStr += DOWN_LEFT_RIGHT_CHAR

            elif cell == {'W', 'A', 'D'}:
                canvasStr += UP_LEFT_RIGHT_CHAR

            elif cell == {'W', 'A', 'S', 'D'}:
                canvasStr += CROSS_CHAR

            else:
                canvasStr += ' '

        canvasStr += '\n'

    return canvasStr


# Store all movements
moves = []


# Main program loop
while True:

    # Display the drawing
    print(getCanvasString(canvas, cursorX, cursorY))

    print("WASD keys to move, H for help, C to clear,")
    print("F to save, or QUIT.")

    response = input("> ").upper()

    # Quit
    if response == 'QUIT':
        print("Thanks for playing!")
        sys.exit()

    # Help
    elif response == 'H':
        print("Enter W, A, S, and D characters to move the cursor")
        print("and draw a line behind it as it moves.")
        print()
        print("Example:")
        print("DDD       draws a horizontal line")
        print("SSSDDDWWWAAA   draws a box")
        print()
        print("Enter F to save your drawing to a text file.")

        input("Press Enter to return to the program...")
        continue

    # Clear canvas
    elif response == 'C':
        canvas = {}
        moves.append('C')

    # Save drawing
    elif response == 'F':

        try:
            print("Enter filename to save to:")
            filename = input("> ")

            if not filename.endswith('.txt'):
                filename += '.txt'

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(''.join(moves) + '\n')
                file.write(getCanvasString(canvas, None, None))

            print("Drawing saved successfully!")

        except Exception:
            print("ERROR: Could not save file.")

    # Process movement commands
    for command in response:

        # Ignore invalid characters
        if command not in ('W', 'A', 'S', 'D'):
            continue

        moves.append(command)

        # Create the first line
        if canvas == {}:

            if command in ('W', 'S'):
                canvas[(cursorX, cursorY)] = {'W', 'S'}

            elif command in ('A', 'D'):
                canvas[(cursorX, cursorY)] = {'A', 'D'}

        # Move UP
        if command == 'W' and cursorY > 0:
            canvas[(cursorX, cursorY)].add('W')
            cursorY -= 1

        # Move DOWN
        elif command == 'S' and cursorY < CANVAS_HEIGHT - 1:
            canvas[(cursorX, cursorY)].add('S')
            cursorY += 1

        # Move LEFT
        elif command == 'A' and cursorX > 0:
            canvas[(cursorX, cursorY)].add('A')
            cursorX -= 1

        # Move RIGHT
        elif command == 'D' and cursorX < CANVAS_WIDTH - 1:
            canvas[(cursorX, cursorY)].add('D')
            cursorX += 1

        else:
            continue

        # Create a new set for the new position
        if (cursorX, cursorY) not in canvas:
            canvas[(cursorX, cursorY)] = set()

        # Add the connecting direction
        if command == 'W':
            canvas[(cursorX, cursorY)].add('S')

        elif command == 'S':
            canvas[(cursorX, cursorY)].add('W')

        elif command == 'A':
            canvas[(cursorX, cursorY)].add('D')

        elif command == 'D':
            canvas[(cursorX, cursorY)].add('A')