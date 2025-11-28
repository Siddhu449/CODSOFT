import random
import tkinter as tk
from tkinter import messagebox

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("400x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Initialize scores
        self.user_score = 0
        self.computer_score = 0
        self.tie_count = 0
        self.round_count = 0
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎮 Rock Paper Scissors", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Score display
        self.score_frame = tk.Frame(self.root, bg='#34495e', relief='ridge', bd=2)
        self.score_frame.pack(pady=10, padx=20, fill='x')
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"🏆 You: {self.user_score}   🤖 Computer: {self.computer_score}   🤝 Ties: {self.tie_count}",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            pady=8
        )
        self.score_label.pack()
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Choose your move:",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        instructions.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=15)
        
        # Choice buttons with icons
        self.rock_btn = tk.Button(
            button_frame,
            text="🪨 Rock",
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.play_game("rock")
        )
        self.rock_btn.grid(row=0, column=0, padx=8, pady=5)
        
        self.paper_btn = tk.Button(
            button_frame,
            text="📄 Paper",
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            bg='#2ecc71',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.play_game("paper")
        )
        self.paper_btn.grid(row=0, column=1, padx=8, pady=5)
        
        self.scissors_btn = tk.Button(
            button_frame,
            text="✂️ Scissors",
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.play_game("scissors")
        )
        self.scissors_btn.grid(row=0, column=2, padx=8, pady=5)
        
        # Results display frame
        result_main_frame = tk.Frame(self.root, bg='#34495e', relief='sunken', bd=2)
        result_main_frame.pack(pady=15, padx=20, fill='x')
        
        # Choices display
        choices_frame = tk.Frame(result_main_frame, bg='#34495e')
        choices_frame.pack(pady=10)
        
        self.user_choice_label = tk.Label(
            choices_frame,
            text="You: ❓",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#3498db'
        )
        self.user_choice_label.grid(row=0, column=0, padx=15)
        
        vs_label = tk.Label(
            choices_frame,
            text="VS",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='#f39c12'
        )
        vs_label.grid(row=0, column=1, padx=15)
        
        self.computer_choice_label = tk.Label(
            choices_frame,
            text="Computer: ❓",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.computer_choice_label.grid(row=0, column=2, padx=15)
        
        # Result display
        self.result_label = tk.Label(
            result_main_frame,
            text="Make your move!",
            font=('Arial', 16, 'bold'),
            bg='#34495e',
            fg='#f1c40f',
            pady=10
        )
        self.result_label.pack()
        
        # Action buttons frame
        action_frame = tk.Frame(self.root, bg='#2c3e50')
        action_frame.pack(pady=15)
        
        # Play again button
        self.play_again_btn = tk.Button(
            action_frame,
            text="🔄 Play Again",
            font=('Arial', 12, 'bold'),
            width=12,
            height=1,
            bg='#9b59b6',
            fg='white',
            relief='raised',
            bd=2,
            command=self.reset_round,
            state=tk.DISABLED
        )
        self.play_again_btn.grid(row=0, column=0, padx=10)
        
        # Reset game button
        reset_btn = tk.Button(
            action_frame,
            text="🔄 New Game",
            font=('Arial', 12, 'bold'),
            width=12,
            height=1,
            bg='#e67e22',
            fg='white',
            relief='raised',
            bd=2,
            command=self.reset_game
        )
        reset_btn.grid(row=0, column=1, padx=10)
        
        # Game rules
        rules_frame = tk.Frame(self.root, bg='#2c3e50')
        rules_frame.pack(pady=10)
        
        rules_label = tk.Label(
            rules_frame,
            text="🎯 Rock beats Scissors | ✂️ Scissors beat Paper | 📄 Paper beats Rock",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#95a5a6',
            wraplength=350
        )
        rules_label.pack()
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Enjoy the game! 🎮",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#7f8c8d'
        )
        footer_label.pack(pady=10)
    
    def play_game(self, user_choice):
        # Disable choice buttons during result display
        self.rock_btn.config(state=tk.DISABLED)
        self.paper_btn.config(state=tk.DISABLED)
        self.scissors_btn.config(state=tk.DISABLED)
        
        # Reset all button colors first
        self.rock_btn.config(bg='#3498db')
        self.paper_btn.config(bg='#2ecc71')
        self.scissors_btn.config(bg='#e74c3c')
        
        # Highlight user's choice
        if user_choice == "rock":
            self.rock_btn.config(bg='#2980b9')
        elif user_choice == "paper":
            self.paper_btn.config(bg='#27ae60')
        elif user_choice == "scissors":
            self.scissors_btn.config(bg='#c0392b')
        
        # Get computer's choice
        computer_choice = random.choice(["rock", "paper", "scissors"])
        
        # Update choice displays with icons
        choice_icons = {
            "rock": "🪨",
            "paper": "📄", 
            "scissors": "✂️"
        }
        
        self.user_choice_label.config(text=f"You: {choice_icons[user_choice]}")
        self.computer_choice_label.config(text=f"Computer: {choice_icons[computer_choice]}")
        
        # Determine winner
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update result display with emojis
        result_emojis = {
            "You win!": "🎉 You win! 🎉",
            "You lose!": "😞 You lose! 😞", 
            "It's a tie!": "🤝 It's a tie! 🤝"
        }
        
        self.result_label.config(text=result_emojis.get(result, result))
        
        # Update scores and colors
        if "win" in result.lower():
            self.user_score += 1
            self.result_label.config(fg='#2ecc71')  # Green for win
        elif "lose" in result.lower():
            self.computer_score += 1
            self.result_label.config(fg='#e74c3c')  # Red for lose
        else:
            self.tie_count += 1
            self.result_label.config(fg='#f39c12')  # Orange for tie
        
        # Update score display
        self.score_label.config(
            text=f"🏆 You: {self.user_score}   🤖 Computer: {self.computer_score}   🤝 Ties: {self.tie_count}"
        )
        
        # Enable play again button
        self.play_again_btn.config(state=tk.NORMAL)
    
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        
        winning_combinations = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        
        if winning_combinations[user_choice] == computer_choice:
            return "You win!"
        else:
            return "You lose!"
    
    def reset_round(self):
        # Reset choice displays
        self.user_choice_label.config(text="You: ❓", fg='#3498db')
        self.computer_choice_label.config(text="Computer: ❓", fg='#e74c3c')
        self.result_label.config(text="Make your move!", fg='#f1c40f')
        
        # Reset button colors
        self.rock_btn.config(bg='#3498db')
        self.paper_btn.config(bg='#2ecc71')
        self.scissors_btn.config(bg='#e74c3c')
        
        # Enable choice buttons
        self.rock_btn.config(state=tk.NORMAL)
        self.paper_btn.config(state=tk.NORMAL)
        self.scissors_btn.config(state=tk.NORMAL)
        
        # Disable play again button
        self.play_again_btn.config(state=tk.DISABLED)
    
    def reset_game(self):
        # Reset scores
        self.user_score = 0
        self.computer_score = 0
        self.tie_count = 0
        
        # Update score display
        self.score_label.config(
            text=f"🏆 You: {self.user_score}   🤖 Computer: {self.computer_score}   🤝 Ties: {self.tie_count}"
        )
        
        # Reset round
        self.reset_round()

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()