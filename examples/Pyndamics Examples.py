# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Using Pyndamics to Simulate Dynamical Systems
# 
# Pyndamics provides a way to describe a dynamical system in terms of the differential equations, or the stock-flow formalism. It is a wrapper around the Scipy odeint function, with further functionality for time plots, phase plots, and vector fields.
# 
# Page for this package: [https://code.google.com/p/pyndamics/](https://code.google.com/p/pyndamics/)

# <codecell>

from pyndamics import Simulation

# <markdowncell>

# ## Population of Mice - Exponential Growth
# 
# ### Specifying the Differential Equation

# <codecell>

sim=Simulation()   # get a simulation object

sim.add("mice'=b*mice - d*mice",    # the equations
    100,                            # initial value
    plot=True)                      # display a plot

sim.params(b=1.1,d=0.08)

sim.run(0,4)

# <markdowncell>

# ### Specifying the Inflows/Outflows

# <codecell>

sim=Simulation()   # get a simulation object

sim.stock("mice",100,plot=False)
sim.inflow("mice","b*mice")
sim.outflow("mice","d*mice")

sim.params(b=1.1,d=0.08)

sim.run(0,4)

# <markdowncell>

# ### Plotting Manually

# <codecell>

x,y=sim.t,sim.mice
plot(x,y,'r--')
xlabel('Days')
ylabel('Number of Mice')

# <markdowncell>

# ## Predator-Prey Dynamics

# <codecell>

sim=Simulation()

sim.add("deer' = r*deer*(1-deer/K)-c*deer*wolf",
                initial_value=350,
                plot=True)

sim.add("wolf' = -Wd*wolf+D*deer*wolf",
                initial_value=50,
                plot=True)

sim.params(r=0.25,D=0.001,c=0.005,Wd=0.3,K=1e500)

print sim.equations()
sim.run(0,500)

# <codecell>

from pyndamics import phase_plot
phase_plot(sim,'deer','wolf')

# <markdowncell>

# ## Exponential vs Logistic

# <codecell>

sim=Simulation()

# logistic growth
sim.add("pop' = r*pop*(1-pop/K)",
                initial_value=350,
                plot=1)

# exponential growth
sim.add("pop2' = r*pop2",
                initial_value=350,
                plot=1)


sim.params(r=0.25,K=3000)

sim.run(0,5)

# <markdowncell>

# ## Damped Spring - Second-order Differential Equations
# 
# When specifying the initial conditions for a 2nd-order equation, you need to specify the value of the variable (e.g. position) and its first derivative (e.g. velocity).  The simulator automatically changes the equations into a set of 1st-order equations.

# <codecell>

sim=Simulation()
sim.add("x''=-k*x/m -b*x'",[10,0],plot=True)
sim.params(k=1.0,m=1.0,b=0.5)
print sim.equations()
sim.run(0,20)

# <markdowncell>

# ## Vector Field Example

# <codecell>

sim=Simulation()
sim.add("p'=p*(1-p)",0.1,plot=True)
sim.run(0,10)

# <markdowncell>

# Arrows scaled by the magnitude...

# <codecell>

from pyndamics import vector_field
vector_field(sim,p=linspace(-1,2,20))

# <markdowncell>

# Arrows rescaled to constant value...

# <codecell>

vector_field(sim,rescale=True,p=linspace(-1,2,20))

# <markdowncell>

# ## The Lorenz System
# 
# [http://en.wikipedia.org/wiki/Lorenz_system](http://en.wikipedia.org/wiki/Lorenz_system)

# <codecell>

sim=Simulation()
sim.add("x'=sigma*(y-x)",14,plot=True)
sim.add("y'=x*(rho-z)-y",8.1,plot=True)
sim.add("z'=x*y-beta*z",45,plot=True)
sim.params(sigma=10,beta=8.0/3,rho=15)
sim.run(0,50,num_iterations=10000)  # increase the resolution

# <codecell>

phase_plot(sim,'x','z')

# <codecell>

phase_plot(sim,'x','y','z')

# <codecell>


