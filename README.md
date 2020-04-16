# SARS SEIR Simulation
Agent-based model testing effectiveness of mask usage. Using Monte Carlo simulations, informed by real-world parameters, various conditions can be examined for their power to slow or halt pathogen transmission.


## Agent-Based SEIR Model
Infectious disease spreads through its ability to infect hosts (agents) and be transmitted to new agents. The agent's state is then said to be either susceptible (without particular disease but able to acquire it), exposed (has contracted the disease but is not symptomatic or infectious), infected (symptomatic or asymptomatic and infectious), or recovered (experienced infection and no longer infectious). The rate of transition from one state to another can describe a pathogen's spread through a population. 

Python's is used for agent data storage and computation of which agents transition and how. A graphical display through the matplotlib and seaborn packages are used for the visual of agent's position and state during iterative steps. Data from each simulation is tidily written to a .csv file where data analysis can quickly be done with pandas, seaborn, and scipy packages.

The current script has a lot of unnecessary if-thens, will be cleaned up in the future.
