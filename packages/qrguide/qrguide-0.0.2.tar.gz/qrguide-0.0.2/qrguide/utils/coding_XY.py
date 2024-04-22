# For utility function on the conding system of editing events
# Still under active development (24/03/2023)

import numpy as np

def seq_encoder(i, j):
    """
    Quick function for encoding editing positions into Lindel-like code
    
    Parameters
    ----------
    i: int
        The first deleted position (row index)
    j: int
        The last deteted position (column index)
    
    Return
    ------
    RV: The Lindel-like code (dtype: str)

    Examples
    --------
    >>> seq_encoder(1, 7)
    '-1+9'
    """
    return '%d+%d' %(-i, i+j+1)


def seq_decoder(code, row_offset=-2, col_offset=-2, pamsite_shift=0):
    """
    Quick function without too much check for decoding Lindel-like
    code into matrix index

    Be careful with these entries (with default row_offset=2 & col_offset=2):

    * [40, 40]: deletion >= 38
    * [2, 40]:  insertion >= 3
    * [2, 0]:   insertion == 2
    * [2, 1]:   insertion == 1
    * [0, 34]:  (optional) an ordinary deletion but never happend in this dataset
    
    Parameters
    ----------
    code: str
        The Lindel-like code
    row_offset: int
        The offset of row index
    col_offset: int
        The offset of column index
    pamsite_shift:
        The shift of PAM site (not considerred yet)
        
    Return
    ------
    (i, j): the row and column index for start and stop position in deletion

    Examples
    --------
    >>> seq_decoder('-1+9')
    array([3, 9])
    """
    if code == '>38':
        # for deletion length > 38
        RV = [38, 38]
    elif code == '3':
        # for insertion length >= 3
        RV = [0, -3] # Note, -3 is reverse index
    else:
        _start, _len = code.split('+')
        if _len.isnumeric():
            RV = [-int(_start), int(_len) + int(_start) - 1]
        else:
            # for insertion
            RV = [0, -len(_len)]
            
    # ajust by considering offset
    RV = np.array(RV) - np.array([row_offset, col_offset])

    return RV



def X_maker(Refseq, cutsite=None, coding_style='int',
            base_coding={'A': 0, 'C': 1, 'G': 2, 'T': 3}):
    """Extract the sequence into QR-code matrix and one-hot matrices

    Parameters
    ----------
    Refseq: str
        A sequence of letters, as a string
    cutsite: int
        The cutsite; note this position is the redundant, 
        as the start of both seq1 and seq2 (X1 and X2)
    coding_style: str 
        The way to label nucleotide in QR_mat. 
        Default: int , Integar coding; optional : one_hot, which will result in multi channel
    base_coding: dict
        The dictionary for base coding, starting from zero.
        Default: {'A': 0, 'C': 1, 'G': 2, 'T': 3}.
        To cosider 'N': {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4}.

    Examples
    --------
    >>> X_maker('CGAATCG', cutsite=5)
    (array([[4., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 3.],
            [0., 2., 0.]]),
    array([[0., 0., 0., 1.],
            [1., 0., 0., 0.],
            [1., 0., 0., 0.],
            [0., 0., 1., 0.],
            [0., 1., 0., 0.]]),
    array([[0., 0., 0., 1.],
            [0., 1., 0., 0.],
            [0., 0., 1., 0.]]))
    """
        
    if cutsite is None:
        cutsite = int(len(Refseq) / 2)

    # import pandas as pd
    # X1_df = pd.get_dummies([x for x in Refseq[:cutsite]])
    # X2_df = pd.get_dummies([x for x in Refseq[cutsite:]])

    seq1 = Refseq[:cutsite][::-1]
    seq2 = Refseq[(cutsite-1):]

    N_bases = len(base_coding)

    QR_mat = np.zeros((len(seq1), len(seq2))) if coding_style == 'int' else np.zeros((len(seq1), len(seq2), N_bases))
    X1_mat = np.zeros((len(seq1), len(base_coding)))
    X2_mat = np.zeros((len(seq2), len(base_coding)))

    # one hot encoding sequence before and after cut site (both inclusive)
    for i in range(len(seq1)):
        X1_mat[i, base_coding[seq1[i]]] = 1
    for j in range(len(seq2)):
        X2_mat[j, base_coding[seq2[j]]] = 1

    # QR code for base match
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                # QR_mat[i, j] = 1
                if coding_style == 'int':
                    QR_mat[i, j] = 1 + base_coding[seq1[i]]
                elif coding_style == 'one_hot':
                    QR_mat[i, j, base_coding[seq1[i]]] = 1  
                else:
                    raise ValueError("Undefine coding style")

    return QR_mat, X1_mat, X2_mat
