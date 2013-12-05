# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Using Pyndamics to Perform Bayesian Parameter Estimation in Dynamical Systems
# 
# Pyndamics provides a way to describe a dynamical system in terms of the differential equations, or the stock-flow formalism. It is a wrapper around the Scipy odeint function, with further functionality for time plots, phase plots, and vector fields.  The MCMC component of this package uses pymc (version 2 right now): http://pymc-devs.github.io/pymc/.  
# 
# Page for this package: [https://code.google.com/p/pyndamics/](https://code.google.com/p/pyndamics/)

# <codecell>

from pyndamics import Simulation
from pyndamics.mcmc import MCMCModel

# <markdowncell>

# ## A linear growth example
# 
# Data from [http://www.seattlecentral.edu/qelp/sets/009/009.html](http://www.seattlecentral.edu/qelp/sets/009/009.html)

# <markdowncell>

# ### Plot the data

# <codecell>

t=array([0,2,4,6,8,10,12])
h=array([1.0,1.5,2.2,3.2,4.3,5.2,5.6])

plot(t,h,'-o')
xlabel('Days')
ylabel('Height [cm]')

# <markdowncell>

# ### Run an initial simulation
# 
# Here, the constant value ($a=1$) is hand-picked, and doesn't fit the data particularly well.

# <codecell>

sim=Simulation()
sim.add("h'=a",1,plot=True)
sim.add_data(t=t,h=h,plot=True)
sim.params(a=1)
sim.run(0,12)

# <markdowncell>

# ### Fit the model parameter, $a$
# 
# Specifying the prior probability distribution for $a$ as uniform between -10 and 10.

# <codecell>

model=MCMCModel(sim,{'a':[-10,10]})
model.fit(iter=25000)

# <markdowncell>

# What is the best fit parameter value?

# <codecell>

model.a

# <markdowncell>

# ### Rerun the model

# <codecell>

sim.run(0,12)

# <markdowncell>

# ### Plot the posterior histogram

# <codecell>

model.plot_distributions()

# <markdowncell>

# ### Plot the posterior histogram with the normal approximation

# <codecell>

model.plot_distributions(show_normal=True)

# <markdowncell>

# ### Fit the model parameter, $a$, and the initial value of the variable, $h$

# <codecell>

model=MCMCModel(sim,{'a':[-10,10],'initial_h':[0,4]})
model.fit(iter=25000)

# <codecell>

sim.run(0,12)
model.plot_distributions(show_normal=True)

# <markdowncell>

# ### Plot the simulations for many samplings of the simulation parameters

# <codecell>

sim.noplots=True  # turn off the simulation plots
for i in range(500):
    model.draw()
    sim.run(0,12)
    plot(sim.t,sim.h,'g-',alpha=.1)
sim.noplots=False  # gotta love a double-negative
plot(t,h,'bo')  # plot the data

# <markdowncell>

# ## Logistic Model with the Same Data

# <codecell>

sim=Simulation()
sim.add("h'=a*h*(1-h/K)",1,plot=True)
sim.add_data(t=t,h=h,plot=True)
sim.params(a=1,K=10)
sim.run(0,12)

# <markdowncell>

# ### Fit the model parameters, $a$ and $K$, and the initial value of the variable, $h$

# <codecell>

model=MCMCModel(sim,{'a':[0.001,5],'K':[0.1,40],'initial_h':[0,4]})
model.fit(iter=25000)
print sim.a,sim.K

# <markdowncell>

# ### Plot the Results

# <codecell>

sim.run(0,12)
model.plot_distributions(show_normal=True)

# <markdowncell>

# ### Plot the joint distribution between parameters, $a$ and $K$

# <codecell>

model.plot_joint_distribution('a','K',show_prior=False)

# <markdowncell>

# ...showing the joint, with the prior, to see how much the inference constrains the final best estimates of the parameters

# <codecell>

model.plot_joint_distribution('a','K',show_prior=True)

# <markdowncell>

# ### Sample Runs

# <codecell>

sim.noplots=True
for i in range(500):
    model.draw()
    sim.run(0,12)
    plot(sim.t,sim.h,'g-',alpha=.1)
sim.noplots=False  # gotta love a double-negative
plot(t,h,'bo')
xlabel('Days')
ylabel('Height [cm]')

# <markdowncell>

# ### Plot the 95% credible interval for the dynamics of the system

# <codecell>

plot(t,model['h_data'].value,'o')
plot(t,model['h'].stats()['mean'],'--')
plot(t,model['h'].stats()['95% HPD interval'], 'r:')
xlabel('Days')
ylabel('Height [cm]')

# <codecell>


