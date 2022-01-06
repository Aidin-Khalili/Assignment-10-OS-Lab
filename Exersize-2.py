import arcade
import random
import math
import enum

#To be flexible we define these value & assign them firstly.
SCREEN_TITLE = "snake"
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
SCREEN_HEADER = 50
SNAKE_SEGMENT_RADIUS = 10
SNAKE_LENGTH = 1
SNAKE_SPEED = 1 / 10

class move_Direct(enum.Enum):#This is as standard but we can change it. (flexible for these things)
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class Snake():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__score = 0
        self.__num_Of_Moves = 0
        self.__body = self.body_Generation()
        self.__food = None
        self.__bad_Food = None
        self.__move_Direct = move_Direct.Right
        self.__dead = False
        arcade.schedule(self.update_value, SNAKE_SPEED)
        arcade.schedule(self.SpawnFood, random.random() * 2)
        arcade.schedule(self.SpawnBadFood,random.random() * 2)
    def get_Score(self):
        return self.__score
    def get_Num_Of_Moves(self):
        return self.__num_Of_Moves
    def get_Body(self):
        return self.__body
    def get_Poop(self):
        return self.__bad_Food
    def get_Useful_Food(self):
        return self.__food
    def get_Die_Situation(self):
        return self.__dead
    def body_Generation(self):
        body = []
        while len(body) < SNAKE_LENGTH:
            x = int(self.__width / 2 - len(body))
            y = int(self.__height / 2)
            coor = [x, y]
            body.append(coor)
        return body
    def KeyPressed(self, key):
        if key == arcade.key.UP and not self.__move_Direct == move_Direct.Down:
            self.__move_Direct = move_Direct.Up
        elif key == arcade.key.DOWN and not self.__move_Direct == move_Direct.Up:
            self.__move_Direct = move_Direct.Down
        elif key == arcade.key.RIGHT and not self.__move_Direct == move_Direct.Left:
            self.__move_Direct = move_Direct.Right
        elif key == arcade.key.LEFT and not self.__move_Direct == move_Direct.Right:
            self.__move_Direct = move_Direct.Left
        if key == arcade.key.ENTER:
            self.reset_all()
    def reset_all(self):
        self.__score = 0
        self.__num_Of_Moves = 0
        self.__move_Direct = move_Direct.Right
        self.__dead = False
        self.__body = self.body_Generation()
        self.__food = None
        self.__bad_Food = None
    def move_Snake(self):
        new_body = []
        x = 0
        y = 0
        if self.__move_Direct == move_Direct.Right or self.__move_Direct == move_Direct.Left:
            if self.__move_Direct == move_Direct.Right:
                x = 1
            else:
                x = -1
        elif self.__move_Direct == move_Direct.Up or self.__move_Direct == move_Direct.Down:
            if self.__move_Direct == move_Direct.Up:
                y = 1
            else:
                y = -1
        head = self.__body[0]
        new_head = [head[0] + x, head[1] + y]
        new_body.append(new_head)
        for i, _ in enumerate(self.__body):
            if not i == 0:
                new_body.append(self.__body[i - 1])
        self.__num_Of_Moves += 1
        edgeCollision = False
        if new_head[0] < 0 or new_head[0] > self.__width:
            edgeCollision = True
        if new_head[1] < 0 or new_head[1] > self.__height:
            edgeCollision = True
        return new_body, edgeCollision
    def detecting_Colision_To_Body(self, body):
        head = body[0]
        dead = False
        if head in body[1:]:
            dead = True
        return dead

    def get_Mines_Score(self):
        dead = False
        if self.__score < 0:
            dead = True
        return dead

    def SpawnFood(self, _):
        x, y = self.get_Rand_Coordinate()
        self.__food = [x, y]
        arcade.unschedule(self.SpawnFood)

    def SpawnBadFood(self, _):
        x,y = self.get_Rand_Coordinate()
        self.__bad_Food = [x,y]
        arcade.unschedule(self.SpawnBadFood)

    def get_Rand_Coordinate(self):
        x = random.randint(0, self.__width)
        y = random.randint(0, self.__height)
        if [x, y] in self.__body and self.calculate_Dis_Between_2_Points(self.__body[0], [x, y]) > 5:
            x, y = self.get_Rand_Coordinate()
        return x, y

    def calculate_Dis_Between_2_Points(self, first_point, second_point):
        x_dist = abs(first_point[0] - second_point[0])
        y_dist = abs(first_point[1] - second_point[1])
        x_dist_pow = math.pow(x_dist, 2)
        y_dist_pow = math.pow(y_dist, 2)
        dist = abs(math.sqrt(x_dist_pow + y_dist_pow))
        return int(dist)

    def checking_Eating_Food(self, body):
        head = body[0]
        is_Eating_Flag = False
        if self.__food == head:
            self.__score += 2
            self.__food = None
            is_Eating_Flag = True
            arcade.schedule(self.SpawnFood, random.random() * 2)
        return is_Eating_Flag

    def checking_Eating_Bad_Food(self, body):
        head = body[0]
        is_Eating_Flag = False
        if self.__bad_Food == head:
            self.__score -= 1
            self.__bad_Food = None
            is_Eating_Flag = True
            arcade.schedule(self.SpawnBadFood, random.random() * 2)
        return is_Eating_Flag

    def update_value(self, _):
        if not self.__dead:
            new_body, self.__dead = self.move_Snake()
            if not self.__dead:
                self.__dead = self.detecting_Colision_To_Body(new_body)
            if not self.__dead:
                self.__dead = self.get_Mines_Score()
            if not self.__dead:
                new_segment = self.checking_Eating_Food(new_body)
                if new_segment:
                    new_body.append(self.__body[-1])
            if not self.__dead:
                self.checking_Eating_Bad_Food(new_body)
            if not self.__dead:
                self.__body = new_body


