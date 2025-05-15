import sys, math, os
import gurobipy as gp
from gurobipy import GRB

def c(n,m):
	if n>=m:
		return math.factorial(n)//(math.factorial(m)*math.factorial(n-m))
	else:
		return 0

def Lucas(n, m, p):
    if m == 0:
        return 1
    return (c(n % p, m % p) * Lucas(n // p, m // p, p)) % p

def check_comb(y,p):
	t_bound=math.floor(y/(p-1))
	#print("RE ",y,p-1,y/(p-1),t_bound)
	sum=0
	for i in range(1,t_bound+1):
		sum+=Lucas(y,i*(p-1),p)
		sum%=p
	#print("RE ",sum)
	if sum!=0:
		return False
	else:
		return True
		
def check_multinomial(n, list_m, p):
	result=1
	for ele in list_m:
		result*=Lucas(n,ele,p)
		n-=ele
		if result==0:
			break
	if result==0:
		return True
	else:
		return False

p=int(sys.argv[1])

d=int(sys.argv[2])
n=int(sys.argv[3])

s=int(sys.argv[4])

R1=int(sys.argv[5])
R2=int(sys.argv[6])
R3=int(sys.argv[7])

total_round=R1+R2+R3

L=int(sys.argv[8])

str_eq_2_term=sys.argv[9]

str_list=str_eq_2_term.split("_")

eq_2_term=[[0 for i in range(s)] for j in range(L)]
for j in range(L):
	for i in range(s):
		eq_2_term[j][i]=str_list[s*j+i]

for ele in eq_2_term:
	print("RE ",ele)
print("RE ")

gp.setParam("LogToConsole", 0)

# Create a new model
m = gp.Model("bound_detect")

# Create variables
v_var=[]
for r in range(R2-1):
	v_var.append( m.addVar(0, vtype=GRB.INTEGER, name="v_"+str(r)) )

u_var=[[] for r in range(R2-1)]
for r in range(R2-1):
	for j in range(1,R2-r):
		u_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="u_"+str(r)+"_"+str(j)) )

g_var=[[] for r in range(R2)]
for r in range(R2):
	if r==R2-1:
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_1") )
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_0") )
	else:
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_"+str((R2-r))) )

total_degree_bound=m.addVar(0, vtype=GRB.INTEGER, name="td")

# Add constraints
for r in range(R2):
	if r==R2-1:
		left_side=g_var[r][0]+g_var[r][1]
	else:
		left_side=v_var[r]+g_var[r][0]
		for j in range(1,R2-r):
			left_side+=u_var[r][j-1]
	
	if r==0:
		right_side=d**R3
	else:
		right_side=0
		for j in range(r):
			right_side+=d*u_var[j][R2-r-1]
	
	if r==0:
		m.addConstr(left_side<=right_side)
	else:	
		m.addConstr(left_side==right_side)

right_side=0
for r in range(R2-1):
	right_side+=v_var[r]
right_side=d*(g_var[R2-1][1]+right_side)
for r in range(R2):
	right_side+=g_var[r][0]
m.addConstr(total_degree_bound==right_side,"ceq")

# Set objective
m.setObjective(total_degree_bound, GRB.MAXIMIZE)

# Optimize model
m.optimize()

for v in m.getVars():
	print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

thv=round( m.objVal )

print("RE","thv",thv)

delete_type=[]
all_records=[]

# Create a new model
m = gp.Model("step1_check")

# Create variables
max_t=math.floor((d**R1)*thv/(p-1))+1-s
print("RE max_t",max_t)

if max_t>=p**2 or (d**R1)*thv>=p**3:
	print("RE Code Need to be Modified")
	sys.exit(0)

#vars
start_consider_R2=0
for r in range(R2):
	if d**(R3+r)>=p-1:
		start_consider_R2=r
		break
print("RE start_consider_R2",start_consider_R2)

max_comb_value=thv
if thv<d**(R3+R2-1):
	max_comb_value=d**(R3+R2-1)
comb_part=math.floor(math.log(max_comb_value,p))
print("RE comb_part",comb_part)

v_var=[]
for r in range(R2-1):
	v_var.append( m.addVar(0, vtype=GRB.INTEGER, name="v_"+str(r)) )

u_var=[[] for r in range(R2-1)]
for r in range(R2-1):
	for j in range(1,R2-r):
		u_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="u_"+str(r)+"_"+str(j)) )

