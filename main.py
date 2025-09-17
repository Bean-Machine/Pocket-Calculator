from tkinter import *

# Create initial variables

displayVal = "0"  # the number on display
displayReset = True  # reset display for new number entry
expression = ""  # stores the expression to evaluate
expression2 = "" # sub expression for storing multiply and divide operations (which take precedence)
register1 = "0"  # for multiple equals operations
lastOperation = ""  # keeps track of which operation to perform
lastKey = "num"  # makes sure you can only perform one operation between number entries
newEquals = True  # is this the first time you've pressed the equals key in a row?
roundingErrorFactor = 100000000000000    # for correcting Pycharm's rounding errors when dealing with floats

# Create functions

def input0():
    global displayVal, displayReset, register1, output, lastKey, expression, expression2, counter
    counter[16] = buttonDuration
    if displayReset:
        displayVal = "0"
    else:
        displayVal += "0"
    canvas.itemconfig(output, text=displayVal)
    lastKey = "num"
    print(expression + " :: " + expression2)

def input1():
    inputNumber("1", 12)
def input2():
    inputNumber("2", 13)
def input3():
    inputNumber("3", 14)
def input4():
    inputNumber("4", 8)
def input5():
    inputNumber("5", 9)
def input6():
    inputNumber("6", 10)
def input7():
    inputNumber("7", 4)
def input8():
    inputNumber("8", 5)
def input9():
    inputNumber("9", 6)

def inputNumber(n, c):
    global displayVal, displayReset, register1, output, lastKey, expression, expression2, counter
    if lastKey == "equals":
        expression, expression2 = "", ""
    counter[c] = buttonDuration
    if displayReset:
        displayVal = n
        displayReset = False
    else:
        displayVal += n
    canvas.itemconfig(output, text=displayVal, anchor="e")
    lastKey = "num"
    print(expression + " :: " + expression2)

def inputPoint():
    global displayVal, displayReset, register1, output, lastKey, expression, counter
    counter[17] = buttonDuration
    if displayReset:
        displayVal = "0."
        displayReset = False
    else:
        if displayVal.count(".") == 0:
            displayVal += "."
    canvas.itemconfig(output, text=displayVal)
    lastKey = "num"
    print(expression + " :: " + expression2)

def plus():
    global displayVal, displayReset, lastOperation, newEquals, lastKey, expression, expression2, counter
    counter[15] = buttonDuration
    if expression2 != "":
        expression += expression2
        expression2 = ""
    if lastKey == "operation":
        expression = expression[:len(expression) - 1]
    elif lastKey != "equals":
        expression += displayVal
    expression = calculateDisplayValue(expression)
    canvas.itemconfig(output, text=expression)
    expression += "+"
    lastOperation = "+"
    displayReset, newEquals, lastKey = True, True, "operation"
    print(expression + " :: " + expression2)

def minus():
    global displayVal, displayReset, lastOperation, newEquals, lastKey, expression, expression2, counter
    counter[11] = buttonDuration
    if expression2 != "":
        expression += expression2
        expression2 = ""
    if lastKey == "operation":
        expression = expression[:len(expression) - 1]
    elif lastKey != "equals":
        expression += displayVal
    expression = calculateDisplayValue(expression)
    canvas.itemconfig(output, text=expression)
    expression += "-"
    lastOperation = "-"
    displayReset, newEquals, lastKey = True, True, "operation"
    print(expression + " :: " + expression2)

def multiply():
    global displayVal, displayReset, lastOperation, newEquals, lastKey, expression, expression2, counter
    counter[7] = buttonDuration
    if lastKey == "operation":
        expression = expression[:len(expression) - 1]
    elif lastKey != "equals":
        expression2 += displayVal
    elif lastKey == "equals":
        expression2 += expression
        expression = ""
    expression2 = calculateDisplayValue(expression2)
    canvas.itemconfig(output, text=expression2)
    expression2 += "*"
    lastOperation = "*"
    displayReset, newEquals, lastKey = True, True, "operation"
    print(expression + " :: " + expression2)

