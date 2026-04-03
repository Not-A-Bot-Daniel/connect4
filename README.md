# 🔴 Connect 4: Terminal Edition 🟡

A Python implementation of the classic Connect 4 game, developed as a hands-on project to explore Python, study, and improve my programming skills.

## 📖 Project Overview
The objective of this project was to build a functional game engine from scratch, focusing on efficient board evaluation and recursive search algorithms. It features a dynamic "AI" opponent named **B1P**, designed to provide an escalating challenge as the player improves.

## 🛠️ Key Features
* **Bot Decision Making**: Implemented using the **Minimax algorithm** with **Alpha-Beta pruning** to optimize search depth and performance.
* **Smart Heuristics**: The AI is programmed to prioritize high-value areas of the board, such as the center column, to maximize its winning potential.
* **Interactive UI**: A color-coded terminal interface with falling token animations.
* **Audio Integration**: Uses the `pygame` library to handle background music and sound effects, including a specialized "God Mode" soundtrack.

## 🧠 Technical Deep-Dive
* **Board Representation**: The game state is managed via a 2D matrix, with logical checks for win conditions (Horizontal, Vertical, and Diagonal).
* **Search Optimization**: Alpha-Beta pruning is used to significantly reduce the number of nodes evaluated by the Minimax tree, allowing for deeper look-ahead.
* **Game Loop**: A robust loop that handles turn transitions, input validation, and real-time board updates.

## 🚀 Getting Started
1. **Prerequisites**: Ensure you have Python 3 installed.
2. **Installation**: Install the required sound library:

## 🎵 Credits & Resources
* **Casual Mode Music**: "Retro Arcade Game Music 2" by Monume (via Pixabay)
* **God Mode Music**: "To The Death" by Junipersona (via Pixabay)
* **Game Icon**: Generated using OpenAI's ChatGPT (DALL-E 3)
  
   ```bash
   pip install pygame
   python 4inarow.py
