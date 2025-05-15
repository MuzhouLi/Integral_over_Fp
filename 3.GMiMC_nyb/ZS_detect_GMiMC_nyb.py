import sys, math, os
from sage.all import *

p=int(sys.argv[1])

d=int(sys.argv[2])

n=int(sys.argv[3])

s=int(sys.argv[4])

R=int(sys.argv[5])

active_pos=[]

for j in range(s):
	active_pos.append( int(sys.argv[6+j]) )

if R<s:
	print("Already ZS.")
	sys.exit()

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

group_num=int(n/2)

WList=["" for round_index in range(group_num*R)]
ZList_BeforeS=["" for round_index in range(group_num*R)]
Output=[["" for i in range(n)] for round_index in range(R)]

xList=[var("x_"+str(i)+"_") for i in range(n)]
inList=[var("x_"+str(i)+"_") for i in range(n)]
outList=["" for i in range(n)]

for i in range(n):
	if i not in active_pos:
		xList[i]=var("c_"+str(i))
		inList[i]=var("c_"+str(i))

for round_index in range(R):
	print(round_index)
	#print(inList)
	
	for branch in range(group_num):
		W_index = group_num*round_index+branch
		left_branch_index = 2*branch+0
		right_branch_index = 2*branch+1
		
		for i in range(n):
			if "x_"+str(i)+"_" in str(inList[left_branch_index]):
				tmpV=inList[left_branch_index]-xList[i]
				WList[W_index] = xList[i]+var("k_"+str(W_index))
				ZList_BeforeS[W_index] = var("W_"+str(W_index))+tmpV
			else:
				if "c_"+str(i) in str(inList[left_branch_index]):
					tmpV=inList[left_branch_index]-xList[i]
					WList[W_index] = var("k_"+str(W_index))
					ZList_BeforeS[W_index] = var("W_"+str(W_index))+tmpV
	
	for branch in range(group_num):
		W_index = group_num*round_index+branch
		left_branch_index = 2*branch+0
		right_branch_index = 2*branch+1
		
		thisz = var("Z_"+str(W_index))
		
		outList[left_branch_index] = inList[left_branch_index]
		outList[right_branch_index] = inList[right_branch_index]+thisz
	
	for i in range(n-1):
		inList[i]=outList[i+1]
	inList[n-1]=outList[0]
	
	for i in range(n):
		Output[round_index][i]=inList[i]

#'''
print("=============== W ===============")
for round_index in range(group_num*R):
	print("W_"+str(round_index)+" = "+str(WList[round_index]))
	if (round_index+1)%group_num==0:
		print()
print()

print("=============== Z ===============")
for round_index in range(group_num*R):
	print("Z_"+str(round_index)+" = ("+str(ZList_BeforeS[round_index])+")^d")
	if (round_index+1)%group_num==0:
		print()
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

start_R=math.ceil( math.log(s*(p-1)-1,d) - 1 )

if start_R>=R:
	print("Already ZS.")
	sys.exit()
else:
	print("Start to detect with pos=",active_pos,".")
	print()

max_z_in_each=[0 for i in range(n)]
for i in range(n):
	this_out=str(Output[R-1][i])
	zarr=this_out.replace(" ","").split("+")
	thisz=[]
	for ele in zarr:
		if 'Z' in ele:
			thisz.append(int((ele.split("_"))[1]))
	print(i,thisz)
	
	max_z=thisz[0]
	if len(thisz)>=2:
		for ele in thisz:
			if ele>max_z:
				max_z=ele
	max_z_in_each[i]=max_z
min_i=0
min_z=max_z_in_each[0]
for i in range(1,n):
	if max_z_in_each[i]<min_z:
		min_z=max_z_in_each[i]
		min_i=i

tmpTargetZ=[min_z+i for i in range(group_num)]
print("Detecting ",tmpTargetZ)
print()

max_degree_z=[0 for _ in range(group_num*R)]
ori_max_degree_z=R
for round_index in range(group_num*R):
	max_degree_z[round_index]=ori_max_degree_z
	if (round_index+1)%group_num==0:
		ori_max_degree_z-=1
print("max_degree_z : ")
for round_index in range(R):
	for pos in range(group_num):
		print(max_degree_z[round_index*group_num+pos],end=" ")
	print()
print()

index_each_x={}
for w in active_pos:
	tmp_arr=[]
	for round_index in range(group_num*R):
		if str(xList[w]) in str(WList[round_index]):
			tmp_arr.append(round_index)
	index_each_x[w]=tmp_arr



def Comb_Cancel_T1(conds,m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len):
	f.write("ASSERT( "+conds+" => ("+m1_var+"_sum_m_its_aplusb_its_b="+int2binstr(p-1,len_sum_m)+") ); \n")
	f.write("\n")
	

def Comb_Cancel_T2(conds,m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len):
	len_diff=len_sum_m-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	f.write("ASSERT( "+conds+" => ")
	f.write("( IF ("+m1_var+"_sum_m_its_aplusb_its_b="+int2binstr(p-1,len_sum_m)+") THEN ")
	f.write("((BVLT( "+zero_add+m1_var+"_p_0 , "+m1_var+"_sum_m_radical )) OR ((BVGE( "+zero_add+m1_var+"_p_0 , "+m1_var+"_sum_m_radical )) AND (BVGE( "+m1_var+"_p_0 , "+int2binstr(2,each_len)+" )) AND (NOT("+m1_var+"_sum_m_radical="+int2binstr(0,len_sum_m)+")) AND (NOT("+m1_var+"_sum_m_radical="+zero_add+m1_var+"_p_0)) ))")
	f.write(" ELSE ")
	f.write("(BVGE( "+zero_add+m1_var+"_p_0 , "+m1_var+"_sum_m_radical ))")
	f.write(" ENDIF )")
	f.write(" ); \n")
	f.write("\n")
	
	
def Comb_Cancel_T3(conds,m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len):
	if 2**Fv1_var_len<len_L:
		max_L_Fv1=math.ceil( math.log(len_L,2) )
	else:
		max_L_Fv1=Fv1_var_len
	
	len_diff=max_L_Fv1-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
		
	len_diff=len_sum_m-Fv1_var_len
	if len_diff>0:
		zero_add2="0b"
		for j in range(len_diff):
			zero_add2+="0"
		zero_add2+="@"
	else:
		zero_add2=""
	
	len_diff=Fv1_var_len-len_sum_m
	if len_diff>0:
		zero_add3="0b"
		for j in range(len_diff):
			zero_add3+="0"
		zero_add3+="@"
	else:
		zero_add3=""
	
	f.write("ASSERT( "+conds+" => ")
	f.write("( IF (BVLE("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) THEN (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")) ELSE ( IF ("+m1_var+"_sum_m_its_aplusb_its_a = "+int2binstr(0,len_sum_m)+" ) THEN (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")) ELSE (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_modp_plus1 ,"+zero_add2+Fv1_var+")) ENDIF ) ENDIF )")
	f.write(" ); \n")
	f.write("\n")
	
	
def Comb_Cancel_T4(conds,m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len):
	if 2**Fv1_var_len<len_L:
		max_L_Fv1=math.ceil( math.log(len_L,2) )
	else:
		max_L_Fv1=Fv1_var_len
	
	len_diff=max_L_Fv1-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	len_diff=len_sum_m-Fv1_var_len
	if len_diff>0:
		zero_add2="0b"
		for j in range(len_diff):
			zero_add2+="0"
		zero_add2+="@"
	else:
		zero_add2=""
	
	len_diff=Fv1_var_len-len_sum_m
	if len_diff>0:
		zero_add3="0b"
		for j in range(len_diff):
			zero_add3+="0"
		zero_add3+="@"
	else:
		zero_add3=""
	
	#=>left is C_A_Fv
	tmp_cond_1="((BVLE("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")))"
	tmp_cond_2="((BVGT("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND ("+m1_var+"_sum_m_its_aplusb_its_a="+int2binstr(0,len_sum_m)+") AND (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")))"
	
	#=>left is 0
	tmp_cond_3="((BVLE("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND (BVLT("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")))"
	tmp_cond_4="((BVGT("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND ("+m1_var+"_sum_m_its_aplusb_its_a="+int2binstr(0,len_sum_m)+") AND (BVLT("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b ,"+zero_add2+Fv1_var+")))"
	tmp_cond_5="((BVGT("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND ("+m1_var+"_sum_m_its_aplusb_its_a="+int2binstr(1,len_sum_m)+") AND (BVLT("+zero_add3+m1_var+"_sum_m_its_aplusb_modp_plus1 ,"+zero_add2+Fv1_var+")))"
	tmp_cond_6="((BVGT("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND ("+m1_var+"_sum_m_its_aplusb_its_a="+int2binstr(1,len_sum_m)+") AND ("+m1_var+"_sum_m_its_aplusb_its_b ="+int2binstr(p-1,len_sum_m)+"))"
	
	#=>left is C_A+1_Fv
	tmp_cond_7="((BVGT("+int2binstr(len_L,max_L_Fv1)+","+zero_add+Fv1_var+")) AND ("+m1_var+"_sum_m_its_aplusb_its_a="+int2binstr(1,len_sum_m)+") AND (BVGE("+zero_add3+m1_var+"_sum_m_its_aplusb_modp_plus1 ,"+zero_add2+Fv1_var+")) AND (BVLE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(p-2,len_sum_m)+")))"
	
	len_diff=len_sum_m-each_len
	if len_diff>0:
		zero_add4="0b"
		for j in range(len_diff):
			zero_add4+="0"
		zero_add4+="@"
	else:
		zero_add4=""
	
	#=>right is 0
	tmp_cond_8="(BVLT( "+zero_add4+m1_var+"_p_0 , "+m1_var+"_sum_m_minusFv_radical ))"
	
	#=>right is C_m0_*
	tmp_cond_9="(BVGE( "+zero_add4+m1_var+"_p_0 , "+m1_var+"_sum_m_minusFv_radical ))"
	
	#=>C_A_Fv=1
	tmp_cond_10="("+m1_var+"_sum_m_its_aplusb_its_b="+int2binstr(1,len_sum_m)+")"
	tmp_cond_11="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(2,len_sum_m)+")) AND ("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b="+zero_add2+Fv1_var+"))"
	
	#=>C_A_Fv=A
	tmp_cond_12="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(2,len_sum_m)+")) AND ("+Fv1_var+"="+int2binstr(1,Fv1_var_len)+"))"
	tmp_cond_13="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(2,len_sum_m)+")) AND ("+zero_add3+m1_var+"_sum_m_its_aplusb_modp_minus1="+zero_add2+Fv1_var+"))"
	
	#=>C_m0_*=1
	tmp_cond_14="(BVLE("+m1_var+"_p_0,"+int2binstr(1,each_len)+"))"
	tmp_cond_15="((BVGE("+m1_var+"_p_0,"+int2binstr(2,each_len)+")) AND ("+m1_var+"_sum_m_minusFv_radical="+int2binstr(0,len_sum_m)+"))"
	tmp_cond_16="((BVGE("+m1_var+"_p_0,"+int2binstr(2,each_len)+")) AND ("+m1_var+"_sum_m_minusFv_radical="+zero_add4+m1_var+"_p_0))"
	
	#=>C_m0_*=m0
	tmp_cond_17="((BVGE("+m1_var+"_p_0,"+int2binstr(2,each_len)+")) AND ("+m1_var+"_sum_m_minusFv_radical="+int2binstr(1,len_sum_m)+"))"
	tmp_cond_18="((BVGE("+m1_var+"_p_0,"+int2binstr(2,each_len)+")) AND ("+m1_var+"_sum_m_minusFv_radical="+zero_add4+m1_var+"_p_0_minus1_modp))"
	
	#=>C_A+1_Fv=1
	tmp_cond_19="("+m1_var+"_sum_m_its_aplusb_its_b="+int2binstr(0,len_sum_m)+")"
	tmp_cond_20="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(1,len_sum_m)+")) AND ("+zero_add3+m1_var+"_sum_m_its_aplusb_modp_plus1="+zero_add2+Fv1_var+"))"
	
	#=>C_A+1_Fv=A+1
	tmp_cond_21="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(1,len_sum_m)+")) AND ("+Fv1_var+"="+int2binstr(1,Fv1_var_len)+"))"
	tmp_cond_22="((BVGE("+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(1,len_sum_m)+")) AND ("+zero_add3+m1_var+"_sum_m_its_aplusb_its_b="+zero_add2+Fv1_var+"))"
	
	f.write("ASSERT( "+conds+" => (")
	f.write("(("+tmp_cond_3+" OR "+tmp_cond_4+" OR "+tmp_cond_5+" OR "+tmp_cond_6+") AND "+tmp_cond_9+")")
	f.write(" OR ")
	f.write("(("+tmp_cond_1+" OR "+tmp_cond_2+" OR "+tmp_cond_7+") AND "+tmp_cond_8+")")
	f.write(" OR ")
	f.write("(("+tmp_cond_1+" OR "+tmp_cond_2+") AND "+tmp_cond_9+" AND ("+tmp_cond_10+" OR "+tmp_cond_11+") AND ( "+tmp_cond_17+" OR "+tmp_cond_18+" ))")
	f.write(" OR ")
	f.write("(("+tmp_cond_1+" OR "+tmp_cond_2+") AND "+tmp_cond_9+" AND ("+tmp_cond_12+" OR "+tmp_cond_13+") AND ( "+tmp_cond_14+" OR "+tmp_cond_15+" OR "+tmp_cond_16+" ))")
	f.write(" OR ")
	f.write("(("+tmp_cond_1+" OR "+tmp_cond_2+") AND "+tmp_cond_9+" AND ("+tmp_cond_12+" OR "+tmp_cond_13+") AND ( "+tmp_cond_17+" OR "+tmp_cond_18+") AND ( NOT( "+zero_add4+m1_var+"_p_0 = "+m1_var+"_sum_m_its_aplusb_its_b ) ))")
	f.write(" OR ")
	f.write("("+tmp_cond_7+" AND "+tmp_cond_9+" AND ( "+tmp_cond_19+" OR "+tmp_cond_20+" ) AND ("+tmp_cond_17+" OR "+tmp_cond_18+"))")
	f.write(" OR ")
	f.write("("+tmp_cond_7+" AND "+tmp_cond_9+" AND ( "+tmp_cond_21+" OR "+tmp_cond_22+" ) AND ("+tmp_cond_14+" OR "+tmp_cond_15+" OR "+tmp_cond_16+"))")
	f.write(" OR ")
	f.write("("+tmp_cond_7+" AND "+tmp_cond_9+" AND ( "+tmp_cond_21+" OR "+tmp_cond_22+" ) AND ("+tmp_cond_17+" OR "+tmp_cond_18+") AND (NOT( "+zero_add4+m1_var+"_p_0 = "+m1_var+"_sum_m_its_aplusb_modp_plus1 )))")
	f.write(") ); \n")
	f.write("\n")
	