def divide():
    global displayVal, displayReset, lastOperation, newEquals, lastKey, expression, expression2, counter
    counter[3] = buttonDuration
    if lastKey == "operation":
        expression = expression[:len(expression) - 1]
    elif lastKey != "equals":
        expression2 += displayVal
    elif lastKey == "equals":
        expression2 += expression
        expression = ""
    expression2 = calculateDisplayValue(expression2)
    canvas.itemconfig(output, text=expression2)
    expression2 += "/"
    lastOperation = "/"
    displayReset, newEquals, lastKey = True, True, "operation"
    print(expression + " :: " + expression2)

def equals():
    global displayVal, displayReset, register1, output, lastOperation, newEquals, lastKey, expression, expression2, counter
    counter[18] = buttonDuration
    print(lastOperation, newEquals)
    if lastOperation == "+" or lastOperation == "-" or lastOperation == "":
        if newEquals:
            expression += displayVal
            register1 = displayVal
            displayVal = calculateDisplayValue(expression)
            newEquals = False
        elif lastOperation != "":
            expression += lastOperation + register1
            displayVal = calculateDisplayValue(expression)
        expression = displayVal
    elif lastOperation == "*" or lastOperation == "/":
        if newEquals:
            expression2 += displayVal
            register1 = displayVal
            displayVal = calculateDisplayValue(expression + expression2)
            newEquals = False
        elif lastOperation != "":
            expression2 += lastOperation + register1
            displayVal = calculateDisplayValue(expression2)
        expression2 = displayVal
    canvas.itemconfig(output, text=displayVal)
    print(expression + " :: " + expression2)
    displayReset = True
    lastKey = "equals"

def ac():
    global displayVal, displayReset, register1, output, lastOperation, newEquals, expression, expression2, counter
    counter[0] = buttonDuration
    displayVal, displayReset, register1, expression, expression2 = "0", True, "0", "", ""
    lastOperation, newEquals = "", True
    canvas.itemconfig(output, text=displayVal)

def percent():
    global displayVal, displayReset, register1, output, lastOperation, newEquals, expression, expression2, counter
    counter[2] = buttonDuration
    displayVal = str(float(displayVal) * 0.01)
    displayVal = calculateDisplayValue(displayVal)
    canvas.itemconfig(output, text=displayVal)
    print(expression + " :: " + expression2)

def plusMinus():
    global displayVal, displayReset, register1, output, lastOperation, newEquals, expression, counter
    counter[1] = buttonDuration
    displayVal = str(float(displayVal) * -1)
    if float(displayVal).is_integer():
        displayVal = str(int(float(displayVal)))
    canvas.itemconfig(output, text=displayVal)
    print(expression + " :: " + expression2)

def calculateDisplayValue(expr):
    temp = evaluate(expr)
    temp = round(temp * roundingErrorFactor) / roundingErrorFactor      # eliminates PyCharm's floating point errors
    if float(temp).is_integer():
        temp = int(float(temp))
    return str(temp)

def keyInput(event):
    global displayVal, displayReset, register1, output, lastKey, expression
    num = event.keysym
    if num == "BackSpace":
        displayVal = displayVal[:len(displayVal)-1]
        if displayVal == "" or displayVal == "0":
            displayVal = "0"
            displayReset = True
            expression = ""
        expression = expression[:len(expression)-1]
        canvas.itemconfig(output, text=displayVal)
        print(expression + " :: " + expression2)
    elif num == "period":
        inputPoint()
    elif num == "percent":
        percent()
    elif num == "Escape":
        ac()
    elif num == "plus":
        plus()
    elif num == "minus":
        minus()
    elif num == "asterisk":
        multiply()
    elif num == "slash":
        divide()
    elif num == "equal" or num == "Return":
        equals()
    else:
        try:
            n = int(num)
            commands = ('input0()', 'input1()', 'input2()', 'input3()',
                        'input4()', 'input5()', 'input6()',
                        'input7()', 'input8()', 'input9()')
            eval(commands[n])
        except:
            pass

