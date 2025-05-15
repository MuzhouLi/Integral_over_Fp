import random, sys

p=int(sys.argv[1])

d=int(sys.argv[2])

n=int(sys.argv[3])

s=int(sys.argv[4])

R1=int(sys.argv[5])
R2=int(sys.argv[6])
R3=int(sys.argv[7])

matrix=[[random.randint(1, p - 1) for i in range(n)] for j in range(n)]

round_key=[[random.randint(0, p - 1) for i in range(n)] for r in range(R1+R2+R3+1)]

def Enc(plaintext, round_key):
	tmp=[0 for i in range(n)]
	
	for i in range(n):
		plaintext[i]=( plaintext[i] + round_key[0][i] )%p
	
	for r in range(R1):
		for i in range(n):
			tmp[i]=( (plaintext[i])**d )%p
		for i in range(n):
			plaintext[i]=0
			for j in range(n):
				plaintext[i]+=matrix[i][j]*tmp[j]
				plaintext[i]%=p
			plaintext[i]=( plaintext[i] + round_key[r+1][i] )%p
	
	for r in range(R2):
		for i in range(n):
			if i==0:
				tmp[i]=( (plaintext[i])**d )%p
			else:
				tmp[i]=plaintext[i]
		for i in range(n):
			plaintext[i]=0
			for j in range(n):
				plaintext[i]+=matrix[i][j]*tmp[j]
				plaintext[i]%=p
			plaintext[i]=( plaintext[i] + round_key[r+1+R1][i] )%p
	
	for r in range(R3):
		for i in range(n):
			tmp[i]=( (plaintext[i])**d )%p
		for i in range(n):
			plaintext[i]=0
			for j in range(n):
				plaintext[i]+=matrix[i][j]*tmp[j]
				plaintext[i]%=p
			plaintext[i]=( plaintext[i] + round_key[r+1+R1+R2][i] )%p
	
	return plaintext

fixed_x = [ random.randint(0, p - 1) for i in range(n-s)]


if s==1:
	sum=[0 for i in range(n)]
	for x_0 in range(p):
		plaintext=[x_0]+fixed_x
		ciphertext=[0 for i in range(n)]
		ciphertext=Enc(plaintext,round_key)
		
		for i in range(n):
			sum[i]+=ciphertext[i]
			sum[i]%=p
	print(sum)

if s==2:
	sum=[0 for i in range(n)]
	for x_0 in range(p):
		print(x_0)
		for x_1 in range(p):
			plaintext=[x_0,x_1]+fixed_x
			ciphertext=[0 for i in range(n)]
			ciphertext=Enc(plaintext,round_key)
			
			for i in range(n):
				sum[i]+=ciphertext[i]
				sum[i]%=p
	print(sum)

if s==3:
	sum=[0 for i in range(n)]
	for x_0 in range(p):
		print(x_0)
		for x_1 in range(p):
			for x_2 in range(p):
				plaintext=[x_0,x_1,x_2]+fixed_x
				ciphertext=[0 for i in range(n)]
				ciphertext=Enc(plaintext,round_key)
				
				for i in range(n):
					sum[i]+=ciphertext[i]
					sum[i]%=p
	print(sum)