class Game_UI(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEADER, SCREEN_TITLE)
        arcade.set_background_color( arcade.color.SMOKY_BLACK )
        GridWidth, GridHeight = self.CalcGrid()
        self.snake = Snake(GridWidth, GridHeight)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(0,SCREEN_HEIGHT + 1, SCREEN_WIDTH, SCREEN_HEIGHT + 1, arcade.color.DUTCH_WHITE, 2)
        try:
            score = self.snake.get_Score()
            arcade.draw_text("Score = " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER / 4, arcade.color.WHITE_SMOKE, 24)
        except:
            score = "..."
            arcade.draw_text("Score = " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)
        try:
            dead = self.snake.get_Die_Situation()
            score = self.snake.get_Score()
            score > 0
        except:
            dead = False
        if dead:
            arcade.draw_text("Game over!", 0, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 60, width = SCREEN_WIDTH, align = "center")
        elif score < 0:
            arcade.draw_text("You get negative score!", 0, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 60, width = SCREEN_WIDTH, align = "center")
        self.draw_body()
        self.draw_food()
        self.draw_Badfood()

    def on_key_press(self, key, modifier):
        try:
            self.snake.KeyPressed(key)
        except:
            print("There is an error for handeling key pass!")

    def CalcGrid(self):
        width = (SCREEN_WIDTH / SNAKE_SEGMENT_RADIUS) - 1
        height = (SCREEN_HEIGHT / SNAKE_SEGMENT_RADIUS) - 1
        return width, height

    def draw_body(self):
        try:
            body = self.snake.get_Body()
        except:
            body = [[0,0]]
        for i, coor in enumerate(body):
            color = arcade.color.DARK_PASTEL_GREEN
            if i == 0:
                color = arcade.color.GRANNY_SMITH_APPLE
            arcade.draw_circle_filled(coor[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, coor[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, color)

    def draw_food(self):
        try:
            food = self.snake.get_Useful_Food()
        except:
            food = None
        if not food == None:
            arcade.draw_circle_filled(food[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, food[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, arcade.color.RED)

    def draw_Badfood(self):
        try:
            badfood = self.snake.get_Poop()
        except:
            badfood = None
        if not badfood == None:
            arcade.draw_circle_filled(badfood[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, badfood[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, arcade.color.DARK_BROWN)


game = Game_UI()
arcade.run()