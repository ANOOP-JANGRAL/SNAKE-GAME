import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        
        self.width = 400
        self.height = 400
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game)
        self.restart_button.pack()
        
        # Initialize the game
        self.snake_speed = 100  # Snake speed in milliseconds
        self.restart_game()
    
    def restart_game(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.snake_direction = 'Right'
        self.food = None
        self.score = 0
        
        self.canvas.delete("all")
        self.create_food()
        self.update_snake()
        
        self.master.bind("<KeyPress>", self.on_key_press)
        self.run_game()
    
    def run_game(self):
        self.move_snake()
        self.master.after(self.snake_speed, self.run_game)
    
    def update_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill='green', tags="snake")
    
    def create_food(self):
        if self.food is not None:
            self.canvas.delete("food")
        
        x = random.randint(0, (self.width - 10) // 10) * 10
        y = random.randint(0, (self.height - 10) // 10) * 10
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='red', tags="food")
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == 'Up':
            head_y -= 10
        elif self.snake_direction == 'Down':
            head_y += 10
        elif self.snake_direction == 'Left':
            head_x -= 10
        elif self.snake_direction == 'Right':
            head_x += 10
        
        new_head = (head_x, head_y)
        
        if self.check_collision(new_head):
            self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", fill="white", font=('Arial', 24))
            self.canvas.create_text(self.width // 2, self.height // 2 + 30, text="Press 'Restart' to play again", fill="white", font=('Arial', 14))
            self.master.unbind("<KeyPress>")
            return
        
        self.snake = [new_head] + self.snake[:-1]
        
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.score += 1
            self.create_food()
        
        self.update_snake()
    
    def check_collision(self, head):
        if (head[0] < 0 or head[0] >= self.width or
            head[1] < 0 or head[1] >= self.height or
            head in self.snake):
            return True
        return False
    
    def on_key_press(self, event):
        new_direction = event.keysym
        if new_direction in ['Up', 'Down', 'Left', 'Right']:
            if (new_direction == 'Up' and self.snake_direction != 'Down' or
                new_direction == 'Down' and self.snake_direction != 'Up' or
                new_direction == 'Left' and self.snake_direction != 'Right' or
                new_direction == 'Right' and self.snake_direction != 'Left'):
                self.snake_direction = new_direction

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()