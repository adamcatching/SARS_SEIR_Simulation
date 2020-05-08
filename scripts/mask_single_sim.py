# Import python packages
import numpy as np
import matplotlib.pyplot as plt
import sys

# Set percentage of asymptomatic
per_asympt = int(sys.argv[1]) * .01
# Set the random number
rand_num = int(sys.argv[2])
# Set iteration
set_iter = str(sys.argv[3])

for h in range(5):
    for g in range(5):
        # Fixing random state for reproducibility
        np.random.seed(rand_num)

        """# Which replicate is this simulation
        g = int(sys.argv[1])
        # Use different percentages of mask wearers
        h = int(sys.argv[2])"""
        # Set percent of sheltering in place
        per_shelt = int(g * 2)
        # Set percent of masked agents
        per_mask = int(h * 2)

        # Name the datafile
        run_name = 'mask_per_' + str(per_mask) + '0_shelter_' + str(per_shelt) + '0_asymp_' + per_asympt +  '_striter_' + set_iter
        dataname = '../data/test_run/' + run_name + '.csv'
        dataname_1 = '../data/test_run/' + run_name + '_agents.csv'
        f = open(dataname, 'w')
        # Write header of the file
        f.write('# Data from simulation of 500 agents with various levels\
         of sheltering or mask usage\n')
        f.write('time,percent sheltering,percent wearing masks,infected,\
        exposed,recovered,infected with mask,susceptible with mask,\
        infected symptomatic,infected asymptomatic,new infected,percent asymptomatic\n')

        e = open(dataname_1, 'w')
        e.write('# Individual agent data from each time point\n')
        e.write('position x,position y,state,symptomatic,number infected,mask\n')

        """Values of the simulation"""

        # Figure ratio
        fig_rat = .35355
        # Set boundaries
        xboundaries = [0, 60 * fig_rat]
        yboundaries = [0, 60 * fig_rat]
        xmax, ymax = xboundaries[1]+.5 , yboundaries[1]+.5

        # Number of agents
        n_agents = int(4000 * round(fig_rat ** 2, 2))
        # Set delta t
        dt = 1
        # Set velocity
        velo = .15


        # Define the array of agents with given properties
        agents = np.zeros(n_agents, dtype=[('position', float, 2),
                                           ('velocity', float, 2),
                                           ('color', str, 20),
                                           ('state', str, 20),
                                           ('time', int, 1),
                                           ('symptomatic', int, 1),
                                           ('num infected', int, 1),
                                           ('mask', bool, 1),
                                           ('touch', int, 1)])



        """Calculate initial values of agents"""
        # Define the initial random positions within the figure
        agents['position'] = np.random.uniform(0, xmax, (n_agents, 2))
        # Define the initial velocity angles
        init_angles = np.random.uniform(0, 2 * np.pi, n_agents)
        # Get initial x and y velocities from angles
        velocities = np.array([[np.sin(x), np.cos(x)] for x in init_angles]) 
        velocities *= velo
        # Get percentage of agents 'sheltering'
        num_shelt = int(per_shelt * n_agents * .1)
        # Make sheltering agents static (if any)
        velocities[:num_shelt] = np.zeros((num_shelt, 2))
        # Number of hours for asymptomatic incubation
        asympt_incubate = 24 * 5.1
        # Number of hours for symptomatic incubation
        sympt_incubate = 24 * 4.6
        # Number of hours for asymptomatic infection
        asympt_infect = 7*24
        # Number of hours for symptomatic infection
        sympt_infect = 12
        # Define values for infection gamma pdf
        g_shape, g_scale = 0.25, 4
        # Probability reduction for asymptomatic carrier
        asym_prob = .66


        """Assign values to agents"""
        # Assign velocities
        agents['velocity'] = velocities
        # Assign color (Navy is the default susceptible agent)
        agents['color'] = np.array(['Navy'] * n_agents)
        # Set agents to be symptomatic
        agents['state'] = np.array(['Susceptible'] * n_agents)
        agents['time'] = np.array([0] * n_agents)
        n_mask = [True] * per_mask + [False] * (10-per_mask)
        agents['mask'] = np.random.choice(n_mask, n_agents, replace=True)
        agents['color'][agents['mask'] == True] = 'Dodgerblue'
        agents['symptomatic'] = np.zeros(n_agents)
        agents['num infected'] = np.zeros(n_agents)

        # Make the one agent infected
        agents['color'][0] = 'Violet'
        agents['state'][0] = 'Exposed'
        agents['time'][0] = 1
        agents['mask'][0] = False
        agents['symptomatic'][0] = 1
        temp_exposed = 1
        temp_infected = 0
        i = 0

        while temp_exposed != 0 or temp_infected != 0:

            """
            Take the information from the data stored in the agents array
            to calculate if an infected agent recovers, if two agents 
            interact, and if the agent bounces off a boundary
            """
            #print(i)
            if i % 72 == 0:
                print(str(3 * int(i / 72)) + ' days simulated')
            i += 1

            # Set number of new infected 
            new_infected = 0

            # Iterate over all agents 
            for j in range(n_agents):
                if agents['time'][j] != 0:
                    # Calculate if agent is exposed or infected
                    agent_j_infected = agents['state'][j] == 'Infected'
                    agent_j_exposed = agents['state'][j] == 'Exposed'
                    # Store time agent has been in this state
                    agent_j_time = agents['time'][j]
                    # Calculate if the agent is symptomatic or not
                    agent_j_sympt = agents['symptomatic'][j]
                    if agent_j_infected and agent_j_sympt:
                        if agents['time'][j] >= sympt_infect:
                            agents['state'][j] = 'Recovered'
                            agents['color'][j] = 'Darkgreen'
                            agents['time'][j] = 1
                        else:
                            agents['time'][j] += 1
                    elif agent_j_infected and not agent_j_sympt:
                        if agents['time'][j] >= asympt_infect:
                            agents['state'][j] = 'Recovered'
                            agents['color'][j] = 'Darkgreen'
                            agents['time'][j] = 1
                        else:
                            agents['time'][j] += 1
                    elif agent_j_exposed and agent_j_sympt:
                        if agents['time'][j] >= sympt_incubate:
                            agents['state'][j] = 'Infected'
                            agents['color'][j] = 'Firebrick'
                            agents['time'][j] = 1
                            new_infected += 1
                        else:
                            agents['time'][j] += 1
                    elif agent_j_exposed and not agent_j_sympt:
                        if agents['time'][j] >= asympt_incubate:
                            agents['state'][j] = 'Infected'
                            agents['color'][j] = 'Coral'
                            agents['time'][j] = 1
                            new_infected += 1
                        else:
                            agents['time'][j] += 1
                    elif agents['state'][j] == 'Recovered' and agents['symptomatic'][j] == 1:
                        if agents['time'][j] > 14*24:
                            agents['time'][j] = 0
                            agents['state'][j] = 'Recovered'

                        else:
                            agents['time'][j] +=1

                # New displacements (prior velocity times change in time)
                deltax_temp = dt * agents['velocity'][j, 0]
                deltay_temp = dt * agents['velocity'][j, 1]
                # New positions
                x = agents['position'][j, 0] + deltax_temp
                y = agents['position'][j, 1] + deltay_temp
                # Compute new velocity
                vx_temp = deltax_temp / dt
                vy_temp = deltay_temp / dt

                # Add interaction
                for k in range(n_agents):
                    # Go through all other agents that could be interacted with
                    if k != j:
                        # Compute components of distance
                        dx = agents['position'][j, 0] - agents['position'][k, 0]
                        dy = agents['position'][j, 1] - agents['position'][k, 1]
                        # Compute distance between agents
                        dist_temp = np.sqrt(dx ** 2 + dy ** 2)
                        # If distance of interaction is closer than both radii, collide
                        if dist_temp <= 1:
                            agents['touch'][j] += 1
                            # Calculate if agents are infected
                            agent_j_infected = agents['state'][j] == 'Infected'
                            agent_k_infected = agents['state'][k] == 'Infected'
                            # Calculate if agents have recovered
                            agent_k_recover = agents['state'][k] == 'Recovered'
                            # Calculate if agents are susceptible
                            agent_j_suscept = agents['state'][j] == 'Susceptible'
                            agent_k_suscept = agents['state'][k] == 'Susceptible'
                            # Calculate if agents are symptomatic
                            agent_j_sympt = agents['symptomatic'][j] == 1
                            # Store time agent has been in this state
                            agent_j_time = agents['time'][j]
                            # If agent j is infected and agent k is susceptible
                            if agent_j_infected:
                                if agent_j_sympt and agent_k_suscept:
                                    # Calculate probability of infection
                                    temp_gam = np.random.gamma(g_shape, g_scale)
                                    if temp_gam >= 1:
                                        # Are the agents wearing masks
                                        agent_j_mask = agents['mask'][j] == True
                                        agent_k_mask = agents['mask'][k] == True
                                        # If the infected is not wearing a mask
                                        if not agent_j_mask and agent_k_mask:
                                            if np.random.random() >= .85:
                                                agents['state'][k] = 'Exposed'
                                                if np.random.random() >= per_asympt:
                                                    agents['symptomatic'][k] = 1
                                                    agents['color'][k] = 'Violet'
                                                    agents['num infected'][j] += 1
                                                else:
                                                    agents['symptomatic'][k] = 0
                                                    agents['color'][k] = 'Indigo'
                                                agents['time'][k] = 1
                                                agents['touch'][j] += 1

                                        # If the susceptible is wearing a mask
                                        elif agent_j_mask and not agent_k_mask:
                                            if np.random.random() >= .95:
                                                agents['state'][k] = 'Exposed'
                                                if np.random.random() >= per_asympt:
                                                    agents['symptomatic'][k] = 1
                                                    agents['color'][k] = 'Violet'
                                                    agents['num infected'][j] += 1
                                                else:
                                                    agents['symptomatic'][k] = 0
                                                    agents['color'][k] = 'Indigo'
                                                agents['time'][k] = 1


                                        # If neither are wearing masks
                                        elif not agent_j_mask and not agent_k_mask:
                                            agents['state'][k] = 'Exposed'
                                            if np.random.random() >= per_asympt:
                                                agents['symptomatic'][k] = 1
                                                agents['color'][k] = 'Violet'
                                                agents['num infected'][j] += 1
                                            else:
                                                agents['symptomatic'][k] = 0
                                                agents['color'][k] = 'Indigo'
                                            agents['time'][k] = 1         
                                elif not agent_j_sympt and agent_k_suscept:
                                    # Get the time that agent j has been infectious
                                    agent_j_time = agents['time'][j]
                                    # Normalize time to infectious period
                                    agent_j_norm_time = agent_j_time / asympt_infect
                                    # Define the probability of asymptomatic infect
                                    temp_gam = np.random.gamma(g_shape, g_scale)
                                    asympt_gam = temp_gam * asym_prob * agent_j_norm_time
                                    if asympt_gam >=1:
                                        # Are the agents wearing masks
                                        agent_j_mask = agents['mask'][j] == True
                                        agent_k_mask = agents['mask'][k] == True

                                        # If the infected is not wearing a mask
                                        if not agent_j_mask and agent_k_mask:
                                            if np.random.random() >= .85:
                                                agents['state'][k] = 'Exposed'
                                                if np.random.random() >= per_asympt:
                                                    agents['symptomatic'][k] = 1
                                                    agents['color'][k] = 'Violet'
                                                    agents['num infected'][j] += 1
                                                else:
                                                    agents['symptomatic'][k] = 0
                                                    agents['color'][k] = 'Indigo'
                                                agents['time'][k] = 1

                                        # If the susceptible is wearing a mask
                                        elif agent_j_mask and not agent_k_mask:
                                            if np.random.random() >= .95:
                                                agents['state'][k] = 'Exposed'
                                                if np.random.random() >= per_asympt:
                                                    agents['symptomatic'][k] = 1
                                                    agents['color'][k] = 'Violet'
                                                    agents['num infected'][j] += 1
                                                else:
                                                    agents['symptomatic'][k] = 0
                                                    agents['color'][k] = 'Indigo'
                                                agents['time'][k] = 1

                                        # If neither are wearing masks
                                        elif not agent_j_mask and not agent_k_mask:
                                            agents['state'][k] = 'Exposed'
                                            if np.random.random() >= per_asympt:
                                                agents['symptomatic'][k] = 1
                                                agents['color'][k] = 'Violet'
                                                agents['num infected'][j] += 1
                                            else:
                                                agents['symptomatic'][k] = 0
                                                agents['color'][k] = 'Indigo'
                                            agents['time'][k] = 1
                                # Calculate if infection would have occured
                                elif agent_j_sympt:
                                    if agent_k_infected or agent_k_recover:
                                        # Get the time that agent j has been infectious
                                        agent_j_time = agents['time'][j]
                                        # Normalize time to infectious period
                                        agent_j_norm_time = agent_j_time / asympt_infect
                                        # Define the probability of asymptomatic infect
                                        temp_gam = np.random.gamma(g_shape, g_scale)
                                        asympt_gam = temp_gam * asym_prob * agent_j_norm_time
                                        if temp_gam >= 1:
                                            # Are the agents wearing masks
                                            agent_j_mask = agents['mask'][j] == True
                                            agent_k_mask = agents['mask'][k] == True
                                            # If the infected is not wearing a mask
                                            if not agent_j_mask and agent_k_mask:
                                                if np.random.random() >= .85/2:
                                                    agents['num infected'][j] += 1
                                            # If the susceptible is wearing a mask
                                            elif agent_j_mask and not agent_k_mask:
                                                if np.random.random() >= .95/2:
                                                    agents['num infected'][j] += 1
                                            # If neither are wearing masks
                                            elif not agent_j_mask and not agent_k_mask:
                                                if np.random.random() >= .5:
                                                    agents['num infected'][j] += 1
                                elif not agent_j_sympt:
                                    if agent_k_infected or agent_k_recover:
                                        # Get the time that agent j has been infectious
                                        agent_j_time = agents['time'][j]
                                        # Normalize time to infectious period
                                        agent_j_norm_time = agent_j_time / asympt_infect
                                        # Define the probability of asymptomatic infect
                                        temp_gam = np.random.gamma(g_shape, g_scale)
                                        asympt_gam = temp_gam * asym_prob * agent_j_norm_time
                                        if asympt_gam >=1:
                                            # Are the agents wearing masks
                                            agent_j_mask = agents['mask'][j] == True
                                            agent_k_mask = agents['mask'][k] == True
                                            # If the infected is not wearing a mask
                                            if not agent_j_mask and agent_k_mask:
                                                if np.random.random() >= .85/2:
                                                    agents['num infected'][j] += 1
                                            # If the susceptible is wearing a mask
                                            elif agent_j_mask and not agent_k_mask:
                                                if np.random.random() >= .95/2:
                                                    agents['num infected'][j] += 1
                                            # If neither are wearing masks
                                            elif not agent_j_mask and not agent_k_mask:
                                                if np.random.random() >= .5:
                                                    agents['num infected'][j] += 1


                # Bounce agents off wall if projected position is beyond boundary conditions
                if x >= xmax:
                    x = 2 * xmax - deltax_temp - agents['position'][j, 0]
                    vx_temp *= -1
                elif x <= 0:
                    x = - deltax_temp - agents['position'][j, 0]
                    vx_temp *= -1
                elif y >= ymax:
                    y = 2 * ymax - deltay_temp - agents['position'][j, 1]
                    vy_temp *= -1
                elif y <= 0:
                    y = - deltay_temp - agents['position'][j, 1]
                    vy_temp *= -1

                # 
                agents['position'][j] = np.array([x, y])
                agents['velocity'][j, 0] = vx_temp
                agents['velocity'][j, 1] = vy_temp
                temp_agents = str(agents['position'][j][0]) + ',' + str(agents['position'][j][1]) + \
                              ',' + str(agents['state'][j]) + ',' + str(agents['symptomatic'][j]) + \
                              ',' + str(agents['num infected'][j]) + ',' + str(agents['mask'][j]) + '\n'
                e.write(temp_agents)

            # Get values of the current time step
            temp_infected = sum(agents['state']=='Infected')
            temp_recovered = sum(agents['state']=='Recovered')
            temp_infect_mask = sum(agents[agents['mask']==True]['state'] == 'Infected')
            temp_suscept_mask = sum(agents[agents['mask']==True]['state'] == 'Susceptible')
            temp_exposed = sum(agents['state']=='Exposed')
            temp_infect_sympt = sum(agents[agents['symptomatic']==1]['state'] == 'Infected')
            temp_infect_asympt = sum(agents[agents['symptomatic']==0]['state'] == 'Infected')
            temp_write = str(i) + ',' + str(round(per_shelt * .1, 1)) + ',' + \
                         str(round(per_mask * .1, 1)) + ',' + str(temp_infected)+ ',' \
                         + str(temp_exposed) + ',' +  str(temp_recovered) + ',' + \
                         str(temp_infect_mask) + ',' + str(temp_suscept_mask) + ',' + \
                         str(temp_infect_sympt) + ',' + str(temp_infect_asympt) + ',' +\
                         str(new_infected) + ',' +  str(per_mask) + '\n'
            # Save current data to a file
            f.write(temp_write)
        # Close file
        f.close()
        e.close()