def findL(max_v,p):
	len_L=math.ceil( math.log(max_v+1,p)-1 )
	return len_L

def Derive_Conds(conds,len_L,m1_var,m1_len,Fv1_var,Fv1_var_len,p):
	#represent m1_var to p-adic numbers
	right_v=0
	for i in range(len_L):
		right_v+=(p-1)*p**i
	right_v+=(p-1)*p**(len_L)
	
	cur_len=len_compute( math.log(right_v,2) )
	
	if cur_len<Fv1_var_len:
		cur_len=Fv1_var_len
	if cur_len<m1_len:
		cur_len=m1_len
	
	each_len=len_compute( math.log(p-1,2) )
	for comb_part in range(len_L+1):
		f.write(m1_var+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
		if comb_part==len_L:
			f.write("ASSERT( BVLE( "+m1_var+"_p_"+str(comb_part)+", "+int2binstr(p-2,each_len)+") ); \n")
		else:
			f.write("ASSERT( BVLE( "+m1_var+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
		
	len_diff=cur_len-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
		
	len_diff=cur_len-m1_len
	if len_diff>0:
		zero_add2="0b"
		for j in range(len_diff):
			zero_add2+="0"
		zero_add2+="@"
	else:
		zero_add2=""
	
	tmpstr=""
	for comb_part in range(len_L+1):
		if comb_part==0:
			tmpstr+=(" , "+zero_add+m1_var+"_p_"+str(comb_part))
			f.write("ASSERT( BVGE( "+zero_add2+m1_var+" , "+zero_add+m1_var+"_p_"+str(comb_part)+" ) ); \n")
		else:
			tmpstr+=(" , BVMULT("+str(cur_len)+", "+zero_add+m1_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
			f.write("ASSERT( BVGE( "+zero_add2+m1_var+" , BVMULT("+str(cur_len)+", "+zero_add+m1_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
	if len_L>=1:
		f.write("ASSERT( "+zero_add2+m1_var+" = BVPLUS("+str(cur_len)+tmpstr+") ); \n")
	else:
		f.write("ASSERT( "+zero_add2+m1_var+" = "+(tmpstr[3:])+" ); \n")
	f.write("\n")
	
	#sum all m_i in p-adic of m
	len_sum_m=len_compute( math.log(len_L+1,2) )+each_len
	f.write(m1_var+"_sum_m : BITVECTOR("+str(len_sum_m)+"); \n")
	len_diff=len_sum_m-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	tmpstr=""
	for comb_part in range(len_L+1):
		tmpstr+=(" , "+zero_add+m1_var+"_p_"+str(comb_part))
		f.write("ASSERT( BVGE( "+m1_var+"_sum_m , "+zero_add+m1_var+"_p_"+str(comb_part)+" ) ); \n")
	if len_L>=1:
		f.write("ASSERT( "+m1_var+"_sum_m = BVPLUS( "+str(len_sum_m)+tmpstr+" ) ); \n")
	else:
		f.write("ASSERT( "+m1_var+"_sum_m = "+(tmpstr[3:])+" ); \n")
	f.write("\n")
	
	#t/p and tmodp
	f.write(m1_var+"_sum_m_its_a, "+m1_var+"_sum_m_its_b, "+m1_var+"_sum_m_its_aplusb, "+m1_var+"_sum_m_its_aplusb_its_a, "+m1_var+"_sum_m_its_aplusb_its_b : BITVECTOR("+str(len_sum_m)+"); \n")
	f.write("ASSERT( BVLE( "+m1_var+"_sum_m_its_b , "+int2binstr(p-1,len_sum_m)+" ) ); \n")
	f.write("ASSERT( BVLE( "+m1_var+"_sum_m_its_aplusb_its_b , "+int2binstr(p-1,len_sum_m)+" ) ); \n")
	
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m , BVMULT("+str(len_sum_m)+","+m1_var+"_sum_m_its_a,"+int2binstr(p,len_sum_m)+") ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m , "+m1_var+"_sum_m_its_b ) ); \n")
	f.write("ASSERT( "+m1_var+"_sum_m = BVPLUS( "+str(len_sum_m)+" , BVMULT("+str(len_sum_m)+","+m1_var+"_sum_m_its_a,"+int2binstr(p,len_sum_m)+") , "+m1_var+"_sum_m_its_b ) ); \n")
	
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb , BVMULT("+str(len_sum_m)+","+m1_var+"_sum_m_its_aplusb_its_a,"+int2binstr(p,len_sum_m)+") ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb , "+m1_var+"_sum_m_its_aplusb_its_b ) ); \n")
	f.write("ASSERT( "+m1_var+"_sum_m_its_aplusb = BVPLUS( "+str(len_sum_m)+" , BVMULT("+str(len_sum_m)+","+m1_var+"_sum_m_its_aplusb_its_a,"+int2binstr(p,len_sum_m)+") , "+m1_var+"_sum_m_its_aplusb_its_b ) ); \n")
	
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb , "+m1_var+"_sum_m_its_a ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb , "+m1_var+"_sum_m_its_b ) ); \n")
	f.write("ASSERT( "+m1_var+"_sum_m_its_aplusb = BVPLUS( "+str(len_sum_m)+" , "+m1_var+"_sum_m_its_a , "+m1_var+"_sum_m_its_b ) ); \n")
	
	f.write("\n")
	
	#(t/p+t mod p) mod p + 1
	f.write(m1_var+"_sum_m_its_aplusb_modp_plus1 : BITVECTOR("+str(len_sum_m)+");\n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb_modp_plus1 , "+m1_var+"_sum_m_its_aplusb_its_b ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m_its_aplusb_modp_plus1 , "+int2binstr(1,len_sum_m)+" ) ); \n")
	f.write("ASSERT( "+m1_var+"_sum_m_its_aplusb_modp_plus1 = BVPLUS("+str(len_sum_m)+","+m1_var+"_sum_m_its_aplusb_its_b,"+int2binstr(1,len_sum_m)+") ); \n")
	f.write("\n")
	
	#(t/p+t mod p) mod p - 1
	f.write(m1_var+"_sum_m_its_aplusb_modp_minus1 : BITVECTOR("+str(len_sum_m)+");\n")
	f.write("ASSERT( IF "+m1_var+"_sum_m_its_aplusb_its_b="+int2binstr(0,len_sum_m)+" THEN "+m1_var+"_sum_m_its_aplusb_modp_minus1="+int2binstr(0,len_sum_m)+" ELSE ("+m1_var+"_sum_m_its_aplusb_its_b = BVPLUS("+str(len_sum_m)+","+m1_var+"_sum_m_its_aplusb_modp_minus1,"+int2binstr(1,len_sum_m)+") ) ENDIF ); \n")
	f.write("\n")
	
	#(m1[0]-1) mod p
	f.write(m1_var+"_p_0_minus1_modp : BITVECTOR("+str(each_len)+");\n")
	f.write("ASSERT( IF "+m1_var+"_p_0="+int2binstr(0,each_len)+" THEN "+m1_var+"_p_0_minus1_modp="+int2binstr(p-1,each_len)+" ELSE "+m1_var+"_p_0=BVPLUS( "+str(each_len)+" , "+m1_var+"_p_0_minus1_modp , "+int2binstr(1,each_len)+" ) ENDIF ); \n")
	f.write("\n")
	
	#t radical
	f.write(m1_var+"_sum_m_radical, "+m1_var+"_sum_m_integral : BITVECTOR("+str(len_sum_m)+");\n")
	f.write("ASSERT( BVLE( "+m1_var+"_sum_m_radical , "+int2binstr(p-2,len_sum_m)+" ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m , BVMULT("+str(len_sum_m)+", "+m1_var+"_sum_m_integral, "+int2binstr(p-1,len_sum_m)+") ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_sum_m , "+m1_var+"_sum_m_radical ) ); \n")
	f.write("ASSERT( "+m1_var+"_sum_m = BVPLUS("+str(len_sum_m)+", BVMULT("+str(len_sum_m)+", "+m1_var+"_sum_m_integral, "+int2binstr(p-1,len_sum_m)+") , "+m1_var+"_sum_m_radical) ); \n")
	f.write("\n")
	
	#t-Fv radical
	f.write(m1_var+"_sum_m_minusFv_radical, "+m1_var+"_sum_m_minusFv_integral, "+m1_var+"_sum_m_minusFv_tmpV : BITVECTOR("+str(len_sum_m)+");\n")
	f.write("ASSERT( BVLE( "+m1_var+"_sum_m_minusFv_radical , "+int2binstr(p-2,len_sum_m)+" ) ); \n")
	max_sum_m_and_Fv1=Fv1_var_len
	if len_sum_m>Fv1_var_len:
		max_sum_m_and_Fv1=len_sum_m
	max_sum_m_and_Fv1+=1
	len_diff=max_sum_m_and_Fv1-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	len_diff=max_sum_m_and_Fv1-len_sum_m
	if len_diff>0:
		zero_add2="0b"
		for j in range(len_diff):
			zero_add2+="0"
		zero_add2+="@"
	else:
		zero_add2=""
	
	f.write("ASSERT( IF (BVGE( "+zero_add2+m1_var+"_sum_m, "+zero_add+Fv1_var+" )) THEN ("+zero_add2+m1_var+"_sum_m = BVPLUS("+str(max_sum_m_and_Fv1)+", "+zero_add2+m1_var+"_sum_m_minusFv_tmpV, "+zero_add+Fv1_var+")) ELSE ("+zero_add+Fv1_var+" = BVPLUS("+str(max_sum_m_and_Fv1)+", "+zero_add2+m1_var+"_sum_m_minusFv_tmpV, "+zero_add2+m1_var+"_sum_m)) ENDIF );\n")
	f.write("ASSERT( (BVGE( "+zero_add2+m1_var+"_sum_m, "+zero_add+Fv1_var+" )) => (("+zero_add2+m1_var+"_sum_m_minusFv_tmpV=BVPLUS("+str(max_sum_m_and_Fv1)+",BVMULT("+str(max_sum_m_and_Fv1)+","+zero_add2+m1_var+"_sum_m_minusFv_integral,"+int2binstr(p-1,max_sum_m_and_Fv1)+"), "+zero_add2+m1_var+"_sum_m_minusFv_radical)) AND (BVGE("+zero_add2+m1_var+"_sum_m_minusFv_tmpV,BVMULT("+str(max_sum_m_and_Fv1)+","+zero_add2+m1_var+"_sum_m_minusFv_integral,"+int2binstr(p-1,max_sum_m_and_Fv1)+"))) AND (BVGE("+zero_add2+m1_var+"_sum_m_minusFv_tmpV,"+zero_add2+m1_var+"_sum_m_minusFv_radical))) );\n")
	f.write("ASSERT( (BVLT( "+zero_add2+m1_var+"_sum_m, "+zero_add+Fv1_var+" )) => (BVPLUS("+str(max_sum_m_and_Fv1)+", "+zero_add2+m1_var+"_sum_m_minusFv_radical, "+zero_add2+m1_var+"_sum_m_minusFv_tmpV) = "+int2binstr(p-1,max_sum_m_and_Fv1)+") );\n")
	f.write("\n")	
	
	#conditions
	Comb_Cancel_T1(conds[0],m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len)
	Comb_Cancel_T2(conds[1],m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len)
	Comb_Cancel_T3(conds[2],m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len)
	Comb_Cancel_T4(conds[3],m1_var,len_sum_m,len_L,each_len,Fv1_var,Fv1_var_len)
	f.write("\n")
	f.write("\n")

