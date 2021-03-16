import numpy as np
import cv2
img = cv2.imread('hardik_1.png',0)
m,n = img.shape
arr = img

print(arr[0][0])

x1,y1,a1,b1 = 0.75,0.53,3.0,4.0
x2,y2,a2,b2 = 0.34,0.49,2.0,7.0

for i in range(0,1000):
    t = x1
    x1 =  (x1 + y1*a1) % 1.0
    y1 =  (b1*t + y1*(1+a1*b1)) % 1.0

    t=x2
    x2 = (x2 + y2*a2) % 1.0
    y2 = (b2*t + y2*(1+a2*b2)) % 1.0

    


p1,p2 = np.zeros(m*n,float) , np.zeros(m*n , float)
c=0



for i in range(0,m):
    for j in range(0,n):
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

print(p1)
print(p2)

N=16

r = np.zeros(N+2,int)

for i in range(0,N+2):
    r[i] = (int)(p1[i]*100000) % (m*n-max(m,n))

print(r)

u = np.zeros((N+2,n), int)
v = np.zeros((N+2,m), int)

for i in range(0,N+2):
    for j in range(0,n):
        u[i][j] = (int)(p1[r[i]+j] * pow(10,14)) % m

for i in range(0,N+2):
    for j in range(0,m):
        v[i][j] = (int)(p2[r[i]+j] * pow(10,14)) % n


K = np.array([arr]*(N+2) , int)

for i in range(0,N+2):
    for j in range(0,n):
        for k in range(0,m):
            c=(j+u[i][j])%n
            K[i][k][c] = arr[k][j] 

for i in range(0,N+2):
    for j in range(0,m):
        for k in range(0,n):
            K[i][j][ (k+v[i][j]) % n] = arr[j][k] 

