# 2020-04-08
# Benjamin Adam Catching
# Andino Lab, UCSF
# Mask Usefulness Against Infectious Agent Propagation

# Import packages
import numpy as np

# Fixing random state for reproducibility
np.random.seed(100)

"""Write each step of each simulation to a .csv file"""
# Initialize file
f = open('all_conditions.csv', 'w')
# Write header of the file
f.write('# Data from simulation of 200 agents with various levels\
 of sheltering or mask usage\n')
f.write('time,percent sheltering,percent wearing masks,infected,recovered,\
    infected with mask,susceptible with mask')

"""Iterate over all conditions"""
# Define the current condition (g = percent sheltering, h = percent masked)
for g in range(10):
    for h in range(10):
        
        """Values of the simulation"""
        # Number of steps
        N_steps = 1000
        # Number of agents
        n_agents = 200
        # Set delta t (time between steps)
        dt = .1
        # Set velocity
        velo = .2
        # Set percent of sheltering in place (e.g. 0.1, 0.5...)
        per_shelt = round(g * .1, 1)

        # Define the array of agents with given properties
        agents = np.zeros(n_agents, dtype=[('position', float, 2),
                                          ('velocity', float, 2),
                                          ('color', str, 20),
                                          ('state', str, 20),
                                          ('time', int, 1),
                                          ('mask', bool, 1)])

        """Calculate initial values of agents"""
        # Define the initial random positions within the figure
        agents['position'] = np.random.uniform(0, 4, (n_agents, 2))
        # Define the initial velocity angles
        init_angles = np.random.uniform(0, 2 * np.pi, n_agents)
        # Get initial x and y velocities from angles
        velocities = np.array([[sin(x), cos(x)] for x in init_angles]) * velo
        # Get percentage of agents 'sheltering'
        num_shelt = int(per_shelt * n_agents)
        # Make sheltering agents static (if any)
        velocities[:num_shelt] = np.zeros((num_shelt, 2))

        """Assign values to agents"""
        # Assign velocities
        agents['velocity'] = velocities
        # Assign color (Navy is the default susceptible agent)
        agents['color'] = np.array(['Navy'] * n_agents)
        #
        agents['state'] = np.array(['Susceptible'] * n_agents)
        agents['time'] = np.array([0] * n_agents)
        per_mask = [True] * h + [False] * (10-h)
        agents['mask'] = np.random.choice(per_mask, 200, replace=True)
        agents['color'][agents['mask'] == True] = 'Dodgerblue'

        # Make the one agent infected
        agents['color'][0] = 'Firebrick'
        agents['state'][0] = 'Infected'
        agents['time'][0] = 1
        agents['mask'][0] = False

        """Define the values of the display"""
        # Set boundaries for the agents to run around
        xboundaries = [0, 4]
        yboundaries = [0, 4]
        xmax, ymax = xboundaries[1], yboundaries[1]
        # Define the figure
        fig = plt.figure()
        ax = plt.axes(xlim=(0, xmax), ylim=(0, ymax))
        # Initialize the plot
        scatter = ax.scatter(agents['position'][:, 0], 
                             agents['position'][:, 1],
                             color=agents['color'])

        def update(i):
            """
            Take the information from the data stored in the agents array
            to calculate if an infected agent recovers, if two agents 
            interact, and if the agent bounces off a boundary
            """


            # Iterate over all agents 
            for j in range(n_agents):
                if agents['time'][j] != 0:
                    agent_j_infected = agents['state'][j] == 'Infected'
                    agent_j_time = agents['time'][j] >= 200
                    if agent_j_infected and agent_j_time:
                        agents['state'][j] = 'Recovered'
                        agents['color'][j] = 'Darkgreen'
                        agents['time'][j] = 0
                    elif agent_j_infected:
                        agents['time'][j] += 1
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
                        if dist_temp <= .05:
                            # If one of the agents is infected, determine if 
                            # the other agent should be infected, if both are 
                            # wearing a mask no one is infected
                            agent_j = agents['state'][j] == 'Infected'
                            agent_k = agents['state'][k] == 'Susceptible'
                            if agent_j and agent_k:
                                agent_k_mask = agents['mask'][j]
                                agent_j_mask = agents['mask'][k]
                                # If susceptible agent is wearing a mask
                                if not agent_j_mask and agent_k_mask:
                                    # 50% chance of infection
                                    if np.random.random() >= .5:
                                        # Update susceptible to infected
                                        agents['state'][k] = 'Infected'
                                        agents['color'][k] = 'Orangered'
                                        agents['time'][k] = 1
                                # If infected agent is wearing a mask
                                elif agent_j_mask and not agent_k_mask:
                                    # 5% chance of infection
                                    if np.random.random() >= .95:
                                        # Update susceptible to infected
                                        agents['state'][k] = 'Infected'
                                        agents['color'][k] = 'Firebrick'
                                        agents['time'][k] = 1
                                # If neither are wearing a mask
                                elif not agent_j_mask and not agent_k_mask:
                                    agents['state'][k] = 'Infected'
                                    agents['color'][k] = 'Firebrick'
                                    agents['time'][k] = 1

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

                # Update the scatter collection, with the new colors, sizes and positions.
                scatter.set_color(agents['color'])
                scatter.set_offsets(agents['position'])

            # Get values of the current time step
            temp_infected = sum(agents['state']=='Infected')
            temp_recovered = sum(agents['state']=='Recovered')
            temp_infect_mask = sum(agents[agents['mask']==True]['state'] == 'Infected')
            temp_suscept_mask = sum(agents[agents['mask']==True]['state'] == 'Susceptible')
            temp_write = str(i) + ',' + str(round(g * .1, 1)) + ',' + \
                         str(round(h * .1, 1)) + ',' + str(temp_infected) \
                         + ',' + str(temp_recovered) + ',' + \
                         str(temp_infect_mask) + ',' + str(temp_suscept_mask) \
                         + '\n'
            # Save current data to a file
            f.write(temp_write)

        # Animate the simulation by iterating
        animation = FuncAnimation(fig, update, frames=N_steps, interval=20)
        temp_name = 'baseline_'+ str(h) + '0percent_masked_' + str(g) + '0percent_shelter.gif'
        animation.save(temp_name, writer='imagemagick')
f.close()