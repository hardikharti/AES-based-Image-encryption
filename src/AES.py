import math
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt
import chaos #chaos file
from PIL import Image

#Reading the image

img = cv2.imread(r'C:\Users\hardi\Documents\GitHub\AES-based-Image-encryption\src\image.png',0)
m,n = img.shape
matrix=img
print("Shape of the matrix:",m,n)


def get_roundkeys():
  #round keys from chaos 
    keys = chaos.main()
    
    return keys
def left_cycle(N, count): 
    
    N = hex(int(N)).split('x')[-1] 
      
   
    S = ( bin(int(N, 16))[2:] ).zfill(32) 
      
     
    # rotate the string by a specific count 
      
    S = (S[int(count) : ] + S[0 : int(count)]) 
    return (int(S,2))

def right_cycle(N, count): 
    
    N = hex(int(N)).split('x')[-1] 
  
    S = ( bin(int(N, 16))[2:] ).zfill(32) 
     
    # rotate the string by a specific count 
    S = (S[16 - int(count) : ] + S[0 : 32 - int(count)]) 
    return (int(S,2))

          

def encrypt():
    keys = get_roundkeys()
    
    #adding round 0 key
    cipher = [[[] for __ in range(m) ] for _ in range(11)]

    for i in range(m):
        for j in range(n):
            cipher[0][i].append(keys[0][i][j] ^ matrix[i][j])
    #print(cipher[0])
    
    #rounds 1-9

    for i in range(1,10):
        sum=0
        for j in range(m):
                for k in range(n):
                    sum=sum+cipher[i-1][j][k]
        

       
        if i%2==0:
            #diffusion step
            diff_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    sum=sum-cipher[i-1][j][k]
                    v=math.floor((sum/pow(256,5)) * pow(10,10,256))
                    diff_state[j].append(cipher[i-1][j][k] ^ v)
                    if j==1 and k==1:
                        diff_state[j][k] = diff_state[j][k]^124

            #print(dif_state)
            
            #shift rows
            shiftrow_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    shiftrow_state[j].append(diff_state[j][(k+j)%n])
            #print(shiftrow_state)
            
            #linear transformation
            lin_state = []
            trans_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    lin_state.append(shiftrow_state[j][k])

            #print(lin_state)
            #Seperating 16 bytes into 4 groups of 4 bytes
            for k in range(0,m*n,16):
                j=k
                a=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                j+=4
                b=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
               
                j+=4
                c=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                j+=4
                d=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                #applying linear transformation operations 
                d1= left_cycle(d ^ left_cycle(c,3) ^ left_cycle(a,10),7)
                b1= left_cycle(left_cycle(a,13) ^ left_cycle(c,7) ^ b,1)
                a1= left_cycle(b1 ^ d1 ^left_cycle(a,13),5) 
                c1= left_cycle(right_cycle(b1,7) ^ c ^ d1,22)

                #converting back to 32 bit binary

                a1 = ( bin(a1)[2:] ).zfill(32)
                b1 = ( bin(b1)[2:] ).zfill(32)
                c1 = ( bin(c1)[2:] ).zfill(32)
                d1 = ( bin(d1)[2:] ).zfill(32)

            #putting the values back to linear state list
            for j in range(0,m*n,16):
                k=j
                lin_state[k]=int(a1[0:8],2) 
                lin_state[k+1]=int(a1[8:16],2) 
                lin_state[k+2]=int(a1[16:24],2) 
                lin_state[k+3]=int(a1[24:32],2)
                
                k+=4
                lin_state[k]=int(b1[0:8],2) 
                lin_state[k+1]=int(b1[8:16],2) 
                lin_state[k+2]=int(b1[16:24],2) 
                lin_state[k+3]=int(b1[24:32],2)
                
                k+=4
                lin_state[k]=int(c1[0:8],2) 
                lin_state[k+1]=int(c1[8:16],2) 
                lin_state[k+2]=int(c1[16:24],2) 
                lin_state[k+3]=int(c1[24:32],2)
                
                k+=4
                lin_state[k]=int(d1[0:8],2) 
                lin_state[k+1]=int(d1[8:16],2) 
                lin_state[k+2]=int(d1[16:24],2) 
                lin_state[k+3]=int(d1[24:32],2)
                #print(lin_state)            
            
            #Converting the list back to a matrix
            x=0
            for j in range(m):
                for k in range(n):
                    trans_state[j].append(lin_state[x])
                    x=x+1
                    
            #add roundkey
            roundkey = keys[i]  
            for j in range(m):
                for k in range(n):
                    cipher[i][j].append(roundkey[j][k] ^ trans_state[j][k])
            #print(cipher[i])

        else:
            #print(cipher[0][m-1][n-1])

            #diffusion step
            #print(sum)
            diff_state = [[0 for _ in range(n)] for _ in range(m)]
            for j in range(m-1,-1,-1):
                for k in range(n-1,-1,-1):
                    sum=sum-cipher[i-1][j][k]
                    v=math.floor(((sum/pow(256,5)) * pow(10,10))%256)
                    #print(v)
                    diff_state[j][k]=(cipher[i-1][j][k] ^ v)
                    if j==m and k==n:
                        diff_state[j][k] = diff_state[j][k]^124

            #print(diff_state)
            
            #shift rows
            
            shiftrow_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    #print((k+j)%n)
                    shiftrow_state[j].append(diff_state[j][(k+j)%n])
            #print(diff_state[1])
            #print(shiftrow_state[1])
            
            #linear transformation
            lin_state = []
            trans_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    lin_state.append(shiftrow_state[j][k])

            #print(lin_state)
            #Seperating 16 bytes into 4 groups of 4 bytes
            for k in range(0,m*n,16):
                j=k
                a=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                j+=4
                b=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
               
                j+=4
                c=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                j+=4
                d=((((lin_state[j])<<8) +(lin_state[j+1])<<8) +(lin_state[j+2])<<8) +(lin_state[j+3])
                
                #applying linear transformation operations 
                d1= left_cycle(d ^ left_cycle(c,3) ^ left_cycle(a,10),7)
                b1= left_cycle(left_cycle(a,13) ^ left_cycle(c,7) ^ b,1)
                a1= left_cycle(b1 ^ d1 ^left_cycle(a,13),5) 
                c1= left_cycle(right_cycle(b1,7) ^ c ^ d1,22)

                #converting back to 32 bit binary

                a1 = ( bin(a1)[2:] ).zfill(32)
                b1 = ( bin(b1)[2:] ).zfill(32)
                c1 = ( bin(c1)[2:] ).zfill(32)
                d1 = ( bin(d1)[2:] ).zfill(32)

            #putting the values back to linear state list
            for j in range(0,m*n,16):
                k=j
                lin_state[k]=int(a1[0:8],2) 
                lin_state[k+1]=int(a1[8:16],2) 
                lin_state[k+2]=int(a1[16:24],2) 
                lin_state[k+3]=int(a1[24:32],2)
                
                k+=4
                lin_state[k]=int(b1[0:8],2) 
                lin_state[k+1]=int(b1[8:16],2) 
                lin_state[k+2]=int(b1[16:24],2) 
                lin_state[k+3]=int(b1[24:32],2)
                
                k+=4
                lin_state[k]=int(c1[0:8],2) 
                lin_state[k+1]=int(c1[8:16],2) 
                lin_state[k+2]=int(c1[16:24],2) 
                lin_state[k+3]=int(c1[24:32],2)
                
                k+=4
                lin_state[k]=int(d1[0:8],2) 
                lin_state[k+1]=int(d1[8:16],2) 
                lin_state[k+2]=int(d1[16:24],2) 
                lin_state[k+3]=int(d1[24:32],2)
                #print(lin_state)            
            
            #Converting the list back to a matrix
            x=0
            for j in range(m):
                for k in range(n):
                    trans_state[j].append(lin_state[x])
                    x=x+1
                    
            
                    
            #add roundkey
            roundkey = keys[i]  
            for j in range(m):
                for k in range(n):
                    cipher[i][j].append(roundkey[j][k] ^ trans_state[j][k])
            #print(cipher[i])
        
    #round 10 
        
    #add roundkey
    roundkey = keys[10]  
    for j in range(m):
        for k in range(n):
            cipher[10][j].append(roundkey[j][k] ^ shiftrow_state[j][k])
    #print(cipher[10])
    im=np.zeros((m,n))
    #im=cipher[10]
    im = np.asarray(cipher[10])
    print("Encrypted matrix:")
    print(cipher[10])
    #converting the array to an encrypted image
    Image.fromarray(im).show()
   
    #print(cipher[10])






encrypt()

print("\n")