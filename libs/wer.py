#-*- coding: utf-8 -*-
#!/usr/bin/env python
# source: https://github.com/zszyellow/WER-in-python/blob/master/wer.py
# modified by Gabriel Culbertson

import sys
import numpy

from .tokenize import tokenize

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0: 
                d[0][j] = j
            elif j == 0: 
                d[i][0] = i
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d

def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0: 
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]

# def alignedPrint(list, r, h, result):
#     '''
#     This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
#     Attributes:
#         list   -> the list of steps.
#         r      -> the list of words produced by splitting reference sentence.
#         h      -> the list of words produced by splitting hypothesis sentence.
#         result -> the rate calculated based on edit distance.
#     '''
#     print "REF:",
#     for i in range(len(list)):
#         if list[i] == "i":
#             count = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count += 1
#             index = i - count
#             print " "*(len(h[index])),
#         elif list[i] == "s":
#             count1 = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count1 += 1
#             index1 = i - count1
#             count2 = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count2 += 1
#             index2 = i - count2
#             if len(r[index1]) < len(h[index2]):
#                 print r[index1] + " " * (len(h[index2])-len(r[index1])),
#             else:
#                 print r[index1],
#         else:
#             count = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count += 1
#             index = i - count
#             print r[index],
#     print
#     print "HYP:",
#     for i in range(len(list)):
#         if list[i] == "d":
#             count = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count += 1
#             index = i - count
#             print " " * (len(r[index])),
#         elif list[i] == "s":
#             count1 = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count1 += 1
#             index1 = i - count1
#             count2 = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count2 += 1
#             index2 = i - count2
#             if len(r[index1]) > len(h[index2]):
#                 print h[index2] + " " * (len(r[index1])-len(h[index2])),
#             else:
#                 print h[index2],
#         else:
#             count = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count += 1
#             index = i - count
#             print h[index],
#     print
#     print "EVA:",
#     for i in range(len(list)):
#         if list[i] == "d":
#             count = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count += 1
#             index = i - count
#             print "D" + " " * (len(r[index])-1),
#         elif list[i] == "i":
#             count = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count += 1
#             index = i - count
#             print "I" + " " * (len(h[index])-1),
#         elif list[i] == "s":
#             count1 = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count1 += 1
#             index1 = i - count1
#             count2 = 0
#             for j in range(i):
#                 if list[j] == "d":
#                     count2 += 1
#             index2 = i - count2
#             if len(r[index1]) > len(h[index2]):
#                 print "S" + " " * (len(r[index1])-1),
#             else:
#                 print "S" + " " * (len(h[index2])-1),
#         else:
#             count = 0
#             for j in range(i):
#                 if list[j] == "i":
#                     count += 1
#             index = i - count
#             print " " * (len(r[index])),
#     print
#     print "WER: " + result

def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """

    if isinstance(r, str):
        r = tokenize(r)
        # print(r)

    if isinstance(h, str):
        h = tokenize(h)
        # print(h)

    # build the matrix
    d = editDistance(r, h)
    result = float(d[len(r)][len(h)]) / len(r)
    return result

def clean_extra_words(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """

    if isinstance(r, str):
        r = tokenize(r)

    if isinstance(h, str):
        h = tokenize(h)

    # build the matrix
    d = editDistance(r, h)
    step_list = getStepList(r, h, d)
    # print(r, h)
    # print(len(step_list), len(h), len(r), step_list)

    out_words = []
    deletes = 0
    for i, op in enumerate(step_list):
        if op == 'i':
            pass
            # out_words.append('.')
        elif op == 'd':
            deletes += 1
        else:
            out_words.append(h[i - deletes])

        # if op == "d":
        #     count = 0
        #     for j in range(i):
        #         if step_list[j] == "i":
        #             count += 1
        #     index = i - count
        #     # out_words.append(h[index])
        #     out_words.append('d')
        # elif op == "s":
        #     count1 = 0
        #     for j in range(i):
        #         if step_list[j] == "i":
        #             count1 += 1
        #     index1 = i - count1
        #     count2 = 0
        #     for j in range(i):
        #         if step_list[j] == "d":
        #             count2 += 1
        #     index2 = i - count2
        #     out_words.append('s')
        #     # out_words.append(h[index])
        #     # if len(r[index1]) > len(h[index2]):
        #     #     out_words.append('.')
        #     #     # out_words.append(h[index])
        #     # else:
        #     #     out_words.append('.')
        #     #     # out_words.append(h[index])
        # else:
        #     count = 0
        #     for j in range(i):
        #         if step_list[j] == "d":
        #             count += 1
        #     index = i - count
        #     out_words.append('e')
        #     # out_words.append(h[index])

    # for i,op in enumerate(step_list):
    #     if step_list[i] == "i":
    #         count = 0
    #         for j in range(i):
    #             if step_list[j] == "d":
    #                 count += 1
    #         index = i - count
    #         out_words.append('i')
    #     elif step_list[i] == "s":
    #         count1 = 0
    #         for j in range(i):
    #             if step_list[j] == "i":
    #                 count1 += 1
    #         index1 = i - count1
    #         count2 = 0
    #         for j in range(i):
    #             if step_list[j] == "d":
    #                 count2 += 1
    #         index2 = i - count2
    #         # out_words.append('s')
    #     else:
    #         count = 0
    #         for j in range(i):
    #             if step_list[j] == "i":
    #                 count += 1
    #         index = i - count
    #         out_words.append('e')

    # print(len(h), h)
    # print(len(out_words), out_words)

    return ' '.join(out_words)

if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    r = file(filename1).read().split()
    h = file(filename2).read().split()
    wer(r, h)