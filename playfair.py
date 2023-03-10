# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:59:57 2020

Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Mallika Gupta
Date: February 28,2023
Project 4: Playfair Cipher
"""

from string import ascii_lowercase

## The function createTable(phrase) takes an argument called phrase.This function removes
## any non-letter characters from the phrase given by the user and converts it 
## to lowercase. It also removes the letter q if it is included in the phrase
## and removes duplicate letters  as well. It prints only 25 letters instead 
## of 26, as the the ciphertable can only store 25.It creates the 5*5 ciphertable
## with the 25 letters, and returns it.

def createTable(phrase):
    phrase = ''.join(filter(str.isalpha, phrase)).lower()
    phrase = phrase.replace('q', '')
    phrase = ''.join(sorted(set(phrase), key=phrase.index))
    alphabet = 'abcdefghijklmnoprstuvwxyz'
    for letter in alphabet:
        if letter not in phrase:
            phrase += letter
    ciphertable = [list(phrase[i:i+5]) for i in range(0, 25, 5)]
    return ciphertable

## The function splitStrin(plaintext) takes a plaintext string as input and 
## returns a list of bigrams which are two character pairs. This function
## should remove function, spaces, punctuation and Q's. Also, the uppercase
## letters should be converted to lowercase.

def splitString(plaintext):
    plaintext = plaintext.lower()
    plaintext = ''.join(c for c in plaintext if c.isalpha() and c != 'q')

    bigrams = []
    for i in range(0, len(plaintext), 2):
        if i + 1 < len(plaintext):
            bigrams.append(plaintext[i:i+2])
        else:
            bigrams.append(plaintext[i] + 'x')

    return bigrams

## The function playfairRuleOne(pair is the first function which manipulates
## the bigrams one at a time. It looks at the two characters within the input
## bigram to see if they are identical or not.If both of the letters are the 
## same, the second letter should be replaced with an 'x'. If the first letter 
## is 'x', the second letter should be replaced with 'z'. Otherwise, if the two
## letters are different, the original pair should be returned.

def playfairRuleOne(pair):
    # Do a check to see if the pair contains two identical letters
    if pair[0] == pair[1]:
        # If the first letter is 'x', replace the second letter with 'z'
        if pair[0] == 'x':
            return 'xz'
        # Otherwise, replace the second letter with 'x'
        else:
            return pair[0] + 'x'
    # If the two letters are different, return the original pair of letters.
    else:
        return pair
    
## The function playfairRuleTwo(pair,table) uses the ciphertable. It looks at
## the coordinates of the two letters in the input bigram to see if they are 
## in the same row. If the two letters are in the same row, 
## they should be replaced with the letters to the immediate right.
 
def playfairRuleTwo(pair, table):
    # Find the coordinates of the two letters in the table
    row1, col1 = None, None
    row2, col2 = None, None
    for i in range(5):
        for j in range(5):
            if table[i][j] == pair[0]:
                row1, col1 = i, j
            elif table[i][j] == pair[1]:
                row2, col2 = i, j
    # Replace the two letters with the letters to their immediate right
    new_pair = ''
    if row1 == row2:
        new_pair += table[row1][(col1 + 1) % 5]
        new_pair += table[row2][(col2 + 1) % 5]
    else:
        new_pair = pair
    return new_pair

## The function playfairRuleThree(pair,table) checks to see if the two letters 
## in the input bigram appear on the same column of the table. If the two 
## letters are in the same column, they should be replaced with the letters 
## immediately below. This may require the letters in the bottom row to wrap
## around to the top row. Otherwise, it will return the original pair.

def playfairRuleThree(pair, table):
    a, b = pair[0], pair[1]
    a_row, a_col = None, None
    b_row, b_col = None, None
    
    # Find the row and column of each letter in the pair
    for i, row in enumerate(table):
        if a in row:
            a_row, a_col = i, row.index(a)
        if b in row:
            b_row, b_col = i, row.index(b)
    
    # If the letters are in the same column, replace them with the letters below
    if a_col == b_col:
        new_a = table[(a_row + 1) % 5][a_col]
        new_b = table[(b_row + 1) % 5][b_col]
        return new_a + new_b
    
    # Otherwise, return the original pair
    else:
        return pair

## The function playfairRule(pair,table) takes two inputs. It finds the 
## coordinates of the two letters in the table to check if they are both in 
## different rows and columns. These letters should be replaced by the 
## characters in the two corners of the rectangle, and should begin with the 
## character in the same row as the previous first character. The column 
## positions should be swapped, while the row positions remain the same.

def playfairRuleFour(pair, table):
    # Find the coordinates of the two letters in the table
    row1, col1 = None, None
    row2, col2 = None, None
    for i in range(5):
        for j in range(5):
            if table[i][j] == pair[0]:
                row1, col1 = i, j
            elif table[i][j] == pair[1]:
                row2, col2 = i, j
    if row1 != row2 and col1 != col2:
        # Replace the two letters with the other two corners of the rectangle
        new_pair = ''
        new_pair += table[row1][col2]
        new_pair += table[row2][col1]
        return new_pair
    return pair

## The encrypt function exists to call the previous four rules on one of the 
## bigrams that were retrieved from the splitString() function. The rules
## are called in the 3-6 order and the output from each function should be used 
## as input to each subsequent function. The variable result is assigned to the 
## four rules and it is returned.

def encrypt(pair, table):
    result = playfairRuleOne(pair)
    result = playfairRuleTwo(result, table)
    result = playfairRuleThree(result, table)
    result = playfairRuleFour(result, table)
    return result

## The joinPairs function takes a list of all encrypted bigrams and joins
## them together into a single ciphertext string which is returned.

def joinPairs(pairs_list):
    ciphertext = ''.join(pairs_list)
    return ciphertext

## The main() function is used to call the test cases for each of the 
## eight functions.

def main():
    '''
    Example main() function; can be commented out when running your
    tests
    '''
    table = createTable("i am entering a pass phrase")

    # createTable(phrase)
    # splitString(plaintext)
    testCreateTable()
    testSplitString()
    testPlayFairRuleOne()
    testPlayFairRuleTwo(table)
    testPlayFairRuleThree(table)
    testPlayFairRuleFour(table)
    testEncrypt(table)
    testJoinPairs()
    
    splitMessage = splitString("this is a test message")
    pairsList = []

    print(table) # printed for debugging purposes
    
    for pair in splitMessage:
        # Note: encrypt() should call the four rules
        pairsList.append(encrypt(pair, table))
    cipherText = joinPairs(pairsList)    
    
    print(cipherText) #printed as the encrypted output
    #output will be hjntntirnpginprnpm


###############################################################

# Here is where you will write your test case functions
    
## The test case for the function createTable() takes a key or passphrase and returns a
## 5*5 ciphertable of 25 unique characters. All of the characters must be 
## lowercase and there can not be any duplictae letters.

def testCreateTable():
    assert createTable("i am entering a pass phrase") == [['i', 'a', 'm', 'e', 'n'], ['t', 'r', 'g', 'p', 's'], ['h', 'b', 'c', 'd', 'f'], ['j', 'k', 'l', 'o', 'u'], ['v', 'w', 'x', 'y', 'z']]
    assert createTable("programming") == [['p', 'r', 'o', 'g', 'a'], ['m', 'i', 'n', 'b', 'c'], ['d', 'e', 'f', 'h', 'j'], ['k', 'l', 's', 't','u'], ['v', 'w', 'x', 'y', 'z']]
    assert createTable("enter phrase") == [['e','n','t','r','p'],['h','a','s','b','c'],['d','f','g','i','j'],['k','l','m','o','u'],['v','w','x','y','z']]
    assert createTable("passing") == [['p','a','s','i','n'],['g','b','c','d','e'],['f','h','j','k','l'],['m','o','r','t','u'],['v','w','x','y','z']]
    assert createTable("quiet") == [['u','i','e','t','a'],['b','c','d','f','g'],['h','j','k','l','m'],['n','o','p','r','s'],['v','w','x','y','z']]

## The test case for the function splitString() takes a plaintext string as input and 
## returns a list of bigrams which are two character pairs. If the plaintext
## string has an odd length, the 'x' character should be appended onto the last
## bigram. This can be seen in the first test case.

def testSplitString():
    assert splitString("this is my plaintext") == ["th", "is", "is", "my", "pl", "ai", "nt", "ex", "tx"]
    assert splitString("this is my code") == ["th", "is", "is", "my", "co", "de"]
    assert splitString("this is my file") == ["th", "is", "is", "my", "fi", "le"]
    assert splitString("this is my plaintext") == ["th", "is", "is", "my", "pl", "ai", "nt", "ex", "tx"]

## The test case for the function playFairRuleOne() uses the ciphertable to check the two 
## characters within the input bigram. The second letter will be replaced with
## an 'X' if the two letters are the same. The below assert statements
## have examples to check if this rule is applied.s

def testPlayFairRuleOne():
    assert playfairRuleOne("aa") == "ax"
    assert playfairRuleOne("xx") == "xz"
    assert playfairRuleOne("ab") == "ab"
    assert playfairRuleOne("cx") == "cx"
 
## The test case for the function playFairRuleTwo() checks if the two letters in the input
## bigram appear on the same row of the table. If they are, they should be 
## replaced with the letters to the immediate right. The below assert statements
## have examples to check if this rule is applied.

def testPlayFairRuleTwo(table):
    assert playfairRuleTwo("am", table) == "me"
    assert playfairRuleTwo("pt", table) == "sr"
    assert playfairRuleTwo("cf", table) == "dh"
    assert playfairRuleTwo("ed", table) == "ed"
    assert playfairRuleTwo("ma", table) == "em"
    
## The test case for the fucntion playFairRuleThree() checks to see if the two letters in the
## input bigram appear on the same column of the table. If they are, they should
## be replaced with the letters immediately below each. The below assert statements
## have examples to check if this rule is applied.

def testPlayFairRuleThree(table):
    assert playfairRuleThree("th", table) == "hj"
    assert playfairRuleThree("lg", table) == "xc"
    assert playfairRuleThree("tv", table) == "hi"
    assert playfairRuleThree("ax", table) == "ax"
    
## The test case for the function playFairRuleFour() checks to see if the two letters in the 
## input bigram are both in different rows and different columns. They should 
## be replaced by the characters in the other two corners of the rectangle, and 
## also begin with the character in the same row as the previous first character.
## The below assert statements have examples to check if this rule is applied.

def testPlayFairRuleFour(table):
    assert playfairRuleFour("fm", table) == "cn"
    assert playfairRuleFour("as", table) == "nr"
    assert playfairRuleFour("jw", table) == "kv"
    assert playfairRuleFour("do", table) == "do"
    assert playfairRuleFour("ir", table) == "at"
    
## The test case for the function encrypt() checks to see if the four rules are 
## called in the specific order. The output from each function should be used
## as input to each subsequent function. 
def testEncrypt(table):
    #print(encrypt("fr", table))
    assert encrypt("fr", table) == "bs"
    assert encrypt("ub", table) == "kf"
    assert encrypt("zk", table) == "wu"
    assert encrypt("zk", table) == "wu"
    assert encrypt("ma", table) == "em"

## The test case for the function joinPairs() checks to see if the list of all 
## the encrypted bigrams and joins them together into a single ciphertext string.

def testJoinPairs():
    assert joinPairs(["aa","ax"]) == "aaax"
    assert joinPairs(["zz","zk"]) == "zzzk"
    assert joinPairs(["ab","ax"]) == "abax"
    assert joinPairs(["ot","sk"]) == "otsk"
    












###############################################################    
    
if __name__ == "__main__":
    main()        