#The following are codes for monte carlo simulation
import numpy as np
import matplotlib.pyplot as plt

# added  -------------------- 
from random import randint 

dir = "./img"
# ---------------------------

class Road:
    def __init__(self, length, intersection):
        self.length = length
        self.intersection = intersection
        self.vehicles = []  # List to store vehicles on the road
        self.green_time = 0
        self.red_time = 0

class Intersection:
    def __init__(self, roads):
        self.roads = roads

class Vehicle:
    def __init__(self, position, speed, arrival_time):
        self.position = position
        self.speed = speed
        self.arrival_time = arrival_time

class TrafficLight:
    def __init__(self, road, mode='fixed'):
        self.road = road
        self.mode = mode

    def update(self, time_step):
        if self.mode == 'fixed':
            self.road.green_time -= time_step
            self.road.red_time -= time_step
            if self.road.green_time <= 0 and self.road.red_time <= 0:
                self.road.green_time = 45  # Switch to green for 45 seconds
                self.road.red_time = 156  # Switch to red for 156 seconds
        elif self.mode == 'smart':
            num_vehicles = len(self.road.vehicles)
            if num_vehicles > 0:
                for road in self.road.intersection.roads:
                    if road == self.road:
                        road.green_time = max(45, road.green_time)  # Minimum green time of 45 seconds
                        road.red_time = 0
                    else:
                        road.red_time += time_step
            else:
                for road in self.road.intersection.roads:
                    road.green_time = 0
                    road.red_time += time_step

class TrafficSystem:
    def __init__(self, roads, intersections, traffic_lights):
        self.roads = roads
        self.intersections = intersections
        self.traffic_lights = traffic_lights
        self.time_step = 1

    def simulate(self, duration):
        time = 0
        total_wait_time = 0
        num_vehicles_waited = 0

        while time < duration:
            for light in self.traffic_lights:
                light.update(self.time_step)

            # Simulate vehicle movement
            for road in self.roads:
                road.vehicles = [vehicle for vehicle in road.vehicles if vehicle.position < road.length]
                for vehicle in road.vehicles:
                    vehicle.position += vehicle.speed
                    if vehicle.position >= road.length:
                        wait_time = time - vehicle.arrival_time
                        total_wait_time += wait_time
                        num_vehicles_waited += 1
                if np.random.rand() < 0.3:  # 30% chance of a new vehicle arrival
                    speed = np.random.randint(1, 6)  # Random speed between 1 and 5
                    vehicle = Vehicle(position=0, speed=speed, arrival_time=time)
                    road.vehicles.append(vehicle)

            time += self.time_step

        if num_vehicles_waited > 0:
            return total_wait_time / num_vehicles_waited
        else:
            return 0

def main(roadlengths, trafficlightmodes, cnt):
    # Define the components
    road1 = Road(length=roadlengths[0], intersection=None)
    road2 = Road(length=roadlengths[1], intersection=None)
    road3 = Road(length=roadlengths[2], intersection=None)
    road4 = Road(length=roadlengths[3], intersection=None)
    intersection = Intersection(roads=[road1, road2, road3, road4])
    traffic_light1 = TrafficLight(road=road1, mode=trafficlightmodes[0])
    traffic_light2 = TrafficLight(road=road2, mode=trafficlightmodes[1])
    traffic_light3 = TrafficLight(road=road3, mode=trafficlightmodes[2])
    traffic_light4 = TrafficLight(road=road4, mode=trafficlightmodes[3])
    road1.intersection = intersection
    road2.intersection = intersection
    road3.intersection = intersection
    road4.intersection = intersection
    roads = [road1, road2, road3, road4]
    intersections = [intersection]
    traffic_lights = [traffic_light1, traffic_light2, traffic_light3, traffic_light4]

    # Set up simulation parameters
    simulation_durations = range(100, 1001, 100)

    # Create empty lists to store data for plotting
    time_steps = []
    congestion_traditional = []
    congestion_smart = []

    # Run the simulation for different time durations
    for duration in simulation_durations:
        # Create the traffic system
        traffic_system = TrafficSystem(roads=roads, intersections=intersections, traffic_lights=traffic_lights)
        congestion_traditional.append(traffic_system.simulate(duration=duration))

        congestion_smart.append(traffic_system.simulate(duration=duration))

        time_steps.append(duration)

    # Plot the results for traditional traffic light
    plt.plot(time_steps, congestion_traditional, label='Traditional Traffic Light')
    plt.xlabel('Time Duration')
    plt.ylabel('Congestion Level')
    # plt.title('Congestion Level - Traditional Traffic Light')
    plt.title(f'Congestion Level - Traditional Traffic Light\nRoad lengths: {roadlengths}\nModes: {trafficlightmodes}',fontsize=8)
    plt.legend()
    plt.savefig(f"{dir}/{str(cnt).zfill(4)}_traditional.png")

    # Plot the results for smart traffic light
    plt.plot(time_steps, congestion_smart, label='Smart Traffic Light')
    plt.xlabel('Time Duration')
    plt.ylabel('Congestion Level')
    # plt.title('Congestion Level - Smart Traffic Light')
    plt.title(f'Congestion Level - Smart Traffic Light\nRoad lengths: {roadlengths}\nModes: {trafficlightmodes}',fontsize=8)
    plt.legend()
    plt.savefig(f"{dir}/{str(cnt).zfill(4)}_smart.png")

# added -------------------
for cnt in range(100):
    print(cnt,"/ 100")
    roadlengths = [randint(100, 500) for _ in range(4)]
    trafficlightmodes = [["fixed","smart"][randint(0,1)] for _ in range(4)] # 50 : 50 = fixed : smart
    main(roadlengths,trafficlightmodes,cnt)
 # ------------------------
