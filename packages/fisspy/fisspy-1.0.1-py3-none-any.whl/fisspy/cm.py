from __future__ import absolute_import, print_function, division

import numpy as np
from matplotlib.colors import LinearSegmentedColormap,ListedColormap
import sys

__author__ = "Juhyeong Kang "
__email__ = "jhkang@astro.snu.ac.kr"

    
def create_cdict(r, g, b):
    i = np.linspace(0, 1, 256)

    cdict = dict(
        (name, list(zip(i, el / 255.0, el / 255.0)))
        for el, name in [(r, 'red'), (g, 'green'), (b, 'blue')]
    )
    return cdict 
   


def hac(r=False):
     
    hr=np.array([0, 0, 1, 2, 3, 4, 4, 6, 6, 7, 8, 9, 10, 10, 12, 12, 13, 14, 15,
                 16, 16, 18, 18, 19, 20, 21, 22, 23, 24, 25, 25, 26, 27, 28, 29,
                 30, 31, 31, 33, 33, 34, 35, 36, 37, 37, 39, 39, 40, 41, 42, 43,
                 43, 45, 45, 46, 47, 48, 49, 50, 51, 51, 52, 53, 54, 55, 56, 57,
                 58, 58, 59, 60, 61, 62, 63, 64, 64, 66, 66, 67, 68, 69, 70, 70,
                 72, 72, 73, 74, 75, 76, 76, 78, 78, 79, 80, 81, 82, 83, 84, 84,
                 86, 87, 88, 89, 91, 92, 93, 94, 96, 97, 98, 99, 100, 102, 102,
                 104, 105, 106, 107, 108, 110, 111, 112, 113, 115, 116, 117, 118,
                 120, 121, 121, 123, 124, 125, 126, 128, 129, 130, 131, 132, 134,
                 135, 136, 137, 139, 139, 141, 142, 143, 144, 145, 147, 148, 149,
                 150, 152, 153, 154, 155, 156, 158, 158, 160, 161, 162, 163, 165,
                 166, 167, 168, 169, 171, 172, 173, 174, 176, 176, 178, 178, 179,
                 179, 179, 180, 180, 180, 181, 181, 181, 182, 182, 182, 183, 183,
                 183, 184, 186, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197,
                 198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 209, 210, 212,
                 213, 214, 215, 216, 217, 218, 219, 221, 222, 223, 224, 225, 226,
                 227, 228, 230, 231, 232, 233, 234, 235, 237, 238, 239, 240, 241,
                 242, 243, 244, 245, 247, 248, 249, 250, 251, 252, 253, 255])
                  
    hg=np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4,
                 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8,
                 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12,
                 12, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15,
                 15, 15, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 18, 18, 18, 18,
                 18, 19, 19, 19, 20, 20, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26,
                 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 33, 34, 36, 38, 39,
                 41, 43, 44, 46, 47, 49, 51, 53, 54, 56, 58, 59, 61, 62, 64, 66,
                 67, 69, 71, 73, 74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 91, 92,
                 94, 96, 97, 99, 101, 102, 104, 106, 107, 109, 110, 112, 114, 116,
                 117, 119, 121, 122, 124, 125, 127, 129, 130, 132, 134, 136, 137,
                 138, 140, 142, 144, 145, 147, 149, 150, 152, 153, 155, 157, 158,
                 160, 162, 164, 165, 166, 168, 170, 172, 173, 175, 177, 179, 180,
                 181, 183, 185, 187, 188, 190, 192, 193, 195, 196, 198, 200, 201,
                 203, 205, 207, 208, 210, 211, 213, 215, 216, 218, 220, 221, 223,
                 225, 226, 228, 229, 231, 233, 235, 236, 238, 240, 241, 243, 244,
                 246, 248, 250, 251, 253, 255])

    hb=np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5,
                 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
                 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15,
                 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19, 19,
                 19, 20, 20, 20, 20, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 23,
                 24, 24, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 28, 28,
                 28, 28, 29, 29, 29, 29, 30, 30, 30, 30, 31, 31, 31, 32, 32, 32,
                 32, 33, 33, 33, 33, 34, 34, 34, 35, 35, 35, 35, 36, 36, 36, 36,
                 37, 37, 37, 38, 38, 38, 38, 39, 39, 39, 39, 40, 40, 40, 41, 41,
                 41, 41, 42, 42, 42, 42, 43, 43, 43, 44, 44, 44, 44, 45, 45, 45,
                 45, 46, 46, 46, 47, 47, 47, 47, 48, 48, 48, 48, 49, 50, 51, 52,
                 53, 54, 55, 56, 57, 59, 62, 65, 68, 71, 74, 78, 81, 84, 87, 90,
                 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 130,
                 133, 136, 138, 141, 144, 148, 151, 154, 157, 160, 163, 166, 169,
                 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 203, 206, 209,
                 212, 215, 217, 221, 224, 227, 230, 233, 236, 239, 242, 245, 248,
                 251, 255])
    
    hadic=create_cdict(hr,hg,hb)
    hardic=create_cdict(hr[::-1],hg[::-1],hb[::-1])
    if r:
        return LinearSegmentedColormap('mytables',hardic)
    else:
        return LinearSegmentedColormap('mytables',hadic)

