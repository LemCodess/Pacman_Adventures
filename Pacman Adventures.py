from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import sys
import time

current_time = time.time()
last_time = current_time


frozen = False
go_right, go_left, go_up, go_down = True, True, True, True
score = 0
speed = 140
catcher_color = (1,1,1)

delay = 1

r = random.uniform(0.5,1)
g = random.uniform(0.5,1)
b = random.uniform(0.5,1)
ghost_color = (r,g,b)

colour = 0
night = True

# Function to identify the zone of a line
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6

# Function to map any point to Zone 0
def to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

# Function to convert back from Zone 0 to original zone
def from_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

# Function to draw pixel
def draw_pixel(x, y,size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# draw_line function 
def draw_line(x1, y1, x2, y2, size):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = to_zone_0(x1, y1, zone)
    x2, y2 = to_zone_0(x2, y2, zone)
    
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy - dx)
    y = y1
    
    for x in range(int(x1), int(x2 + 1)):
        xp, yp = from_zone_0(x, y, zone)
        draw_pixel(xp, yp, size)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

def draw_circle(r, c_x, c_y):
    x = 0
    y = r
    d = 1-r
    while(x<= y):
        if (d<0):
            x += 1
            d = d+ 2*x + 3
        else:
            x = x+1
            y =y-1
            d = d + 2*x -2*y + 5
        #print(x,y)
        draw_pixel(x+ c_x,y+ c_y,2)
        draw_pixel(y+ c_x,x+ c_y,2)
        draw_pixel(y+ c_x,-x+ c_y,2)
        draw_pixel(x+ c_x,-y+ c_y,2)
        draw_pixel(-x+ c_x,-y+ c_y,2)
        draw_pixel(-y+ c_x,-x+ c_y,2)
        draw_pixel(-y+ c_x,x+ c_y,2)
        draw_pixel(-x+ c_x,y+ c_y,2)

class BoundingBox:
    def __init__(self, bottom_left, top_right, size):
        # Bottom left and top right points of the bounding box
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.size = size

        self.x1, self.y1 = self.bottom_left
        self.x2, self.y2 = self.top_right

    def draw(self):

        draw_line(self.x1, self.y1, self.x2, self.y1, self.size)  # Bottom
        draw_line(self.x1, self.y2, self.x2, self.y2, self.size)  # Top
        draw_line(self.x1, self.y1, self.x1, self.y2, self.size)  # Left
        draw_line(self.x2, self.y1, self.x2, self.y2, self.size) 

lower_bound = 640
upper_bound = 680
restart_button = BoundingBox((20,lower_bound),(70,upper_bound),1)

pause_button = BoundingBox((255,lower_bound),(325,upper_bound),1)

play_button = BoundingBox((255,lower_bound),(325,upper_bound),1)



cross_button = BoundingBox((540,lower_bound),(580,upper_bound),1)

pacman = BoundingBox((265,20),(290,45),1)

#diamondB = BoundingBox((500,500),(600,600),1)
points = []
points_clean = []
point_db = {}
#diamonds.append(diamondB)

def generate_points():
    global line_boundaries, line_boundaries_2
    global points, points_clean, point_db
    #print("inside generator")
    width = 5 

    r, x, y = width, random.uniform(10,500), random.uniform(10,600)

    x1 = x-5
    x2 = x+5
    y1 = y-5
    y2 = y+5
    
    
    new_pointB = BoundingBox((x1,y1),(x2,y2),1)

    if check_shooter_collision(new_pointB, line_boundaries):
        pass
    elif check_shooter_collision(new_pointB, line_boundaries_2):
        pass
    else:
        points.append(new_pointB)
    #points_clean.append((x,y,r))

    #point_db[new_pointB] = (x,y,r)




def restart(button):
   x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

   m_x = (x1 + x2)/2
   m_y = (y1 + y2)/2


   glColor3f(0, 1, 1)
   draw_line(x1, m_y, m_x, y2,2) 
   draw_line(x1, m_y, m_x, y1,2) 
   draw_line(x1, m_y, x2, m_y,2) 

   glColor3f(0, 0, 0) 
   #button.draw()


def pause(button):
    x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

    m_x = (x1 + x2)/2
    m_y = (y1 + y2)/2


    glColor3f(1, 0.75, 0)
    draw_line(m_x-5, y1, m_x-5, y2,2) 
    draw_line(m_x+5, y1, m_x+5, y2,2) 
    

    glColor3f(0, 0, 0) 
    #button.draw()

