import sys, math, os, random

p=int(sys.argv[1])

d=int(sys.argv[2])

n=int(sys.argv[3])

s=int(sys.argv[4])#Only traverse left most s blocks, since Dis_Round can be added by (n-s) rounds. 

R=int(sys.argv[5])


def Enc(plaintext,ciphertext):
	for round in range(R):
		ciphertext[n-1]=plaintext[0]
		tmpV=(plaintext[0]+round_key[round])**d
		tmpV%=p
		for j in range(n-1):
			ciphertext[j]=(plaintext[j+1]+tmpV)%p
		for j in range(n):
			plaintext[j]=ciphertext[j]

total_c=1000
counter=0
for t in range(total_c):
	
	round_key=[random.randint(1, p - 1) for r in range(R)]
	
	if R>n:
		fixed_x=[]
		for i in range(n-s):
			go=True
			while go:
				thisx=random.randint(1, p - 1)
				if (thisx+round_key[i+s])%p!=0:
					go=False
					fixed_x.append(thisx)
				else:
					go=True
	else:
		fixed_x = [ random.randint(1, p - 1) for i in range(n-s)]
	
	if s==1:
		sum=[0 for i in range(n)]
		for x_0 in range(p):
			plaintext=[x_0]+fixed_x
			ciphertext=[0 for i in range(n)]
			Enc(plaintext,ciphertext)
			
			for i in range(n):
				sum[i]+=plaintext[i]
				sum[i]%=p
	
	if s==2:
		sum=[0 for i in range(n)]
		for x_0 in range(p):
			#print(x_0)
			for x_1 in range(p):
				plaintext=[x_0,x_1]+fixed_x
				ciphertext=[0 for i in range(n)]
				Enc(plaintext,ciphertext)
				
				for i in range(n):
					sum[i]+=plaintext[i]
					sum[i]%=p
		
	if s==3:
		sum=[0 for i in range(n)]
		for x_0 in range(p):
			#print(x_0)
			for x_1 in range(p):
				for x_2 in range(p):
					plaintext=[x_0,x_1,x_2]+fixed_x
					ciphertext=[0 for i in range(n)]
					Enc(plaintext,ciphertext)
					
					for i in range(n):
						sum[i]+=plaintext[i]
						sum[i]%=p
		
	
	
	#print(sum)
	sum_this=0
	for i in range(1,n):
		sum_this+=sum[i]
	sum_this-=(n-2)*sum[0]
	sum_this%=p
	if sum_this==0:
		allzero=True
	else:
		allzero=False
	print(t,sum_this,allzero,counter)
	#print(round_key)
	#print(fixed_x)
	#print()
	
	if allzero:
		counter+=1

print()
print("percent : ",counter/total_c*100,"%")
















