import json
import matplotlib.pyplot as plt

#Universal Constants
sigma = 5.67*(10**(-8))

with open('Settings.json') as f:
    data = json.load(f)
settings = data['Settings'][0]

#Material Constants
curie_temp = settings["curie_temp"] #Curie Temperature of Iron, biggest Component of Steel
epsilon = settings["epsilon"]
csp = settings["csp"]
m = settings["m"] #Mass of Object in kg
A = settings["A"] #Surface Area of Object in m^2

#initial conditions
dt = settings["dt"] #Time step in seconds
Pzu = settings["Pzu"] #Power from circuit in W, loss in Coil is Subtracted by utilising Efficiency Eta
eta_before = settings["eta_before"] #calculated efficiency from Mathematica Notebook
curie_factor = settings["curie_factor"]
eta_curie = curie_factor * eta_before #Efficiency loss due to reaching Curie-Temperature
Tinit = settings["Tinit"] #Initial Temperature in K
Pab = 0 #Power less per Cycle, based on Temperature
dT = 0 #used to store Temperature change per Cycle
dP = 0 #used to store Power change per Cycle
timecodes = []
Temperatures = []

T = Tinit 
for i in range(round(100/dt) + 1):
    T = T + dT
    Pab = epsilon * sigma * A * (T**4 - 293.15**4)
    if (T < curie_temp):
        dP = eta_before * Pzu - Pab
    else:
        dP = eta_curie * Pzu - Pab
    dT = (dP*dt)/(m*csp)
    timecodes.append(dt*i)
    Temperatures.append(T)
    
#print(timecodes)
#print(Temperatures)

with open('TempGraph.txt', 'w') as f:
    for i,elem in enumerate(timecodes):
        f.write(str(timecodes[i]) + " " + str(Temperatures[i]) + '\n')    
    
#plt.plot(timecodes, Temperatures)
#plt.show()