def play(button):
    x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

    m_x = (x1 + x2)/2
    m_y = (y1 + y2)/2


    glColor3f(1, 0.75, 0)
    draw_line(m_x-10, y1, m_x-10, y2,2) 
    draw_line(m_x-10, y1, x2, m_y,2)
    draw_line(m_x-10, y2, x2, m_y,2) 
    

    glColor3f(0, 0, 0) 
    #button.draw()

def cross(button):
   x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

   m_x = (x1 + x2)/2
   m_y = (y1 + y2)/2

    
   glColor3f(1,0,0)
   draw_line(x1, y2, x2, y1,2) 
   draw_line(x1, y1, x2, y2,2) 
   
   glColor3f(0, 0, 0) 
   #button.draw()

def shooter(button, color):

    x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

    m_x = (x1 + x2)/2
    m_y = (y1 + y2)/2


    x,y,z = color

    center = (x2-x1)/2
    center_half = center/2
    #m_d = (x2-m_x)/2
    #m_d_2 = (y2-m_y)/2

    glColor3f(1,1,0)
    draw_circle(center, m_x, m_y)

    draw_line(m_x, m_y, m_x + center_half  +1 , m_y + center_half +1, 2)
    draw_line(m_x, m_y, m_x + center_half, m_y - center_half, 2)
    #draw_circle(10, 100, 300)

    glColor3f(0, 0, 0) 
    #button.draw()

def point_draw(button):
   global point_db, night

   #x,y,r = point_db[button]

   x1, x2, y1, y2 = button.x1, button.x2, button.y1, button.y2

   m_x = (x1 + x2)/2
   m_y = (y1 + y2)/2

   #x,y,z = color
   if not night:
       glColor3f(1.0, 0, 1.0)
   else:
       glColor3f(1.0, 1.0, 1.0)

   radius = int((x2-x1)/2)
   x = m_x
   y = m_y
   #print("trying to draw",radius,x,y)
   #print(r,x,y)
   for i in range(radius,3,-1):
        
        draw_circle(i,x,y)

   #draw_circle((x2-x1)/2, m_x, m_y) 
   
   glColor3f(0, 0, 0) 
   #button.draw()


def freeze_points():
    global frozen
    frozen = not frozen

def draw_points(x,y,r):
    glColor3f(1.0, 1.0, 1.0) 
    #print(r,x,y)
    for i in range(r,2,-1):
        draw_circle(i,x,y)


line_boundaries_2 = []
lines_2 = [
        # Vertical lines
        (0, 5, 0, 630),
        (600, 5, 600, 630),
        (300, 5, 300, 35),
        (340, 390, 340, 540),
        (70, 55, 70, 440),
        (250, 500, 250, 540),
        (250, 300, 250, 390),
        (300, 110, 300, 200),
        (450, 300, 450, 450),
        (525, 200, 525, 300),


    # Horizontal lines
        (0, 5, 630, 5),
        (0, 630, 600, 630),
        (0, 540, 250, 540),
        (70, 440, 220, 440),
        (250, 300, 450, 300),
        (70, 200, 180, 200),
        (70, 55, 240, 55),
        (70, 120, 150, 120),
        (250, 200, 350, 200),
        (420, 200, 600, 200),
        (340, 540, 540, 540),
        (525, 450, 640, 450),
        (300, 110, 500, 110)

        ]
line_boundaries = []
lines = [
    #vertical
        (0, 5, 0, 630),
        (600, 5, 600, 630),
        (450, 315, 450, 630),
        (230, 600, 230, 630),
        (100, 300, 100, 450),
        (100, 100, 100, 230),
        (350, 230, 350, 530),
        (530, 570, 530, 630),
    #horizontal
        (0, 5, 630, 5),
        (0, 630, 600, 630),
        (100, 100, 300, 100),
        (300, 100, 400, 100),
        (230, 230, 400, 230),
        (100, 450, 230, 450),
        (100, 530, 350, 530),
        (530, 230, 600, 230),
        (500, 100, 600, 100)
]

for line in lines:
        
    x1, y1, x2, y2 = line
           
    line_box = BoundingBox((x1-1,y1-1),(x2+1,y2+1),2)

    line_boundaries.append(line_box) 

# for line in line_boundaries:
#     print(line.x1,line.x2,line.y1,line.y2)

for line2 in lines_2:
    x1, y1, x2, y2 = line2

    line_box_2 = BoundingBox((x1 - 1, y1 - 1), (x2 + 1, y2 + 1), 2)

    line_boundaries_2.append(line_box_2)

