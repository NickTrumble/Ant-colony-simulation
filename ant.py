#class containing ants
import numpy as np
import pygame

class Ant:

    def __init__(self, pos, col = (50, 30, 0)):
        #individual ant stuff - keep
        self.col = col
        self.sf = 1
        self.body = 3 * self.sf
        self.head = 4 * self.sf
        self.tail = 5 * self.sf
        
        self.hasFood = False
        self.target = None
        self.food = 0

        (self.x, self.y) = pos
        self.theta = np.random.uniform(0, 2 * np.pi)

    def move(self, step_size, bounds, foodmap, nest, aPheromone, bPheromone):
        (newX, newY) = self.next_location(step_size, foodmap, aPheromone, bPheromone, nest)

        if newX < 0 or newX >= bounds.width:
            self.theta = np.pi - self.theta
            newX = np.clip(newX, 0, bounds.width - 1)
        if newY < 0 or newY >= bounds.height:
            self.theta = -self.theta
            newY = np.clip(newY, 0, bounds.height - 1)

        self.theta = (self.theta + 2 * np.pi) % (2 * np.pi)
        self.x = newX
        self.y = newY

        if not self.hasFood:
            self.take_food(foodmap, nest)
        else:
            self.return_food(nest)

    def next_location(self, step_size, foodmap, aPheremone, bPheremone, nest):
        self.follow_pheromone(aPheremone, bPheremone, foodmap, nest)
        if not self.hasFood:
            self.search_radius(foodmap)

            if self.target is not None:
                self.move_to_target()
        else:
            self.target = nest
            #self.move_to_target()

        newX = self.x + step_size * np.cos(self.theta)
        newY = self.y + step_size * np.sin(self.theta)
        return (newX, newY)

    # def pathfind_random(self):
    #     newTheta = self.theta + np.random.rand() - 0.5
    #     self.theta = (newTheta + 2 * np.pi) % (2 * np.pi)
    #     return

    def render(self, screen, xOff, yOff):
        headCenter = (
            (self.head + self.body) * np.cos(self.theta) + self.x + xOff, 
            (self.head + self.body) * np.sin(self.theta) + self.y + yOff
            )
        bodyCenter = (
            self.x + xOff, 
            self.y + yOff
            )
        tailCenter = (
                - (self.tail + self.body) * np.cos(self.theta) + self.x + xOff, 
                - (self.tail + self.body) * np.sin(self.theta) + self.y + yOff
                )
        
        pygame.draw.circle(screen, self.col, headCenter, self.head) #head
        pygame.draw.circle(screen, self.col, bodyCenter, self.body) #body
        pygame.draw.circle(screen, self.col, tailCenter, self.tail) #tail

    def move_to_target(self):
        dx, dy = (self.target[0] - self.x, self.target[1] - self.y)
        self.theta = np.arctan2(dy, dx) + np.random.uniform(-0.5, 0.5)

    def search_radius(self, foodmap, radius = 15):
        x, y = int(self.x), int(self.y)
        xmin = max(x - radius, 0)
        xmax = min(x + radius, foodmap.shape[0] - 1)
        ymin = max(y - radius, 0)
        ymax = min(y + radius, foodmap.shape[1] - 1)

        local_food = foodmap[xmin:xmax, ymin:ymax]

        food = np.argwhere(local_food > 0)

        best_index = None
        best_dist = np.inf
        for i, j in food:
            dx, dy = i + xmin, j + ymin
            dist = (x - dx) ** 2 + (y - dy) ** 2
            if dist < best_dist:
                best_dist = dist
                best_index = (dx, dy)

        self.target = best_index        

    def take_food(self, foodmap, nest):
        x, y = int(self.x), int(self.y)

        if np.any(foodmap[x - 1:x + 1, y - 1:y + 1]) > 0:
            foodmap[x - 1:x + 1, y - 1:y + 1] = np.maximum(foodmap[x - 1:x + 1, y - 1:y + 1] - 0.5, 0)

            self.hasFood = True
            self.food += 0.5
            self.target = nest

    def return_food(self, nest):
        if not self.hasFood:
            return
       
        x, y = int(self.x), int(self.y)

        if abs(x - nest[0]) < 2 and abs(y - nest[1]) < 2:
            self.food = 0
            self.hasFood = False
            self.target = None

    def follow_pheromone(self, aPheromone, bPheromone, foodmap, nest):
        sensor_dist = 5
        sensor_angle = np.pi / 6 #30 degrees left and right
        turn_strength = 0.3

        left_angle = self.theta - sensor_angle
        right_angle = self.theta + sensor_angle
        forward_angle = self.theta

        left_score = self.sample_angle(aPheromone, bPheromone, foodmap, nest, left_angle, sensor_dist)
        right_score = self.sample_angle(aPheromone, bPheromone, foodmap, nest, right_angle, sensor_dist)
        front_score = self.sample_angle(aPheromone, bPheromone, foodmap, nest, forward_angle, sensor_dist)

        #store score for all three sides and move towards the best
        #searching for food:
        #aPheromone  - 1, bPheromone + 1
        #finding nest
        #aPheromone  + 1, bPheromone - 1

        turn = 0.0 #how far to turn
        if left_score > right_score and left_score > front_score:
            turn -= turn_strength
        elif right_score > front_score:
            turn += turn_strength
        else:
            turn = 0.0
        
        self.theta += turn + np.random.uniform(-0.1, 0.1)

    def sample_angle(self, aPheromone, bPheromone, foodmap, nest, angle, sensor_dist):
        (x, y) = int(self.x), int(self.y)
        (dx, dy) = int(x + sensor_dist * np.cos(angle)), int(y + sensor_dist * np.sin(angle))

        if dx < 0 or dy < 0 or dx > foodmap.shape[0] - 1 or dy > foodmap.shape[1] - 1:
            return 0.0

        score = 0.0
        if not self.hasFood:
            #follow bPheromone and foodmap
            score += foodmap[dx, dy] * 2
            score += bPheromone[dx, dy] * 5
            score -= aPheromone[dx, dy] * 0.3

        else:
            score += aPheromone[dx, dy] * 3
            score -= bPheromone[dx, dy] * 0.2
            
            dist = (dx - nest[0]) ** 2 + (dy - nest[1]) ** 2
            score += 30.0 / (dist + 10.0)

        return score
    
    # def search_for_food(self, foodmap):
    #     radius = 10
    #     xmin = max(0, int(self.x - radius))
    #     xmax = min(foodmap.shape[0], int(self.x + radius))
    #     ymin = max(0, int(self.y - radius))
    #     ymax = min(foodmap.shape[1], int(self.y + radius))

    #     x, y = np.meshgrid(np.arange(xmin,xmax), np.arange(ymin,ymax), indexing='ij')
    #     local_foodmap = foodmap[xmin:xmax, ymin:ymax]

    #     if len(np.argwhere(local_foodmap)) == 0:
    #         return

    #     dist_squared = (x - self.x) ** 2 + (y - self.y) ** 2
    #     dist = np.sqrt(dist_squared + 0.000001)
    #     dot_product = (x - self.x) * np.cos(self.theta) + (y - self.y) * np.sin(self.theta)

    #     #more attracted to closer things and in view
    #     weighted_angle = np.clip(dot_product / (dist + 0.0001), 0, 1) ** 2
    #     weighted_dist = 1 / (1 + dist_squared) 

    #     score = local_foodmap * weighted_angle * weighted_dist # scores food based on distance and angles
    #     score[dist > radius] = 0
    #     flattened_score = score.flatten()
    #     sum = np.sum(flattened_score)

    #     if sum == 0:
    #         self.target = None
    #         return

    #     probabilities = flattened_score / (sum)
    #     flatindex = np.random.choice(len(flattened_score), p = probabilities)
    #     index = np.unravel_index(flatindex, score.shape)

    #     self.target = (index[0] + xmin, index[1] + ymin)