def leftClick(event):
    xCo = event.x
    yCo = event.y
    if yCo > sqSize + margin:
        commands = (("ac()", "plusMinus()", "percent()", "divide()"),
                    ('input7()', 'input8()', 'input9()', "multiply()"),
                    ('input4()', 'input5()', 'input6()', "minus()"),
                    ('input1()', 'input2()', 'input3()', "plus()"),
                    ('input0()', 'input0()', "inputPoint()", "equals()"))
        xCo = int((xCo-margin) / sqSize)
        yCo -= sqSize + margin
        yCo = int(yCo / sqSize)
        try:
            eval(commands[yCo][xCo])
        except:
            pass

# My own re-write of the eval() function (for arithemetical expressions only)
def evaluate(expr):
    digits = ".0123456789"
    operations = "+-*/"
    numberList = []
    opList = []
    # Parse expression and separate it into numbers and operations
    temp = ""
    lastC = ""
    if expr[0] == "-":                              # make the first number negative if the expression starts with "-"
        lastC = "-"                                 # set lastC to an operation so the "-" gets added to the first number
    for c in expr:
        if c in digits:
            temp += c
        elif c in operations and lastC in digits:
            numberList.append(temp)
            temp = ""
            opList.append(c)
        elif c == "-" and lastC in operations:      # add "-" to negative numbers
            temp += c
        lastC = c
    numberList.append(temp)                         # get the last number after expression has been parsed
    # First pass for multiply and divide
    for i in range(len(opList)):
        if opList[i] == "*":
            a = float(numberList[i])
            b = float(numberList[i+1])
            numberList[i+1] = str(a * b)
            numberList[i], opList[i] = None, None
        elif opList[i] == "/":
            a = float(numberList[i])
            b = float(numberList[i + 1])
            numberList[i + 1] = str(a / b)
            numberList[i], opList[i] = None, None
    # Remove all None types from both lists
    for i in range(opList.count(None)):
        opList.remove(None)
        numberList.remove(None)
    # Second pass for add and subtract
    for i in range(len(opList)):
        if opList[i] == "+":
            a = float(numberList[i])
            b = float(numberList[i + 1])
            numberList[i + 1] = str(a + b)
            numberList[i], opList[i] = None, None
        elif opList[i] == "-":
            a = float(numberList[i])
            b = float(numberList[i + 1])
            numberList[i + 1] = str(a - b)
            numberList[i], opList[i] = None, None
    # Return the last element of the numberList as a float
    return float(numberList[-1])


# Implement GUI -----------------------------------------------------------------------------

margin = 4
sqSize = 60
numMargin = int(sqSize / 2) + margin
width = sqSize * 4
height = sqSize * 6
x0 = margin
x1 = x0 + sqSize
x2 = x1 + sqSize
x3 = x2 + sqSize
x4 = x3 + sqSize
y0, y1, y2, y3 = x1, x2, x3, x4
y4 = y3 + sqSize
y5 = y4 + sqSize

numFont = ("Helvetica", "30")
numFont2 = ("Helvetica", "24")
numFont3 = ("Helvetica", "34")
buttons = [0] * 19              # array for button backgrounds
counter = [0] * 19              # counter array for button presses
number = [""] * 10

lineColor = "grey"
orange = "#ff9b32"
paleGrey = "#cccccc"
darkGrey = "#444444"
buttonPress = "#888888"
buttonDuration = 10

window = Tk()
window.resizable(width=False, height=False)
window.bind("<Key>", keyInput)              # key input
window.bind("<Button-1>", leftClick)        # left mouse click

canvas = Canvas(window, width=width+margin, height=height+margin, bg="white")
canvas.pack(side=TOP)

outputField = canvas.create_rectangle(x0, margin, x4, y0, fill=darkGrey)