g_var=[[] for r in range(R2)]
for r in range(R2):
	if r==R2-1:
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_1") )
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_0") )
	else:
		g_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="g_"+str(r)+"_"+str((R2-r))) )

sum_var=[]
for r in range(start_consider_R2,R2):
	sum_var.append( m.addVar(0, vtype=GRB.INTEGER, name="sum_"+str(r)) )

w_var=[]
for r in range(R2+1):
	w_var.append( m.addVar(0, vtype=GRB.INTEGER, name="w_"+str(r)) )

h_var=[[] for r in range(R2+1)]
for r in range(R2+1):
	for j in range(L):
		h_var[r].append( m.addVar(0, vtype=GRB.INTEGER, name="h_"+str(r)+"_"+str(j)) )

m_var=[]
for j in range(L):
	m_var.append( m.addVar(0, vtype=GRB.INTEGER, name="m_"+str(j)) )

degree_y_var=[]
for i in range(s):
	degree_y_var.append( m.addVar(0, vtype=GRB.INTEGER, name="dy_"+str(i)) )

for i in range(s):
	right_side=0
	for j in range(L):
		tmpv=eq_2_term[j][i]
		if tmpv!=0:
			right_side+=tmpv*m_var[j]
	m.addConstr( degree_y_var[i]==right_side )

for r in range(R2):
	if r==R2-1:
		left_side=g_var[r][0]+g_var[r][1]
	else:
		left_side=v_var[r]+g_var[r][0]
		for j in range(1,R2-r):
			left_side+=u_var[r][j-1]
	
	if r==0:
		right_side=d**R3
	else:
		right_side=0
		for j in range(r):
			right_side+=d*u_var[j][R2-r-1]
	
	if r==0:
		m.addConstr(left_side<=right_side)
	else:	
		m.addConstr(left_side==right_side)
	
	if r>=start_consider_R2:
		m.addConstr( left_side==sum_var[r-start_consider_R2], "c2"+str(r) )

for r in range(R2+1):
	if r==R2:
		right_side=0
		for j in range(R2-1):
			right_side+=v_var[j]
		right_side=d*(g_var[R2-1][1]+right_side)
	else:
		right_side=g_var[r][0]
	
	m.addConstr( w_var[R2-r]==right_side, "cw"+str(r) )

for r in range(R2+1):
	m.addConstr( w_var[r]==sum(h_var[r]), "cw2"+str(r) )

for j in range(L):
	right_side=0
	for r in range(R2+1):
		right_side+=h_var[r][j]
	m.addConstr( m_var[j]==right_side, "cm"+str(j) )


mx_var=[]
my_var=[]
mz_var=[]
mult_var=[]
mult_m_var=[]
mult_t_var=[]
sum_xyz_1=[]
for i in range(s):
	mx_var.append( m.addVar(0, vtype=GRB.INTEGER, name="mx_"+str(i)) )
	my_var.append( m.addVar(0, vtype=GRB.INTEGER, name="my_"+str(i)) )
	mz_var.append( m.addVar(0, vtype=GRB.INTEGER, name="mz_"+str(i)) )
	mult_var.append( m.addVar(0, vtype=GRB.INTEGER, name="mult_"+str(i)) )
	mult_m_var.append( m.addVar(0, vtype=GRB.INTEGER, name="mult_m_"+str(i)) )
	mult_t_var.append( m.addVar(0, vtype=GRB.INTEGER, name="mult_t_"+str(i)) )
	sum_xyz_1.append( m.addVar(0, vtype=GRB.INTEGER, name="sum_xyz_1_"+str(i)) )

bool_var=[]
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_a") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_b") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_c") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_d") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_a2") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_b2") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_c2") )
bool_var.append( m.addVar(vtype=GRB.BINARY, name="bool_d2") )

# Add constraints
for i in range(s):
	m.addConstr( degree_y_var[i]>=p-1, "c"+str(i) )
m.addConstr( sum(degree_y_var)<=(d**R1)*thv, "c_"+str(s) )
m.addConstr( sum(degree_y_var)>=s*(p-1), "c_"+str(s+1) )

for i in range(s-1):
	m.addConstr( degree_y_var[i]<=degree_y_var[i+1] )

