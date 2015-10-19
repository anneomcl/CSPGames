import copy
import heapq

def wordlist_to_data():
    f = open("Resources/wordlist.txt")
    data = dict()
    for line in f:
        category = line.split(":\t")[0]
        values = (((line.split(":\t")[1:])[0]).split("\n"))[0].split(", ")
        data[category] = values
    return data

def puzzle_to_assignment(file):
    f = open(file)
    puzzle = dict()
    for line in f:
        category = line.split(": ")[0]
        if(len(line.split(": ")) > 1):
            values = list(map(int, (line.split(": "))[1].split(", ")))
            puzzle[category] = values
        else:
            size = category
    return [int(size), puzzle]

def isComplete(assignment, csp):
    if len(assignment) < 1:
        return False
    for category in csp:
        stringToCheck = ""
        for index in csp[category]:
            stringToCheck += assignment[index - 1]
        if stringToCheck not in wordList[category]:
            return False
    return True

def createVariablesDomain(assignment, csp):
    vars = dict()
    for category in csp[1]:
        indices = csp[1][category]
        for i in indices:
            if i not in vars:
                vars[i] = 1
            else:
                vars[i]+=1

    heap = []
    for val in vars:
        heapq.heappush(heap,((vars[val]*-1, val))) #priority, index

    return heap

def selectUnassignedVariableLetter(assignment, csp):
    return heapq.heappop(varHeap)[1]

def findLetterPos(category, index):
    j = 0
    for i in category:
        if i == index:
            return j
        j+=1
    return -1

def findAllLettersSatisfyingConstraintsAtI(index, categories, assignment,csp):
    letters = []
    category = categories[0]
    pos = findLetterPos(csp[category], index)
    found = False
    for word in wordList[category]:
        letter = word[pos]
        if(len(categories) == 1 and letter not in letters):
            letters.append(letter)
        if(index in invalidLetters and letter not in invalidLetters[index]):
            for cat in categories[1:]:
                found = False
                posNext = findLetterPos(csp[cat], index)
                for w in wordList[cat]:
                    if w[posNext] == letter:
                        found = True
                        break
                if found == False:
                    addInvalidLetter(invalidLetters, letter, index)
                    break
            if letter not in letters and found == True:
                letters.append(letter)


    return letters

def addInvalidLetter(invalidList, letter, i):
    if i in invalidList:
        invalidList[i].append(letter)
    else:
        invalidList[i] = letter

def selectBestValuesLetter(assignment,csp,var):
    categories = constraintsPerIndex[var]
    return findAllLettersSatisfyingConstraintsAtI(var, categories, assignment, csp)

def isConsistent(value, assignment, csp, var):
    temp = assignment[var - 1]
    assignment[var - 1] = value

    for category in csp:
        stringToCheck = ""
        for index in csp[category]:
            stringToCheck += assignment[index - 1]
        i = 0
        consistent = False
        for letter in stringToCheck:
            if(letter != '0'):
                for word in wordList[category]:
                    if word[i] == letter:
                        consistent = True
                        break
                if consistent == False:
                    assignment[var - 1] = temp
                    return False
            i+=1
    return True

def updateBestLetters(bestLetters, var, value, csp):
    #find every constraint var exists in 3 -> body, adjective
    #for each constraint, for each word in constraint, is there a combo of valid + value + valid?

    categories = constraintsPerIndex[var]

    for cat in categories:
        valA = []
        valB = []
        posVal = findLetterPos(csp[cat], var)
        posA = 0
        posB = 1
        if(posVal == 0):
            posA = 1
            posB = 2
        elif(posVal == 1):
            posB = 2
        for word in wordList[cat]:
            if(word[posVal]) == value:
                if word[posA] in bestLetters[csp[cat][posA]] and word[posB] in bestLetters[csp[cat][posB]]:
                    valA.append(word[posA])
                    valB.append(word[posB])
        bestLetters[csp[cat][posA]] = [item for item in bestLetters[csp[cat][posA]] if item in valA]
        bestLetters[csp[cat][posB]] = [item for item in bestLetters[csp[cat][posB]] if item in valB]

def checkIfBestLettersEmpty():
    global bestLetters
    for i in bestLetters:
        if len(bestLetters[i]) < 1:
            return True
    return False

def reportFailure(value, assignment):
    global number
    number +=1

def reportSuccess(value, assignment):

    global numberS
    numberS +=1

def recursive_backtracking_letter(assignment, csp):

    if isComplete(assignment, csp):
        return assignment

    var = 0
    if len(varHeap) > 0:
        var = selectUnassignedVariableLetter(assignment, csp)
    else:
        return []

    global bestLetters
    temp = copy.deepcopy(bestLetters)
    vals =  bestLetters[var] #guaranteed to be locally consistent for given var
    for value in vals:
        printBool = True
        if isConsistent(value, assignment, csp, var):
            print((' ').join(assignment) + " -> ", end = "")
            assignment[var - 1] = value
            updateBestLetters(bestLetters, var, value, csp)
            if(checkIfBestLettersEmpty()):
                bestLetters = copy.deepcopy(temp)
                bestLetters[var].remove(value)
                if(printBool):
                    printBool = False
                reportFailure(value, assignment)
                continue
            result = recursive_backtracking_letter(assignment, csp)
            if result != []:
                reportSuccess(value, result)
                return result

            assignment[var - 1] = '0'
            bestLetters[var].remove(value)


    priority = -1*len(constraintsPerIndex[var])
    heapq.heappush(varHeap, (priority, var))
    reportFailure(value, assignment)
    return []

def initAssignment(size):
    ret = []
    i = 0
    while i < size:
        ret.append('0')
        invalidLetters[i+1] = []
        i+=1
    return ret

def findConstraintsByIndex(puzzle):
    ret = dict()
    for category in puzzle:
        for index in puzzle[category]:
            if index in ret:
                ret[index].append(category)
            else:
                ret[index] = [category]
    return ret

def findAllValidLetters(assignment, csp):
    ret = dict()
    j = 1
    for i in assignment:
        vals = selectBestValuesLetter(assignment, csp, j)
        ret[j] = vals
        j+=1
    return ret

def recursive_backtracking_word(assignment, csp):
    return []

def solve(puzzle, mode):
    p = puzzle_to_assignment(puzzle) #returns puzzleSize, puzzleDictionary
    global constraintsPerIndex
    constraintsPerIndex = findConstraintsByIndex(p[1])
    assignment = initAssignment(p[0])
    global varHeap
    varHeap = createVariablesDomain(assignment, p) #call heappop to get most constrained val
    global bestLetters
    bestLetters = findAllValidLetters(assignment, p[1])
    print("Root -> ", end = "")
    if(mode == "letter"):
        print(recursive_backtracking_letter(assignment, p[1]))
    if(mode == "word"):
        print(recursive_backtracking_word(assignment, p[1]))
    global numberS
    global number
    print("Fail: " + str(number))
    print("Success: " + str(numberS))
    varHeap = 0
    constraintsPerIndex = 0
    global invalidLetters
    invalidLetters = dict()
    number = 0
    numberS = 0
    bestLetters = 0



#Start execution
wordList = wordlist_to_data()
varHeap = 0
constraintsPerIndex = 0
invalidLetters = dict()
number = 0
numberS = 0
bestLetters = 0
solve("Resources/puzzle1.txt", "letter")
solve("Resources/puzzle2.txt", "letter")
solve("Resources/puzzle3.txt", "letter")
solve("Resources/puzzle4.txt", "letter")
solve("Resources/puzzle5.txt", "letter")

