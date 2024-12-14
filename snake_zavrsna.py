import pygame, sys, random
from pygame.math import Vector2

# Initialize pygame
pygame.init()
score_font = pygame.font.Font(None, 40)     # Font for score text
title_font = pygame.font.Font(None, 60)        # Font for title text
# Define colors
GREEN = (173, 204, 96)      # Light green color
DARK_GREEN = (43, 51, 24)       # Dark green color
WHITE = (255, 255, 255)     # White color

# Grid settings
cell_size = 30      # Size of each cell in the grid
number_of_cells = 25       # Number of cells in the grid

# Border settings
OFFSET = 75     # Offset for drawing the grid

# Food class to manage food behavior
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)        # Generate initial position for food def draw(self):

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)       # Create a rectangle for the food
        screen.blit(food_surface, food_rect)        # Draw the food on the screen

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)      # Generate random x-coordinate
        y = random.randint(0, number_of_cells - 1)      # Generate random y-coordinate
        return Vector2(x, y)        # Return the position as a Vector2 object

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()      # Generate random position
        while position in snake_body:       # Ensure the position is not on the snake
            position = self.generate_random_cell()      
        return position     # Return the valid position

# Snake class to manage snake behavior
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]       # Initial positions of the snake's body segments
        self.direction = Vector2(1, 0)      # Initial direction of the snake
        self.add_segment = False        # Flag to indicate if a new segment should be added
        self.eat_sound = pygame.mixer.Sound("eat.mp3")       # Sound when the snake eats food
        self.wall_hit_sound = pygame.mixer.Sound("wall.mp3")     # Sound when the snake hits a wall

    def draw(self):
        for segment in self.body:       # Draw each segment of the snake
            segment_rect = pygame.Rect(OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)        # Create a rectangle for the segment
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)        # Draw the segment on the screen

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)      # Move the snake by adding a new head based on the current direction
        if self.add_segment:        # Check if a new segment should be added
            self.add_segment = False
        else:
            self.body.pop()     # Remove the last segment to simulate movement

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]       # Reset the snake's body to the initial position
        self.direction = Vector2(1, 0)      # Reset the snake's direction to the initial direction

# Game class to manage game logic
class Game:
    def __init__(self):
        self.snake = Snake()        # Create a Snake object
        self.food = Food(self.snake.body)       # Create a Food object
        self.state = "Running"  # Initial state of the game
        self.score = 0      # Initial score
        self.high_score = self.load_high_score()  # Load high score from file

    def draw(self):
        self.food.draw()        # Draw the food
        self.snake.draw()       # Draw the snake

    def update(self):
        if self.state == "Running":     # Update game logic only if the game is running
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:        # Check if the snake's head is on the food
            self.food.position = self.food.generate_random_pos(self.snake.body)     # Generate a new position for the food
            self.snake.add_segment = True       # Add a new segment to the snake
            self.score += 1     # Increase the score
            if self.score > self.high_score:  # Update high score if the current score is higher
                self.high_score = self.score
            self.snake.eat_sound.play()     # Play the eat sound

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:       # Check for collision with horizontal edges
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:       # Check for collision with vertical edges
            self.game_over()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]     # Exclude the head from the snake's body
        if self.snake.body[0] in headless_body:     # Check if the snake's head collides with its body
            self.game_over()

    def game_over(self):
        self.snake.reset()      # Reset the snake's position
        self.food.position = self.food.generate_random_pos(self.snake.body)     # Generate a new position for the food
        self.state = "Stopped"  # Change the game state to stopped
        self.save_high_score()  # Save high score when game ends
        self.score = 0  # Reset the score
        self.snake.wall_hit_sound.play()    # Play the wall hit sound

    def save_high_score(self):
        with open("highscore.txt", "w") as file:    # Open the highscore file in write mode
            file.write(str(self.high_score))    # Write the high score to the file

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:    # Open the highscore file in read mode
                return int(file.read()) # Read and return the high score from the file
        except FileNotFoundError:
            return 0  # Default high score if file doesn't exist

# Create game window
screen = pygame.display.set_mode((2 * OFFSET + cell_size * number_of_cells, 2 * OFFSET + cell_size * number_of_cells))  # Set the size of the game window
pygame.display.set_caption("Retro Snake")   #Set the window title

# Clock for controlling the frame rate
clock = pygame.time.Clock() 
food_surface = pygame.image.load("food.png")    # Load the food image
game = Game()   # Create a Game object

SNAKE_UPDATE = pygame.USEREVENT     # Create a custom event for updating the snake
pygame.time.set_timer(SNAKE_UPDATE, 100)    # Set a timer to trigger the custom event every 100 milliseconds

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:  
            game.update()   # Update the game state
        if event.type == pygame.QUIT:
            game.save_high_score()  # Save high score before quitting
            pygame.quit()   # Quit pygame
            sys.exit()      # Exit the program

        if event.type == pygame.KEYDOWN:
            if game.state == "Stopped":
                game.state = "Running"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):      # Change direction to up
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):       # Change direction to down
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):        # Change direction to left
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):      # Change direction to right
                game.snake.direction = Vector2(1, 0)

    # Drawing
    screen.fill(GREEN)      # Fill the screen with green color

    pygame.draw.rect(screen, DARK_GREEN,
                     (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 5)       # Draw the border
    game.draw()     # Draw the game elements

    title_surface = title_font.render("Retro Snake", True, DARK_GREEN)      # Render the title text
    score_surface = score_font.render(f"Score: {game.score}", True, DARK_GREEN)     # Render the score text
    high_score_surface = score_font.render(f"High Score: {game.high_score}", True, DARK_GREEN)      # Render the highscore text

    screen.blit(title_surface, (OFFSET - 5, 20))    # Draw the title on the screen
    screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))     # Draw the score on the screen
    screen.blit(high_score_surface, (OFFSET + 200, OFFSET + cell_size * number_of_cells + 10))      # Draw  the highscore on the screen

    pygame.display.update()     # Update the display
    clock.tick(60)      # Cap the frame rate at 60 FPS