def Special_Comb_D1(contained_Z_index, bZ, m1_var, m1_len, m2_var, m2_len, Fv1_var, Fv1_var_len, Fv0_var, Fv0_var_len):
	max_tmp=m1_len
	if m2_len>max_tmp:
		max_tmp=m2_len
	if Fv1_var_len>max_tmp:
		max_tmp=Fv1_var_len
	if max_tmp<Fv0_var_len:
		max_tmp=Fv0_var_len
	cond_var_len=math.ceil( math.log(2*d+2,2) )+max_tmp
	f.write("cond_var_"+str(bZ)+"_"+str(contained_Z_index)+" : BITVECTOR("+str(cond_var_len)+"); \n")
	
	#compute cond_var and restrict that cond_var=d*m1+m2-d*Fv1-Fv0 and p-1 | cond_var
	len_diff=cond_var_len-m2_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	right_eq=zero_add+m2_var
	
	len_diff=cond_var_len-m1_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		right_eq+=(", "+zero_add+m1_var)
	right_eq=("BVPLUS( "+str(cond_var_len)+" , "+right_eq+" )")
	
	f.write("ASSERT( BVLE( cond_var_"+str(bZ)+"_"+str(contained_Z_index)+" , "+right_eq+" ) ); \n")
	
	len_diff=cond_var_len-Fv0_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	left_eq=zero_add+Fv0_var
	
	len_diff=cond_var_len-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		left_eq+=(", "+zero_add+Fv1_var)
	left_eq=("BVPLUS("+str(cond_var_len)+" , cond_var_"+str(bZ)+"_"+str(contained_Z_index)+" , "+left_eq+" )")
	
	f.write("ASSERT( "+left_eq+" = "+right_eq+" ); \n")
	f.write("ASSERT( BVMOD( "+str(cond_var_len)+" , cond_var_"+str(bZ)+"_"+str(contained_Z_index)+" , "+int2binstr(p-1,cond_var_len)+" ) = "+int2binstr(0,cond_var_len)+" ); \n")
	f.write("\n")

	#vars used in determining which case
	each_len=len_compute( math.log(p-1,2) )
	if Fv0_var_len<each_len:
		len_Fv0_plus_pminus1=2*each_len
	else:
		len_Fv0_plus_pminus1=2*Fv0_var_len
	
	f.write(m1_var+"_Fv"+str(bZ)+"_plus_pminus1 : BITVECTOR("+str(len_Fv0_plus_pminus1)+"); \n")
	
	len_diff=len_Fv0_plus_pminus1-Fv0_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	f.write("ASSERT( "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 = BVPLUS( "+str(len_Fv0_plus_pminus1)+" , "+zero_add+Fv0_var+", "+int2binstr(p-1,len_Fv0_plus_pminus1)+" ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 , "+zero_add+Fv0_var+" ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 , "+int2binstr(p-1,len_Fv0_plus_pminus1)+" ) ); \n")
	f.write("\n")
		
	len_diff=len_Fv0_plus_pminus1-m2_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	#List different conditions under different Fv0 and Fv1
	f.write(m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_1, "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_2, "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_3, "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_4 : BITVECTOR(1); \n")
	
	conds=["( "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_1 = 0b1 )", "( "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_2 = 0b1 )", "( "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_3 = 0b1 )", "( "+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_4 = 0b1 )"]
	
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+m2_var+","+int2binstr(p-1,m2_len)+")) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_1 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVLT("+m2_var+","+int2binstr(p-1,m2_len)+")) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_2 = 0b1) ); \n")
	
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND (BVGE("+m2_var+","+int2binstr(p-1,m2_len)+")) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_3 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND (BVLT("+m2_var+","+int2binstr(p-1,m2_len)+")) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_4 = 0b1) ); \n")
		
	f.write("ASSERT( (( BVGE( "+Fv0_var+" , "+int2binstr(1,Fv0_var_len)+" ) ) AND ( BVLE( "+Fv0_var+" , "+int2binstr(p-2,Fv0_var_len)+" ) ) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE( "+zero_add+m2_var+" , "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 )) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_1 = 0b1) ); \n")
	f.write("ASSERT( (( BVGE( "+Fv0_var+" , "+int2binstr(1,Fv0_var_len)+" ) ) AND ( BVLE( "+Fv0_var+" , "+int2binstr(p-2,Fv0_var_len)+" ) ) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVLT( "+zero_add+m2_var+" , "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 )) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_2 = 0b1) ); \n")
	
	f.write("ASSERT( (( BVGE( "+Fv0_var+" , "+int2binstr(1,Fv0_var_len)+" ) ) AND ( BVLE( "+Fv0_var+" , "+int2binstr(p-2,Fv0_var_len)+" ) ) AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND (BVGE( "+zero_add+m2_var+" , "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 )) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_3 = 0b1) ); \n")
	f.write("ASSERT( (( BVGE( "+Fv0_var+" , "+int2binstr(1,Fv0_var_len)+" ) ) AND ( BVLE( "+Fv0_var+" , "+int2binstr(p-2,Fv0_var_len)+" ) ) AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND (BVLT( "+zero_add+m2_var+" , "+m1_var+"_Fv"+str(bZ)+"_plus_pminus1 )) ) => ("+m1_var+"_label_"+str(bZ)+"_"+str(contained_Z_index)+"_4 = 0b1) ); \n")
	
	f.write("\n")
	
	#add conditions according to these labels
	#extra vars
	max_v=(d**(max_degree_z[contained_Z_index]))
	len_L=findL(max_v,p)
	
	if len_L>p:
		print("Code Not Support")
		sys.exit()
	
	Derive_Conds(conds,len_L,m1_var,m1_len,Fv1_var,Fv1_var_len,p)
	
