import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt
from PIL import Image
#reading the image and storing it in an array
img = cv2.imread(r'C:\Users\hardi\Documents\GitHub\AES-based-Image-encryption\src\image.png',0)
m,n = img.shape
arr = img
#print(m,n)

#function to update the values in p1 and p2 arrays
def pinit(x1,x2,y1,y2,a1,a2,b1,b2,m,n,p1,p2):
    
    c=0

    for _ in range(0,m*n):
        
            s1,s2 = 0,0
            if(c%2 == 0 ):
                s1=x1
                s2=x2
            else:
                s1=y1
                s2=y2

            p1[c] = s1
            p2[c] = s2
            t = x1
            x1 =  (x1 + y1*a1) % 1.0
            y1 =  (b1*t + y1*(1+a1*b1)) % 1.0

            t=x2
            x2 = (x2 + y2*a2) % 1.0
            y2 = (b2*t + y2*(1+a2*b2)) % 1.0

            c=c+1   
   
    return x1,x2,y1,y2

#iterating through the initial randomness
def xyinit(x1,x2,y1,y2,a1,a2,b1,b2):
    for _ in range(0,1000):
        t = x1
        x1 =  (x1 + y1*a1) % 1.0
        y1 =  (b1*t + y1*(1+a1*b1)) % 1.0

        t=x2
        x2 = (x2 + y2*a2) % 1.0
        y2 = (b2*t + y2*(1+a2*b2)) % 1.0
    return x1,x2,y1,y2

#assigning values to be shifted in u and v lists
def uvinit(u,v,p1,p2,r,N,m,n):
    prod=pow(10,14)
    for i in range(0,N+2):
        for j in range(0,n):
            u[i][j] = (int)(p1[r[i]+j] * prod) % m

    for i in range(0,N+2):
        for j in range(0,m):
            v[i][j] = (int)(p2[r[i]+j] * prod) % n

    return u,v

#scrambling the image to generate keys
def kinit(K,u,v,p1,p2,r,N,m,n,arr):
    for i in range(0,N+2):
        for j in range(0,n):
            for k in range(0,m):
                c=(j+u[i][j])%n
                K[i][k][c] = arr[k][j] 

    for i in range(0,N+2):
        for j in range(0,m):
            for k in range(0,n):
                K[i][j][ (k+v[i][j]) % n] = arr[j][k] 
    return K


def main():
    

    #initializing the parameters for chaos map
    x1,y1,a1,b1 = 0.75,0.53,3.0,4.0
    x2,y2,a2,b2 = 0.34,0.49,2.0,7.0

    #iterationg for 1000 times just to come out of the buffer zone of chaos mapping
    x1,x2,y1,y2 = xyinit(x1,x2,y1,y2,a1,a2,b1,b2)

    #p1 and p2 are the 1-D chaos maps 
    p1,p2 = np.zeros(m*n,float) , np.zeros(m*n , float)
    x1,x2,y1,y2 = pinit(x1,x2,y1,y2,a1,a2,b1,b2,m,n,p1,p2)

    #N is the number of rounds
    N=10

    #r is the index from which values will be taken for scrambling the image for key generation
    r = np.zeros(N+2,int)
    for i in range(0,N+2):
        r[i] = (int)(p1[i]*100000) % (m*n-max(m,n))

    #u and v are arrays for scrambling the image to generate the key
    u = np.zeros((N+2,n), int)
    v = np.zeros((N+2,m), int)
    u,v=uvinit(u,v,p1,p2,r,N,m,n)

    #K is the key matrix where K[i] represents key for ith round
    K = np.array([arr]*(N+2) , int)
    K = kinit(K,u,v,p1,p2,r,N,m,n,arr)
    
    return K

main()
