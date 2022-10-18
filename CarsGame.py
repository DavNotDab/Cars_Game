
import turtle, time, math, random
turtle.setup(1400,740,0,0)


#-------------------------GLOBAL-VARIABLES-------------------------

COLORS = ['red', 'blue', 'green', 'yellow']
CRASH_DISTANCE = 15    # Distance the car has to be from the track border in order to cause a crash

# Writers's positions depending on the track number
WRITERS = {1:[(480, 270), (480, 120)], 2:[(-220, 70), (200, -70)], 3:[(-520, 260), (-370, -140)], 4:[(-130, 270), (-146, 25)]}

# Counters's positions depending on the track number
COUNTERS = {1:[(480, 270), (480, 120)], 2:[(-220, 70), (200, -70)], 3:[(-520, 260), (-370, -140)], 4:[(-130, 270), (-146, 25)]}

# Traffic light's positions depending on the track number
TRAFFIC_LIGHTS = {1:(85, -65), 2:(400, -50), 3:(385, -100), 4:(350, -320)}
        

#-------------------------IMAGES-REGISTRATION-------------------------


p = turtle.Screen()
p.tracer(0)

for i in range(1,20):
    p.register_shape(rf'.\Explosion\explosion{i}.gif')    # Explosion images
    
for i in range(7):
    p.register_shape(rf'.\Circuitos\semaforo{i}.gif')     # Traffic light images
    
directoryR = r'.\Carred\Cred'
directoryY = r'.\Caryellow\Cyellow'
directoryB = r'.\Carblue\Cblue'
directoryG= r'.\Cargreen\Cgreen'
  
directories = [directoryR, directoryY, directoryB, directoryG]

# Every shape is composed by the directory name plus the index plus .gif

shapes = (f'{directory}{i}.gif' for directory in directories for i in range(1,17))    # Cars images

for f in shapes:
    p.register_shape(f)
        

#-------------------------EXCEPTIONS-------------------------


class NotStartedError(Exception):
    pass

class StartedError(Exception):
    pass

class NoParameterError(Exception):
    pass


#-------------------------CAR-CLASS-------------------------


