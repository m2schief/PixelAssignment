#Functions to create and use cost matrices for assignments
import random
random.seed(139381512)

import numpy as np
from scipy.optimize import linear_sum_assignment

def MatrixCost(m1: np.matrix, m2: np.matrix):
    '''
    Returns a square-difference cost matrix given two matrices of equal size
    with only one row of ints

    m1 values are the rows, m2 values are the columns
    '''
    arrSize = m1.shape[1]

    #Create nxn matrices; one with repeated rows, other with repeated columns
    m1_row = np.transpose(m1) * np.ones((1, arrSize), dtype=int)
    m2_col = np.ones((arrSize, 1), dtype=int) * m2

    #subtract and square for a square-diff cost matrix
    cost = np.square(m1_row - m2_col)

    return cost

def TupleMatrixCost(m1, m2):
    '''
    Returns a square-difference cost matrix given two lists of equal size 
    of tuples of ints

    m1 values are the rows, m2 values are the columns
    '''

    #split tuples into seperate lists, named for RGB image type
    rArray_1, gArray_1, bArray_1 = zip(*m1)
    rArray_2, gArray_2, bArray_2 = zip(*m2)

    #add costs between the values together for total cost
    costM = MatrixCost(np.matrix(rArray_1), np.matrix(rArray_2)) 
    + MatrixCost(np.matrix(gArray_1), np.matrix(gArray_2)) 
    + MatrixCost(np.matrix(bArray_1), np.matrix(bArray_2))

    #square root to represent cost as pixel distance
    costM = np.sqrt(costM)
    return costM

def AssignMatrix(row_pixels, cost_matrix):
    '''
    Creates a new array with the same data as row_pixels, designed to 
    optimize the cost_matrix
    '''

    #use the hungarian algorithm for an ideal matching O(n^3) 
    rowind, colind = linear_sum_assignment(cost_matrix)

    size = len(row_pixels)
    #create a python list with m2 arranged akin to m1
    sortedArray = [0] * size
    for i in range(size):
        sortedArray[colind[i]] = row_pixels[i]
    
    return sortedArray