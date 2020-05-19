# SARS SEIR Simulation
Agent-based model testing effectiveness of mask usage. Using Monte Carlo simulations, informed by real-world parameters, various conditions can be examined for their power to slow or halt pathogen transmission.


## Agent-Based SEIR Model
Infectious disease spreads through its ability to infect hosts (agents) and be transmitted to new agents. The agent's state is then said to be either susceptible (without particular disease but able to acquire it), exposed (has contracted the disease but is not symptomatic or infectious), infected (symptomatic or asymptomatic and infectious), or recovered (experienced infection and no longer infectious). The rate of transition from one state to another can describe a pathogen's spread through a population. 

Python's is used for agent data storage and computation of which agents transition and how. A graphical display through the matplotlib and seaborn packages are used for the visual of agent's position and state during iterative steps. Data from each simulation is tidily written to a .csv file where data analysis can quickly be done with pandas, seaborn, and scipy packages.

To simulate 500 agents over different combinations of mask and sheltering parameters, use the mask_and_shelter_sim.py script.

**python mask_and_shelter_sim.py a b c** 
    * Where a is the chance of an infected agent being asymptomatic (a=50 -> 50%)
    * Where b is the random number generator seed, an integer
    * Where c is the simulation replicate to distinguish output files, an integer
    
To simulation 500 agents for a given condition and output a movie of the simulation in the form of a .gif use mask_sim_animate.py 
**python mask_sim_animate.py a b c d**
    * Where a is the percent of agents wearing a mask (a=60 -> 60%)
    * Where b is the percent of agents sheltering in place (b=40 -> 40%)
    * Where c is the percent of infected agents that are asymptomatic (c=50 -> 50%)
    * Where d is the is the random number generator seed, an integer
    
    
The random number generator seeds used for 100 simulations of each condition were: 12, 23, 29, 34, 39, 42, 52, 63, 68, 98, 99, 109, 111, 117, 123, 126, 132, 133, 146, 167, 177, 202, 232, 247, 251, 261, 275, 279, 320, 339, 355, 365, 380, 384, 390, 393, 414, 415, 421, 424, 445, 461, 468, 514, 515, 519, 526, 529, 536, 541, 544, 554, 559, 573, 574, 583, 589, 608, 612, 616, 618, 619, 628, 629, 630, 638, 639, 673, 693, 697, 712, 717, 720, 722, 724, 730, 741, 752, 761, 764, 766, 767, 805, 824, 830, 835, 868, 871, 881, 889, 899, 900, 910, 913, 920, 946, 1137, 1425, 2718, 3038