class Car(turtle.Turtle):
    
    def __init__(self,name,x,y,color='red'):
        '''Creates a Car object, hereditary from Turtle.
        It will be the object a player controls in the game.
        Given parameters are:
         name: car's name (could be Player_1 or player_2)
         x,y: coordinates where the car will appear
         color: color of the car
        '''
        super().__init__()
        self.name = name
        self.color = color
        self.pencolor('white')
        self.up()
        self.x = x
        self.y = y
        self.goto(self.x,self.y)
        self.seth(180)
        self.shape(rf'.\Car{self.color}\C{self.color}9.gif')    # Every time a Car is created, it's shown facing north
        self.speed = 0
        self.started = False
        self.orientation = {}
        self.angle = 0.0
        self.health = 100
        self.lives = 3
        self.laps_completed = 0
        self.reached_points = set([])


    def changeColor(self):
        '''Changes the color of every car position to match his actual one'''
        for i in range(1,17):
            self.orientation[self.angle] = rf'.\Car{self.color}\C{self.color}{i}.gif'
            self.angle += 22.5


    def start_car(self):
        '''Starts the car if it's stopped, otherwise an error message is shown'''
        try:        
            if not self.started:
                self.started = True
                self.clear()
                self.write('Brum', align='center', font=('Comic Sans MS', 10, 'bold'))
                p.ontimer(self.clear, 500)
            else:
                raise StartedError('Car is already started!')
            
        except StartedError:
            self.clear()
            self.write('Brum brum', align='center', font=('Comic Sans MS', 10, 'bold'))
            p.ontimer(self.clear, 500)
        
        
    def stop_car(self):
        '''Stops the car if started and speed = 0, otherwise an error message is shown'''
        if self.speed != 0:
            raise StartedError('Speed must be 0 to be able to stop the car!')
        
        elif self.started:
            self.started = False
        else:
            raise NotStartedError('Car is already stopped!')
    
    
    def speed_up_car(self):
        '''Speeds up the car if started, otherwhise an error message is shown'''
        try:
            if not self.started:
                raise NotStartedError('Car must be started to be able to speed up!')
            elif -3 <= self.speed <= 3:
                self.speed += 2
            else:
                self.speed += 4
                
        except NotStartedError:
            self.clear()
            self.write('Start the car!', align='center', font=('Comic Sans MS', 10, 'bold'))
            p.ontimer(self.clear, 500)
        
        
    def slow_down_car(self):
        '''Slows down the car if started, otherwhise an error message is shown.
        If speed is equal or below 0, the car will go backwards'''
        try:
            if not self.started:
                raise NotStartedError('Car must be started to go backwards!')
            elif -3 <= self.speed <= 3:
                self.speed -= 2
            else:
                self.speed -= 4
                
        except NotStartedError:
            self.clear()
            self.write('Start the car!', align='center', font=('Comic Sans MS', 10, 'bold'))
            p.ontimer(self.clear, 500)
            

    def give_orientation(self):
        '''Returns car's orientation according to his heading'''
        return self.orientation[self.heading()]     # Internal Turtle function that returns angle from X-axis
           
           
    def turn_right(self):
        '''Turns the car 22.5 degrees to the right (clockwise)'''
        self.seth(self.heading()-22.5)
        self.shape(self.give_orientation())
        
        
    def turn_left(self):
        '''Turns the car 22.5 degrees to the left (counterclockwise)'''
        self.seth(self.heading()+22.5)
        self.shape(self.give_orientation())
        
        
    def on_track(self):
        '''Checks the car is on the track. If it comes too close to the track borders it produces a crash'''
        points_list = GAME.track_points
        for i in range(0, len(points_list) - 1, 4):
            if self.distance(points_list[i]) < CRASH_DISTANCE or self.distance(points_list[i + 1]) < CRASH_DISTANCE:
                self.crash()
            elif self.distance(points_list[i + 2]) < CRASH_DISTANCE or self.distance(points_list[i + 3]) < CRASH_DISTANCE:
                self.crash()
    
    
    def explosion(self):
        '''Shows a car's explosion and deduct a life'''
        self.lives -= 1
        self.reached_points.clear()    # Reset the progress of the current lap
        
        if self is GAME.j1:    # Checks if self is player 1 or player 2 of the game
            GAME.write_lives.write_data(self, f'Lives: {self.lives}')
        else:
            GAME.write_lives_2.write_data(self, f'Lives: {self.lives}')
            
        for i in range(1,20):
            self.shape(rf'.\Explosion\explosion{i}.gif')
            p.update()
            time.sleep(0.04)
        self.hideturtle()
        
        if self.lives == 0:    # Checks if the player has any life left
            
            if GAME.j1 is not self:    # The player NOT exploding wins
                GAME.victory(GAME.j1)
            else:
                GAME.victory(GAME.j2)
                
        else:    # Respawn the car if it has lives left
            self.respawn()   
            if GAME.j1 is self:
                GAME.write_health.write_data(self, f'Health: {self.health}')
            else:
                GAME.write_health_2.write_data(self, f'Health: {self.health}')
    
    
    def respawn(self):
        '''Respawn the car at the beginning of the track after exploding and losing a life'''
        self.goto(self.x, self.y)
        self.seth(180)
        self.shape(rf'.\Car{self.color}\C{self.color}9.gif')
        self.showturtle()
        self.speed = 0
        self.health = 100


    def closest_points(self):
        '''Returns the track's closest points to the car, they can be two or four, depending on how close they are'''
        points_list = GAME.track_points
        closest_points = []
        for i in range(0,len(points_list)-1,4):
            if self.distance(points_list[i]) < 25 or self.distance(points_list[i+2]) < 25:
                closest_points.append(points_list[i])
                closest_points.append(points_list[i+2])

            elif self.distance(points_list[i+1]) < 25 or self.distance(points_list[i+3]) < 25:
                closest_points.append(points_list[i+1])
                closest_points.append(points_list[i+3])
                
        return closest_points
        
        
    def give_angle(self):
        '''Returns the angle between the car heading and the track border orientation'''
        closest_points = self.closest_points()
        
        p1 = closest_points[0]
        p2 = closest_points[-1]
        difY = p2[1] - p1[1]
        difX = p2[0] - p1[0]
        
        track_orientation = abs(round(math.atan2(difY, difX) * 180.0 / math.pi, 2))
       
        car_heading = self.heading()
        if car_heading > 180:
            car_heading = 360 - car_heading
     
        angle = round(abs(track_orientation - car_heading), 2)
        if angle > 90:
            angle = 180 - angle
        
        return angle
        
        
    def crash(self):
        '''Produces a crash against the track and calculates the damage taken'''
        angle = self.give_angle()
        speed = abs(self.speed)

        damage = calculate_damages(speed, angle)

        self.deduct_health(damage)


    def car_crash(self, car):
        '''Produces a crash between cars and calculates and deducts the damage taken'''
        if self.distance(car) < 25:
            speed_1 = abs(self.speed)
            speed_2 = abs(car.speed)
            total_speed = abs(speed_1 - speed_2)

            if total_speed % 2 != 0:
                total_speed += 1
            else:
                total_speed += 2

            damages = {2: 5, 4: 10, 6: 20, 8: 30, 10: 40, 12: 50, 14: 60, 16: 70, 18: 80, 20: 90, 22: 95}
            # Diccionary of speeds as keys and damages taken by cars as values

            try:
                damage = damages[total_speed]
            except  KeyError:    # If speed is above 22 car will always explode
                damage = 100

            if speed_1 > speed_2:
                car.deduct_health(damage, 2)
            elif speed_2 > speed_1:
                self.deduct_health(damage, 2)
            else:
                dice = random.randint(1,2)    # If both cars have the same speed, the one taking damage is chosen randomly
                if dice == 1:
                    car.deduct_health(damage, 2)
                else:
                    self.deduct_health(damage, 2)


    def deduct_health(self, damage, mode = 1):
        '''Deducts car's health and respawn it in the closest guide point'''
        guide_points = GAME.track_guide_points

        self.health -= damage

        if self.health > 0:
            if self is GAME.j1:    # Updates the health values in the screen
                GAME.write_health.write_data(self, f'Health: {self.health}')
            else:
                GAME.write_health_2.write_data(self, f'Health: {self.health}')

            distance = 999.0
            closest_point = None
            for i in range(len(guide_points)-1):    # Determines the closest point, where it will respawn
                if self.distance(guide_points[i]) < distance:
                    closest_point = guide_points[i+1]
                    distance = self.distance(guide_points[i])

            if mode == 1 and self.speed > 4:   # Mode = 1 if it's a track crash, otherwise it's a car crash
                self.speed -= 4                # If crash against the track, reduces the car's speed
            self.goto(closest_point)

        else:                   # If health is below 0, it round it to 0 and the car explodes
            self.health = 0
            self.explosion()


    def complete_lap(self):
        '''Add points to reached_points list and if all points are reached a lap is completed and progress is restarted'''
        if isinstance(GAME, Versus_Game):    # Laps doesn't matter in Versus mode
            pass

        # This ckecks if every point neccesary to mark a lap as completed has been reached
        if len(self.reached_points) >= int(len(GAME.track_guide_points) / 9) and self.distance(GAME.track_guide_points[3]) < 95.0:
            self.laps_completed += 1
            self.reached_points.clear()    # If a lap is completed, set of points is cleared and progress is restarted

            if isinstance(GAME, Normal_Game):    # If it's a Normal game, a completed lap is added to the screen counter
                if GAME.j1 is self:
                    GAME.write_laps.write_data(self, f'Vueltas dadas: {self.laps_completed}')
                else:
                    GAME.write_laps_2.write_data(self, f'Vueltas dadas: {self.laps_completed}')

                if self.laps_completed == GAME.laps:
                    GAME.victory(self)

            else:    # If game is in individual time trial mode, game concludes when first lap is completed
                GAME.victory(self)

        for i in range(3, len(GAME.track_guide_points), 9):
            if self.distance(GAME.track_guide_points[i]) < 85:
                self.reached_points.add(GAME.track_guide_points[i])    # Add every reached point


