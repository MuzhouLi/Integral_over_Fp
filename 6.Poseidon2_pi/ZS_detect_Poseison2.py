import sys,math,os

p=int(sys.argv[1])
n=int(sys.argv[2])
s=int(sys.argv[3])
R1=int(sys.argv[4])
R2=int(sys.argv[5])
R3=int(sys.argv[6])
d=int(sys.argv[7])

R=R1+R2+R3

def C(n,m):
    if n>=m:
        return math.factorial(n)//(math.factorial(m)*math.factorial(n-m))
    else:
        return 0


def p_to_len(p):
    result=0
    while p>0:
        p=p//2
        result+=1
    return result

def dec_to_binstr(x,str_len):
    result=""
    tmp=[]
    while x>0:
        tmp.append(x%2)
        x=x//2
    tmp.reverse()
    result+="0bin"
    for i in range(str_len-len(tmp)):
        result+="0"
    for i in range(len(tmp)):
        result+=chr(tmp[i]+48)
    return result

def pad_length(var,var_len,out_len):
    if var_len==out_len:
        return var
    else:
        return "0bin{}@{}".format("0"*(out_len-var_len),var)
    
def SUM(var_list,var_len,out_len):
    result=pad_length(var_list[0],var_len[0],out_len)
    for i in range(1,len(var_list)):
        result="BVPLUS({},{},{})".format(out_len,result,pad_length(var_list[i],var_len[i],out_len))
    return result

def vector_up(x,begin):
    n=len(x)
    if begin==n-1:
        return x,0
    x,mask=vector_up(x,begin+1)
    if mask==1:
        return x,1
    if mask==0:
        deg=0
        for i in range(begin+1,n):
            deg+=x[i]
            x[i]=0
        if deg==0:
            return x,0
        x[begin]+=1
        x[n-1]=deg-1
        return x,1