def cac(r=False):
    cr=np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5,
                 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11,
                 11, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16,
                 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19, 19, 19, 20, 20, 20,
                 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 24, 24, 24, 24, 25, 25,
                 25, 26, 26, 26, 26, 27, 27, 27, 28, 28, 30, 31, 32, 34, 35, 36,
                 37, 39, 40, 41, 42, 43, 45, 46, 47, 49, 50, 51, 53, 53, 55, 56,
                 57, 59, 60, 61, 63, 64, 65, 67, 67, 69, 70, 71, 73, 74, 75, 76,
                 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 92, 92, 94, 95, 96,
                 98, 99, 100, 102, 103, 104, 106, 106, 108, 109, 110, 112, 113,
                 114, 115, 117, 118, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                 130, 130, 132, 133, 133, 135, 136, 136, 138, 138, 139, 141, 141,
                 142, 144, 146, 148, 149, 151, 153, 155, 157, 158, 160, 162, 164,
                 166, 167, 169, 171, 172, 174, 176, 178, 180, 181, 183, 185, 187,
                 189, 190, 192, 194, 196, 198, 199, 201, 203, 204, 206, 208, 210,
                 212, 213, 215, 217, 219, 221, 222, 224, 226, 228, 230, 232, 233,
                 235, 236, 238, 240, 242, 244, 245, 247, 249, 251, 253, 255])
    
    cg=np.array([0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10, 11,
                 12, 12, 13, 13, 14, 15, 15, 16, 16, 17, 18, 18, 19, 19, 20, 21,
                 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 28, 29, 30, 30,
                 31, 31, 32, 33, 33, 34, 34, 35, 36, 36, 37, 37, 38, 39, 39, 40,
                 40, 41, 42, 42, 43, 43, 44, 45, 45, 46, 46, 47, 48, 48, 49, 49,
                 50, 51, 51, 52, 52, 53, 54, 54, 55, 55, 56, 57, 57, 58, 59, 60,
                 61, 62, 63, 64, 65, 66, 67, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                 76, 77, 78, 78, 79, 81, 82, 83, 84, 86, 87, 88, 90, 91, 92, 94,
                 95, 96, 97, 99, 100, 101, 103, 104, 105, 107, 108, 109, 110, 112,
                 113, 114, 116, 117, 118, 120, 121, 122, 124, 125, 126, 127, 129,
                 130, 131, 133, 134, 135, 137, 138, 139, 140, 142, 143, 144, 146,
                 147, 148, 150, 151, 152, 153, 155, 156, 157, 159, 160, 161, 162,
                 164, 165, 166, 168, 169, 170, 172, 173, 174, 175, 177, 178, 179,
                 181, 182, 183, 185, 186, 187, 188, 190, 191, 192, 194, 195, 196,
                 197, 199, 200, 201, 203, 204, 205, 207, 208, 209, 210, 212, 213,
                 214, 216, 217, 218, 220, 221, 222, 223, 225, 226, 227, 229, 230,
                 231, 232, 234, 235, 236, 238, 239, 240, 242, 243, 244, 245, 247,
                 248, 249, 251, 252, 253, 255])
    
    cb=np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5,
                 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10,
                 10, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14,
                 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19,
                 19, 19, 20, 20, 20, 20, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23,
                 23, 24, 24, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 28,
                 28, 28, 28, 29, 29, 29, 29, 30, 30, 30, 30, 31, 31, 31, 32, 32,
                 32, 32, 33, 33, 33, 33, 34, 34, 34, 35, 35, 35, 35, 36, 36, 36,
                 36, 37, 37, 37, 38, 38, 38, 38, 39, 39, 39, 39, 40, 40, 40, 41,
                 41, 41, 41, 42, 42, 42, 42, 43, 43, 43, 44, 44, 44, 44, 45, 45,
                 45, 45, 46, 46, 46, 47, 47, 47, 47, 48, 48, 48, 48, 50, 53, 55,
                 57, 60, 62, 65, 67, 69, 72, 74, 77, 80, 83, 86, 89, 92, 95, 97,
                 100, 103, 106, 109, 111, 115, 117, 120, 123, 126, 129, 131, 135,
                 137, 140, 143, 146, 149, 151, 154, 157, 160, 163, 166, 169, 172,
                 174, 177, 180, 183, 186, 188, 192, 194, 197, 200, 203, 206, 208,
                 212, 214, 217, 220, 223, 226, 228, 231, 234, 237, 240, 243, 246,
                 249, 251, 255])
    
    cadic=create_cdict(cr,cg,cb)
    cardic=create_cdict(cr[::-1],cg[::-1],cb[::-1])
    if r:
        return LinearSegmentedColormap('mytables',cardic)
    else:
        return LinearSegmentedColormap('mytables',cadic)

