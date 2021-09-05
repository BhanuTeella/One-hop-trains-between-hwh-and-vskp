#From the Train_details_22122017.csv finding out all the trains that run through the stations VSKP,HWH,BBS and separeting the into seperate files and also simultaneously making a list of the train numbers 
f=open('Train_details_22122017.csv','r')
v=open('vskp.csv','w')
h=open('hwh.csv','w')
b=open('bbs.csv','w')
header=f.readline()
v.write(header)
b.write(header)
h.write(header)
l=f.readline()
vskp,hwh,bbs=[],[],[]
while (l):
 lcomp=l.strip().split(',')
 if lcomp[3]=='VSKP':
   v.write(l)
   vskp=vskp+[lcomp[0]]
 elif lcomp[3]=='HWH':
   h.write(l)
   hwh=hwh+[lcomp[0]]
 elif lcomp[3]=='BBS':
   b.write(l)
   bbs=bbs+[lcomp[0]]
 l=f.readline()
f.close()
v.close()
b.close()
h.close()
0
"""finding out trains that run between vskp and hwh"""
vskphwhtrains=[]
count=0
for i in vskp:
  if i in hwh:
    vskphwhtrains.append(i)
    

"""finding out trains that run between bbs and hwh"""
bbshwhtrains=[]
count=0
for i in bbs:
  if i in hwh:
    bbshwhtrains.append(i)
    

"""finding out trains that run between bbs and vskp"""
bbsvskptrains=[]
count=0
for i in bbs:
  if i in vskp:
    bbsvskptrains.append(i)
   
# making list of the trains(other than the direct trains) that only run between BBS and VSKP and BBS and HWH
f=open('bbs.csv','r')
header=f.readline()
l=f.readline()
d2={}
d1={}
while (l):
 lcomp=l.strip().split(',')
 if lcomp[0] in bbsvskptrains and lcomp[0] not in bbshwhtrains:
   d2[lcomp[0]]=[lcomp[5],lcomp[6]]
 elif lcomp[0] in bbshwhtrains and lcomp[0] not in bbsvskptrains:
   d1[lcomp[0]]=[lcomp[5],lcomp[6]]  
 l=f.readline()
f.close()

#code to seperate those trains that run from hwh to bbs and those that run from bbs to hwh
hwhbbs={}
bbshwh={}
for i in d1:
  if int(i)%2==0:
    bbshwh[i]=d1[i]  #This part of code is specific to trains to this case. the train routes are       
  else:              #manually observed and seperated into different directions
    hwhbbs[i]=d1[i]
del bbshwh['15644']
del hwhbbs['15643']
bbshwh["15643"]=d1["15643"]
hwhbbs['15644']=d1["15644"]

#code to seperate those trains that run from vskp to bbs and those that run from bbs to vskp

l1=["2841","6057","7439","11020","12660","12773","12830",'12845','12898','15630','15906','15930','17015','18463','18496','18508','20815','20817','22603','22605','22612','22614','22642','22644','22807','22809','22819','22825','22833','22849','22851','22855','22853','22871','22873','22879','22882']
vskpbbs={}
bbsvskp={}

for i in d2:
  if i in l1:
    bbsvskp[i]=d2[i] #This part of code is specific to trains to this case. the train routes are    
  else:              #manually observed and seperated into different directions
    vskpbbs[i]=d2[i]

#finding out all feasible pairs of trains for one-hop to travel from vskp to hwh. Two trains are 
#feasible for one-hop when the second train departures from bbs only after the first trains arrives at bbs 
onehophv={}
for i in hwhbbs:
  for j in bbsvskp:
    if bbsvskp[j][1]>hwhbbs[i][0]:
     if i in onehophv:
       onehophv[i].append([j,bbsvskp[j][1],hwhbbs[i][0]])
       
     else:
       onehophv[i]=[]
       onehophv[i].append([j,bbsvskp[j][1],hwhbbs[i][0]])

#finding out all feasible pairs of trains for one-hop to travel from hwh to vskp. Two trains are 
#feasible for one-hop when the second train departures from bbs only after the first trains arrives at bbs        

onehopvh={}
for i in vskpbbs:
  for j in bbshwh:
    if bbshwh[j][1]>vskpbbs[i][0]:
     if i in onehopvh:
        onehopvh[i].append([j,bbshwh[j][1],vskpbbs[i][0]])

     else:
       onehopvh[i]=[]
       onehopvh[i].append([j,bbshwh[j][1],vskpbbs[i][0]])
       

#Writing to file, the details of all those feasible pairs of trains for one-hop to travel from hwh to vskp, with a hop within 2hr
f=open('onehophv.csv','w')
f.write("hwh-vskp\n")
for i in onehophv:
  for j in onehophv[i]:
   arr=j[2].strip().split(":")
   dep=j[1].strip().split(":")
   a=int(arr[0])*60+int(arr[1])
   d=int(dep[0])*60+int(dep[1])
   t=d-a
   if (t <=120):     #time gap of 2hr(120 min) is choosen. This can be changed according to requirement.
     f.write(i+","+j[2]+","+j[0]+","+j[1]+","+str(t)+"\n")  
f.close()

#Writing to file, the details of all those feasible pairs of trains for one-hop to travel from vskp to hwh, with a hop within 2hr

f=open('onehopvh.csv','w')
f.write("vskp-hwh\n")
for i in onehopvh:
  for j in onehopvh[i]:
   arr=j[2].strip().split(":")
   dep=j[1].strip().split(":")
   a=int(arr[0])*60+int(arr[1])
   d=int(dep[0])*60+int(dep[1])
   t=d-a
   if (t <=120):   #time gap of 2hr(120 min) is choosen. This can be changed according to requirement.
     f.write(i+","+j[2]+","+j[0]+","+j[1]+","+str(t)+"\n")
f.close()