def Special_Comb_D2(round_index_1,round_index_2, m1_var, m1_len, m2_var, m2_len, m3_var, m3_len, Fv2_var, Fv2_var_len, Fv1_var, Fv1_var_len, Fv0_var, Fv0_var_len,extra_label_index):	
	max_tmp=m1_len
	if m2_len>max_tmp:
		max_tmp=m2_len
	if m3_len>max_tmp:
		max_tmp=m3_len
	if Fv1_var_len>max_tmp:
		max_tmp=Fv1_var_len
	if Fv2_var_len>max_tmp:
		max_tmp=Fv2_var_len
	if max_tmp<Fv0_var_len:
		max_tmp=Fv0_var_len
	cond_var_len=math.ceil( math.log(4*d+2,2) )+max_tmp
	f.write("cond_var_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" : BITVECTOR("+str(cond_var_len)+"); \n")
	
	#compute cond_var and restrict that p-1 | d(m1+m2)+m3-d(Fv1+Fv2)-Fv0
	left_eq=""
	len_diff=cond_var_len-m1_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		left_eq+=(" , "+zero_add+m1_var)
	
	len_diff=cond_var_len-m2_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		left_eq+=(" , "+zero_add+m2_var)
	
	len_diff=cond_var_len-m3_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	left_eq+=(" , "+zero_add+m3_var)
	
	left_eq="BVPLUS("+str(cond_var_len)+left_eq+")"
	
	right_eq=""
	len_diff=cond_var_len-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		right_eq+=(" , "+zero_add+Fv1_var)
	
	len_diff=cond_var_len-Fv2_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		right_eq+=(" , "+zero_add+Fv2_var)
	
	len_diff=cond_var_len-Fv0_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	right_eq+=(" , "+zero_add+Fv0_var)
	
	right_eq="BVPLUS("+str(cond_var_len)+" , cond_var_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+right_eq+")"
	
	f.write("ASSERT( "+left_eq+" = "+right_eq+" ); \n")
	f.write("ASSERT( BVLE( cond_var_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+left_eq+" ) ); \n")
	f.write("ASSERT( BVMOD( "+str(cond_var_len)+" , cond_var_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-1,cond_var_len)+" ) = "+int2binstr(0,cond_var_len)+" ); \n")
	f.write("\n")
	
	#vars used in determining which case
	#Fv0+(p-1)
	each_len=len_compute( math.log(p-1,2) )
	if Fv0_var_len<each_len:
		len_Fv0_plus_pminus1=2*each_len
	else:
		len_Fv0_plus_pminus1=2*Fv0_var_len
	
	f.write(m1_var+"_Fv0_plus_pminus1 : BITVECTOR("+str(len_Fv0_plus_pminus1)+"); \n")
	
	len_diff=len_Fv0_plus_pminus1-Fv0_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	f.write("ASSERT( "+m1_var+"_Fv0_plus_pminus1 = BVPLUS( "+str(len_Fv0_plus_pminus1)+" , "+zero_add+Fv0_var+", "+int2binstr(p-1,len_Fv0_plus_pminus1)+" ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_Fv0_plus_pminus1 , "+zero_add+Fv0_var+" ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_Fv0_plus_pminus1 , "+int2binstr(p-1,len_Fv0_plus_pminus1)+" ) ); \n")
	f.write("\n")
	
	#d*m2+m3
	max_tmp=m2_len
	if m3_len>max_tmp:
		max_tmp=m3_len
	len_dm2_m3=math.ceil( math.log(d+1,2) )+max_tmp
	f.write(m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" : BITVECTOR("+str(len_dm2_m3)+"); \n")
	
	tmpstr=""
	len_diff=len_dm2_m3-m2_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		tmpstr+=(" , "+zero_add+m2_var)
	f.write("ASSERT( BVGE( "+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , BVPLUS("+str(len_dm2_m3)+tmpstr+") ) ); \n")
	
	len_diff=len_dm2_m3-m3_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	tmpstr+=(" , "+zero_add+m3_var)
	f.write("ASSERT( "+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" = BVPLUS("+str(len_dm2_m3)+tmpstr+") ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+zero_add+m3_var+" ) ); \n")
	f.write("\n")
	
	#d*m1+m3
	max_tmp=m1_len
	if m3_len>max_tmp:
		max_tmp=m3_len
	len_dm1_m3=math.ceil( math.log(d+1,2) )+max_tmp
	f.write(m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" : BITVECTOR("+str(len_dm1_m3)+"); \n")
	
	tmpstr=""
	len_diff=len_dm1_m3-m1_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	for j in range(d):
		tmpstr+=(" , "+zero_add+m1_var)
	f.write("ASSERT( BVGE( "+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , BVPLUS("+str(len_dm1_m3)+tmpstr+") ) ); \n")
	
	len_diff=len_dm1_m3-m3_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	tmpstr+=(" , "+zero_add+m3_var)
	f.write("ASSERT( "+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" = BVPLUS("+str(len_dm1_m3)+tmpstr+") ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+zero_add+m3_var+" ) ); \n")
	f.write("\n")
	
	max_len=m1_len
	if max_len<m2_len:
		max_len=m2_len
	if max_len<Fv2_var_len:
		max_len=Fv2_var_len						
	if max_len<Fv1_var_len:
		max_len=Fv1_var_len
	len_m_minus_Fv=1+max_len
	f.write(m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+", "+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" : BITVECTOR("+str(len_m_minus_Fv)+"); \n")
	f.write(m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1, "+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 : BITVECTOR("+str(len_m_minus_Fv)+"); \n")
	
	#(m1-Fv2) and mod p-1
	len_diff=len_m_minus_Fv-m1_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	left_eq=zero_add+m1_var
	
	len_diff=len_m_minus_Fv-Fv2_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	f.write("ASSERT( "+left_eq+" = BVPLUS("+str(len_m_minus_Fv)+" , "+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+zero_add+Fv2_var+" ) ); \n")
	f.write("ASSERT( BVGE( "+left_eq+" , "+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ) ); \n")
	f.write("ASSERT( "+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 = BVMOD("+str(len_m_minus_Fv)+","+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_m_minus_Fv)+") ); \n")
	
	#(m2-Fv1) and mod p-1
	len_diff=len_m_minus_Fv-m2_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	left_eq=zero_add+m2_var
	
	len_diff=len_m_minus_Fv-Fv1_var_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	f.write("ASSERT( "+left_eq+" = BVPLUS("+str(len_m_minus_Fv)+" , "+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+zero_add+Fv1_var+" ) ); \n")
	f.write("ASSERT( BVGE( "+left_eq+" , "+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ) ); \n")
	f.write("ASSERT( "+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 = BVMOD("+str(len_m_minus_Fv)+","+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_m_minus_Fv)+") ); \n")
	
	#(m1-Fv2)%(p-1)+(m2-Fv1)%(p-1)
	len_extra_cond=1+len_m_minus_Fv
	f.write(m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" : BITVECTOR("+str(len_extra_cond)+"); \n")
	f.write("ASSERT( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" = BVPLUS("+str(len_extra_cond)+" , 0b0@"+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 , 0b0@"+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , 0b0@"+m1_var+"_m1_minus_Fv2_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 ) ); \n")
	f.write("ASSERT( BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , 0b0@"+m1_var+"_m2_minus_Fv1_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_mod_pminus1 ) ); \n")
	f.write("\n")
	
	#List different conditions under different Fv0 and Fv1
	f.write(m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1, "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2, "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3, "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 : BITVECTOR(1); \n")
	f.write(m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1, "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2, "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3, "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 : BITVECTOR(1); \n")
	
	conds_1=["( "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1 )", "( "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1 )","( "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1 )", "( "+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1 )"]
	conds_2=["( "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1 )", "( "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1 )","( "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1 )", "( "+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1 )"]
	
	#3
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE("+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_dm2_m3)+")) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLE("+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_dm2_m3)+")) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) ); \n")
	
	#4
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ( BVGE( "+Fv2_var+" , "+int2binstr(1,Fv2_var_len)+" ) ) AND ( BVLE( "+Fv2_var+" , "+int2binstr(p-2,Fv2_var_len)+" ) ) AND (BVGE("+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_dm2_m3)+")) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ( BVGE( "+Fv2_var+" , "+int2binstr(1,Fv2_var_len)+" ) ) AND ( BVLE( "+Fv2_var+" , "+int2binstr(p-2,Fv2_var_len)+" ) ) AND (BVLE("+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_dm2_m3)+")) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) ); \n")
	
	#5
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVGE("+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_dm1_m3)+")) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVLE("+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_dm1_m3)+")) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) ); \n")
	
	#6
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE("+m3_var+","+int2binstr(p-1,m3_len)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND (BVLE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-2,len_extra_cond)+" )) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND (BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-1,len_extra_cond)+" )) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	
	#7
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVGE("+m3_var+","+int2binstr(p-1,m3_len)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVLE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-2,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-1,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	
	#8
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVGE("+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_dm1_m3)+")) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND ( BVGE( "+Fv1_var+" , "+int2binstr(1,Fv1_var_len)+" ) ) AND ( BVLE( "+Fv1_var+" , "+int2binstr(p-2,Fv1_var_len)+" ) ) AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVLE("+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_dm1_m3)+")) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) ); \n")
	
	#9
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE("+m3_var+","+int2binstr(p-1,m3_len)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVLE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-2,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-1,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	
	#10
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVGE("+m3_var+","+int2binstr(p-1,m3_len)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVLE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-2,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1)) ); \n")
	f.write("ASSERT( (("+Fv0_var+" = "+int2binstr(p-1,Fv0_var_len)+") AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLE("+m3_var+","+int2binstr(p-2,m3_len)+")) AND ((BVGE( "+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" , "+int2binstr(p-1,len_extra_cond)+" ))) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	
	len_diff=len_Fv0_plus_pminus1-len_dm2_m3
	if len_diff>0:
		zero23_add="0b"
		for j in range(len_diff):
			zero23_add+="0"
		zero23_add+="@"
	else:
		zero23_add=""
	
	len_diff=len_dm2_m3-len_Fv0_plus_pminus1
	if len_diff>0:
		zero23_add2="0b"
		for j in range(len_diff):
			zero23_add2+="0"
		zero23_add2+="@"
	else:
		zero23_add2=""
	
	#12
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE("+zero23_add+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero23_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLT("+zero23_add+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero23_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) ); \n")
	
	#13
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVGE("+zero23_add+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero23_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(0,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLT("+zero23_add+m1_var+"_dm2_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero23_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) ); \n")
	
	len_diff=len_Fv0_plus_pminus1-len_dm1_m3
	if len_diff>0:
		zero13_add="0b"
		for j in range(len_diff):
			zero13_add+="0"
		zero13_add+="@"
	else:
		zero13_add=""
	
	len_diff=len_dm1_m3-len_Fv0_plus_pminus1
	if len_diff>0:
		zero13_add2="0b"
		for j in range(len_diff):
			zero13_add2+="0"
		zero13_add2+="@"
	else:
		zero13_add2=""
	
	#14
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVGE("+zero13_add+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero13_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(0,Fv2_var_len)+") AND (BVLT("+zero13_add+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero13_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) ); \n")
	
	len_diff=len_Fv0_plus_pminus1-m3_len
	if len_diff>0:
		zero3_add="0b"
		for j in range(len_diff):
			zero3_add+="0"
		zero3_add+="@"
	else:
		zero3_add=""
	
	len_diff=m3_len-len_Fv0_plus_pminus1
	if len_diff>0:
		zero3_add2="0b"
		for j in range(len_diff):
			zero3_add2+="0"
		zero3_add2+="@"
	else:
		zero3_add2=""
	
	#15
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVLE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVGE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	
	#16
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVGE( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVLE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND ("+Fv1_var+" = "+int2binstr(p-1,Fv1_var_len)+") AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVGE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	
	#17
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+"="+int2binstr(0,Fv2_var_len)+") AND (BVGE("+zero13_add+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero13_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+"="+int2binstr(0,Fv2_var_len)+") AND (BVLT("+zero13_add+m1_var+"_dm1_m3_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+" ,"+zero13_add2+m1_var+"_Fv0_plus_pminus1)) ) => ("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) ); \n")
	
	#18
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVGE( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVLE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_2 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND ("+Fv2_var+" = "+int2binstr(p-1,Fv2_var_len)+") AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVGE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_1 = 0b1)) ); \n")
	
	#19
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVGE( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVLE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-2,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1) OR ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_4 = 0b1)) ); \n")
	f.write("ASSERT( ((BVGE("+Fv0_var+","+int2binstr(1,Fv0_var_len)+")) AND (BVLE("+Fv0_var+","+int2binstr(p-2,Fv0_var_len)+")) AND (BVGE("+Fv1_var+","+int2binstr(1,Fv1_var_len)+")) AND (BVLE("+Fv1_var+","+int2binstr(p-2,Fv1_var_len)+")) AND (BVGE("+Fv2_var+","+int2binstr(1,Fv2_var_len)+")) AND (BVLE("+Fv2_var+","+int2binstr(p-2,Fv2_var_len)+")) AND (BVLT( "+zero3_add+m3_var+","+zero3_add2+m1_var+"_Fv0_plus_pminus1)) AND (BVGE("+m1_var+"_extra_cond_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+","+int2binstr(p-1,len_extra_cond)+")) ) => (("+m2_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1) AND ("+m1_var+"_label_"+str(round_index_1)+"_"+str(round_index_2)+extra_label_index+"_3 = 0b1)) ); \n")
	
	f.write("\n")
	
	#extra vars
	max_v=(d**(TargetZ+1-round_index_2))
	len_L=findL(max_v,p)
	
	if len_L>p:
		print("Code Not Support 2")
		sys.exit()
	
	Derive_Conds(conds_1,len_L,m1_var,m1_len,Fv2_var,Fv2_var_len,p)
	
	max_v=(d**(TargetZ+1-round_index_1))
	len_L=findL(max_v,p)
	
	if len_L>p:
		print("Code Not Support 3")
		sys.exit()
	
	Derive_Conds(conds_2,len_L,m2_var,m2_len,Fv1_var,Fv1_var_len,p)

def Special_Comb_D3(m1plusm2_var, last_var, uhat_var_arr, these_var_len, uhat_max_p):
	max_v=2**these_var_len
	max_p=math.floor(math.log(max_v,p)) 
	cur_len=len_compute( math.log(p**(max_p+1),2) )#length of these vars in p-adic
	
	if cur_len<these_var_len:
		cur_len=these_var_len
	
	each_len=len_compute( math.log(p-1,2) )
	for comb_part in range(max_p+1):
		f.write(m1plusm2_var+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
		f.write("ASSERT( BVLE( "+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
		f.write(last_var+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
		f.write("ASSERT( BVLE( "+last_var+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")

	len_diff=cur_len-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	len_diff=cur_len-these_var_len
	if len_diff>0:
		zero_add_2="0b"
		for j in range(len_diff):
			zero_add_2+="0"
		zero_add_2+="@"
	else:
		zero_add_2=""
	
	right_hand=""
	for comb_part in range(max_p+1):
		if comb_part==0:
			right_hand+=(", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+"")
			f.write("ASSERT( BVGE( "+zero_add_2+m1plusm2_var+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" ) ); \n")
		else:					
			right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
			f.write("ASSERT( BVGE( "+zero_add_2+m1plusm2_var+", BVMULT("+str(cur_len)+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
	
	if max_p>=1:
		f.write("ASSERT( "+zero_add_2+m1plusm2_var+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
	else:
		f.write("ASSERT( "+zero_add_2+m1plusm2_var+" = "+(right_hand[2:])+" ); \n")
	
	right_hand=""
	for comb_part in range(max_p+1):
		if comb_part==0:
			right_hand+=(", "+zero_add+last_var+"_p_"+str(comb_part)+"")
			f.write("ASSERT( BVGE( "+zero_add_2+last_var+", "+zero_add+last_var+"_p_"+str(comb_part)+" ) ); \n")
		else:					
			right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+last_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
			f.write("ASSERT( BVGE( "+zero_add_2+last_var+", BVMULT("+str(cur_len)+", "+zero_add+last_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
	
	if max_p>=1:
		f.write("ASSERT( "+zero_add_2+last_var+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
	else:
		f.write("ASSERT( "+zero_add_2+last_var+" = "+(right_hand[2:])+" ); \n")
	f.write("\n")
	
	#add constraints
	sum_len=len_compute( math.log(len(uhat_var_arr)+1,2) )+each_len
	len_diff=sum_len-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	if uhat_max_p<=max_p:
		for comb_part in range(max_p+1):
			if comb_part<uhat_max_p+1:
				tmpstr=""
				for ele in uhat_var_arr:
					tmpstr+=(", "+zero_add+ele+"_p_"+str(comb_part))
					f.write("ASSERT( BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+ele+"_p_"+str(comb_part)+" ) ); \n")
				tmpstr+=(", "+zero_add+last_var+"_p_"+str(comb_part))
				f.write("ASSERT( BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+last_var+"_p_"+str(comb_part)+" ) ); \n")
				if len(uhat_var_arr)>=1:
					f.write("ASSERT( "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = BVPLUS("+str(sum_len)+tmpstr+") ); \n")
				else:
					f.write("ASSERT( "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = "+(tmpstr[2:])+" ); \n")
			else:
				f.write("ASSERT( "+m1plusm2_var+"_p_"+str(comb_part)+" = "+last_var+"_p_"+str(comb_part)+" ); \n")
	else:
		for comb_part in range(uhat_max_p+1):
			tmpstr=""
			for ele in uhat_var_arr:
				tmpstr+=(", "+zero_add+ele+"_p_"+str(comb_part))
				f.write("ASSERT( BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+ele+"_p_"+str(comb_part)+" ) ); \n")
			if comb_part<max_p+1:
				tmpstr+=(", "+zero_add+last_var+"_p_"+str(comb_part))
				f.write("ASSERT( BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+last_var+"_p_"+str(comb_part)+" ) ); \n")
				if len(uhat_var_arr)>=1:
					f.write("ASSERT( "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = BVPLUS("+str(sum_len)+tmpstr+") ); \n")
				else:
					f.write("ASSERT( "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = "+(tmpstr[2:])+" ); \n")
			else:
				if len(uhat_var_arr)>=2:
					f.write("ASSERT( "+int2binstr(0,sum_len)+" = BVPLUS("+str(sum_len)+tmpstr+") ); \n")
				else:
					f.write("ASSERT( "+int2binstr(0,sum_len)+" = "+(tmpstr[2:])+" ); \n")
	
	f.write("\n")
	
	
def Special_Comb_D4(m1_var, m1_len, m2_var, m2_len, m1plusm2_var, uhat_var_arr, these_var_len, uhat_max_p):
	max_v=2**these_var_len
	max_p=math.floor(math.log(max_v,p)) 
	cur_len=len_compute( math.log(p**(max_p+1),2) )#length of these vars in p-adic
	
	if cur_len<these_var_len:
		cur_len=these_var_len
	
	each_len=len_compute( math.log(p-1,2) )
	for comb_part in range(max_p+1):
		f.write(m1plusm2_var+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
		f.write("ASSERT( BVLE( "+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
		
	len_diff=cur_len-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	len_diff=cur_len-these_var_len
	if len_diff>0:
		zero_add_2="0b"
		for j in range(len_diff):
			zero_add_2+="0"
		zero_add_2+="@"
	else:
		zero_add_2=""
	
	right_hand=""
	for comb_part in range(max_p+1):
		if comb_part==0:
			right_hand+=(", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+"")
			f.write("ASSERT( BVGE( "+zero_add_2+m1plusm2_var+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" ) ); \n")
		else:					
			right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
			f.write("ASSERT( BVGE( "+zero_add_2+m1plusm2_var+", BVMULT("+str(cur_len)+", "+zero_add+m1plusm2_var+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
	
	if max_p>=1:
		f.write("ASSERT( "+zero_add_2+m1plusm2_var+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
	else:
		f.write("ASSERT( "+zero_add_2+m1plusm2_var+" = "+(right_hand[2:])+" ); \n")
	f.write("\n")
	
	#add constraints
	sum_len=len_compute( math.log(len(uhat_var_arr)+1,2) )+each_len
	len_diff=sum_len-each_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	total_cond=""
	if uhat_max_p<=max_p:
		for comb_part in range(max_p+1):
			if comb_part<uhat_max_p+1:
				tmpstr=""
				for ele in uhat_var_arr:
					tmpstr+=(", "+zero_add+ele+"_p_"+str(comb_part))
					total_cond+=("(BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+ele+"_p_"+str(comb_part)+" )) AND ")
				if len(uhat_var_arr)>=2:
					total_cond+=("("+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = BVPLUS("+str(sum_len)+tmpstr+"))")
				else:
					total_cond+=("("+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = "+(tmpstr[2:])+")")
				
				if comb_part<max_p:
					total_cond+=(" AND ")
			else:
				if comb_part==max_p:
					total_cond+=("("+m1plusm2_var+"_p_"+str(comb_part)+" = "+int2binstr(0,each_len)+")")
				else:
					total_cond+=("("+m1plusm2_var+"_p_"+str(comb_part)+" = "+int2binstr(0,each_len)+") AND ")
	else:
		for comb_part in range(uhat_max_p+1):
			tmpstr=""
			for ele in uhat_var_arr:
				tmpstr+=(", "+zero_add+ele+"_p_"+str(comb_part))
				total_cond+=("(BVGE( "+m1plusm2_var+"_p_"+str(comb_part)+" , "+ele+"_p_"+str(comb_part)+" )) AND ")
			if comb_part<max_p+1:
				if len(uhat_var_arr)>=2:
					total_cond+=("("+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = BVPLUS("+str(sum_len)+tmpstr+")) AND ")
				else:
					total_cond+=("("+zero_add+m1plusm2_var+"_p_"+str(comb_part)+" = "+(tmpstr[2:])+") AND ")
			else:
				if comb_part==uhat_max_p:
					if len(uhat_var_arr)>=2:
						total_cond+=("("+int2binstr(0,sum_len)+" = BVPLUS("+str(sum_len)+tmpstr+"))")
					else:
						total_cond+=("("+int2binstr(0,sum_len)+" = "+(tmpstr[2:])+")")
				else:
					if len(uhat_var_arr)>=2:
						total_cond+=("("+int2binstr(0,sum_len)+" = BVPLUS("+str(sum_len)+tmpstr+")) AND ")
					else:
						total_cond+=("("+int2binstr(0,sum_len)+" = "+(tmpstr[2:])+") AND ")
	
	len_diff=these_var_len-m1_len
	if len_diff>0:
		zero_add="0b"
		for j in range(len_diff):
			zero_add+="0"
		zero_add+="@"
	else:
		zero_add=""
	
	len_diff=m1_len-these_var_len
	if len_diff>0:
		zero_add2="0b"
		for j in range(len_diff):
			zero_add2+="0"
		zero_add2+="@"
	else:
		zero_add2=""
	
	len_diff=these_var_len-m2_len
	if len_diff>0:
		zero_add3="0b"
		for j in range(len_diff):
			zero_add3+="0"
		zero_add3+="@"
	else:
		zero_add3=""
	
	len_diff=m2_len-these_var_len
	if len_diff>0:
		zero_add4="0b"
		for j in range(len_diff):
			zero_add4+="0"
		zero_add4+="@"
	else:
		zero_add4=""
	
	tmp_cond=""
	for ele in uhat_var_arr:
		tmp_cond+=(" AND (BVGE( "+zero_add2+ele+" , "+zero_add+m1_var+" ))")
		tmp_cond+=(" AND (BVGE( "+zero_add4+ele+" , "+zero_add3+m2_var+" ))")
	
	f.write("ASSERT( ("+(tmp_cond[5:])+") => ("+total_cond+") ); \n")
	f.write("\n")

def Check_Repeat(all_need_considered_combs,this_Comb):
	for ele in all_need_considered_combs:
		if len(this_Comb)==len(ele):
			repeated=True
			for ele_count in range(len(ele)):
				if this_Comb[ele_count]!=ele[ele_count]:
					repeated=False
					break
			if repeated:
				return True
	return False

def List_All_Size2(index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ,fix_v):
	if bZ in index_same_part:#form is [v,u_*_0,u_*_a]
		#fixed u_*_a vars
		this_Comb=["MultiComb( m1, [v_"+str(contained_Z_index_2)+" , u_"+str(contained_Z_index_2)+"_"+str(bZ)+"]) * MultiComb( m2, [v_"+str(contained_Z_index_1)+" , u_"+str(contained_Z_index_1)+"_"+str(bZ)+"])","v_"+str(contained_Z_index_2)+" + u_"+str(contained_Z_index_2)+"_"+str(bZ)+" = m1","v_"+str(contained_Z_index_1)+" + u_"+str(contained_Z_index_1)+"_"+str(bZ)+" = m2","v_"+str(bZ)+" = d*(u_"+str(contained_Z_index_2)+"_"+str(bZ)+" + u_"+str(contained_Z_index_1)+"_"+str(bZ)+") + m3","Fv_"+str(contained_Z_index_2),"Fv_"+str(contained_Z_index_1),"Fv_"+str(bZ)]
		
		tmpstr=""
		for ele in u_var_arr[contained_Z_index_2]:
			if ele!=bZ:
				tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
		tmpstr=tmpstr[3:]
		if tmpstr=="":
			tmpstr="m1 = TR_"+str(contained_Z_index_2)
		else:
			tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
		this_Comb.append(tmpstr)
		
		tmpstr=""
		for ele in u_var_arr[contained_Z_index_1]:
			if ele!=bZ:
				tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
		tmpstr=tmpstr[3:]
		if tmpstr=="":
			tmpstr="m2 = TR_"+str(contained_Z_index_1)
		else:
			tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
		this_Comb.append(tmpstr)
		
		m3_part=[]
		for tmp_cZ in contain_Z:
			if tmp_cZ!=contained_Z_index_1 and tmp_cZ!=contained_Z_index_2 and bZ in z_index[tmp_cZ]:
				m3_part.append(tmp_cZ)
		
		tmpstr=""
		for ele in m3_part:
			tmpstr+=(" + u_"+str(ele)+"_"+str(bZ))
		tmpstr=tmpstr[3:]
		if len(m3_part)>=1:
			tmpstr=("m3 = d*("+tmpstr+")")
		else:
			tmpstr=("m3 = 0")
		this_Comb.append(tmpstr)
		
		if not Check_Repeat(all_need_considered_combs,this_Comb):
			all_need_considered_combs.append(this_Comb)
		
			print(this_Comb)
			print()
			
			extra_label_index="_2v0_"+str(bZ)
			for i in index_same_part:
				extra_label_index+=("_"+str(i))
			
			m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
			f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
			
			len_diff=m1_len-var_len_arr[contained_Z_index_2]
			if len_diff>0:
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			else:
				zero_add=""
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_2]:
				if ele != bZ:
					tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
			if tmpstr=="":
				tmpstr=m1_var
			else:
				tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
			f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
			f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
			
			m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
			f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
			
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_1]:
				if ele != bZ:
					tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
			if tmpstr=="":
				tmpstr=m2_var
			else:
				tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
			f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
			f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
			
			m3_var="m3_rr_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m3_len=var_len_arr[bZ]+len_compute( math.log(d,2) )
			f.write(m3_var+" : BITVECTOR("+str(m3_len)+"); \n")
			
			max_len_here=m3_len
			for ele in m3_part:
				if var_len_arr[ele]>max_len_here:
					max_len_here=var_len_arr[ele]
			tmpstr=""
			for ele in m3_part:
				len_diff=max_len_here-var_len_arr[ele]
				if len_diff>0:
					zero_add="0b"
					for j in range(len_diff):
						zero_add+="0"
					zero_add+="@"
				else:
					zero_add=""
				
				len_diff=max_len_here-m3_len
				if len_diff>0:
					zero_add2="0b"
					for j in range(len_diff):
						zero_add2+="0"
					zero_add2+="@"
				else:
					zero_add2=""
				for j in range(d):
					tmpstr+=(" , "+zero_add+"u_"+str(ele)+"_"+str(bZ))
				f.write("ASSERT( BVGE( "+zero_add2+m3_var+" , "+zero_add+"u_"+str(ele)+"_"+str(bZ)+" ) ); \n")
			if len(m2_part)>=1:
				f.write("ASSERT( "+zero_add2+m3_var+" = BVPLUS( "+str(max_len_here)+tmpstr+" ) ); \n")
			else:
				f.write("ASSERT( "+m3_var+" = "+int2binstr(0,m3_len)+" ); \n")
			
			Fv2_var="Fv_"+str(contained_Z_index_2)
			Fv2_var_len=var_len_arr[contained_Z_index_2]
			
			Fv1_var="Fv_"+str(contained_Z_index_1)
			Fv1_var_len=var_len_arr[contained_Z_index_1]
			
			Fv0_var="Fv_"+str(bZ)
			Fv0_var_len=var_len_arr[bZ]
			
			Special_Comb_D2(contained_Z_index_1,contained_Z_index_2, bZ, m1_var, m1_len, m2_var, m2_len, m3_var, m3_len, Fv2_var, Fv2_var_len, Fv1_var, Fv1_var_len, Fv0_var, Fv0_var_len,extra_label_index)
			
		#fixed v_vars
		if fix_v:
			this_Comb=["MultiComb( m1 + m2, [uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(index_same_part[1])+" , m1 + m2 - uhat_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(index_same_part[1])+"])"]
			
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_2]:
				if ele not in index_same_part:
					tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
			tmpstr+=(" + v_"+str(contained_Z_index_2))
			tmpstr=tmpstr[3:]
			if tmpstr=="":
				tmpstr="m1 = TR_"+str(contained_Z_index_2)
			else:
				tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
			this_Comb.append(tmpstr)
			
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_1]:
				if ele not in index_same_part:
					tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
			tmpstr+=(" + v_"+str(contained_Z_index_1))
			tmpstr=tmpstr[3:]
			if tmpstr=="":
				tmpstr="m2 = TR_"+str(contained_Z_index_1)
			else:
				tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
			this_Comb.append(tmpstr)
			
			tmpstr=("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(index_same_part[1])+" = u_"+str(contained_Z_index_2)+"_"+str(index_same_part[1])+" + u_"+str(contained_Z_index_1)+"_"+str(index_same_part[1]))
			this_Comb.append(tmpstr)
			
			if not Check_Repeat(all_need_considered_combs,this_Comb):
				all_need_considered_combs.append(this_Comb)
			
				print(this_Comb)
				print()
				
				extra_label_index="_20a_"+str(bZ)
				for i in index_same_part:
					extra_label_index+=("_"+str(i))
				
				m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
				m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
				f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
				
				len_diff=m1_len-var_len_arr[contained_Z_index_2]
				if len_diff>0:
					zero_add="0b"
					for j in range(len_diff):
						zero_add+="0"
					zero_add+="@"
				else:
					zero_add=""
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_2]:
					if ele not in index_same_part:
						tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
				tmpstr+=(" , "+zero_add+"v_"+str(contained_Z_index_2))
				if tmpstr=="":
					tmpstr=m1_var
				else:
					tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
				f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
				f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
				
				m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
				m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
				f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
				
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_1]:
					if ele not in index_same_part:
						tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
				tmpstr+=(" , v_"+str(contained_Z_index_1))
				if tmpstr=="":
					tmpstr=m2_var
				else:
					tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
				f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
				f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
				
				m1plusm2_var="m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
				m1plusm2_len=1+var_len_arr[contained_Z_index_1]
				f.write("m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(m1plusm2_len)+"); \n")
				
				f.write("ASSERT( "+m1plusm2_var+" = BVPLUS("+str(m1plusm2_len)+", 0b0@"+m1_var+", 0b0@"+m2_var+" ) ); \n")
				f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m1_var+" ) ); \n")
				f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m2_var+" ) ); \n")
				
				last_var="last_var_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
				last_var_len=1+var_len_arr[contained_Z_index_1]
				f.write("last_var_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(last_var_len)+"); \n")
				
				uhat_var_arr=[]
				for ele in index_same_part:
					if ele!=bZ:
						uhat_var_arr.append(("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)))
				uhat_var_len=1+var_len_arr[contained_Z_index_1]
				
				total_len=len_compute(math.log(1+len(index_same_part)-1,2))+m1plusm2_len
				len_diff=total_len-m1plusm2_len
				if len_diff>0:
					zero_add="0b"
					for j in range(len_diff):
						zero_add+="0"
					zero_add+="@"
				else:
					zero_add=""
				tmpstr=", "+zero_add+last_var
				f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+last_var+" ) ); \n")
				for ele in uhat_var_arr:
					tmpstr+=(", "+zero_add+ele)
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+ele+" ) ); \n")
				if len(uhat_var_arr)>=1:
					f.write("ASSERT( "+zero_add+m1plusm2_var+" = BVPLUS("+str(total_len)+tmpstr+") ); \n")
				else:
					f.write("ASSERT( "+zero_add+m1plusm2_var+" = "+(tmpstr[2:])+" ); \n")
				
				max_v=(d**(max_degree_z[contained_Z_index_1]))
				uhat_max_p=math.floor(math.log(max_v,p)) 
				
				Special_Comb_D3(m1plusm2_var, last_var, uhat_var_arr, uhat_var_len, uhat_max_p)
				
		
	else:#form is [v,u_*_a1,u_*_a2]
		#fixed v_vars
		this_Comb=["MultiComb( m1 + m2, [ uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(index_same_part[0])+" , uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(index_same_part[1])+"])"]
		
		tmpstr=""
		for ele in u_var_arr[contained_Z_index_2]:
			if ele not in index_same_part:
				tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
		tmpstr+=(" + v_"+str(contained_Z_index_2))
		tmpstr=tmpstr[3:]
		if tmpstr=="":
			tmpstr="m1 = TR_"+str(contained_Z_index_2)
		else:
			tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
		this_Comb.append(tmpstr)
		
		tmpstr=""
		for ele in u_var_arr[contained_Z_index_1]:
			if ele not in index_same_part:
				tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
		tmpstr+=(" + v_"+str(contained_Z_index_1))
		tmpstr=tmpstr[3:]
		if tmpstr=="":
			tmpstr="m2 = TR_"+str(contained_Z_index_1)
		else:
			tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
		this_Comb.append(tmpstr)
		
		for ele in index_same_part:
			tmpstr=("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = u_"+str(contained_Z_index_2)+"_"+str(ele)+" + u_"+str(contained_Z_index_1)+"_"+str(ele))
			this_Comb.append(tmpstr)
			
			tmpstr="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" >= m1"#cond_1
			this_Comb.append(tmpstr)
			
			tmpstr="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" >= m2"#cond_2
			this_Comb.append(tmpstr)
		
		if not Check_Repeat(all_need_considered_combs,this_Comb):
			all_need_considered_combs.append(this_Comb)
		
			print(this_Comb)
			print()
			
			#Only when cond_1 and cond_2 holds, we add conditions here
			extra_label_index="_2va1a2_"+str(bZ)
			for i in index_same_part:
				extra_label_index+=("_"+str(i))
			
			m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
			f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
			
			len_diff=m1_len-var_len_arr[contained_Z_index_2]
			if len_diff>0:
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			else:
				zero_add=""
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_2]:
				if ele not in index_same_part:
					tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
			tmpstr+=(" , "+zero_add+"v_"+str(contained_Z_index_2))
			if tmpstr=="":
				tmpstr=m1_var
			else:
				tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
			f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
			f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
			
			m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
			f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
			
			tmpstr=""
			for ele in u_var_arr[contained_Z_index_1]:
				if ele not in index_same_part:
					tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
			tmpstr+=(" , v_"+str(contained_Z_index_1))
			if tmpstr=="":
				tmpstr=m2_var
			else:
				tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
			f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
			f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
			
			m1plusm2_var="m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
			m1plusm2_len=1+var_len_arr[contained_Z_index_1]
			f.write("m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(m1plusm2_len)+"); \n")
			
			f.write("ASSERT( "+m1plusm2_var+" = BVPLUS("+str(m1plusm2_len)+", 0b0@"+m1_var+", 0b0@"+m2_var+" ) ); \n")
			f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m1_var+" ) ); \n")
			f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m2_var+" ) ); \n")
			
			uhat_var_arr=[]
			for ele in index_same_part:
				if ele!=bZ:
					uhat_var_arr.append(("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)))
			uhat_var_len=1+var_len_arr[contained_Z_index_1]
			
			total_len=len_compute(math.log(1+len(index_same_part)-1,2))+m1plusm2_len
			len_diff=total_len-m1plusm2_len
			if len_diff>0:
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			else:
				zero_add=""
			tmpstr=""
			for ele in uhat_var_arr:
				tmpstr+=(", "+zero_add+ele)
				f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+ele+" ) ); \n")
			if len(uhat_var_arr)>=2:
				f.write("ASSERT( "+zero_add+m1plusm2_var+" = BVPLUS("+str(total_len)+tmpstr+") ); \n")
			else:
				f.write("ASSERT( "+zero_add+m1plusm2_var+" = "+(tmpstr[2:])+" ); \n")
			
			max_v=(d**(max_degree_z[contained_Z_index_1]))
			uhat_max_p=math.floor(math.log(max_v,p)) 
			
			Special_Comb_D4(m1_var, m1_len, m2_var, m2_len, m1plusm2_var, uhat_var_arr, uhat_var_len, uhat_max_p)
		
	

def List_All(index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ):
	if len(index_same_part)>=2:
		if len(index_same_part)==2:
			List_All_Size2(index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ,True)
		else:
			if bZ in index_same_part:
				#fixed one of these u_*_j vars where j>=1
				for ele in index_same_part:
					if ele!=bZ:
						tmp_index_same_part=[bZ,ele]
						print(tmp_index_same_part)
						List_All_Size2(tmp_index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ,False)
				
				#fixed v_vars
				this_Comb=[]
				
				tmpstr1=""
				tmpstr2=""
				for ele in index_same_part:
					if ele!=bZ:
						this_tmp_str="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)
						tmpstr1+=(" , "+this_tmp_str)
						tmpstr2+=(" + "+this_tmp_str)
				tmpstr1=tmpstr1[3:]
				tmpstr2=tmpstr2[3:]
				tmpstr2=" m1 + m2 - ("+tmpstr2+")"
				
				this_Comb.append("MultiComb( m1 + m2, [ "+tmpstr1+" , "+tmpstr2+" ])")
				
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_2]:
					if ele not in index_same_part:
						tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
				tmpstr+=(" + v_"+str(contained_Z_index_2))
				tmpstr=tmpstr[3:]
				if tmpstr=="":
					tmpstr="m1 = TR_"+str(contained_Z_index_2)
				else:
					tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
				this_Comb.append(tmpstr)
				
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_1]:
					if ele not in index_same_part:
						tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
				tmpstr+=(" + v_"+str(contained_Z_index_1))
				tmpstr=tmpstr[3:]
				if tmpstr=="":
					tmpstr="m2 = TR_"+str(contained_Z_index_1)
				else:
					tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
				this_Comb.append(tmpstr)
				
				for ele in index_same_part:
					if ele!=bZ:
						tmpstr=("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = u_"+str(contained_Z_index_2)+"_"+str(ele)+" + u_"+str(contained_Z_index_1)+"_"+str(ele))
						this_Comb.append(tmpstr)
				
				if not Check_Repeat(all_need_considered_combs,this_Comb):
					all_need_considered_combs.append(this_Comb)
				
					print(this_Comb)
					print()
					
					extra_label_index="_0a_"+str(bZ)
					for i in index_same_part:
						extra_label_index+=("_"+str(i))
					
					m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
					f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
					
					len_diff=m1_len-var_len_arr[contained_Z_index_2]
					if len_diff>0:
						zero_add="0b"
						for j in range(len_diff):
							zero_add+="0"
						zero_add+="@"
					else:
						zero_add=""
					tmpstr=""
					for ele in u_var_arr[contained_Z_index_2]:
						if ele not in index_same_part:
							tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
					tmpstr+=(" , "+zero_add+"v_"+str(contained_Z_index_2))
					if tmpstr=="":
						tmpstr=m1_var
					else:
						tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
					f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
					f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
					
					m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
					f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
					
					tmpstr=""
					for ele in u_var_arr[contained_Z_index_1]:
						if ele not in index_same_part:
							tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
					tmpstr+=(" , v_"+str(contained_Z_index_1))
					if tmpstr=="":
						tmpstr=m2_var
					else:
						tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
					f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
					f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
					
					m1plusm2_var="m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m1plusm2_len=1+var_len_arr[contained_Z_index_1]
					f.write("m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(m1plusm2_len)+"); \n")
					
					f.write("ASSERT( "+m1plusm2_var+" = BVPLUS("+str(m1plusm2_len)+", 0b0@"+m1_var+", 0b0@"+m2_var+" ) ); \n")
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m1_var+" ) ); \n")
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m2_var+" ) ); \n")
					
					last_var="last_var_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					last_var_len=1+var_len_arr[contained_Z_index_1]
					f.write("last_var_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(last_var_len)+"); \n")
					
					uhat_var_arr=[]
					for ele in index_same_part:
						if ele!=bZ:
							uhat_var_arr.append(("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)))
					uhat_var_len=1+var_len_arr[contained_Z_index_1]
					
					total_len=len_compute(math.log(1+len(index_same_part)-1,2))+m1plusm2_len
					len_diff=total_len-m1plusm2_len
					if len_diff>0:
						zero_add="0b"
						for j in range(len_diff):
							zero_add+="0"
						zero_add+="@"
					else:
						zero_add=""
					tmpstr=", "+zero_add+last_var
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+last_var+" ) ); \n")
					for ele in uhat_var_arr:
						tmpstr+=(", "+zero_add+ele)
						f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+ele+" ) ); \n")
					if len(uhat_var_arr)>=1:
						f.write("ASSERT( "+zero_add+m1plusm2_var+" = BVPLUS("+str(total_len)+tmpstr+") ); \n")
					else:
						f.write("ASSERT( "+zero_add+m1plusm2_var+" = "+(tmpstr[2:])+" ); \n")
					
					max_v=(d**(max_degree_z[contained_Z_index_1]))
					uhat_max_p=math.floor(math.log(max_v,p))
					
					Special_Comb_D3(m1plusm2_var, last_var, uhat_var_arr, uhat_var_len, uhat_max_p)
				
				
				#fixed u_*_0 vars
				tmp_index_same_part=[]
				for ele in index_same_part:
					if ele!=bZ:
						tmp_index_same_part.append(ele)
				
				List_All(tmp_index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ)
				
			else:
				#fixed v_vars
				this_Comb=[]
				
				tmpstr1=""
				for ele in index_same_part:
					this_tmp_str="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)
					tmpstr1+=(" , "+this_tmp_str)
				tmpstr1=tmpstr1[3:]
					
				this_Comb.append("MultiComb( m1 + m2, [ "+tmpstr1+" ])")
				
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_2]:
					if ele not in index_same_part:
						tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
				tmpstr+=(" + v_"+str(contained_Z_index_2))
				tmpstr=tmpstr[3:]
				if tmpstr=="":
					tmpstr="m1 = TR_"+str(contained_Z_index_2)
				else:
					tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
				this_Comb.append(tmpstr)
				
				tmpstr=""
				for ele in u_var_arr[contained_Z_index_1]:
					if ele not in index_same_part:
						tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
				tmpstr+=(" + v_"+str(contained_Z_index_1))
				tmpstr=tmpstr[3:]
				if tmpstr=="":
					tmpstr="m2 = TR_"+str(contained_Z_index_1)
				else:
					tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
				this_Comb.append(tmpstr)
				
				for ele in index_same_part:
					if ele!=bZ:
						tmpstr=("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = u_"+str(contained_Z_index_2)+"_"+str(ele)+" + u_"+str(contained_Z_index_1)+"_"+str(ele))
						this_Comb.append(tmpstr)
						
						tmpstr="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" >= m1"
						this_Comb.append(tmpstr)
						
						tmpstr="uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" >= m2"
						this_Comb.append(tmpstr)
				
				if not Check_Repeat(all_need_considered_combs,this_Comb):
					all_need_considered_combs.append(this_Comb)
				
					print(this_Comb)
					print()
					
					extra_label_index="_aa_"+str(bZ)
					for i in index_same_part:
						extra_label_index+=("_"+str(i))
					
					m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
					f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
					
					len_diff=m1_len-var_len_arr[contained_Z_index_2]
					if len_diff>0:
						zero_add="0b"
						for j in range(len_diff):
							zero_add+="0"
						zero_add+="@"
					else:
						zero_add=""
					tmpstr=""
					for ele in u_var_arr[contained_Z_index_2]:
						if ele not in index_same_part:
							tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
					tmpstr+=(" , "+zero_add+"v_"+str(contained_Z_index_2))
					if tmpstr=="":
						tmpstr=m1_var
					else:
						tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
					f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
					f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
					
					m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
					f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
					
					tmpstr=""
					for ele in u_var_arr[contained_Z_index_1]:
						if ele not in index_same_part:
							tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
					tmpstr+=(" , v_"+str(contained_Z_index_1))
					if tmpstr=="":
						tmpstr=m2_var
					else:
						tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
					f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
					f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
					
					m1plusm2_var="m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
					m1plusm2_len=1+var_len_arr[contained_Z_index_1]
					f.write("m1plusm2_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index+" : BITVECTOR("+str(m1plusm2_len)+"); \n")
					
					f.write("ASSERT( "+m1plusm2_var+" = BVPLUS("+str(m1plusm2_len)+", 0b0@"+m1_var+", 0b0@"+m2_var+" ) ); \n")
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m1_var+" ) ); \n")
					f.write("ASSERT( BVGE( "+m1plusm2_var+" , 0b0@"+m2_var+" ) ); \n")
					
					uhat_var_arr=[]
					for ele in index_same_part:
						if ele!=bZ:
							uhat_var_arr.append(("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)))
					uhat_var_len=1+var_len_arr[contained_Z_index_1]
					
					total_len=len_compute(math.log(1+len(index_same_part)-1,2))+m1plusm2_len
					len_diff=total_len-m1plusm2_len
					if len_diff>0:
						zero_add="0b"
						for j in range(len_diff):
							zero_add+="0"
						zero_add+="@"
					else:
						zero_add=""
					tmpstr=""
					for ele in uhat_var_arr:
						tmpstr+=(", "+zero_add+ele)
						f.write("ASSERT( BVGE( "+m1plusm2_var+" , "+ele+" ) ); \n")
					if len(uhat_var_arr)>=2:
						f.write("ASSERT( "+zero_add+m1plusm2_var+" = BVPLUS("+str(total_len)+tmpstr+") ); \n")
					else:
						f.write("ASSERT( "+zero_add+m1plusm2_var+" = "+(tmpstr[2:])+" ); \n")
					
					max_v=(d**(max_degree_z[contained_Z_index]))
					uhat_max_p=math.floor(math.log(max_v,p))
					
					Special_Comb_D4(m1_var, m1_len, m2_var, m2_len, m1plusm2_var, uhat_var_arr, uhat_var_len, uhat_max_p)

basic_Z_index=[i for i in range(group_num)]
for target_z_index in tmpTargetZ:
	
	TargetZ=target_z_index
	
	str_pos=""
	for j in active_pos:
		str_pos+=("_"+str(j))
	
	file_name="gmimc_nyb_"+str(p)+"_"+str(d)+"_"+str(n)+"_"+str(s)+"_"+str(R)+"_"+str(TargetZ)+"_pos"+str_pos

	f=open(file_name+".cvc","w")

	contain_Z=[TargetZ]
	tmp_arr=[TargetZ]
	while len(tmp_arr)>=1:
		tmp_arr.sort()
		this_z_arr=str(ZList_BeforeS[int(tmp_arr[-1])]).replace(" ","").split("+")
		for ele in this_z_arr:
			if 'Z' in ele:
				this_tmp=int( (ele.split("_"))[1] )
				if this_tmp not in contain_Z:
					contain_Z.append( this_tmp )
				if this_tmp not in tmp_arr:
					tmp_arr.append( this_tmp )
		contain_Z.sort()
		tmp_arr.sort()
		tmp_arr.pop()
		
	#print(TargetZ, contain_Z)
	
	#basic vars
	var_len_arr={}
	z_index={}
	u_var_arr={}
	for contained_Z_index in contain_Z:
		
		tmpstr=str(ZList_BeforeS[contained_Z_index]).replace(" ","").split("+")[1:]
		#print(tmpstr)
		
		this_z_index=[]
		for ele in tmpstr:
			x=int(ele.split("_")[1])
			this_z_index.append(x)
		z_index[contained_Z_index]=this_z_index
		
		max_v=(len(this_z_index)+1)*(d**(max_degree_z[contained_Z_index]))
		var_len=len_compute( math.log(max_v,2) )
		
		if var_len<math.ceil( math.log(p-1,2) ):
			var_len=math.ceil( math.log(p-1,2) )
		
		var_len_arr[contained_Z_index]=var_len
		
		f.write("v_"+str(contained_Z_index)+" : BITVECTOR("+str(var_len)+"); \n")
		
		this_u_var=[]
		for ele in tmpstr:
			x=int(ele.split("_")[1])
			
			f.write("u_"+str(contained_Z_index)+"_"+str(x)+" : BITVECTOR("+str(var_len)+"); \n")
			this_u_var.append(x)
		
		u_var_arr[contained_Z_index]=this_u_var
		
		f.write("this_right_"+str(contained_Z_index)+" : BITVECTOR("+str(var_len)+"); \n")

	f.write("\n")
	
	#basic conditions I: relations
	for contained_Z_index in contain_Z:
		if len(z_index[contained_Z_index])>0:
			this_left=", v_"+str(contained_Z_index)
			f.write("ASSERT( BVGE( this_right_"+str(contained_Z_index)+", v_"+str(contained_Z_index)+") ); \n")
			for x in z_index[contained_Z_index]:
				this_left+=(", u_"+str(contained_Z_index)+"_"+str(x))
				f.write("ASSERT( BVGE( this_right_"+str(contained_Z_index)+", u_"+str(contained_Z_index)+"_"+str(x)+") ); \n")
			f.write("ASSERT( BVPLUS("+str( var_len_arr[contained_Z_index] )+this_left+") = this_right_"+str(contained_Z_index)+" ); \n")
		else:
			f.write("ASSERT( this_right_"+str(contained_Z_index)+" = v_"+str(contained_Z_index)+" ); \n")
		
		if contained_Z_index==TargetZ:
			this_right=int2binstr(d,var_len_arr[contained_Z_index])
		else:
			tmp_this_right=""
			for i in contain_Z:
				if contained_Z_index in z_index[i]:
					len_diff=var_len_arr[contained_Z_index]-var_len_arr[i]
					if len_diff>0:
						zero_add="0b"
						for j in range(len_diff):
							zero_add+="0"
						zero_add+="@"
					else:
						zero_add=""
					tmp_this_right+=(", "+zero_add+"u_"+str(i)+"_"+str(contained_Z_index))
					f.write("ASSERT( BVGE( this_right_"+str(contained_Z_index)+" , "+zero_add+"u_"+str(i)+"_"+str(contained_Z_index)+" ) );\n")
					
			this_right=""
			for j in range(d):
				this_right+=tmp_this_right
			
			this_right="BVPLUS("+str(var_len_arr[contained_Z_index])+this_right+")"
			
		f.write("ASSERT( this_right_"+str(contained_Z_index)+" = "+this_right+" ); \n")
		
		f.write("\n")

	#basic conditions II: combinations not zero mod p using Lucas Theorem
	for contained_Z_index in contain_Z:
		max_v=(d**(max_degree_z[contained_Z_index]))
		if max_v>p-1 and contained_Z_index not in basic_Z_index:
			max_p=math.floor(math.log(max_v,p))
			cur_len=len_compute( math.log(p**(max_p+1),2) )
			
			if cur_len<var_len_arr[contained_Z_index]:
				cur_len=var_len_arr[contained_Z_index]
			
			each_len=len_compute( math.log(p-1,2) )
			for comb_part in range(max_p+1):
				f.write("this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
				f.write("ASSERT( BVLE( this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
				
				f.write("vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
				f.write("ASSERT( BVLE( vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
				for x in z_index[contained_Z_index]:
					f.write("up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
					f.write("ASSERT( BVLE( up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")
			
			len_diff=cur_len-each_len
			if len_diff>0:
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			else:
				zero_add=""
			
			len_diff=cur_len-var_len_arr[contained_Z_index]
			if len_diff>0:
				zero_add_2="0b"
				for j in range(len_diff):
					zero_add_2+="0"
				zero_add_2+="@"
			else:
				zero_add_2=""
			
			right_hand=""
			for comb_part in range(max_p+1):
				if comb_part==0:
					right_hand+=(", "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+"")
					f.write("ASSERT( BVGE( "+zero_add_2+"this_right_"+str(contained_Z_index)+", "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+" ) ); \n")
				else:					
					right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
					f.write("ASSERT( BVGE( "+zero_add_2+"this_right_"+str(contained_Z_index)+", BVMULT("+str(cur_len)+", "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
			
			if max_p>=1:
				f.write("ASSERT( "+zero_add_2+"this_right_"+str(contained_Z_index)+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
			else:
				f.write("ASSERT( "+zero_add_2+"this_right_"+str(contained_Z_index)+" = "+(right_hand[2:])+" ); \n")
			
			right_hand=""
			for comb_part in range(max_p+1):
				if comb_part==0:
					right_hand+=(", "+zero_add+"vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+"")
					f.write("ASSERT( BVGE( "+zero_add_2+"v_"+str(contained_Z_index)+", "+zero_add+"vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+" ) ); \n")
				else:					
					right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+"vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
					f.write("ASSERT( BVGE( "+zero_add_2+"v_"+str(contained_Z_index)+", BVMULT("+str(cur_len)+", "+zero_add+"vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
			
			if max_p>=1:
				f.write("ASSERT( "+zero_add_2+"v_"+str(contained_Z_index)+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
			else:
				f.write("ASSERT( "+zero_add_2+"v_"+str(contained_Z_index)+" = "+(right_hand[2:])+" ); \n")
			
			for x in z_index[contained_Z_index]:			
				right_hand=""
				for comb_part in range(max_p+1):
					if comb_part==0:
						right_hand+=(", "+zero_add+"up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+"")
						f.write("ASSERT( BVGE( "+zero_add_2+"u_"+str(contained_Z_index)+"_"+str(x)+", "+zero_add+"up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+" ) ); \n")
					else:
						right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+"up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
						f.write("ASSERT( BVGE( "+zero_add_2+"u_"+str(contained_Z_index)+"_"+str(x)+", BVMULT("+str(cur_len)+", "+zero_add+"up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
				
				if max_p>=1:
					f.write("ASSERT( "+zero_add_2+"u_"+str(contained_Z_index)+"_"+str(x)+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
				else:
					f.write("ASSERT( "+zero_add_2+"u_"+str(contained_Z_index)+"_"+str(x)+" = "+(right_hand[2:])+" ); \n")
			
			#print(contained_Z_index,z_index[contained_Z_index],len(z_index[contained_Z_index]))
			sum_each_len=len_compute( math.log((len(z_index[contained_Z_index])+1)*(p-1),2) )
			
			len_diff=sum_each_len-each_len
			if len_diff>0:
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			else:
				zero_add=""
			
			for comb_part in range(max_p+1):
				right_hand=", "+zero_add+"vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+""
				f.write("ASSERT( BVGE( this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+", vp_"+str(contained_Z_index)+"_p_"+str(comb_part)+") ); \n")
				for x in z_index[contained_Z_index]:
					right_hand+=(", "+zero_add+"up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+"")
					f.write("ASSERT( BVGE( this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+", up_"+str(contained_Z_index)+"_"+str(x)+"_p_"+str(comb_part)+") ); \n")
				if max_p>=1:
					f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+" = BVPLUS("+str(sum_each_len)+right_hand+") ); \n")
				else:
					f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index)+"_p_"+str(comb_part)+" = "+(right_hand[2:])+" ); \n")
		f.write("\n")
	f.write("\n")
	
	#target vars and conditions
	for contained_Z_index in contain_Z:
		f.write("Fv_"+str(contained_Z_index)+" : BITVECTOR("+str(var_len_arr[contained_Z_index])+"); \n")
		
		max_len=len_compute( math.log(p-1,2) )
		zero_add=""
		if max_len<=var_len_arr[contained_Z_index]:
			max_len=var_len_arr[contained_Z_index]
		else:
			len_diff=max_len-var_len_arr[contained_Z_index]
			zero_add="0b"
			for j in range(len_diff):
				zero_add+="0"
			zero_add+="@"
		
		f.write("ASSERT( IF ((BVGE("+zero_add+"v_"+str(contained_Z_index)+","+int2binstr(p-1,max_len)+")) AND (BVMOD("+str(max_len)+","+zero_add+"v_"+str(contained_Z_index)+","+int2binstr(p-1,max_len)+")="+int2binstr(0,max_len)+")) THEN "+zero_add+"Fv_"+str(contained_Z_index)+"="+int2binstr(p-1,max_len)+" ELSE "+zero_add+"Fv_"+str(contained_Z_index)+"=BVMOD("+str(max_len)+","+zero_add+"v_"+str(contained_Z_index)+","+int2binstr(p-1,max_len)+") ENDIF ); \n")

	f.write("\n")

	condition_Fv={}
	for w in active_pos:
		tmpFv=[]
		for contained_Z_index in contain_Z:
			if contained_Z_index in index_each_x[w]:
				tmpFv.append(contained_Z_index)
		condition_Fv[w]=tmpFv
	
	for w in active_pos:
		max_len=len_compute( math.log(p-1,2) )
		if len(condition_Fv[w])>1:
			for ele in condition_Fv[w]:
				this_len=var_len_arr[ ele ]
				if this_len>max_len:
					max_len=this_len
			max_len+=len_compute(math.log(len(condition_Fv[w]),2))
			
			f.write("sumFv_"+str(w)+" : BITVECTOR("+str(max_len)+");\n")
			
			sumFv=""
			for ele in condition_Fv[w]:
				len_diff=max_len-var_len_arr[ ele ]
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
				sumFv+=(", "+zero_add+"Fv_"+str(ele))
				f.write("ASSERT( BVGE( sumFv_"+str(w)+" , "+zero_add+"Fv_"+str(ele)+" ) ); \n")
			
			f.write("ASSERT( sumFv_"+str(w)+" = BVPLUS("+str(max_len)+sumFv+") ); \n")
			f.write("ASSERT( BVGE( sumFv_"+str(w)+" , "+int2binstr(p-1,max_len)+") ); \n")
			
		else:
			this_len=var_len_arr[ condition_Fv[w][0] ]
			if max_len<=this_len:
				max_len=this_len
				zero_add=""
			else:
				len_diff=max_len-this_len
				zero_add="0b"
				for j in range(len_diff):
					zero_add+="0"
				zero_add+="@"
			f.write("ASSERT( "+zero_add+"Fv_"+str(condition_Fv[w][0])+"="+int2binstr(p-1,max_len)+" ); \n")
		f.write("\n")
	f.write("\n")
	
	all_need_considered_combs=[]

	#List all possible cancellation within one Comb
	for bZ in basic_Z_index:
		for contained_Z_index in contain_Z:
			if contained_Z_index not in basic_Z_index:
				max_v=(d**(max_degree_z[contained_Z_index]))
				if max_v>p-1:
					#construct the input of Special_Comb_D1
					if bZ in z_index[contained_Z_index]:
						m1_minused_part=[]
						for ele in z_index[contained_Z_index]:
							if ele!=bZ:
								m1_minused_part.append(ele)
						
						m2_part=[]
						for tmp_cZ in contain_Z:
							if tmp_cZ!=contained_Z_index and bZ in z_index[tmp_cZ]:
								m2_part.append(tmp_cZ)
						
						this_Comb=["MultiComb( m1, [v_"+str(contained_Z_index)+" , u_"+str(contained_Z_index)+"_"+str(bZ)+"])","v_"+str(contained_Z_index)+" + u_"+str(contained_Z_index)+"_"+str(bZ)+" = m1", "v_"+str(bZ)+" = d*u_"+str(contained_Z_index)+"_"+str(bZ)+" + m2","Fv_"+str(contained_Z_index),"Fv_"+str(bZ)]
						
						tmpstr=""
						for ele in m1_minused_part:
							tmpstr+=(" + u_"+str(contained_Z_index)+"_"+str(ele))
						tmpstr=tmpstr[3:]
						if tmpstr=="":
							tmpstr="m1 = TR_"+str(contained_Z_index)
						else:
							tmpstr="m1 = TR_"+str(contained_Z_index)+" - ("+tmpstr+")"
						this_Comb.append(tmpstr)
						
						tmpstr=""
						for ele in m2_part:
							tmpstr+=(" + u_"+str(ele)+"_"+str(bZ))
						tmpstr=tmpstr[3:]
						if len(m2_part)>=1:
							tmpstr=("m2 = d*("+tmpstr+")")
						else:
							tmpstr=("m2 = 0")
						this_Comb.append(tmpstr)
						
						if not Check_Repeat(all_need_considered_combs,this_Comb):
							all_need_considered_combs.append(this_Comb)
						
							print(this_Comb)
							print()
							
							m1_var="m1_r_"+str(bZ)+"_"+str(contained_Z_index)
							m1_len=var_len_arr[contained_Z_index]
							f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
							
							tmpstr=""
							for ele in m1_minused_part:
								tmpstr+=(" , u_"+str(contained_Z_index)+"_"+str(ele))
							if tmpstr=="":
								tmpstr=m1_var
							else:
								tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
							
							f.write("ASSERT( this_right_"+str(contained_Z_index)+" = "+tmpstr+" ); \n")
							f.write("ASSERT( BVLE( "+m1_var+" , this_right_"+str(contained_Z_index)+" ) ); \n")
							
							m2_var="m2_r_"+str(bZ)+"_"+str(contained_Z_index)
							m2_len=var_len_arr[contained_Z_index]+len_compute( math.log(d,2) )
							f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
							
							max_len_here=m2_len
							for ele in m2_part:
								if var_len_arr[ele]>max_len_here:
									max_len_here=var_len_arr[ele]
							tmpstr=""
							for ele in m2_part:
								len_diff=max_len_here-var_len_arr[ele]
								if len_diff>0:
									zero_add="0b"
									for j in range(len_diff):
										zero_add+="0"
									zero_add+="@"
								else:
									zero_add=""
								
								len_diff=max_len_here-m2_len
								if len_diff>0:
									zero_add2="0b"
									for j in range(len_diff):
										zero_add2+="0"
									zero_add2+="@"
								else:
									zero_add2=""
								for j in range(d):
									tmpstr+=(" , "+zero_add+"u_"+str(ele)+"_"+str(bZ))
								f.write("ASSERT( BVGE( "+zero_add2+m2_var+" , "+zero_add+"u_"+str(ele)+"_"+str(bZ)+" ) ); \n")
							if len(m2_part)>=1:
								f.write("ASSERT( "+zero_add2+m2_var+" = BVPLUS( "+str(max_len_here)+tmpstr+" ) ); \n")
							else:
								f.write("ASSERT( "+m2_var+" = "+int2binstr(0,m2_len)+" ); \n")
							
							Fv1_var="Fv_"+str(contained_Z_index)
							Fv1_var_len=var_len_arr[contained_Z_index]
							
							Fv0_var="Fv_"+str(bZ)
							Fv0_var_len=var_len_arr[bZ]
							
							Special_Comb_D1(contained_Z_index, bZ, m1_var, m1_len, m2_var, m2_len, Fv1_var, Fv1_var_len, Fv0_var, Fv0_var_len)

	#List all possible cancellation within two Combs
	#Within each, list all need-to-considered forms when fixing some vars
	for bZ in basic_Z_index:
		for contained_Z_index_1 in contain_Z:
			if contained_Z_index_1 not in basic_Z_index:
				max_v_1=(d**(max_degree_z[contained_Z_index_1]))
				if max_v_1>p-1:
					for contained_Z_index_2 in contain_Z:
						if contained_Z_index_2 not in basic_Z_index and contained_Z_index_2>contained_Z_index_1:
							max_v_2=(d**(max_degree_z[contained_Z_index_2]))
							if max_v_2>p-1:
								
								all_possible=[]
								
								index_same_part=[]
								for ele in u_var_arr[contained_Z_index_1]:
									if ele in u_var_arr[contained_Z_index_2]:
										index_same_part.append(ele)
								
								print(contained_Z_index_1,u_var_arr[contained_Z_index_1])
								print(contained_Z_index_2,u_var_arr[contained_Z_index_2])
								print("same_part :		 ",index_same_part)
								print()
								
								#claim all uhat_vars
								for ele in index_same_part:
									if ele!=bZ:
										f.write("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" : BITVECTOR("+str((1+var_len_arr[contained_Z_index_1]))+"); \n")
										
										len_diff=1+var_len_arr[contained_Z_index_1]-var_len_arr[contained_Z_index_2]
										if len_diff>0:
											zero_add="0b"
											for j in range(len_diff):
												zero_add+="0"
											zero_add+="@"
										else:
											zero_add=""
										f.write("ASSERT( uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = BVPLUS("+str((1+var_len_arr[contained_Z_index_1]))+", 0b0@u_"+str(contained_Z_index_1)+"_"+str(ele)+", "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele)+" ) ); \n")
										f.write("ASSERT( BVGE( uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" , 0b0@u_"+str(contained_Z_index_1)+"_"+str(ele)+" ) ); \n")
										f.write("ASSERT( BVGE( uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele)+" ) ); \n")
										f.write("\n")
										
										#split uhat vars into p-adic
										max_v=(d**(max_degree_z[contained_Z_index_1]))
										max_p=math.floor(math.log(max_v,p)) 
										cur_len=len_compute( math.log(p**(max_p+1),2) )#length of uhat_var in p-adic
										
										if cur_len<var_len_arr[contained_Z_index_1]+1:
											cur_len=var_len_arr[contained_Z_index_1]+1
										
										each_len=len_compute( math.log(p-1,2) )
										for comb_part in range(max_p+1):
											f.write("uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+" : BITVECTOR("+str(each_len)+"); \n")
											f.write("ASSERT( BVLE( uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+", "+int2binstr(p-1,each_len)+") ); \n")

										len_diff=cur_len-each_len
										if len_diff>0:
											zero_add="0b"
											for j in range(len_diff):
												zero_add+="0"
											zero_add+="@"
										else:
											zero_add=""
										
										len_diff=cur_len-var_len_arr[contained_Z_index_1]-1
										if len_diff>0:
											zero_add_2="0b"
											for j in range(len_diff):
												zero_add_2+="0"
											zero_add_2+="@"
										else:
											zero_add_2=""
										
										right_hand=""
										for comb_part in range(max_p+1):
											if comb_part==0:
												right_hand+=(", "+zero_add+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+"")
												f.write("ASSERT( BVGE( "+zero_add_2+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+", "+zero_add+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+" ) ); \n")
											else:					
												right_hand+=(", BVMULT("+str(cur_len)+", "+zero_add+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" )")
												f.write("ASSERT( BVGE( "+zero_add_2+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+", BVMULT("+str(cur_len)+", "+zero_add+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+"_p_"+str(comb_part)+", "+int2binstr(p**comb_part,cur_len)+" ) ) ); \n")
										if max_p>=1:
											f.write("ASSERT( "+zero_add_2+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = BVPLUS("+str(cur_len)+right_hand+") ); \n")
										else:
											f.write("ASSERT( "+zero_add_2+"uhat_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+"_"+str(ele)+" = "+(right_hand[2:])+" ); \n")
										f.write("\n")
								
								if len(index_same_part)>0:
									if len(index_same_part)==1:
										if bZ in index_same_part:#form is [v,u_*_0]
											this_Comb=["MultiComb( m1, [v_"+str(contained_Z_index_2)+" , u_"+str(contained_Z_index_2)+"_"+str(bZ)+"]) * MultiComb( m2, [v_"+str(contained_Z_index_1)+" , u_"+str(contained_Z_index_1)+"_"+str(bZ)+"])","v_"+str(contained_Z_index_2)+" + u_"+str(contained_Z_index_2)+"_"+str(bZ)+" = m1","v_"+str(contained_Z_index_1)+" + u_"+str(contained_Z_index_1)+"_"+str(bZ)+" = m2","v_"+str(bZ)+" = d*(u_"+str(contained_Z_index_2)+"_"+str(bZ)+" + u_"+str(contained_Z_index_1)+"_"+str(bZ)+") + m3","Fv_"+str(contained_Z_index_2),"Fv_"+str(contained_Z_index_1),"Fv_"+str(bZ)]
											
											tmpstr=""
											for ele in u_var_arr[contained_Z_index_2]:
												if ele not in index_same_part:
													tmpstr+=(" + u_"+str(contained_Z_index_2)+"_"+str(ele))
											tmpstr=tmpstr[3:]
											if tmpstr=="":
												tmpstr="m1 = TR_"+str(contained_Z_index_2)
											else:
												tmpstr="m1 = TR_"+str(contained_Z_index_2)+" - ("+tmpstr+")"
											this_Comb.append(tmpstr)
											
											tmpstr=""
											for ele in u_var_arr[contained_Z_index_1]:
												if ele not in index_same_part:
													tmpstr+=(" + u_"+str(contained_Z_index_1)+"_"+str(ele))
											tmpstr=tmpstr[3:]
											if tmpstr=="":
												tmpstr="m2 = TR_"+str(contained_Z_index_1)
											else:
												tmpstr="m2 = TR_"+str(contained_Z_index_1)+" - ("+tmpstr+")"
											this_Comb.append(tmpstr)
											
											m3_part=[]
											for tmp_cZ in contain_Z:
												if tmp_cZ!=contained_Z_index_1 and tmp_cZ!=contained_Z_index_2 and bZ in z_index[tmp_cZ]:
													m3_part.append(tmp_cZ)
											
											tmpstr=""
											for ele in m3_part:
												tmpstr+=(" + u_"+str(ele)+"_"+str(bZ))
											tmpstr=tmpstr[3:]
											if len(m3_part)>=1:
												tmpstr=("m3 = d*("+tmpstr+")")
											else:
												tmpstr=("m3 = 0")
											this_Comb.append(tmpstr)
											
											if not Check_Repeat(all_need_considered_combs,this_Comb):
												all_need_considered_combs.append(this_Comb)
											
												print(this_Comb)
												print()
												
												extra_label_index="_v0_"+str(bZ)
												for i in index_same_part:
													extra_label_index+=("_"+str(i))
												
												m1_var="m1_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
												m1_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
												f.write(m1_var+" : BITVECTOR("+str(m1_len)+"); \n")
												
												len_diff=m1_len-var_len_arr[contained_Z_index_2]
												if len_diff>0:
													zero_add="0b"
													for j in range(len_diff):
														zero_add+="0"
													zero_add+="@"
												else:
													zero_add=""
												tmpstr=""
												for ele in u_var_arr[contained_Z_index_2]:
													if ele not in index_same_part:
														tmpstr+=(" , "+zero_add+"u_"+str(contained_Z_index_2)+"_"+str(ele))
												if tmpstr=="":
													tmpstr=m1_var
												else:
													tmpstr=("BVPLUS( "+str(m1_len)+", "+m1_var+tmpstr+" )")
												f.write("ASSERT( "+zero_add+"this_right_"+str(contained_Z_index_2)+" = "+tmpstr+" ); \n")
												f.write("ASSERT( BVLE( "+m1_var+" , "+zero_add+"this_right_"+str(contained_Z_index_2)+" ) ); \n")
												
												m2_var="m2_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
												m2_len=var_len_arr[contained_Z_index_1]#var_len_arr[contained_Z_index_2] <= var_len_arr[contained_Z_index_1]
												f.write(m2_var+" : BITVECTOR("+str(m2_len)+"); \n")
												
												tmpstr=""
												for ele in u_var_arr[contained_Z_index_1]:
													if ele not in index_same_part:
														tmpstr+=(" , u_"+str(contained_Z_index_1)+"_"+str(ele))
												if tmpstr=="":
													tmpstr=m2_var
												else:
													tmpstr=("BVPLUS( "+str(m2_len)+", "+m2_var+tmpstr+" )")
												f.write("ASSERT( this_right_"+str(contained_Z_index_1)+" = "+tmpstr+" ); \n")
												f.write("ASSERT( BVLE( "+m2_var+" , this_right_"+str(contained_Z_index_1)+" ) ); \n")
												
												m3_var="m3_rr_"+str(bZ)+"_"+str(contained_Z_index_1)+"_"+str(contained_Z_index_2)+extra_label_index
												m3_len=var_len_arr[bZ]+len_compute( math.log(d,2) )
												f.write(m3_var+" : BITVECTOR("+str(m3_len)+"); \n")
												
												max_len_here=m3_len
												for ele in m3_part:
													if var_len_arr[ele]>max_len_here:
														max_len_here=var_len_arr[ele]
												tmpstr=""
												for ele in m3_part:
													len_diff=max_len_here-var_len_arr[ele]
													if len_diff>0:
														zero_add="0b"
														for j in range(len_diff):
															zero_add+="0"
														zero_add+="@"
													else:
														zero_add=""
													
													len_diff=max_len_here-m3_len
													if len_diff>0:
														zero_add2="0b"
														for j in range(len_diff):
															zero_add2+="0"
														zero_add2+="@"
													else:
														zero_add2=""
													for j in range(d):
														tmpstr+=(" , "+zero_add+"u_"+str(ele)+"_"+str(bZ))
													f.write("ASSERT( BVGE( "+zero_add2+m3_var+" , "+zero_add+"u_"+str(ele)+"_"+str(bZ)+" ) ); \n")
												if len(m3_part)>=1:
													f.write("ASSERT( "+zero_add2+m3_var+" = BVPLUS( "+str(max_len_here)+tmpstr+" ) ); \n")
												else:
													f.write("ASSERT( "+m3_var+" = "+int2binstr(0,m3_len)+" ); \n")
												
												Fv2_var="Fv_"+str(contained_Z_index_2)
												Fv2_var_len=var_len_arr[contained_Z_index_2]
												
												Fv1_var="Fv_"+str(contained_Z_index_1)
												Fv1_var_len=var_len_arr[contained_Z_index_1]
												
												Fv0_var="Fv_"+str(bZ)
												Fv0_var_len=var_len_arr[bZ]
												
												Special_Comb_D2(contained_Z_index_1,contained_Z_index_2, bZ, m1_var, m1_len, m2_var, m2_len, m3_var, m3_len, Fv2_var, Fv2_var_len, Fv1_var, Fv1_var_len, Fv0_var, Fv0_var_len, extra_label_index)
											
									else:
										List_All(index_same_part,all_need_considered_combs,contained_Z_index_1,contained_Z_index_2,bZ)


	print(len(all_need_considered_combs))

	f.write("QUERY(FALSE); \n")
	f.write("COUNTEREXAMPLE; \n")

	f.close()


'''
if final_ZS:
	print("Our INT: DisRound = "+str((n-s+R+n-1))+" with s="+str(s)+", where R="+str(R))
	print("PreCRYPTO(Block cipher usage) INT is : DisRound ="+str((2*n-2+math.floor(math.log(p-2,d))))+" with s=1, where R="+str(math.floor((math.log(p-2,d)))))
	print("PreChen INT is : DisRound= "+str((3*n-3))+" with s="+str((n-1))+".")
	print("PreCRYPTO TDC is : DisRound="+str((n**2-n-2))+" with s="+str((n-2))+".")

print("Done!")
#'''

	
	
	
	

















	
