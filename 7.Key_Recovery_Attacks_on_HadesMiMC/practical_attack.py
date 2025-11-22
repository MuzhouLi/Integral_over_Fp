import random, sys

p=int(sys.argv[1])

d=int(sys.argv[2])

n=int(sys.argv[3])

s=int(sys.argv[4])

R1=int(sys.argv[5])
R2=int(sys.argv[6])
R3=int(sys.argv[7])

matrix=[[random.randint(1, p - 1) for i in range(n)] for j in range(n)]

round_key=[[random.randint(0, p - 1) for i in range(n)] for r in range(R1+R2+R3+1+1)]

right_key=[]
for i in range(n):
	right_key.append( round_key[R1+R2+R3+1][i] )

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
	
	#Key Recovery Round
	for i in range(n):
		tmp[i]=( (plaintext[i])**d )%p
		plaintext[i]=( tmp[i] + round_key[1+R1+R2+R3][i] )%p

	return plaintext

Sbox_Inv=[0 for x in range(p)]
Sbox=[( x**d )%p for x in range(p)]

for x in range(p):
	Sbox_Inv[Sbox[x]]=x

fixed_x = [ random.randint(0, p - 1) for i in range(n-s)]

V=[[0 for x in range(p)] for i in range(n)]

if s==2:
	for x_0 in range(p):
		print(x_0)
		for x_1 in range(p):
			plaintext=[x_0,x_1]+fixed_x
			ciphertext=[0 for i in range(n)]
			ciphertext=Enc(plaintext,round_key)
			
			for i in range(n):
				V[i][ ciphertext[i] ]+=1

elif s==3:
	for x_0 in range(p):
		print(x_0)
		for x_1 in range(p):
			for x_2 in range(p):
				plaintext=[x_0,x_1,x_2]+fixed_x
				ciphertext=[0 for i in range(n)]
				ciphertext=Enc(plaintext,round_key)
				
				for i in range(n):
					V[i][ ciphertext[i] ]+=1
else:
	print("wrong args")
	sys.exit(0)

for i in range(n):
	for guessed_rk in range(p):
		sum=0
		for possible_x in range(p):
			tmpv=Sbox_Inv[ (possible_x-guessed_rk+p)%p ]
			sum+=tmpv*V[i][possible_x]
			sum%=p
			
		if sum==0:			
			if guessed_rk==right_key[i]:
				print("possible rk_"+str(i)+"="+str(guessed_rk)+" : same as right key")
		