for i in range(s):
	m.addConstr( degree_y_var[i]==mx_var[i]*(p**2)+my_var[i]*p+mz_var[i] )
	m.addConstr( mx_var[i]<=p-1 )
	m.addConstr( my_var[i]<=p-1 )
	m.addConstr( mz_var[i]<=p-1 )
	
	m.addConstr( mult_var[i]==mult_m_var[i]*p+mult_t_var[i] )
	m.addConstr( mult_m_var[i]<=p-1 )
	m.addConstr( mult_t_var[i]<=p-1 )
	m.addConstr( mult_m_var[i]+mult_t_var[i]>=1 )
	
	#remove sum comb mod p =0 while exist comb mod p not 0
	m.addConstr( (bool_var[4]==1) >> (mx_var[i]<=p-2) )
	m.addConstr( (bool_var[4]==1) >> ((mx_var[i]+my_var[i]+mz_var[i])==sum_xyz_1[i]*(p-1)) )
	m.addConstr( (bool_var[4]==1) >> (sum_xyz_1[i]<=p-2) )
	
	m.addConstr( (bool_var[5]==1) >> (mx_var[i]==p-1) )
	m.addConstr( (bool_var[5]==1) >> (my_var[i]==0) )
	m.addConstr( (bool_var[5]==1) >> (mz_var[i]>=1) )
	
	m.addConstr( (bool_var[6]==1) >> (mx_var[i]==p-1) )
	m.addConstr( (bool_var[6]==1) >> (my_var[i]>=1) )
	
	m.addConstr( bool_var[7]==gp.or_(bool_var[4],bool_var[5],bool_var[6]) )
	m.addConstr( bool_var[7]==1 )

need_to_require=[]
for r in range(start_consider_R2,R2):
	if r==R2-1:
		this_to_require=[ sum_var[r-start_consider_R2], [g_var[r][0],g_var[r][1]] ]
	else:
		this_to_require=[ sum_var[r-start_consider_R2], [v_var[r],g_var[r][0]] ]
		for j in range(1,R2-r):
			(this_to_require[1]).append( u_var[r][j-1] )
	need_to_require.append( this_to_require )

for r in range(R2+1):
	this_to_require=[w_var[r], []]
	for j in range(L):
		(this_to_require[1]).append( h_var[r][j] )
	need_to_require.append( this_to_require )

for num in range(len(need_to_require)):
	ele=need_to_require[num]
	
	sum_part_var=[]
	for part_index in range(comb_part+1):
		sum_part_var.append( m.addVar( 0, vtype=GRB.INTEGER, name="sum_part_"+str(num)+"_"+str(part_index) ) )
	each_part_var=[]
	for j in range(len(ele[1])):
		this_part_var=[]
		for part_index in range(comb_part+1):
			this_part_var.append( m.addVar( 0, vtype=GRB.INTEGER, name="this_part_"+str(num)+"_"+str(j)+"_"+str(part_index) ) )
		each_part_var.append( this_part_var )
	
	right_side=0
	for part_index in range(comb_part+1):
		m.addConstr( sum_part_var[part_index]<=p-1 )
		right_side+=(p**part_index)*sum_part_var[part_index]
	m.addConstr( ele[0]==right_side )
	
	for j in range(len(ele[1])):
		right_side=0
		for part_index in range(comb_part+1):
			m.addConstr( each_part_var[j][part_index]<=p-1 )
			right_side+=(p**part_index)*(each_part_var[j][part_index])
		m.addConstr( ele[1][j]==right_side )
	
	for part_index in range(comb_part+1):
		right_side=0
		for j in range(len(ele[1])):
			right_side+=each_part_var[j][part_index]
		m.addConstr( sum_part_var[part_index]==right_side )

m.Params.PoolSearchMode = 1 #def: 0, sol first: 1, best sols: 2
m.Params.Threads = 16

sol_num=0

goon=True
while goon:
	m.update()
	m.optimize()
	nSol = m.SolCount
	
	if nSol>0:
		sol_num+=1
		
		print("RE sol_num =",sol_num)
		
		this_record=[]
		for i in range(s):
			v=degree_y_var[i]
			#print("RE ",i,v.x,v.x,round(v.x))
			this_record.append( round(v.x) )
		print("RE ",this_record)
		
		all_records.append(this_record)
		
		break
		
	else:
		goon=False
print("RE",all_records,len(all_records))

if len(all_records)==0:
	print("RE ZS due to no valid records.")
else:
	print("RE NotZS")

print("RE Done!")