buttons[0] = canvas.create_rectangle(x0,y0,x1,y1, fill=paleGrey)
buttons[1] = canvas.create_rectangle(x1,y0,x2,y1, fill=paleGrey)
buttons[2] = canvas.create_rectangle(x2,y0,x3,y1, fill=paleGrey)
buttons[3] = canvas.create_rectangle(x3,y0,x4,y1, fill=orange)
buttons[4] = canvas.create_rectangle(x0,y1,x1,y2, fill=paleGrey)
buttons[5] = canvas.create_rectangle(x1,y1,x2,y2, fill=paleGrey)
buttons[6] = canvas.create_rectangle(x2,y1,x3,y2, fill=paleGrey)
buttons[7] = canvas.create_rectangle(x3,y1,x4,y2, fill=orange)
buttons[8] = canvas.create_rectangle(x0,y2,x1,y3, fill=paleGrey)
buttons[9] = canvas.create_rectangle(x1,y2,x2,y3, fill=paleGrey)
buttons[10] = canvas.create_rectangle(x2,y2,x3,y3, fill=paleGrey)
buttons[11] = canvas.create_rectangle(x3,y2,x4,y3, fill=orange)
buttons[12] = canvas.create_rectangle(x0,y3,x1,y4, fill=paleGrey)
buttons[13] = canvas.create_rectangle(x1,y3,x2,y4, fill=paleGrey)
buttons[14] = canvas.create_rectangle(x2,y3,x3,y4, fill=paleGrey)
buttons[15] = canvas.create_rectangle(x3,y3,x4,y4, fill=orange)
buttons[16] = canvas.create_rectangle(x0,y4,x2,y5, fill=paleGrey)
buttons[17] = canvas.create_rectangle(x2,y4,x3,y5, fill=paleGrey)
buttons[18] = canvas.create_rectangle(x3,y4,x4,y5, fill=orange)

number[0] = canvas.create_text(sqSize+numMargin, 5*sqSize+numMargin, text="0", fill="black", font=numFont)
for i in range(0,3):
    for j in range(0,3):
        num = (i*3)+j+1
        xCo = (j * sqSize) + numMargin
        yCo = (4 - i) * sqSize + numMargin
        number[num] = canvas.create_text(xCo, yCo, text=str(num), fill="black", font=numFont)
pointT = canvas.create_text(2*sqSize+numMargin, 5*sqSize+numMargin, text=".", fill="black", font=numFont)
equalsT = canvas.create_text(3*sqSize+numMargin, 5*sqSize+numMargin, text="=", fill="white", font=numFont)
plusT = canvas.create_text(3*sqSize+numMargin, 4*sqSize+numMargin, text="+", fill="white", font=numFont)
minusT = canvas.create_text(3*sqSize+numMargin, 3*sqSize+numMargin, text="-", fill="white", font=numFont)
multiplyT = canvas.create_text(3*sqSize+numMargin, 2*sqSize+numMargin, text="X", fill="white", font=numFont2)
divideT = canvas.create_text(3*sqSize+numMargin, sqSize+numMargin, text="/", fill="white", font=numFont)
acT = canvas.create_text(numMargin, sqSize+numMargin, text="AC", fill="black", font=numFont2)
negT = canvas.create_text(sqSize+numMargin, sqSize+numMargin, text="+/-", fill="black", font=numFont)
percentT = canvas.create_text(2*sqSize+numMargin, sqSize+numMargin, text="%", fill="black", font=numFont)

output = canvas.create_text(width-numMargin/2, numMargin, text=displayVal, fill="white", font=numFont3, anchor="e")

# Main loop
while True:
    for i in range(len(counter)):
        if counter[i] > 0:
            counter[i] -= 1
            canvas.itemconfig(buttons[i], fill=buttonPress)
        else:
            if i in (3, 7, 11, 15, 18):
                canvas.itemconfig(buttons[i], fill=orange)
            else:
                canvas.itemconfig(buttons[i], fill=paleGrey)
    window.update()

window.mainloop()