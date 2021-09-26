import numpy as np
import matplotlib.pyplot as plt

class person:
    """Person class"""
    def __init__(self, status, ID, part, pref=None):
        
        self.status = status #Engaged / Not engaged. 1 for engaged, 0 for not engaged
        self.ID = ID #The persons ID
        self.part = part #Name of engagement partner

        if pref == None:
            pref = []
        else:
            self.pref = pref #Preference, list of ordered candidates after preference

    def set_engaged(self, new_partner):
        #Toggle status between 0 and 1
        self.status = 1 #Set status as engaged
        self.part = new_partner #Set engagement to partner
    
    def set_free(self):
        self.status = 0
        self.part = 'free'
    
    def propose(self):
        #Propose to first woman in preference, remove her from list of candidates
        self.pref.remove(self.pref[0]) 

status = 0 #Everyone "free" at start
partner_in = 'free'

#Initialize men
A = person(status, 'A', partner_in, pref=['a', 'b', 'c', 'd'] )
B = person(status, 'B', partner_in, pref=['b', 'a', 'c', 'd'] )
C = person(status, 'C', partner_in, pref=['a', 'd', 'c', 'b'] )
D = person(status, 'D', partner_in, pref=['d', 'c', 'a', 'b'] )

men_list = [A,B,C,D]

#Initialize women
a = person(status, 'a', partner_in, pref=['A', 'B', 'C', 'D'] )
b = person(status, 'b', partner_in, pref=['D', 'C', 'B', 'A'] )
c = person(status, 'c', partner_in, pref=['A', 'B', 'C', 'D'] )
d = person(status, 'd', partner_in, pref=['C', 'D', 'A', 'B'] )

woman_list = [a,b,c,d]

counter = 0
status_list = [A.status, B.status, C.status, D.status]

#Pair list for visualization
pair_list = []
for man in men_list:
    pair_list.append([man.ID, man.part]) #Saving partner pair (for plotting)


while (np.sum(status_list) < len(men_list)): #While some men still "unpaired"
    counter += 1 #Counting iterations

    for man in men_list: #Looping over men

        #print('Man number: ', man.ID, ' with status = ', man.status, ' and proposal list ', man.pref)
        
        if len(man.pref) > 0 and (man.status == 0): #If still have proposals to do

            #print( man.ID + ' proposing to ' + str(man.pref[0]) + ' with ', man.pref, ' left')
            
            proposee = man.pref[0] #Woman being proposed to

            if eval(proposee).status == 1: #If woman already engaged
                #print('Woman already engaged, with status = ', eval(proposee).status)

                new_par = man.ID
                old_par = eval(proposee).part
                rank_new = eval(proposee).pref.index(new_par)
                rank_old = eval(proposee).pref.index(old_par)

                if rank_new < rank_old: #If woman prefers new man over previous one. Lower rank (index) is preferred
                    #Break up with old man (set old man as free)
                    eval(eval(proposee).part).set_free()

                    #Set new couple.
                    man.set_engaged( man.pref[0] ) #Set man as engaged with new partner
                    eval(man.pref[0]).set_engaged( str(man.ID) ) #Set woman as engaged with new partner (man)

                else:
                    #Keep old couple, do nothing
                    pass

            else:  
                #Woman has no previous partner, instantly pair      
                man.set_engaged( man.pref[0] ) #Set man as engaged with new partner
                eval(man.pref[0]).set_engaged( str(man.ID) ) #Set woman as engaged with new partner (man)
            
            man.propose() #Remove woman from proposal list

        else:
            #If he has no proposals to make
            pass

        pair_list.append([man.ID, man.part]) #Saving partner pair (for plotting)

    status_list = [A.status, B.status, C.status, D.status]
    #print(status_list)

#Print final male / female pairs
for man in men_list:
    print( eval(man.part).part, man.part )
    print('--------------------')

print(pair_list)

def convert(arg):
    ## Temp ##
    if arg == 'free':
        return 0
    if arg == 'A' or arg == 'a':
        return 1
    if arg == 'B' or arg == 'b':
        return 2
    if arg == 'C' or arg == 'c':
        return 3
    if arg == 'D' or arg == 'd':
        return 4


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

plt.rc('font', **font)
plt.rcParams['lines.markersize'] = 40

fig, ax = plt.subplots()
dist = 1

lst = []

dim1 = len(pair_list)
dim2 = len(men_list)

print(type(len(pair_list)))
print(type(len(men_list)))

arr = np.zeros( ( int(dim1/dim2), dim2) )

print(np.shape(arr))

for i in range(len(pair_list)):
    man = convert(pair_list[i][0])
    woman = convert(pair_list[i][1])
    lst.append([man, woman])

print(lst)
print(arr)



for i in range(len(men_list)):
    ax.scatter(1,i+1, label='Man ' + str(i))
    ax.scatter(3,i+1, label='Woman ' + str(i))

for i in range(8,12):
    if lst[i] == 0:
        pass
    else:
        ax.plot([1, 3] , [lst[i][0], lst[i][1]], 'k--')

#plt.legend()
plt.ylabel(['A', 'B', 'C', 'D'])
plt.show()