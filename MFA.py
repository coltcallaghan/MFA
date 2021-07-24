import math
from math import sqrt
import numpy as np
import sys

# Get the 10 figure grid references for user (Mortar Line)
def get_my_grids():
    my_grid_x = int(input("What is your 5 figure X asis reference? "))
    my_grid_y = int(input("What is your 5 figure Y asis reference? "))
    print("\nYour grid is: ",my_grid_x, " ", my_grid_y, "\n")
    return my_grid_x, my_grid_y 

# Get the 10 figure grid references for enemy
def get_enemy_grids():
    enemy_grid_x = int(input("What is the enemies 5 figure X asis reference? "))
    enemy_grid_y = int(input("What is the enemies 5 figure Y asis reference? "))
    print("\nEnemy grid is: ",enemy_grid_x, " ", enemy_grid_y, "\n")
    return enemy_grid_x, enemy_grid_y

# Find length of sides of triangle
def get_length(my_grid_x, my_grid_y, enemy_grid_x, enemy_grid_y):
    length_x = enemy_grid_x -my_grid_x 
    length_y = enemy_grid_y - my_grid_y
    # print("X co-ord length", length_x)
    # print("Y co-ord length",length_y)
    return length_x, length_y


# Find out the distance to the enemy
def calculate_distance(length_x, length_y):
    displacement = round(sqrt(length_x * length_x + length_y * length_y))
    print("\nDistance to target is: ", displacement, "m \n")
    return displacement

# Figure out what quadrant bearing is in and what the value is
def get_bearing(my_grid_x, my_grid_y, enemy_grid_x, enemy_grid_y, length_x, length_y):
    bearing = 0
    if (enemy_grid_x > my_grid_x):
        if (enemy_grid_y > my_grid_y):
            bearing = round((math.atan2(length_y, length_x))*1018.5916357881)
            # 1st quadrant
        else:
            bearing = round((math.atan2(-length_y, length_x))*1018.5916357881) + 1600 
            # 2nd quadrant
    if (enemy_grid_x < my_grid_x):
        if (enemy_grid_y > my_grid_y):
            bearing = round((math.atan2(length_y, -length_x))*1018.5916357881) + 4800
            # 3rd quadrant
        else:
            bearing = round((math.atan2(-length_y, length_x))*1018.5916357881) + 1600
            # 4th quadrant
    return bearing

# Figure out the elevation on which to fire
def get_velocity(displacement):
    initial_velocity = 0
    charge = 0
    if displacement < 520 : # Could not get the exact numbers and v from ballistic kernel
        initial_velocity = 73 
        charge = "primary"
        return initial_velocity, charge
    elif displacement > 520 and displacement < 1120:
        charge = 1
        initial_velocity = 110 
        return initial_velocity, charge
    elif displacement > 1120 and displacement < 1710:
        charge = 2
        initial_velocity = 137 
        return initial_velocity, charge
    elif displacement > 1710 and displacement < 2265:
        charge = 3
        initial_velocity = 162 
        return initial_velocity, charge
    elif displacement > 2265 and displacement < 3080:
        charge = 4
        initial_velocity = 195 
        return initial_velocity, charge
    elif displacement > 3080 and displacement < 3850:
        charge = 5
        initial_velocity = 224 
        return initial_velocity, charge
    elif displacement > 3850:
        initial_velocity = 250 
        charge = 6
        return initial_velocity, charge
    return initial_velocity, charge

def get_elevation(displacement, initial_velocity):
    g = 9.81 #acceleration due to gravity
    X = (g * displacement) / (initial_velocity * initial_velocity)
    elev_radians = np.arcsin(X) # Check (Might need to re add *.5)
    elevation = int(round(elev_radians * 1018.5916357881))
    return elevation

def main():
    print("Can only hit targets less than 4680m away \n")
    my_grid_x, my_grid_y = get_my_grids()
    enemy_grid_x, enemy_grid_y = get_enemy_grids()
    length_x, length_y = get_length(my_grid_x, my_grid_y, enemy_grid_x, enemy_grid_y)
    displacement = calculate_distance(length_x, length_y)
    if  displacement < 200:
        print("Danger close!")
        sys.exit()
    if  displacement > 4680:
        print("The target is too far away!")
        sys.exit()
    bearing = get_bearing(my_grid_x, my_grid_y, enemy_grid_x, enemy_grid_y, length_x, length_y)
    initial_velocity, charge = get_velocity(displacement)
    elevation = get_elevation(displacement, initial_velocity)
    print("Charge " , charge)
    print("Bearing ", bearing, " mils")
    print("Elevation ", elevation, " mils")


main()