# for line in line_boundaries_2:
#     print(line.x1, line.x2, line.y1, line.y2)
first = True
def maze(lv):
    global line_boundaries, line_boundaries_2, lines, lines_2, score, pacman, first, night

    if not night:
        glColor3f(1.0, 0, 1.0)
    else:
        glColor3f(1.0, 1.0, 1.0)


    if score < 5:
        lines = lines
        line_boundaries = line_boundaries

    elif score>=5 and lv == True:
        lines = []
        line_boundaries = []
        pacman = BoundingBox((265,20),(290,45),1)
        lines = lines_2
        line_boundaries = line_boundaries_2

        first = False

        
    for line in lines:

        x1, y1, x2, y2 = line

        draw_line(x1, y1, x2, y2, 2)

ghosts = []
ghost_bounds = []
def rand_colors():
    global r, g, b
    r = random.random()
    g = random.random()
    b = random.random()

    return r,g,b

def spawn_point(x, y, color):
    direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])

    ghosts.append({
        'x': x,
        'y': y,
        'r': color[0],
        'g': color[1],
        'b': color[2],
        'direction': direction
    })
  

speed_g = 100

def draw_ghosts():
    global r, g, b

    global ghosts

    # Loop through each ghost and draw it
    for ghost in ghosts:
        
        glColor3f(ghost['r'], ghost['g'], ghost['b'])
        glPointSize(3)  # Adjust the point size as needed
        
        # Draw the body of the ghost
        glBegin(GL_POINTS)
        glVertex2f(ghost['x'], ghost['y'])  # Body center point
        glVertex2f(ghost['x'] - 5, ghost['y'] - 5)  # Upper left point
        glVertex2f(ghost['x'] + 5, ghost['y'] - 5)  # Upper right point
        glVertex2f(ghost['x'] - 5, ghost['y'] + 5)  # Lower left point
        glVertex2f(ghost['x'] + 5, ghost['y'] + 5)  # Lower right point
        glEnd()

        
        # Draw the eyes of the ghost
        glColor3f(1.0, 1.0, 1.0)  # White color for eyes
        glPointSize(2)  # Adjust the point size for eyes
        glBegin(GL_POINTS)
        glVertex2f(ghost['x'] - 2, ghost['y'] + 2)  # Left eye
        glVertex2f(ghost['x'] + 2, ghost['y'] + 2)  # Right eye
        glEnd()

def draw():
    global frozen , lives
    global catcher_color, ghost_color, points, points_clean, first
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)


    if night:
        glClearColor(colour, colour, colour, colour)  # Night
    else:
        glClearColor(colour, colour, colour, colour)  # Day


    restart(restart_button)

    if not frozen:

        pause(pause_button)

    else:

        play(play_button)

    cross(cross_button)

    if lives == 3:
        glColor3f(1.0, 1.0, 0)
        draw_pixel(400, 660, 10)
        draw_pixel(420, 660, 10)
        draw_pixel(440, 660, 10)
    elif lives == 2:
        glColor3f(1.0, 1.0, 0)
        draw_pixel(400, 660, 10)
        draw_pixel(420, 660, 10)
    elif lives == 1:
        glColor3f(1.0, 1.0, 0)
        draw_pixel(400, 660, 10)


    shooter(pacman,catcher_color)

    for each_pointB in points:
        
        point_draw(each_pointB)
        pass

    draw_ghosts()
    maze(first)
    #draw_points(100,100,5)
    #rand_colors()


    glFlush()

def level1():
    global lines, line_boundaries
    lines = [
    #vertical
        (0, 5, 0, 630),
        (600, 5, 600, 630),
        (450, 315, 450, 630),
        (230, 600, 230, 630),
        (100, 300, 100, 450),
        (100, 100, 100, 230),
        (350, 230, 350, 530),
        (530, 570, 530, 630),
    #horizontal
        (0, 5, 630, 5),
        (0, 630, 600, 630),
        (100, 100, 300, 100),
        (300, 100, 400, 100),
        (230, 230, 400, 230),
        (100, 450, 230, 450),
        (100, 530, 350, 530),
        (530, 230, 600, 230),
        (500, 100, 600, 100)
        ]
    
    line_boundaries = []

    for line in lines:
            
        x1, y1, x2, y2 = line
            
        line_box = BoundingBox((x1-1,y1-1),(x2+1,y2+1),2)

        line_boundaries.append(line_box) 

