import pandas as pd
import numpy as np
import random


#selecionou 4 drivers e 1 construtor
'''def optimal_team(drivers_cost, drivers_points, constructors_cost, constructors_points, budget, driver_order, carrinhos):
    
    n = len(drivers_points)
    m = len(constructors_points)
    
    # Creating a 2D list full of zeros
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, budget + 1):
            # Check if the current driver can be included in the team
            if drivers_cost[i - 1] <= w:
                # Choose the maximum of including or excluding the current driver
                dp[i][w] = max(drivers_points[i - 1] + dp[i - 1][w - drivers_cost[i - 1]], dp[i - 1][w])
            else:
                # If the current driver's cost is more than the available budget, exclude the driver
                dp[i][w] = dp[i - 1][w]

    # Track the selected drivers
    selected_drivers = []
    i, w = n, budget
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            selected_drivers.append(i - 1)
            w -= drivers_cost[i - 1]
        i -= 1

    # Track the selected constructor
    constructor_index = dp[n][budget]
    selected_constructor = constructor_index % (m + 1)  # Calculate the selected constructor index
    
    # Output the results
    print("Maximum points:", dp[n][budget])

    print("\nSelected drivers:")
    for driver_index in selected_drivers:
        print(f"{driver_order[driver_index]} - Points: {drivers_points[driver_index]}, Cost: {drivers_cost[driver_index]}")

    print("\nSelected constructor:")
    print(f"{carrinhos[selected_constructor]} - Points: {constructors_points[selected_constructor]}, Cost: {constructors_cost[selected_constructor]}")
'''

# selecinou 5 drivers apenas
'''def optimal_team(drivers_cost, drivers_points, constructors_cost, constructors_points, budget, driver_order, carrinhos):
    
    n = len(drivers_points)
    m = len(constructors_points)
    
    # Creating a 3D list full of zeros
    dp = [[[0 for _ in range(budget + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

    for j in range(1, m + 1):
        for i in range(1, n + 1):
            for w in range(1, budget + 1):
                # Check if the current driver can be included in the team
                if drivers_cost[i - 1] <= w:
                    # Choose the maximum of including or excluding the current driver
                    dp[j][i][w] = max(drivers_points[i - 1] + dp[j][i - 1][w - drivers_cost[i - 1]], dp[j][i - 1][w])
                    # Check if the current constructor can be included in the team
                    if j > 0 and constructors_cost[j - 1] <= w:
                        # Choose the maximum of including or excluding the current constructor
                        dp[j][i][w] = max(dp[j][i][w], constructors_points[j - 1] + dp[j - 1][i - 1][w - constructors_cost[j - 1]])
                else:
                    # If the current driver's cost is more than the available budget, exclude the driver
                    dp[j][i][w] = dp[j][i - 1][w]

    # Track the selected drivers
    selected_drivers = []
    i, j, w = n, m, budget
    while i > 0 and w > 0:
        if dp[j][i][w] != dp[j][i - 1][w]:
            selected_drivers.append(i - 1)
            w -= drivers_cost[i - 1]
        i -= 1

    # Track the selected constructors
    selected_constructors = []
    while j > 0 and w > 0:
        if dp[j][i][w] != dp[j - 1][i][w]:
            selected_constructors.append(j - 1)
            w -= constructors_cost[j - 1]
        j -= 1

    # Output the results
    print("Maximum points:", dp[m][n][budget])

    print("\nSelected drivers:")
    for driver_index in selected_drivers:
        print(f"{driver_order[driver_index]} - Points: {drivers_points[driver_index]}, Cost: {drivers_cost[driver_index]}")

    print("\nSelected constructors:")
    for constructor_index in selected_constructors:
        print(f"{carrinhos[constructor_index]} - Points: {constructors_points[constructor_index]}, Cost: {constructors_cost[constructor_index]}")
'''