#-------------------------WRITER-CLASS-------------------------


class Writer(turtle.Turtle):

    def __init__(self,x,y):
        '''Creates a Writer object, hereditary from Turtle.
        Used to write all the information about the game on the screen.
        Given parameters x and y are the coordinates where it will appear
        '''
        super().__init__()
        self.hideturtle()
        self.up()
        self.x = x
        self.y = y
        self.goto(self.x,self.y)


    def write_data(self, player, data):
        '''Writes the data of the given player. The data can be lives, health or laps completed'''
        self.pencolor(player.color)
        self.clear()
        self.write(data, align='center', font=('Comic Sans MS', 25, 'bold'))


    def write_game_result(self, player, text):
        '''Writes the game result message for the given player, it can be victory or defeat'''
        self.pencolor(player.color)
        self.clear()
        self.write(text, align='center', font=('Comic Sans MS', 80, 'bold'))


    def write_error(self):
        '''Writes the error message when game parameters are given incorrectly at the beginning of the game'''
        self.clear()
        self.goto(0,250)
        self.write('You did not give the correct parameters!', align='center', font=('Comic Sans MS', 50, 'bold'))
        self.goto(0, -50)
        time.sleep(2)
        self.clear()


#-------------------------TIMER-CLASS-------------------------


class Timer(turtle.Turtle):

    def __init__(self, x, y):
        '''Creates a Timer object, hereditary from Turtle.
        Used to time the game's timer in individual time trial mode.
        Given parameters x and y are the coordinates where it will appear
        '''
        super().__init__()
        self.hideturtle()
        self.up()
        self.x = x
        self.y = y
        self.goto(self.x, self.y)
        self.final_time = None


    def initialize_timer(self, player):
        '''Initializes the timer of the given player at 0.0'''
        self.clear()
        self.goto(self.x,self.y)
        self.pencolor(player.color)
        self.write('Time: 0.0', align='center', font=('Comic Sans MS', 25, 'bold'))
        self.time = time.time()


    def start_timer(self, player):
        '''Starts the timer of the given player and write the updated value of it.
        This function will be called constantly to update the timer, as it is inside the while true loop of the game'''
        self.clear()
        self.pencolor(player.color)
        self.write(f'Time: {round(time.time() - self.time, 1)}', align='center', font=('Comic Sans MS', 25, 'bold'))


    def write_final_time(self, player):
        '''Writes the final time of the given player at the end of the game'''
        self.clear()
        self.pencolor(player.color)
        self.goto(0, -150)
        self.write(f'Time: {round(time.time() - self.time, 2)}', align='center', font=('Comic Sans MS', 70, 'bold'))
        self.final_time = round(time.time() - self.time, 2)