def restart_game():
    global score, frozen, speed, catcher_color, ghost_color, current_time, last_time, lives, score
    global pacman, delay, points, ghosts, speed_g, ghost_bounds
    global go_right, go_left, go_up, go_down, first
    pacman = BoundingBox((265,20),(290,45),1)

    score = 0

    level1()
    lives = 3
    points = []
    ghosts = []
    ghost_bounds = []

    #print("Game Restarted")
    #print("Your Score is", score)

    first = True

    go_right, go_left, go_up, go_down = True, True, True, True
    r = random.uniform(0.5,1)
    g = random.uniform(0.5,1)
    b = random.uniform(0.5,1)
    ghost_color = (r,g,b)

    frozen = False

    
def check_collision(box1, box2):
    # Check if box1's right edge is left of box2's left edge
    # or box1's left edge is right of box2's right edge
    if box1.x2 < box2.x1 or box1.x1 > box2.x2:
        return False
    # Check if box1's top edge is below box2's bottom edge
    # or box1's bottom edge is above box2's top edge
    if box1.y2 < box2.y1 or box1.y1 > box2.y2:
        return False
    # If neither of these are true, the boxes are overlapping
    return True


def check_shooter_collision(shooter_box, maze_boxes):

    for maze_box in maze_boxes:
        if check_collision(shooter_box, maze_box):
            return True
    else: 
        return False
    

def update_ghost_direction(ghost):
    global pacman
    # Calculate the direction vector towards the pacman or shooter object
    catcher_pos = (pacman.x1 + pacman.x2) / 2, (pacman.y1 + pacman.y2) / 2
    direction_x = catcher_pos[0] - ghost['x']
    direction_y = catcher_pos[1] - ghost['y']

    # Normalize the direction vector
    magnitude = (direction_x**2 + direction_y**2)**0.5
    if magnitude != 0:
        direction_x /= magnitude
        direction_y /= magnitude


    return (direction_x, direction_y)

class GhostBoundingBox:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    # Method to check if this bounding box collides with another bounding box
    def collides_with(self, other_box):
        distance_squared = (self.center_x - (other_box.x1 + other_box.x2)/2)**2 + (self.center_y - (other_box.y1 + other_box.y2)/2)**2
        sum_of_radii_squared = (self.radius + (other_box.x2 - other_box.x1)/2)**2
        return distance_squared <= sum_of_radii_squared

lives = 3
def check_ghost_collisions():
    global ghosts, pacman, score, lives

    # Check for collisions between each ghost and the shooter
    for ghost in ghosts:
        ghost_box = GhostBoundingBox(ghost['x'], ghost['y'], 5) # Adjust the radius as needed
        if ghost_box.collides_with(pacman):

                lives -= 1
                print('Remaining lives: ',lives)
                pacman = BoundingBox((265,20),(290,45),1)

                if lives < 1:
                    print("MUHAAAA THE GHOST CAUGHT YOU")
                    print("Ghost collided with Pacman thrice!")
                    print("Final score: ", score)
                    freeze_points()
                ghosts.clear()
                #draw_ghosts()
                restart_game()

def generate_ghost(ghost_count):
    while len(ghosts) < ghost_count:
        x,y = random.uniform(50,500), random.uniform(50,600)
        r,g,b = rand_colors()
        #print("generating points")
        color = (r,g,b)
        spawn_point(x,y,color)