# seleciona drivers ate o budget ser fully gasto
def optimal_team(drivers_cost, drivers_points, constructors_cost, constructors_points, budget, driver_order, carrinhos):
    
    n = len(drivers_points)
    m = len(constructors_points)
    
    # Creating a 3D list full of zeros
    dp = [[[0 for _ in range(budget + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

    for j in range(1, m + 1):
        for i in range(1, n + 1):
            for w in range(1, budget + 1):
                # Check if the current driver can be included in the team
                if drivers_cost[i - 1] <= w:
                    # Choose the maximum of including or excluding the current driver
                    dp[j][i][w] = max(drivers_points[i - 1] + dp[j][i - 1][w - drivers_cost[i - 1]], dp[j][i - 1][w])
                    # Check if the current constructor can be included in the team
                    if j > 0 and constructors_cost[j - 1] <= w:
                        # Choose the maximum of including or excluding the current constructor
                        dp[j][i][w] = max(dp[j][i][w], constructors_points[j - 1] + dp[j - 1][i - 1][w - constructors_cost[j - 1]])
                else:
                    # If the current driver's cost is more than the available budget, exclude the driver
                    dp[j][i][w] = dp[j][i - 1][w]

    # Track the selected drivers
    selected_drivers = []
    i, j, w = n, m, budget
    while i > 0 and w > 0:
        if dp[j][i][w] != dp[j][i - 1][w]:
            selected_drivers.append(i - 1)
            w -= drivers_cost[i - 1]
        i -= 1

    # Track the selected constructors
    selected_constructors = []
    while j > 0 and w > 0:
        if dp[j][i][w] != dp[j - 1][i][w]:
            selected_constructors.append(j - 1)
            w -= constructors_cost[j - 1]
        j -= 1

    # Ensure that exactly 5 drivers and 2 constructors are selected
    while len(selected_drivers) < 5:
        selected_drivers.append(i)
        i -= 1

    while len(selected_constructors) < 2:
        selected_constructors.append(j)
        j -= 1

    # Output the results
    print("Maximum points:", dp[m][n][budget])

    print("\nSelected drivers:")
    for driver_index in selected_drivers:
        print(f"{driver_order[driver_index]} - Points: {drivers_points[driver_index]}, Cost: {drivers_cost[driver_index]}")

    print("\nSelected constructors:")
    for constructor_index in selected_constructors:
        print(f"{carrinhos[constructor_index]} - Points: {constructors_points[constructor_index]}, Cost: {constructors_cost[constructor_index]}")


'''def optimal_team(drivers_cost, drivers_points, constructors_cost, constructors_points, budget, driver_order, carrinhos):
    
    n = len(drivers_points)
    m = len(constructors_points)
    
    # Creating a 3D list full of zeros
    dp = [[[0 for _ in range(budget + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

    for j in range(1, m + 1):
        for i in range(1, n + 1):
            for w in range(1, budget + 1):
                # Check if the current driver can be included in the team
                if drivers_cost[i - 1] <= w:
                    # Choose the maximum of including or excluding the current driver
                    dp[j][i][w] = max(drivers_points[i - 1] + dp[j][i - 1][w - drivers_cost[i - 1]], dp[j][i - 1][w])
                    # Check if the current constructor can be included in the team
                    if j > 0 and constructors_cost[j - 1] <= w:
                        # Choose the maximum of including or excluding the current constructor
                        dp[j][i][w] = max(dp[j][i][w], constructors_points[j - 1] + dp[j - 1][i - 1][w - constructors_cost[j - 1]])
                else:
                    # If the current driver's cost is more than the available budget, exclude the driver
                    dp[j][i][w] = dp[j][i - 1][w]

    # Track the selected drivers
    selected_drivers = []
    i, j, w = n, m, budget
    while i > 0 and w > 0:
        if dp[j][i][w] != dp[j][i - 1][w]:
            selected_drivers.append(i - 1)
            w -= drivers_cost[i - 1]
        i -= 1

    # Track the selected constructors
    selected_constructors = []
    while j > 0 and w > 0:
        if dp[j][i][w] != dp[j - 1][i][w]:
            selected_constructors.append(j - 1)
            w -= constructors_cost[j - 1]
        j -= 1

    # Ensure that exactly 5 drivers and 2 constructors are selected
    selected_drivers = selected_drivers[:5]  # Select only the first 5 drivers

    # Select exactly 2 constructors
    while len(selected_constructors) < 2 and j > 0 and w >= constructors_cost[j - 1]:
        selected_constructors.append(j - 1)
        w -= constructors_cost[j - 1]
        j -= 1

    # Output the results
    print("Maximum points:", dp[m][n][budget])

    print("\nSelected drivers:")
    for driver_index in selected_drivers:
        print(f"{driver_order[driver_index]} - Points: {drivers_points[driver_index]}, Cost: {drivers_cost[driver_index]}")

    print("\nSelected constructors:")
    for constructor_index in selected_constructors:
        print(f"{carrinhos[constructor_index]} - Points: {constructors_points[constructor_index]}, Cost: {constructors_cost[constructor_index]}")

    # Calculate and print the remaining budget
    spent_budget = sum(drivers_cost[i] for i in selected_drivers) + sum(constructors_cost[j] for j in selected_constructors)
    remaining_budget = budget - spent_budget
    print(f"\nTotal budget spent: {spent_budget}")
    print(f"Remaining budget: {remaining_budget}")
'''







driver_order = ['wtf is a km', 'bolinho','hulk','debries',
                'albino', 'xinoca','xinoca da ilha', 'rico',
                'lindao','gelado', 'sapato', 'gigachad', 
                'cone', 'flopis', 'luis', 'eslay',
                'espetador', 'peras', 'i am stupid', 'sid']

carrinhos = ['Williams', 'AlphaTauri',
             'Haas','AstonMartin',
             'AlfaRomeo','McLaren',
             'Alpine','Mercedes',
             'Ferrari','RedBull']

drivers_cost = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
drivers_points = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]

constructors_cost = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
constructors_points = [2, 6, 8, 10, 12, 15, 20, 30, 50]

budget = 100

optimal_team(drivers_cost, drivers_points, constructors_cost, constructors_points, budget, driver_order, carrinhos)





#quick way to create the values without thinking
# random_list = [random.randint(5, 30) for _ in range(20)]
# print(random_list)