def nac(r= False):
    nr=np.array([0, 0, 0, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 8, 9,
                 9, 10, 10, 11, 12, 12, 13, 13, 14, 15, 16,
                 16, 17, 18, 18, 19, 19, 20, 21, 22, 22, 23,
                 23, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30,
                 31, 31, 32, 32, 33, 34, 35, 35, 36, 36, 37,
                 38, 38, 39, 40, 40, 41, 42, 42, 43, 44, 44,
                 45, 45, 46, 47, 48, 48, 49, 49, 50, 51, 51,
                 52, 53, 54, 54, 55, 55, 56, 57, 57, 58, 58,
                 59, 60, 61, 61, 62, 63, 63, 65, 66, 68, 69,
                 71, 72, 73, 75, 76, 77, 79, 80, 81, 83, 84,
                 86, 87, 89, 90, 91, 93, 94, 95, 97, 98, 99,
                 101, 102, 104, 105, 106, 108, 109, 111, 112,
                 113, 115, 116, 117, 119, 120, 121, 123, 124,
                 126, 127, 129, 130, 131, 133, 134, 135, 137,
                 138, 139, 141, 142, 144, 145, 146, 148, 149,
                 151, 152, 153, 155, 156, 157, 158, 160, 162,
                 163, 164, 166, 167, 169, 170, 171, 172, 173,
                 174, 174, 175, 176, 176, 177, 178, 179, 180,
                 180, 181, 182, 182, 183, 184, 185, 187, 187,
                 189, 190, 191, 192, 193, 194, 196, 197, 198,
                 199, 200, 201, 202, 203, 204, 206, 207, 208,
                 209, 210, 211, 213, 213, 215, 216, 217, 218,
                 219, 220, 222, 222, 224, 225, 226, 227, 228,
                 229, 231, 232, 233, 234, 235, 236, 237, 239,
                 240, 241, 242, 243, 244, 245, 246, 248, 248,
                 250, 251, 252, 253, 255])
                  
    ng=np.array([0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6,
                 6, 7, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12,
                 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17,
                 17, 18, 18, 18, 19, 19, 20, 20, 21, 21, 22,
                 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27,
                 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 31,
                 32, 32, 33, 33, 34, 34, 35, 35, 36, 36, 36,
                 37, 37, 38, 38, 39, 39, 40, 40, 40, 41, 41,
                 42, 42, 43, 43, 44, 45, 45, 46, 46, 47, 48,
                 48, 49, 49, 50, 51, 51, 52, 53, 53, 54, 54,
                 55, 56, 56, 57, 57, 59, 60, 62, 63, 65, 66,
                 68, 69, 71, 72, 73, 75, 76, 78, 79, 81, 82,
                 84, 85, 86, 88, 89, 91, 92, 94, 95, 97, 98,
                 99, 101, 102, 104, 105, 107, 108, 110, 111,
                 113, 114, 116, 117, 119, 120, 122, 123, 124,
                 126, 127, 129, 130, 132, 133, 135, 136, 137,
                 139, 140, 142, 143, 145, 146, 148, 149, 150,
                 152, 154, 155, 157, 158, 160, 161, 163, 164,
                 165, 167, 168, 170, 171, 173, 174, 176, 177,
                 178, 180, 181, 183, 184, 186, 187, 189, 190,
                 191, 193, 194, 196, 197, 199, 200, 202, 203,
                 205, 206, 208, 209, 211, 212, 214, 215, 216,
                 218, 219, 221, 222, 224, 225, 227, 228, 229,
                 231, 232, 234, 235, 237, 238, 240, 241, 242,
                 244, 246, 247, 249, 250, 252, 253, 255])

    nb=np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
                 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5,
                 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8,
                 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10,
                 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11,
                 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13,
                 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14,
                 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16,
                 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 18, 18,
                 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19,
                 19, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21,
                 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 23,
                 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 25,
                 27, 29, 30, 32, 34, 36, 37, 39, 42, 45, 48, 52,
                 55, 58, 62, 65, 69, 72, 75, 79, 82, 85, 88, 92,
                 95, 98, 102, 105, 108, 111, 115, 118, 122, 125,
                 128, 131, 134, 138, 141, 145, 148, 151, 155, 158,
                 161, 165, 168, 171, 174, 178, 181, 184, 188, 191,
                 194, 198, 201, 205, 208, 211, 214, 218, 221, 224,
                 228, 231, 234, 237, 241, 244, 248, 251, 255])
    
    nadic=create_cdict(nr,ng,nb)
    nardic=create_cdict(nr[::-1],ng[::-1],nb[::-1])
    if r:
        return LinearSegmentedColormap('mytables',nardic)
    else:
        return LinearSegmentedColormap('mytables',nadic)