#-------------------------GAME-CLASS-------------------------


class Game:

    def __init__(self, players = 1.0, laps=1.0, lives = 1.0):
        '''Creates a Game object with all the given parameters.
        It will be the object which controls all the game features, like players, writers or track.
        Given parameters are:
         players: number of players of the game. It can be 1 or 2.
         laps: number of completed laps necessary to win the game.
         lives: number of lives of every player in the game.
        '''
        self.players = []
        self.laps = int(laps)
        self.lives = int(lives)
        self.track = None
        self.track_points = []
        self.track_guide_points = []

        for i in range(1, int(players) + 1):                                # Creates the Car objects of the game
            self.players.append(Car(f'Player_{i}', 415, -150 - 40 * i))     # at the given coordinates

        self.j1 = self.players[0]
        if players == 2:
            self.j2 = self.players[1]


    def initialize_game(self):
        '''Initializes the game, putting the cars in their start positions, and assinging them their lives'''
        self.j1.lives = self.lives
        self.j1.goto(-450,-138)
        self.j1.shape(rf'.\Car{self.j1.color}\C{self.j1.color}5.gif')

        if len(self.players) == 2:
            self.j2.lives = self.lives
            self.j2.goto(-174,-137)
            self.j2.shape(rf'.\Car{self.j2.color}\C{self.j2.color}5.gif')

        p.update()      # Updates the screen so that changes made are visible


    def change_track(self, track):
        '''Changes the game track to the given one and initializes his track points'''
        self.track = rf'./Circuitos/circuito{track}.gif'

        p.bgpic(self.track)
        p.update()

        with open(rf'./Circuitos/circuito{track}.txt') as f:        # Takes the points from the file and
            for l in f:                                             # Store them in the track_points list
                l2 = l.strip("()\n")
                l3 = l2.split(", ")
                self.track_points.append((float(l3[0]), float(l3[1])))

        with open(rf'./Circuitos/guia{track}.txt') as f:
            for l in f:
                l2 = l.strip("()\n")
                l3 = l2.split(", ")
                self.track_guide_points.append((float(l3[0]), float(l3[1])))

        self.j1.respawn()
        if len(self.players) == 2:
            self.j2.respawn()

        p.update()


    def start_game(self, circuito):
        '''Starts the game allowing players to move'''
        p.onkeypress(self.j1.speed_up_car, key='w')
        p.onkeypress(self.j1.turn_right, key='d')
        p.onkeypress(self.j1.slow_down_car, key='s')                  # Movement keys of player_1
        p.onkeypress(self.j1.turn_left, key='a')
        p.onkeypress(self.j1.start_car, key='e')
        p.onkeypress(self.j1.stop_car, key='p')

        # Writers for player_1's data.
        self.write_lives = Writer(WRITERS[circuito][0][0], WRITERS[circuito][0][1] + 40)
        self.write_health = Writer(WRITERS[circuito][0][0], WRITERS[circuito][0][1])
        self.write_lives.write_data(self.j1, f'Lives: {self.j1.lives}')
        self.write_health.write_data(self.j1, f'Health: {self.j1.health}')

        # This only applies if there are 2 players in the game
        if len(self.players) == 2:
            p.onkeypress(self.j2.speed_up_car, key='Up')
            p.onkeypress(self.j2.turn_right, key='Right')
            p.onkeypress(self.j2.slow_down_car, key='Down')           # Movement keys of player_2
            p.onkeypress(self.j2.turn_left, key='Left')
            p.onkeypress(self.j2.start_car, key='Return')
            p.onkeypress(self.j2.stop_car, key='hyphen')

            # Writers for player_2's data:
            self.write_lives_2 = Writer(WRITERS[circuito][1][0], WRITERS[circuito][1][1] + 40)
            self.write_health_2 = Writer(WRITERS[circuito][1][0], WRITERS[circuito][1][1])
            self.write_lives_2.write_data(self.j2, f'Lives: {self.j2.lives}')
            self.write_health_2.write_data(self.j2, f'Health: {self.j2.health}')

        p.listen()
        p.update()


    def victory(self, player):
        '''Declares the victory for one of the players'''
        self.winner = player
        p.clearscreen()
        p.bgpic(r'./Menus/victoria.gif')
        gameover.write_game_result(player, f'{player.name} Wins!')
        time.sleep(2)
        end_game(self)


    def finish_game(self):
        '''Finish the game, returning it to his initial state'''
        self.track = None
        gameover.clear()
        p.clearscreen()
        p.tracer(0)


