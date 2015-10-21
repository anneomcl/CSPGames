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
        for cat in categories[1:]:
            found = False
            posNext = findLetterPos(csp[cat], index)
            for w in wordList[cat]:
                if w[posNext] == letter:
                    found = True
                    break
            if found == False:
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

def updateBestWords(bestWords, category, w, csp):


    #if we assign a certain word for a certain category, what words are impossible?
    i = 0
    while(i < 3):
        #for each letter
        categoriesToCheck = constraintsPerIndex[csp[category][i]]
        for cat in categoriesToCheck:
            if cat != category:
                vals = []
                #a possible value is one where there exists a word in cat such that word[i] == w[i]
                for word in wordList[cat]:
                    if(word[findLetterPos(csp[cat], csp[category][i])] == w[i]):
                        vals.append(word)
                bestWords[cat] = [item for item in bestWords[cat] if item in vals]

        i+=1

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

def checkIfBestWordsEmpty():
    global bestWords
    for i in bestWords:
        if len(bestWords[i]) < 1:
            return True
    return False


def checkIfBestLettersEmpty():
    global bestLetters
    for i in bestLetters:
        if len(bestLetters[i]) < 1:
            return True
    return False

def reportFailure():
    global number
    number +=1

def reportSuccess(value, assignment):
    global numberS
    numberS +=1

def selectUnassignedVariableWord(assignment, csp):
    a = []
    global availableCategories
    for item in availableCategories:
        priority = 0
        for i in csp[item]:
            priority += (-1)*len(constraintsPerIndex[i])
        a.append((priority, item))

    a.sort()
    var = a[0][1]
    del availableCategories[var]
    return var

def recursive_backtracking_letter(assignment, csp):

    if isComplete(assignment, csp):
        return assignment

    var = 0
    if len(varHeap) > 0:
        var = selectUnassignedVariableLetter(assignment, csp)
    else:
        return []

    global fail
    fail = 0

    global bestLetters
    temp = copy.deepcopy(bestLetters)
    vals =  bestLetters[var] #guaranteed to be locally consistent for given var
    for value in vals:
        if isConsistent(value, assignment, csp, var):
            assignment[var - 1] = value
            if(fail):
                print("\n" + "\t"+ "Position #" + str(var) + ": ")
                print("\t" + value + " (" +((' ').join(assignment))+ ")" + " -> ", end = "")
            else:
                print("\n" +  "Position #" + str(var) + ": ")
                print(value + " (" +((' ').join(assignment))+ ")" + " -> ", end = "")
            updateBestLetters(bestLetters, var, value, csp)
            if(checkIfBestLettersEmpty()):
                bestLetters = copy.deepcopy(temp)
                bestLetters[var].remove(value)
                reportFailure()
                fail = 1
                continue
            result = recursive_backtracking_letter(assignment, csp)
            if result != [] and result not in wordSolutions:
                global wordSolutions
                sol = copy.deepcopy(result)
                wordSolutions.append((' ').join(sol))
                print((' ').join(sol))
                print("Solution Found: " + (' ').join(sol))
                global number
                #print("\nNumber of invalid words tried: " + str(number))
                global numberS
                #print("Times backtracked: " + str(numberS))
                bestLetters = findAllValidLetters(assignment, csp)
                number = 0
                numberS = 0

            assignment[var - 1] = '0'
            bestLetters[var].remove(value)

    bestLetters = findAllValidLetters(assignment, csp)
    priority = -1*len(constraintsPerIndex[var])
    heapq.heappush(varHeap, (priority, var))
    reportFailure()
    global numberS
    numberS += 1
    fail = 0
    print("\n\n" + "Backtracking...")
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

def selectBestValuesWord(assignment, csp):
    words = dict()
    found = False
    invalidWords = []

    for cat in csp:
        words[cat] = []
        #for each category, find words that are possible
        #find indices we want to fill in
        for word in wordList[cat]:
            #for each word in a category
            i = 0
            found = False
            while(i < 3):
                #for each letter in the word, check if that letter could possibly be in that position
                for constraint in constraintsPerIndex[csp[cat][i]]:
                    #ensure that the letter is valid for all possible constraints in that position
                    found = False
                    for w in wordList[constraint]:
                        if((w[findLetterPos(csp[constraint], csp[cat][i])] == word[i]) or constraint == cat):
                            found = True
                            break
                    if found == False:
                        break
                if found == False:
                    break
                i+=1
            if found == True:
                words[cat].append(word)


    return words

def findAllValidWords(assignment,csp):
    ret = dict()
    for category in csp:
        vals = selectBestValuesWord(assignment, csp)
        ret[category] = vals
    return ret

