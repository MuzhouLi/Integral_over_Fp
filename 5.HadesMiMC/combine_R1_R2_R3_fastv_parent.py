import sys, math, os
from sage.all import *

p=int(sys.argv[1])
Field=int(sys.argv[1])

d=int(sys.argv[2])
n=int(sys.argv[3])

s=int(sys.argv[4])

R1=int(sys.argv[5])
R2=int(sys.argv[6])
R3=int(sys.argv[7])

total_round=R1+R2+R3

if d**R1>p-1 or R2==0 or d**R3>p-1:
	print("RE Code only deal with (<=log(p-1,d))+(>=1)+(<=log(p-1,d)).")
	sys.exit(0)

K=PolynomialRing(GF(Field), 2*s+1,
			["y%d" % i for i in range( s )]+
			["A%d" % i for i in range( s+1 )],
			order="degrevlex",
			)

K_var=list(K.gens())

y_var=[K_var[w] for w in range(s)]
A_var=[K_var[s+w] for w in range(s+1)]

A_value={}
for i in range(s+1):
	A_value[ A_var[i] ]=1

eq_1=0
for i in range(s):
	eq_1+=A_var[i]*(y_var[i])**d
eq_1+=A_var[s]

eq_2=eq_1**(d**(R1-1))

eq_2_term=[]
for ele in eq_2.monomials():
	degree_list=[0 for i in range(s)]
	
	y_term=1
	dict_list={}
	for i in range(s):
		degree_list[i]=ele.degree(y_var[i])
		dict_list[ y_var[i] ]=degree_list[i]
		y_term*=(y_var[i])**(degree_list[i])
	
	#print(dict_list,eq_2.coefficient(dict_list))
	
	comb=eq_2.coefficient(dict_list).subs(A_value)
	
	eq_2_term.append( list(dict_list.values()) )
	
	#print(ele,degree_list,comb,y_term)
	
	#eq_2_term.append(comb*y_term)

for ele in eq_2_term:
	print("RE ",ele)
print("RE ")

str_eq_2_term=""
for ele in eq_2_term:
	for i in range(s):
		str_eq_2_term+=((str(ele[i]))+"_")
str_eq_2_term=str_eq_2_term[:-1]
print("RE ",str_eq_2_term)

len_eq_2_term=len(eq_2_term)

# call subparent code
para1=str(p)+" "+str(d)+" "+str(n)+" "+str(s)+" "+str(R1)+" "+str(R2)+" "+str(R3)+" "+str(len_eq_2_term)+" "+str_eq_2_term
para2=str(p)+"_"+str(d)+"_"+str(n)+"_"+str(s)+"_"+str(R1)+"_"+str(R2)+"_"+str(R3)+"_"+str(len_eq_2_term)+"_"

os.system("nohup python3 -u combine_R1_R2_R3_fastv_child.py "+para1+"> result_child_"+para2+".txt &")