#-------------------------NORMAL_GAME-CLASS-------------------------


class Normal_Game(Game):

    def __init__(self, players = 2, laps = 1, lives = 3):
        '''Creates a Normal_Game object, hereditary from Game.
        It will be the classic race gamemode between 2 players.
        Given parameters are:
         players: numer of players of the game. It will be always 2 because it's a race.
         laps: number of completed laps necessary to win the game.
         lives: number of lives of the players in the game.
        '''
        super().__init__(players, laps, lives)


    def start_game(self, track):
        '''Starts the game allowing movement of the players and starting their writers'''
        super().start_game(track)

        # Writers for the laps counters of the players. They are only necessary in this gamemode.
        self.write_laps = Writer(WRITERS[track][0][0], WRITERS[track][0][1] - 40)
        self.write_laps_2 = Writer(WRITERS[track][1][0], WRITERS[track][1][1] - 40)

        self.write_laps.write_data(self.j1, f'Completed laps: {self.j1.laps_completed}')
        self.write_laps_2.write_data(self.j2, f'Completed laps: {self.j2.laps_completed}')


#-------------------------TIME_TRIAL_GAME-CLASS-------------------------


class Time_Trial_Game(Game):

    def __init__(self, players = 1, laps = 1, lives = 1):
        '''Creates a Time_Trial_Game object, hereditary from Game.
        It will be the individual time trial gamemode so will always have one player.
        Given parameters are:
         players: numer of players of the game. It will be always 1 because it's time trial.
         laps: number of completed laps necessary to win the game. It will be always 1 because it's time trial.
         lives: number of lives of the player in the game.
        '''
        super().__init__(players, laps, lives)
        self.timer = None


    def start_game(self, track):
        '''Starts the game allowing movement of the players and starting their writers.
        It also starts the timer in this gamemode'''
        super().start_game(track)

        self.timer = Timer(WRITERS[track][0][0], WRITERS[track][0][1] - 40)
        self.timer.initialize_timer(self.j1)

        if len(self.players) == 2:    # En la P_ContraReloj DEBE haber solo 1 jugador, por eso esto es opcional TODO

            self.timer_2 = Timer(WRITERS[track][1][0], WRITERS[track][1][1] - 40)
            self.timer_2.initialize_timer(self.j2)


    def victory(self, player):
        '''Declares victory of one player of the game.
        This method writes the win message with the time the player finished the game with'''
        self.winner = player
        p.clearscreen()
        p.bgpic(r'./Menus/victoria.gif')
        gameover.write_game_result(player, f'{player.name} Wins!')
        self.timer.write_final_time(player)
        player_time = self.timer.write_final_time(player)
        time.sleep(2)
        self.save_time(player_time)


    def save_time(self, player_time):
        '''Saves the player's time into the Best_Times file of the game'''
        with open('Best_Times.txt', 'a') as f:
            name = p.textinput('Save your Time', 'Enter your Name: ')
            f.write(f'Name: {name}, time: {player_time}\n')

        end_game(self)


    def finish_game(self):
        '''Finishes the game returning it to his original state'''
        gameover.clear()
        self.timer.reset()
        p.ontimer(self.timer.clear, 80)
        p.ontimer(self.timer_2.clear, 80) if len(self.players) > 1 else None
        p.clearscreen()
        p.tracer(0)


