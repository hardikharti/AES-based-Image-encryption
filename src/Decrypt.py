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

          

def decrypt():
    keys = get_roundkeys()
    
    #round 10 key
    decipher = [[[] for __ in range(m) ] for _ in range(11)]

    for i in range(m):
        for j in range(n):
            decipher[0][i].append(keys[10][i][j] ^ matrix[i][j])
    #print(decipher[0])
    
    #rounds 9-1

    for i in range(9,0,-1):
        sum=0
        for j in range(m):
                for k in range(n):
                    sum=sum+decipher[9-i][j][k]
        

       
        if i%2==0:
              
            
            
            #add roundkey
            key_state = [[] for _ in range(m)]
            roundkey = keys[i]  
            for j in range(m):
                for k in range(n):
                    key_state[j].append(roundkey[j][k] ^ decipher[9-i][j][k])
            #print(decipher[i])
            #print(decipher[0][m-1][n-1])

            #linear transformation
            lin_state = []
            trans_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    lin_state.append(key_state[j][k])

            #print(lin_state)

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
                a1= right_cycle(b ^ d ^ right_cycle(a,5),13) 
                c1= right_cycle(c,22) ^ d ^ left_cycle(b,7)
                b1= right_cycle(b,1) ^ right_cycle(a1,13) ^ right_cycle(c1,7)
                d1= right_cycle(d,7) ^ right_cycle(c1,3) ^ right_cycle(a1,10)


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
            
             
            #shift rows
            
            shiftrow_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    #print((k+j)%n)
                    shiftrow_state[j].append(trans_state[j][(k-j + n)%n])
            #print(diff_state[1])
            #print(shiftrow_state[1])

            #diffusion step
            #print(sum)
            diff_state = [[0 for _ in range(n)] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    sum=sum-decipher[9-i][j][k]
                    v=math.floor(((sum/pow(256,5)) * pow(10,10))%256)
                    #print(v)
                    diff_state[j][k]=(shiftrow_state[j][k] ^ v)
                    if j==m and k==n:
                        diff_state[j][k] = diff_state[j][k]^124
            
            for j in range(m):
                for k in range(n):
                    decipher[10-i][j].append(diff_state[j][k])
           

        else:
            #add roundkey
            key_state = [[] for _ in range(m)]
            roundkey = keys[i]  
            for j in range(m):
                for k in range(n):
                    key_state[j].append(roundkey[j][k] ^ decipher[9-i][j][k])
            #print(decipher[i])
            #print(decipher[0][m-1][n-1])

            #linear transformation
            lin_state = []
            trans_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    lin_state.append(key_state[j][k])

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
                a1= right_cycle(b ^ d ^ right_cycle(a,5),13) 
                c1= right_cycle(c,22) ^ d ^ left_cycle(b,7)
                b1= right_cycle(b,1) ^ right_cycle(a1,13) ^ right_cycle(c1,7)
                d1= right_cycle(d,7) ^ right_cycle(c1,3) ^ right_cycle(a1,10)

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
            
            #shift rows
            
            shiftrow_state = [[] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    #print((k+j)%n)
                    shiftrow_state[j].append(trans_state[j][(k-j + n)%n])
            #print(diff_state[1])
            #print(shiftrow_state[1])
                    

            #diffusion step
            #print(sum)
            diff_state = [[0 for _ in range(n)] for _ in range(m)]
            for j in range(m-1,-1,-1):
                for k in range(n-1,-1,-1):
                    sum=sum-decipher[9-i][j][k]
                    v=math.floor(((sum/pow(256,5)) * pow(10,10))%256)
                    #print(v)
                    diff_state[j][k]=(shiftrow_state[j][k] ^ v)
                    if j==m and k==n:
                        diff_state[j][k] = diff_state[j][k]^124
            
            for j in range(m):
                for k in range(n):
                    decipher[10-i][j].append(diff_state[j][k])

            #print(diff_state)

    #round 0 
        
    #add roundkey
    roundkey = keys[0]  
    for j in range(m):
        for k in range(n):
            decipher[10][j].append(roundkey[j][k] ^ decipher[9][j][k])
    #print(decipher[10])
    im=np.zeros((m,n))
    #im=decipher[10]
    im = np.asarray(decipher[10])
    print("Encrypted matrix:")
    print(decipher[10])
    #converting the array to an encrypted image
    Image.fromarray(im).show()
   
    #print(decipher[10])






decrypt()

print("\n")