def fec(r= False):
    
    fr=np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5,
                 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11,
                 11, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16,
                 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19, 19, 19, 20, 20, 20,
                 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 24, 24, 24, 24, 25, 25,
                 25, 26, 26, 26, 26, 27, 27, 27, 28, 28, 30, 31, 32, 34, 35, 36,
                 37, 39, 40, 41, 42, 43, 45, 46, 47, 49, 50, 51, 53, 53, 55, 56,
                 57, 59, 60, 61, 63, 64, 65, 67, 67, 69, 70, 71, 73, 74, 75, 76,
                 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 92, 92, 94, 95, 96,
                 98, 99, 100, 102, 103, 104, 106, 106, 108, 109, 110, 112, 113,
                 114, 115, 117, 118, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                 130, 130, 132, 133, 133, 135, 136, 136, 138, 138, 139, 141, 141,
                 142, 144, 146, 148, 149, 151, 153, 155, 157, 158, 160, 162, 164,
                 166, 167, 169, 171, 172, 174, 176, 178, 180, 181, 183, 185, 187,
                 189, 190, 192, 194, 196, 198, 199, 201, 203, 204, 206, 208, 210,
                 212, 213, 215, 217, 219, 221, 222, 224, 226, 228, 230, 232, 233,
                 235, 236, 238, 240, 242, 244, 245, 247, 249, 251, 253, 255])
    
    fg=np.array([0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10, 11,
                 12, 12, 13, 13, 14, 15, 15, 16, 16, 17, 18, 18, 19, 19, 20, 21,
                 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 28, 29, 30, 30,
                 31, 31, 32, 33, 33, 34, 34, 35, 36, 36, 37, 37, 38, 39, 39, 40,
                 40, 41, 42, 42, 43, 43, 44, 45, 45, 46, 46, 47, 48, 48, 49, 49,
                 50, 51, 51, 52, 52, 53, 54, 54, 55, 55, 56, 57, 57, 58, 59, 60,
                 61, 62, 63, 64, 65, 66, 67, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                 76, 77, 78, 78, 79, 81, 82, 83, 84, 86, 87, 88, 90, 91, 92, 94,
                 95, 96, 97, 99, 100, 101, 103, 104, 105, 107, 108, 109, 110, 112,
                 113, 114, 116, 117, 118, 120, 121, 122, 124, 125, 126, 127, 129,
                 130, 131, 133, 134, 135, 137, 138, 139, 140, 142, 143, 144, 146,
                 147, 148, 150, 151, 152, 153, 155, 156, 157, 159, 160, 161, 162,
                 164, 165, 166, 168, 169, 170, 172, 173, 174, 175, 177, 178, 179,
                 181, 182, 183, 185, 186, 187, 188, 190, 191, 192, 194, 195, 196,
                 197, 199, 200, 201, 203, 204, 205, 207, 208, 209, 210, 212, 213,
                 214, 216, 217, 218, 220, 221, 222, 223, 225, 226, 227, 229, 230,
                 231, 232, 234, 235, 236, 238, 239, 240, 242, 243, 244, 245, 247,
                 248, 249, 251, 252, 253, 255])
    
    fb=np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5,
                 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10,
                 10, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14,
                 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19,
                 19, 19, 20, 20, 20, 20, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23,
                 23, 24, 24, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 28,
                 28, 28, 28, 29, 29, 29, 29, 30, 30, 30, 30, 31, 31, 31, 32, 32,
                 32, 32, 33, 33, 33, 33, 34, 34, 34, 35, 35, 35, 35, 36, 36, 36,
                 36, 37, 37, 37, 38, 38, 38, 38, 39, 39, 39, 39, 40, 40, 40, 41,
                 41, 41, 41, 42, 42, 42, 42, 43, 43, 43, 44, 44, 44, 44, 45, 45,
                 45, 45, 46, 46, 46, 47, 47, 47, 47, 48, 48, 48, 48, 50, 53, 55,
                 57, 60, 62, 65, 67, 69, 72, 74, 77, 80, 83, 86, 89, 92, 95, 97,
                 100, 103, 106, 109, 111, 115, 117, 120, 123, 126, 129, 131, 135,
                 137, 140, 143, 146, 149, 151, 154, 157, 160, 163, 166, 169, 172,
                 174, 177, 180, 183, 186, 188, 192, 194, 197, 200, 203, 206, 208,
                 212, 214, 217, 220, 223, 226, 228, 231, 234, 237, 240, 243, 246,
                 249, 251, 255])
    
    fedic=create_cdict(fb,fg,fr)
    ferdic=create_cdict(fb[::-1],fg[::-1],fr[::-1])
    if r:
        return LinearSegmentedColormap('mytables',ferdic)
    else:
        return LinearSegmentedColormap('mytables',fedic)

def allwhite():
    return ListedColormap(['w','w','w'])

def allblack():
    return ListedColormap(['k','k','k'])

setattr(sys.modules[__name__],'ca',cac())
setattr(sys.modules[__name__],'ca_r',cac(r=True))
setattr(sys.modules[__name__],'ha',hac())
setattr(sys.modules[__name__],'ha_r',hac(r=True))
setattr(sys.modules[__name__],'na',nac())
setattr(sys.modules[__name__],'na_r',nac(r=True))
setattr(sys.modules[__name__],'fe',fec())
setattr(sys.modules[__name__],'fe_r',fec(r=True))
setattr(sys.modules[__name__],'allwhite',allwhite())
setattr(sys.modules[__name__],'allblack',allblack())