#-------------------------VERSUS_GAME-CLASS-------------------------


class Versus_Game(Game):

    def __init__(self, players = 2, laps = 0, lives = 3):
        '''Creates a Versus_Game object, hereditary from Game.
        The only difference with the normal Game is the number of laps.
        They are always 0 because they don't matter in this gamemode.
        Given parameters are:
         players: numer of players of the game. It will be always 2 because it's versus gamemode.
         laps: number of completed laps necessary to win the game. It will be always 0 because it's versus gamemode.
         lives: number of lives of the players in the game.
        '''
        super().__init__(players, laps, lives)


#-------------------------OTHER-FUNCTIONS-------------------------


def calculate_damages(speed, angle):
    '''Calculates the damage taken by a car depending on the speed and angle given'''
    damages = {2:(5,10,20,30),4:(10,20,30,40),8:(15,30,45,60),12:(20,40,60,80),16:(30,50,70,95),20:(50,70,90),24:(70,90),28:95}
    # This dictionary contains differents speeds as keys and the damages taken by the car,
    # depending on the range of the angle within the car crashes against the track border.

    try:
        if angle < 23:    # Here we choose the damage index depending on the angle of the crash
            index = 0
        elif angle < 46:
            index = 1
        elif angle < 69:
            index = 2
        else:
            index = 3
        damage = damages[speed][index]

    except (IndexError, KeyError, TypeError):    # If values are not in the dictionary, damage is always 100.
        damage = 100

    return damage


