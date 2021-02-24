'''Functions used to run hangman'''

def censor(word):
    ''' Returns a censored quote'''
    word_list = list(word)
    index = 0
    space = " "
    for char in word_list:
        if char is not space:
            word_list[index] = "X"
        index += 1

    word_list = ''.join(word_list)
    return word_list

def check(guess, quote, censored):
    '''
    Returns 2 if whole word is found
    Returns 1 if guess is correct
    Returns 0 for incorrect guess
    Function also returns uncensored word
    '''
    found = 0
    if guess == quote: #word exactly matches quote
        return [2, censored]

    quote = list(quote)
    censored = list(censored)
    counter = 0
    while counter < len(quote): #Uncensor correct guesses
        if quote[counter] == guess:
            censored[counter] = guess
            found = 1
        counter += 1

    censored = ''.join(censored)
    if censored == quote:
        found = 2

    return [found, censored]

#Checks for valid guess
#Returns word that is guessed as a string
def guess_sep(word):
    '''
    Function checks syntax of user guess
    Returns 0 for guess length < 7
    Returns 1 for missing space in guess
    Returns 2 for correct syntax
    Retyrbs 3 for messages that don't start with /guess
    '''
    word = word.rstrip()
    length = len(word)
    store = []

    if word.startswith('/guess'):
        if length <= 7:
            return [0, "Please type in guess properly"] #No space for correct wording
        counter = 7
        word = list(word)
        if length > 7:
            if word[6] == " ": #space is given
                while word[counter] == " ":
                    counter += 1
                while counter < length: #get guess
                    store.append(word[counter])
                    counter += 1
            else:
                return [1, "No space provided"] #No space provided
        store = ''.join(store)
        return [2, store] #Correct guess
    return [3, "Not a guess"] #not /guess