def construct_Model(path):
    with open(path,'w') as f:
        
        f.write("%Variables define-----------------------------\n")
        p_len=p_to_len(p)
        
        bound_m=p**3-1+1
        bound_mask=p-1+1
        bound_e=d**(R1-1)+1
        
        L=C(d**(R1-1)+s,s)
        #print("L=",L)
        N=2
        
        v=[0 for _ in range(R2)]
        h=[0 for _ in range(R2)]
        len_v_h=[0 for _ in range(R2)]
        bound_v_h=[0 for _ in range(R2)]
        
        u=[[0 for _ in range(R2)] for _ in range(R2-1)]
        len_u=[[0 for _ in range(R2)] for _ in range(R2-1)]
        bound_u=[[0 for _ in range(R2)] for _ in range(R2-1)]
        
        g=[[0 for _ in range(L+1)] for _ in range(R2+2)]
        len_g=[[0 for _ in range(L+1)] for _ in range(R2+2)]
        bound_g=[[0 for _ in range(L+1)] for _ in range(R2+2)]
        
        e=[[0 for _ in range(s+1)] for _ in range(L+1)]#constant
        len_e=p_to_len(bound_e)
        
        m=[0 for _ in range(s+1)]
        len_m=p_to_len(bound_m)
        len_m_sum=p_to_len(s*bound_m+1)

        v_=[[0 for _ in range(N)] for _ in range(R2)]#get
        h_=[[0 for _ in range(N)] for _ in range(R2)]#get
        u_=[[[0 for _ in range(N)] for _ in range(R2)] for _ in range(R2-1)]#get
        g_=[[[0 for _ in range(N)] for _ in range(L+1)] for _ in range(R2+2)]#get
        C2=[[0 for _ in range(N)] for _ in range(R2)]#get
        C4=[0 for _ in range(N)]#get
        
        x=[0 for _ in range(s+1)]#get
        y=[0 for _ in range(s+1)]#get
        z=[0 for _ in range(s+1)]#get
        len_mask=p_to_len(bound_mask)
        len_mask_sum=p_to_len(3*bound_mask+1)
        for i in range(R2):
            if i==0:
                len_v_h[i]=p_to_len(d**R3+1)
                bound_v_h[i]=(d**R3+1)
            else:
                bound=0
                for j in range(1,i+1):
                    bound+=d**(R3+j)
                bound+=1
                len_v_h[i]=p_to_len(bound)
                bound_v_h[i]=bound
            f.write("v_{}:BITVECTOR({});\n".format(i,len_v_h[i]))
            f.write("ASSERT BVLE(v_{},{});\n".format(i,dec_to_binstr(bound_v_h[i]-1,len_v_h[i])))
            f.write("h_{}:BITVECTOR({});\n".format(i,len_v_h[i]))
            f.write("ASSERT BVLE(h_{},{});\n".format(i,dec_to_binstr(bound_v_h[i]-1,len_v_h[i])))
            v[i]="v_{}".format(i)
            h[i]="h_{}".format(i)
            if len_v_h[i]>=p_len:
                for j in range(N):
                    f.write("_v_{}_{}:BITVECTOR({});\n".format(i,j,len_mask))
                    f.write("_h_{}_{}:BITVECTOR({});\n".format(i,j,len_mask))
                    f.write("ASSERT BVLE(_v_{}_{},{});\n".format(i,j,dec_to_binstr(p-1,len_mask)))
                    f.write("ASSERT BVLE(_h_{}_{},{});\n".format(i,j,dec_to_binstr(p-1,len_mask)))
                    v_[i][j]="_v_{}_{}".format(i,j)
                    h_[i][j]="_h_{}_{}".format(i,j)
                    if i>=1:
                        f.write("_C2_{}_{}:BITVECTOR({});\n".format(i,j,len_mask))
                        f.write("ASSERT BVLE(_C2_{}_{},{});\n".format(i,j,dec_to_binstr(p-1,len_mask)))
                        C2[i][j]="_C2_{}_{}".format(i,j)
        for r in range(1,R2+2):
            bound_g_=0
            if r==1:
                for t in range(R2):
                    if t==0:
                        bound_g_+=d**R3
                    else:
                        bound=0
                        for j in range(1,t+1):
                            bound+=d**(R3+j)
                        bound_g_+=bound
                bound_g_*=d
                bound_g_+=1
            for i in range(1,L+1):
                if r==1:
                    len_g[r][i]=p_to_len(bound_g_)
                    bound_g[r][i]=bound_g_
                else:
                    len_g[r][i]=len_v_h[R2+1-r]
                    bound_g[r][i]=bound_v_h[R2+1-r]
                f.write("g_{}_{}:BITVECTOR({});\n".format(r,i,len_g[r][i]))
                f.write("ASSERT BVLE(g_{}_{},{});\n".format(r,i,dec_to_binstr(bound_g[r][i]-1,len_g[r][i])))
                g[r][i]="g_{}_{}".format(r,i)
                if len_g[r][i]>=p_len:
                    for j in range(N):
                        f.write("_g_{}_{}_{}:BITVECTOR({});\n".format(r,i,j,len_mask))
                        f.write("ASSERT BVLE(_g_{}_{}_{},{});\n".format(r,i,j,dec_to_binstr(p-1,len_mask)))
                        g_[r][i][j]="_g_{}_{}_{}".format(r,i,j)
        for t in range(R2-1):
            for r in range(1,R2-t):
                if t==0:
                    len_u[t][r]=p_to_len(d**R3+1)
                    bound_u[t][r]=(d**R3+1)
                else:
                    bound=0
                    for j in range(1,t+1):
                        bound+=d**(R3+j)
                    bound+=1
                    len_u[t][r]=p_to_len(bound)
                    bound_u[t][r]=bound
                f.write("u_{}_{}:BITVECTOR({});\n".format(t,r,len_u[t][r]))
                f.write("ASSERT BVLE(u_{}_{},{});\n".format(t,r,dec_to_binstr(bound_u[t][r]-1,len_u[t][r])))
                u[t][r]="u_{}_{}".format(t,r)
                if len_u[t][r]>=p_len:
                    for j in range(N):
                        f.write("_u_{}_{}_{}:BITVECTOR({});\n".format(t,r,j,len_mask))
                        f.write("ASSERT BVLE(_u_{}_{}_{},{});\n".format(t,r,j,dec_to_binstr(p-1,len_mask)))
                        u_[t][r][j]="_u_{}_{}_{}".format(t,r,j)
        for i in range(1,L+1):
            for w in range(1,s+1):
                f.write("e_{}_{}:BITVECTOR({});\n".format(i,w,len_e))
                e[i][w]="e_{}_{}".format(i,w)
        for w in range(1,s+1):
            f.write("m_{}:BITVECTOR({});\n".format(w,len_m))
            m[w]="m_{}".format(w)
        
        if len_g[1][1]>=p_len:
            for j in range(N):
                f.write("_C4_{}:BITVECTOR({});\n".format(j,len_mask))
                f.write("ASSERT BVLE(_C4_{},{});\n".format(j,dec_to_binstr(p-1,len_mask)))
                C4[j]="_C4_{}".format(j)
        for w in range(1,s+1):
            f.write("_x_{}:BITVECTOR({});\n".format(w,len_mask))
            f.write("_y_{}:BITVECTOR({});\n".format(w,len_mask))
            f.write("_z_{}:BITVECTOR({});\n".format(w,len_mask))
            f.write("ASSERT BVLE(_x_{},{});\n".format(w,dec_to_binstr(p-1,len_mask)))
            f.write("ASSERT BVLE(_y_{},{});\n".format(w,dec_to_binstr(p-1,len_mask)))
            f.write("ASSERT BVLE(_z_{},{});\n".format(w,dec_to_binstr(p-1,len_mask)))
            x[w]="_x_{}".format(w)
            y[w]="_y_{}".format(w)
            z[w]="_z_{}".format(w)
            var_list=[x[w],y[w],z[w]]
            f.write("ASSERT BVGE({},{});\n".format(SUM(var_list,[len_mask for _ in range(3)],p_to_len(len(var_list)*bound_mask)),dec_to_binstr(1,p_to_len(len(var_list)*bound_mask))))
        f.write("\n")
        
        f.write("%e value-----------------------------\n")
        vec=[0 for _ in range(s+1)]
        vec[s]=d**(R1-1)
        for w in range(1,s+1):
            f.write("ASSERT {}={};\n".format(e[1][w],dec_to_binstr(vec[w],len_e)))
        for i in range(2,L+1):
            vec,mask=vector_up(vec,0)
            if mask==0:
                print("error")
            for w in range(1,s+1):
                f.write("ASSERT {}={};\n".format(e[i][w],dec_to_binstr(vec[w],len_e)))
        f.write("\n")
        
        f.write("%Decompose-----------------------------\n")
        for i in range(R2):
            if len_v_h[i]<p_len:
                continue
            var_list_v=[v_[i][0]]
            var_v_len=[len_mask]
            var_list_h=[h_[i][0]]
            var_h_len=[len_mask]
            for j in range(1,N):
                var_list_v.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(v_[i][j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                var_v_len.append(p_to_len(p**2+p))
                var_list_h.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(h_[i][j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                var_h_len.append(p_to_len(p**2+p))
            f.write("ASSERT {}={};\n".format(pad_length(v[i],len_v_h[i],p_to_len(p**2+p)),SUM(var_list_v,var_v_len,p_to_len(p**2+p))))
            f.write("ASSERT {}={};\n".format(pad_length(h[i],len_v_h[i],p_to_len(p**2+p)),SUM(var_list_h,var_h_len,p_to_len(p**2+p))))
        f.write("\n")
        for r in range(1,R2+2):
            for i in range(1,L+1):
                if len_g[r][i]<p_len:
                    continue
                var_list_g=[g_[r][i][0]]
                var_g_len=[len_mask]
                for j in range(1,N):
                    var_list_g.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(g_[r][i][j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                    var_g_len.append(p_to_len(p**2+p))
                f.write("ASSERT {}={};\n".format(pad_length(g[r][i],len_g[r][i],p_to_len(p**2+p)),SUM(var_list_g,var_g_len,p_to_len(p**2+p))))
        f.write("\n")
        for t in range(R2-1):
            for r in range(1,R2):
                if len_u[t][r]<p_len:
                    continue
                var_list_u=[u_[t][r][0]]
                var_u_len=[len_mask]
                for j in range(1,N):
                    var_list_u.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(u_[t][r][j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                    var_u_len.append(p_to_len(p**2+p))
                f.write("ASSERT {}={};\n".format(pad_length(u[t][r],len_u[t][r],p_to_len(p**2+p)),SUM(var_list_u,var_u_len,p_to_len(p**2+p))))
        f.write("\n")
        for b in range(1,R2):
            if len_v_h[b]<p_len:
                continue
            var_list_C2=[C2[b][0]]
            var_C2_len=[len_mask]
            for j in range(1,N):
                var_list_C2.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(C2[b][j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                var_C2_len.append(p_to_len(p**2+p))
            var_list=[]
            var_len=[]
            for t in range(b):
                var_list.append(u[t][R2-b])
                var_len.append(len_u[t][R2-b])
            f.write("ASSERT BVMULT({},{},{})={};\n".format(p_to_len(p**2+p),dec_to_binstr(d,p_to_len(p**2+p)),SUM(var_list,var_len,p_to_len(p**2+p)),SUM(var_list_C2,var_C2_len,p_to_len(p**2+p))))
        f.write("\n")
        
        if len_g[1][1]>=p_len:
            var_list_C4=[C4[0]]
            var_C4_len=[len_mask]
            for j in range(1,N):
                var_list_C4.append("BVMULT({},{},{})".format(p_to_len(p**2+p),pad_length(C4[j],len_mask,p_to_len(p**2+p)),dec_to_binstr(p**j,p_to_len(p**2+p))))
                var_C4_len.append(p_to_len(p**2+p))
            var_list=[]
            var_len=[]
            for t in range(R2):
                var_list.append(v[t])
                var_len.append(len_v_h[t])
            f.write("ASSERT BVMULT({},{},{})={};\n".format(p_to_len(p**2+p),dec_to_binstr(d,p_to_len(p**2+p)),SUM(var_list,var_len,p_to_len(p**2+p)),SUM(var_list_C4,var_C4_len,p_to_len(p**2+p))))
        
        for w in range(1,s+1):
            var_list=[]
            var_list.append("BVMULT({},0bin{}@{},{})".format(p_to_len(p**3+p**2+p),"0"*(p_to_len(p**3+p**2+p)-len_mask),x[w],dec_to_binstr(p**2,p_to_len(p**3+p**2+p))))
            var_list.append("BVMULT({},0bin{}@{},{})".format(p_to_len(p**3+p**2+p),"0"*(p_to_len(p**3+p**2+p)-len_mask),y[w],dec_to_binstr(p,p_to_len(p**3+p**2+p))))
            var_list.append("0bin{}@_z_{}".format("0"*(p_to_len(p**3+p**2+p)-len_mask),w))
            f.write("ASSERT {}={};\n".format(pad_length(m[w],len_m,p_to_len(p**3+p**2+p)),SUM(var_list,[p_to_len(p**3+p**2+p) for _ in range(len(var_list))],p_to_len(p**3+p**2+p))))
        f.write("\n")
        
        f.write("%m value--------------------------------------\n")
        for w in range(1,s+1):
            var_list1=[]
            for i in range(1,L+1):
                var_list2=[]
                var_len2=[]
                for r in range(1,R2+2):
                    var_list2.append(g[r][i])
                    var_len2.append(len_g[r][i])
                var_list1.append("BVMULT({},0bin{}@{},{})".format(len_m,"0"*(len_m-len_e),e[i][w],SUM(var_list2,var_len2,len_m)))
            f.write("ASSERT {}=BVMULT({},{},{});\n".format(m[w],len_m,dec_to_binstr(d,len_m),SUM(var_list1,[len_m for _ in range(len(var_list1))],len_m)))
        f.write("\n")
        #type-1-condition
        f.write("%Type 1 condition-----------------------------\n")
        for i in range(R2):
            var_list=[]
            var_len=[]
            var_list.append(v[i])
            var_len.append(len_v_h[i])
            var_list.append(h[i])
            var_len.append(len_v_h[i])
            if R2==1:
                break
            if i==0:
                var_list.extend(u[i][1:R2-i])
                var_len.extend(len_u[i][1:R2-i])
                f.write("ASSERT BVLE({},{});\n".format(SUM(var_list,var_len,len_v_h[0]+p_to_len(2+R2-1)+1),dec_to_binstr(d**R3,len_v_h[0]+p_to_len(2+R2-1)+1)))
            else:
                var_list1=[]
                var_len1=[]
                for t in range(i):
                    var_list1.append(u[t][R2-i])
                    var_len1.append(len_u[t][R2-i])
                if i<(R2-1):
                    var_list.extend(u[i][1:R2-i])
                    var_len.extend(len_u[i][1:R2-i])
                    f.write("ASSERT {}=BVMULT({},{},{});\n".format(SUM(var_list,var_len,len_v_h[i]+p_to_len(2+R2-1-i)+1),len_v_h[i]+p_to_len(2+R2-1-i)+1,dec_to_binstr(d,len_v_h[i]+p_to_len(2+R2-1-i)+1),SUM(var_list1,var_len1,len_v_h[i]+p_to_len(2+R2-1-i)+1)))

                else:
                    f.write("ASSERT {}=BVMULT({},{},{});\n".format(SUM(var_list,var_len,len_v_h[i]+p_to_len(2+R2-1-i)+1),len_v_h[i]+p_to_len(2+R2-1-i)+1,dec_to_binstr(d,len_v_h[i]+p_to_len(2+R2-1-i)+1),SUM(var_list1,var_len1,len_v_h[i]+p_to_len(2+R2-1-i)+1)))

        f.write("\n")
        #type-2-condition
        f.write("%Type 2 condition-----------------------------\n")
        for r in range(1,R2+2):
            var_list=[]
            var_len=[]
            var_list1=[]
            var_len1=[]
            for i in range(1,L+1):
                var_list.append(g[r][i])
                var_len.append(len_g[r][i])
            for t in range(R2):
                var_list1.append(v[t])
                var_len1.append(len_v_h[t])
            if r==1:
                f.write("ASSERT {}=BVMULT({},{},{});\n".format(SUM(var_list,var_len,len_g[r][1]+p_to_len(L)+1),len_g[r][1]+p_to_len(L)+1,dec_to_binstr(d,len_g[r][1]+p_to_len(L)+1),SUM(var_list1,var_len1,len_g[r][1]+p_to_len(L)+1)))
            else:
                f.write("ASSERT {}={};\n".format(SUM(var_list,var_len,len_g[r][1]+p_to_len(L)+1),pad_length(h[R2+1-r],len_v_h[R2+1-r],len_g[r][1]+p_to_len(L)+1)))
        f.write("\n")
        #type-3-condition
        f.write("%Type 3 condition-----------------------------\n")
        f.write("%C2C4!=0-----------------------------\n")
        for i in range(N):
        #C2!=0    
            for b in range(1,R2):
                if len_v_h[b]<p_len:
                    continue
                var_list=[v_[b][i],h_[b][i]]
                var_len=[len_mask,len_mask]
                for r in range(1,R2-b):
                    var_list.append(u_[b][r][i])
                    var_len.append(len_mask)
                f.write("ASSERT {}={};\n".format(pad_length(C2[b][i],len_mask,p_to_len(p*len(var_list))),SUM(var_list,var_len,p_to_len(p*len(var_list)))))
        #C4!=0
            for r in range(2,R2+2):
                if len_g[r][1]<p_len:
                    continue
                var_list=[]
                var_len=[]
                for I in range(1,L+1):
                    var_list.append(g_[r][I][i])
                    var_len.append(len_mask)
                f.write("ASSERT {}={};\n".format(pad_length(h_[R2-1+2-r][i],len_mask,p_to_len(p*len(var_list))),SUM(var_list,var_len,p_to_len(p*len(var_list)))))
            if len_g[1][1]>=p_len:
                var_list=[]
                var_len=[]
                for I in range(1,L+1):
                    var_list.append(g_[1][I][i])
                    var_len.append(len_mask)
                f.write("ASSERT {}={};\n".format(pad_length(C4[i],len_mask,p_to_len(p*len(var_list))),SUM(var_list,var_len,p_to_len(p*len(var_list)))))
        f.write("\n")
       
        f.write("%-----------------------\n")
        var_list=[]
        var_len=[]
        var_list1=[]
        var_len1=[]
        for w in range(1,s+1):
            var_list.append(m[w])
            var_len.append(len_m)
            f.write("ASSERT BVGE({},{});\n".format(m[w],dec_to_binstr(p-1,len_m)))
        for i in range(1,L+1):
            for r in range(1,R2+2):
                var_list1.append(g[r][i])
                var_len1.append(len_g[r][i])
        f.write("ASSERT BVGE({},{});\n".format(SUM(var_list,var_len,len_m_sum),dec_to_binstr(s*(p-1),len_m_sum)))
        f.write("ASSERT BVLE({},BVMULT({},{},{}));\n".format(SUM(var_list,var_len,len_m_sum),len_m_sum,dec_to_binstr(d**R1,len_m_sum),SUM(var_list1,var_len1,len_m_sum)))
        f.write("\n")
        #C6!=0
        f.write("%C6!=0-----------------------------\n")
        for w in range(1,s+1):
            f.write("ASSERT IF BVLE({},{}) THEN\n".format(x[w],dec_to_binstr(p-2,len_mask)))
            var_list=[x[w],y[w],z[w]]
            var_len=[len_mask for _ in range(3)]
            f.write("BVMOD({},{},{})={}\n".format(p_to_len(p*3),SUM(var_list,var_len,p_to_len(p*3)),dec_to_binstr(p-1,p_to_len(p*3)),dec_to_binstr(0,p_to_len(p*3))))
            f.write("ELSE\n")
            var_list=[y[w],z[w]]
            var_len=[len_mask for _ in range(2)]
            f.write("BVGE({},{})\n".format(SUM(var_list,var_len,p_to_len(p*3)),dec_to_binstr(1,p_to_len(p*3))))
            f.write("ENDIF;\n")
        f.write("\n")
        f.write("QUERY FALSE;\n")
        f.write("COUNTEREXAMPLE;\n")

path="./hades_p_{}_t_{}_s_{}_R1_{}_R2_{}_R3_{}_d_{}.cvc".format(p,n,s,R1,R2,R3,d)
construct_Model(path)