def select_gamemode():
    '''Changes to the select gamemode screen and creates the game once the gamemode has been selected'''
    p.bgpic(r'.\Menus\menu2.gif')
    p.onkeypress(create_normal_game, '1')
    p.onkeypress(create_time_trial_game, '2')
    p.onkeypress(create_versus_game, '3')
    
    p.listen()
    p.update()


def create_normal_game():
    '''Creates a normal game with the parameters given by the user.
    If the game parameters are given incorrectly,
    an error message is shown and the game goes back to the select gamemode screen
    '''
    global GAME
    p.bgpic(r'.\Menus\menu3.gif')
    try:
        laps = p.numinput('Number of laps', 'Type the number of laps in the game', 1, 1, 10)
        lives = p.numinput('Number of lives', 'Type the number of lives for the players in the game', 3, 1, 10)
        p.bgpic(r'.\Menus\menu6.gif')
    
        if type(laps) != float or type(lives) != float:
            raise NoParameterError('Game parameters are incorrect! Try again')
        
    except NoParameterError:
        gameover.write_error()
        select_gamemode()

    else:
        # Game variable is global, so it can be used in the entire code.
        GAME = Normal_Game(2, laps, lives)
        GAME.initialize_game()

        p.update()

        choose_color_and_track(GAME)    # Here we change to the color and track selection screen
    
    
def create_time_trial_game():
    '''Creates a normal game with the parameters given by the user.
    If the game parameters are given incorrectly,
    an error message is shown and the game goes back to the select gamemode screen
    '''
    global GAME
    p.bgpic(r'.\Menus\menu4.gif')
    try:
        players = p.numinput('Number of players', 'Type the number of players in the game', 2, 1, 2)
        lives = p.numinput('Number of lives', 'Type the number of lives for the players in the game', 3, 1, 10)
        p.bgpic(r'.\Menus\menu6.gif')
        
        if type(players) != float or type(lives) != float:
            raise NoParameterError('Game parameters are incorrect! Try again')
        
    except NoParameterError:
        gameover.write_error()
        select_gamemode()
        pass

    else:
        GAME = Time_Trial_Game(players, 1, lives)
        GAME.initialize_game()

        p.update()

        choose_color_and_track(GAME)
    
    
def create_versus_game():
    '''Creates a versus game with the parameters given by the user.
    If the game parameters are given incorrectly,
    an error message is shown and the game goes back to the select gamemode screen
    '''
    global GAME
    p.bgpic(r'.\Menus\menu5.gif')
    try:
        lives = p.numinput('Number of lives', 'Type the number of lives for the players in the game', 3, 1, 10)
        p.bgpic(r'.\Menus\menu6.gif')
    
        if type(lives) != float:
            raise NoParameterError('Game parameters are incorrect! Try again')
        
    except NoParameterError:
        gameover.write_error()
        select_gamemode()
        pass

    else:
        GAME = Versus_Game(2, 0, lives)
        GAME.initialize_game()

        p.update()

        choose_color_and_track(GAME)
    
    
def choose_color_and_track(p1):
    '''Here you can choose the color of your car, as well as the track you want in the game.'''
    p.onkeypress(None, 'e')    # Delete the 'e' key binding
    
    p.onkeypress(lambda n=p1.j1: change_to_right_color(n), 'd')    # Calls the change color functions as the player 1
    p.onkeypress(lambda n=p1.j1: change_to_left_color(n), 'a')
    
    if len(p1.players) == 2:                         # If 2 players, Calls the change color functions as the player 2
        p.onkeypress(lambda n=p1.j2: change_to_right_color(n), 'Right')
        p.onkeypress(lambda n=p1.j2: change_to_left_color(n), 'Left')
    
    p.listen()
    
    for n in range(1,5):                      # If any number from 1 to 4 is pressed the game starts
        p.onkeypress(lambda x=n: start_game(x, p1), str(n))
        p.listen()