def animate():
    
    glutPostRedisplay()
    global score, delay
    global frozen, go_right, go_left, go_down, go_up
    global speed
    global catcher_color
    global last_time, current_time
    global pacman, points, line_boundaries, line_boundaries_2, ghost_bounds
    global current_time, last_time

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time


    if not frozen:

        for point in ghosts:
            #for each_ghost_boundary in ghost_bounds:
                #print(delta_time)
                point['x'] += speed_g * point['direction'][0]  * delta_time
                point['y'] += speed_g * point['direction'][1]  * delta_time

                new_direction = update_ghost_direction(point)
                # Bounce back from the boundaries
                if point['x'] < 0 or point['x'] > 600:
                    point['direction'] = new_direction
                if point['y'] < 5 or point['y'] > 620:
                    point['direction'] = new_direction


            
        for eachPoint in points:
            
            if check_collision(eachPoint, pacman):

                score += 1
                print("Your score is ", score)
                points.remove(eachPoint)

        check_ghost_collisions()

        if pacman.x1 < 15:
            #go_right = True
            go_left = False

        if pacman.x2 > 585:
            go_right = False
            #go_left = True

        if pacman.x1 > 15 and pacman.x2 < 585:
            #go_right = True
            #go_left = True
            for stopper in range (5, 10):
                temp_box = BoundingBox((pacman.x1 + stopper , pacman.y1), (pacman.x2 + stopper, pacman.y2),1)
                if check_shooter_collision(temp_box, line_boundaries):

                    go_right = False

                else:
                    go_right = True

                temp_box = BoundingBox((pacman.x1 - stopper , pacman.y1), (pacman.x2 - stopper , pacman.y2),1)
                if check_shooter_collision(temp_box, line_boundaries):
                    go_left = False
                        #print("game over")
                        #freeze_points()

                else:
                    go_left = True


        if pacman.y1 < 15:
            
            go_down = False

        if pacman.y2 > 615:
            go_up = False
            

        if pacman.y1 > 15 and pacman.y2 < 615:

            for stopper in range (5, 10):
                temp_box = BoundingBox((pacman.x1 , pacman.y1 - stopper), (pacman.x2, pacman.y2 - stopper),1)
                if check_shooter_collision(temp_box, line_boundaries):
                    go_down = False
                        #print("game over")
                        #freeze_points()
                else:
                    go_down = True

                temp_box = BoundingBox((pacman.x1 , pacman.y1 + stopper), (pacman.x2, pacman.y2 + stopper),1)
                if check_shooter_collision(temp_box, line_boundaries):
                    go_up = False
                        #print("game over")
                        #freeze_points()
                else:
                    go_up = True

        

        while len(points) < 5:

            #print("generating points")
            generate_points()

        if score < 10 :
            generate_ghost(2)
        else:
            generate_ghost(3)


def check_click_inside_box(box, click_x, click_y):
    return box.x1 <= click_x <= box.x2 and box.y1 <= click_y <= box.y2

def handle_special_keys(key , x , y):

    global frozen, go_right, go_left, m1_x, m2_x, m1_y, m2_y, m3

    speed = 15

    if key == GLUT_KEY_RIGHT and frozen == False and go_right:
        pacman.x1 += speed
        pacman.x2 += speed


        #print("Going right")
    elif key == GLUT_KEY_LEFT and frozen == False and go_left:

        pacman.x1 -= speed
        pacman.x2 -= speed


        #print("Going Left")

    elif key == GLUT_KEY_UP and frozen == False and go_up:

        pacman.y1 += speed
        pacman.y2 += speed


    elif key == GLUT_KEY_DOWN and frozen == False and go_down:

        pacman.y1 -= speed
        pacman.y2 -= speed




def handle_keyboard(key, x , y):
    global frozen, go_right, go_left, m1_x, m2_x, m1_y, m2_y, m3
    global night, colour
    speed = 15

    if key == b' ':
        if night == False:
            night = True
            colour = 0

        else:
            night = False
            colour = 1

    if key == b'd' and frozen == False and go_right:
        pacman.x1 += speed
        pacman.x2 += speed


        #print("Going right")
    elif key == b'a' and frozen == False and go_left:

        pacman.x1 -= speed
        pacman.x2 -= speed

    elif key == b'w' and frozen == False and go_up:

        pacman.y1 += speed
        pacman.y2 += speed


    elif key == b's' and frozen == False and go_down:

        pacman.y1 -= speed
        pacman.y2 -= speed


def mouse_click(button, state, x, y):
    global frozen, catcher_color, score
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # 
        window_y = 700 - y  
        window_x = x
        
        # 
        if check_click_inside_box(restart_button, window_x, window_y):
            restart_game()
            print("Restart game")
            
        
        elif check_click_inside_box(pause_button, window_x, window_y) and frozen == False:
            freeze_points()
            print("Game paused! Taking a Break")
            
        
        elif check_click_inside_box(play_button, window_x, window_y) and frozen == True:
            freeze_points()

            print("Game resumed")
            
        
        elif check_click_inside_box(cross_button, window_x, window_y):
            print("GoodBye!")
            print("Your final score is ", score)
            glutLeaveMainLoop()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(600, 700)
    glutInitWindowPosition(400, 0)
    glutCreateWindow(b"Pacman Adventures")
    gluOrtho2D(0, 600, 0, 700)
    glutIdleFunc(animate)
    glutSpecialFunc(handle_special_keys)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(handle_keyboard)
    
    glutDisplayFunc(draw)
    
    glutMainLoop()

if __name__ == "__main__":
    main()