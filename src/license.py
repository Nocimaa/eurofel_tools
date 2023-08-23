#%%
import datetime
import random
date = datetime.datetime.now()

date_str='2023-11-08'

license2='1234-ABCD-EFGH-IJKL-CC'
#        REYD MYEE RMYR YCCD 
#    
license = '0000-0000-0000-0000'

c='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
d=dict()
d1=dict()
for i in range(len(c)):
    d[c[i]]=i
    d1[str(i)]=c[i]



#%%
def get_R(license):
    return (license[0],license[10],license[13])
def get_E(license):
    return (license[1],license[7],license[8])
def get_Y(license):
    return license[2]+license[6]+license[12]+license[15]
def get_D(license):
    return license[3]+license[18]
def get_M(license):
    return license[5]+license[11]
def get_C(license):
    return license[-2]+license[-3]

def decrypt(license):
        Y=get_Y(license)
        M=get_M(license)
        D=get_D(license)

        c='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        d1=dict()
        d2=dict()
        for i in range(len(c)):
            d1[c[i]]=i
            d2[str(i)]=c[i]

        E=[d1[el] for el in get_E(license)]
        R=[d1[el] for el in get_R(license)]
        Y=caesar(get_Y(license),d1,d2,-E[0]**R[0])
        M=caesar(get_M(license),d1,d2,-E[1]**R[1])
        D=caesar(get_D(license),d1,d2,-E[2]**R[2])

        return datetime.date(int(Y),int(M),int(D))



# %%
def caesar(st,dict,dict1,key):
    s=''
    for e in st:
        k=str((dict[e]+key)%36)
        s+=dict1[k]
    return s
# %%

def encrypt(date):
    license = '0000-0000-0000-0000'
    c='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    d1=dict()
    d2=dict()
    for i in range(len(c)):
        d1[c[i]]=i
        d2[str(i)]=c[i]


    E1,R1= random.randint(1,35),random.randint(1,35)
    E2,R2= random.randint(1,35),random.randint(1,35)
    E3,R3= random.randint(1,35),random.randint(1,35)
    C1,C2 = random.randint(0,35),random.randint(0,35)

    L=['0' for i in range(19)]
    L[4]='-'
    L[9]='-'
    L[14]='-'
    L[1],L[7],L[8]=c[E1],c[E2],c[E3]
    L[0],L[10],L[13]=c[R1],c[R2],c[R3]
    L[-2],L[-3]=c[C1],c[C2]


    y=caesar(date.strftime('%Y'),d1,d2,E1**R1)
    m=caesar(date.strftime('%m'),d1,d2,E2**R2)
    d=caesar(date.strftime('%d'),d1,d2,E3**R3)

    L[2],L[6],L[12],L[15]=list(y)
    L[5],L[11]=list(m)
    L[3],L[18]=list(d)

    return "".join(L)


# %%