def change_to_right_color(player):
    '''Changes the color of the player to the one on the right of the actual one in the COLORS list'''
    try:
        player.color = COLORS[COLORS.index(player.color) + 1]    # COLORS is the global variable at the beginning of the program
    except IndexError:
        player.color = COLORS[0]    # If it gets to the end of the list it starts over
        
    player.shape(rf'.\Car{player.color}\C{player.color}5.gif')
    p.update()
    
    
def change_to_left_color(j):
    '''Changes the color of the player to the one on the left of the actual one in the COLORS list'''
    j.color = COLORS[COLORS.index(j.color) - 1]

    j.shape(rf'.\Car{j.color}\C{j.color}5.gif')
    p.update()


def start_game(track, game):
    '''Starts the game. It changes the background to the choosen track and starts the game's loop'''
    game.change_track(track)
    game.j1.changeColor()
    
    start_traffic_light(track, game)

    if len(game.players) == 2:
        game.j2.changeColor()

        while p.bgpic() == rf'./Circuitos/circuito{track}.gif':
            playing(game.j1, game.j2)
    else:
        while p.bgpic() == rf'./Circuitos/circuito{track}.gif':
            playing(game.j1)
        
        
def start_traffic_light(track, game):
    '''Starts the trafic light countdown and when finished hides the traffic light and allow movement'''
    traffic_light = turtle.Turtle()     # It's just a Turtle object
    traffic_light.hideturtle()
    traffic_light.up()
    traffic_light.goto(TRAFFIC_LIGHTS[track][0], TRAFFIC_LIGHTS[track][1])
    traffic_light.showturtle()
    
    p.onkeypress(None, 'd')
    p.onkeypress(None, 'a')
    p.onkeypress(None, 'Right')    # Deletes the binding of these keys, so they don't keep changing colors
    p.onkeypress(None, 'Left')
    
    for i in range(6):
        traffic_light.shape(rf'.\Circuitos\semaforo{i}.gif')
        p.update()
        time.sleep(0.7)
    
    game.start_game(track)
    
    traffic_light.shape(rf'.\Circuitos\semaforo{6}.gif')
    p.update()
    
    p.ontimer(traffic_light.hideturtle, 700)    # Traffic light hides after 700ms


def playing(j1, j2 = None):
    '''This function supervises some aspects of the game while running, like player's speed, lap progress and crashes'''
    speed = 16                 # Speed factor of the cars, the lower it is, the faster they go
    j1.on_track()
    j1.complete_lap()
    if isinstance(GAME, Time_Trial_Game):
        GAME.timer.start_timer(j1)      # In time trial mode game runs slower due to the timer constantly being updated
        speed = 12                      # So car's speed is increased to match this slowed performance
        
    j1.fd(j1.speed / speed)
    
    if j2 is not None:                  # In case game has only one player this gets ignored
        j2.fd(j2.speed / speed)
        j2.on_track()
        j1.car_crash(j2)
        j2.car_crash(j1)
        j2.complete_lap()
        if isinstance(GAME, Time_Trial_Game):
            GAME.timer_2.start_timer(j2)
        
    p.update()
    

def end_game(game):
    '''Ends the game and return to the main menu'''
    game.finish_game()
    del game  # Deletes the game so a new one can be created
    
    p.bgpic(r'.\Menus\menu1.gif')
    p.onkeypress(select_gamemode, 'e')
    p.onkeypress(p.bye, key='Escape')
    p.listen()
    p.update()
    

#-------------------------MAIN-------------------------            

p.bgpic(r'.\Menus\menu1.gif')
    
gameover = Writer(0, -50)    # Special writer which writes end-game messages and NoParameterError

p.onkeypress(select_gamemode, 'e')
p.onkeypress(p.bye, key='Escape')

p.listen()
p.update()

p.mainloop()