def recursive_backtracking_word(assignment, csp):
    if isComplete(assignment, csp):
        return assignment

    var = selectUnassignedVariableWord(assignment, csp)

    global bestWords
    temp = copy.deepcopy(bestWords)
    vals =  bestWords[var] #candidates for a given category
    global fail
    fail = 0
    for value in vals:
        global changed
        changed = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if isConsistentWord(assignment, csp, value, var):
            assignVar(assignment,csp,var,value)
            if(fail):
                print("\n" + "\t"+ var + ": ")
                print("\t" + value + " (" +((' ').join(assignment))+ ")" + " -> ", end = "")
            else:
                print("\n" +  var + ": ")
                print(value + " (" +((' ').join(assignment))+ ")" + " -> ", end = "")
            updateBestWords(bestWords, var, value, csp)
            if(checkIfBestWordsEmpty()):
                i = 0
                while(i < 3):
                    if changed[csp[var][i]  - 1] == 1:
                        assignment[csp[var][i] - 1] = '0'
                    i+=1
                bestWords = copy.deepcopy(temp)
                bestWords[var].remove(value)

                global number
                number += 1
                fail = 1
                continue
            result = recursive_backtracking_word(assignment, csp)
            if result != [] and result not in wordSolutions:
                global wordSolutions
                sol = copy.deepcopy(result)
                wordSolutions.append((' ').join(sol))
                print((' ').join(sol))
                global number
                print("\nSolution Found: " + (' ').join(sol))
                #print("Number of invalid words tried: " + str(number))
                global numberS
                #print("Times backtracked: " + str(numberS))
                number = 0
                numberS = 0
                bestWords = selectBestValuesWord(assignment,csp)
            i = 0
            while(i < 3):
                assignment[csp[var][i] - 1] = '0'
                i+=1
            bestWords[var].remove(value)

    bestWords = selectBestValuesWord(assignment,csp)
    print("\n\n" + "Backtracking...")
    global numberS
    numberS +=1
    fail = 0
    number +=1
    global availableCategories
    availableCategories[var] = copy.deepcopy(csp[var])
    return []

def assignVar(assignment,csp,var,value):
    if(assignment[csp[var][0]-1] == '0'):
        assignment[csp[var][0]-1] = value[0]
        changed[csp[var][0]-1] = 1
    if(assignment[csp[var][1]-1] == '0'):
        assignment[csp[var][1]-1] = value[1]
        changed[csp[var][1]-1] = 1
    if(assignment[csp[var][2]-1] == '0'):
        changed[csp[var][2]-1] = 1
        assignment[csp[var][2]-1] = value[2]

def isConsistentWord(assignment, csp, word, cat):

    if((assignment[csp[cat][0]-1] == word[0] or assignment[csp[cat][0]-1] == '0')
       and (assignment[csp[cat][1]-1] == word[1] or assignment[csp[cat][1]-1] == '0')
       and (assignment[csp[cat][2]-1] == word[2] or assignment[csp[cat][2]-1] == '0')):

        return True
    else:
        return False

def initChanged(size):
    global changed
    i = 0
    while i < size:
        changed.append(0)
        i+=1

def solve(puzzle, mode):
    p = puzzle_to_assignment(puzzle) #returns puzzleSize, puzzleDictionary

    global constraintsPerIndex
    constraintsPerIndex = findConstraintsByIndex(p[1])

    assignment = initAssignment(p[0])

    global varHeap
    varHeap = createVariablesDomain(assignment, p) #call heappop to get most constrained val

    global availableCategories
    availableCategories = copy.deepcopy(p[1])

    global changed
    changed = initChanged(p[0])

    global invalidLetters
    invalidLetters = dict()

    global bestLetters
    bestLetters = findAllValidLetters(assignment, p[1])

    global bestWords
    bestWords = selectBestValuesWord(assignment, p[1])

    global wordSolutions
    wordSolutions = []

    print("Solving " + puzzle + " using " + mode + "-based algorithm ...\n")
    print("Root -> ", end = "")
    if(mode == "letter"):
        result = recursive_backtracking_letter(assignment, p[1])
        print((' ').join(result))
        #print(wordSolutions)
    if(mode == "word"):
        result = recursive_backtracking_word(assignment, p[1])
        #print((' ').join(result))

    print("All solutions: " + str(wordSolutions)+ "\n\n")

    availableCategories = 0
    changed = []
    varHeap = 0
    constraintsPerIndex = 0
    invalidLetters = dict()
    number = 0
    numberS = 0
    bestLetters = 0
    bestWords = 0
    global fail
    fail = 0



#Start execution
wordSolutions = []
availableCategories = 0
changed = []
varHeap = 0
constraintsPerIndex = 0
invalidLetters = dict()
number = 0
numberS = 0
bestLetters = 0
bestWords = 0
fail = 0


wordList = wordlist_to_data()

'''solve("Resources/puzzle1.txt", "word")
solve("Resources/puzzle2.txt", "word")
solve("Resources/puzzle3.txt", "word")
solve("Resources/puzzle4.txt", "word")
solve("Resources/puzzle5.txt", "word")'''
solve("Resources/puzzle1.txt", "letter")
solve("Resources/puzzle2.txt", "letter")
solve("Resources/puzzle3.txt", "letter")
solve("Resources/puzzle4.txt", "letter")
solve("Resources/puzzle5.txt", "letter")

