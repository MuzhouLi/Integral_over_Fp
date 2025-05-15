import sys, math, os
from sage.all import *

p=int(sys.argv[1])

d=int(sys.argv[2])

n=int(sys.argv[3])

s=int(sys.argv[4])#Only traverse left most s blocks, since Dis_Round can be added by (n-s) rounds.

R=int(sys.argv[5])

save_cvc=False

def int2binstr(int_v,len_v):
	tmpstr=""
	for i in range(len_v):
		cur_b=(int_v>>i)&0x1
		tmpstr=str( cur_b )+tmpstr
	tmpstr="0b"+tmpstr
	return tmpstr

def len_compute(i):
	j=math.ceil(i)
	if i-j==0:
		return j+1
	else:
		return j

WList=["" for round_index in range(R)]
ZList_BeforeS=["" for round_index in range(R)]
Output=[["" for i in range(n)] for round_index in range(R)]

xList=[var("x_"+str(i)+"_") for i in range(n)]
inList=[var("x_"+str(i)+"_") for i in range(n)]
outList=["" for i in range(n)]

for i in range(s,n):
	xList[i]=var("c_"+str(i))
	inList[i]=var("c_"+str(i))

for round_index in range(R):
	#print(inList)
	
	if round_index>0:
		for i in range(n):
			if "x_"+str(i)+"_" in str(inList[0]):
				tmp=inList[0]-xList[i]
				WList[round_index]=xList[i]+var("k_"+str(round_index))
				ZList_BeforeS[round_index]=var("W_"+str(round_index))+tmp
			else:
				if "c_"+str(i) in str(inList[0]):
					tmp=inList[0]-xList[i]
					WList[round_index]=var("k_"+str(round_index))
					ZList_BeforeS[round_index]=var("W_"+str(round_index))+tmp
	else:
		WList[round_index]=inList[0]+var("k_"+str(round_index))
		ZList_BeforeS[round_index]=var("W_"+str(round_index))

	thisz=var("Z_"+str(round_index))
	
	for i in range(n-1):
		outList[i]=thisz+inList[i+1]
	
	outList[n-1]=inList[0]
	
	for i in range(n):
		Output[round_index][i]=outList[i]
		inList[i]=outList[i]

#'''
print("=============== W ===============")
for round_index in range(R):
	print("W_"+str(round_index)+" = "+str(WList[round_index]))
print()

print("=============== Z ===============")
for round_index in range(R):
	print("Z_"+str(round_index)+" = ("+str(ZList_BeforeS[round_index])+")^d")
print()

'''
for round_index in range(R):
	print("=============== round "+str(round_index)+" ===============")
	
	for i in range(n):
		print("Y_"+str(round_index)+"_"+str(i)+" = "+str(Output[round_index][i]))
print()	
#'''

'''
which_Z=[[] for i in range(n)]

for i in range(n):
	tmpstr=str(Output[R-1][i]).split("+")
	#print(tmpstr)
	
	for ele in tmpstr:
		if "Z" in ele:
			which_Z[i].append( int(ele.replace(" ","").split("_")[1]) )
	print(which_Z[i])
print()
#'''

target_function=0
for i in range(1,n):
	target_function+=Output[R-1][i]
target_function-=(n-2)*Output[R-1][0]

print("target_function = "+str(target_function))
print()

for str_ele in str(target_function).replace("-","+").split("+"):
	if 'Z' in str_ele:
		if "*" in str_ele:
			this_ele=str_ele.split("*")[1]
		else:
			this_ele=str_ele
		
		targetR=int(this_ele.split("_")[1])+1
		
		print("targetR = ", targetR)
		print()
		
		print("python3 -u ZS_detect_GMiMC.py "+str(p)+" "+str(d)+" "+str(n)+" "+str(s)+" "+str(targetR)+" ")
		







	
