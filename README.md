# PyGame Arkanoid

University internship project: "Python-powered Game Development" — an interactive, feature-rich game built using Python and PyGame, showcasing modern graphics, smooth gameplay mechanics, and advanced game design concepts.

<img width="1056" height="743" alt="image" src="https://github.com/user-attachments/assets/18806495-4f7f-49b2-87e7-76d55fa7c142" />
<img width="1055" height="743" alt="image" src="https://github.com/user-attachments/assets/bd00bd38-178e-49c4-b934-f139d5c2e41e" />
<img width="1205" height="851" alt="image" src="https://github.com/user-attachments/assets/47c5bf7e-fdb2-4517-9abd-11a773db336f" />

## Features

- **Title Screen** with start button and mute instructions
- **Mute Button**: Press `M` during gameplay to mute/unmute sounds
- **15 Unique Levels**: Selectable via keyboard or mouse, each with a preview image
- **Game Over & Win Screens**: Custom backgrounds, restart instructions, and fireworks on win
- **Multiple Power-ups**: Includes Grow Paddle, Laser, Glue, Slow Ball, Multi-ball, Extra Life, and Shrink Paddle
- **Particle Effects**: For brick breaking, paddle/ball collisions, and fireworks
- **Laser Cannons**: Shoot bricks when powered up
- **Responsive Controls** and smooth gameplay

## Requirements

- Python 3.7+
- [PyGame](https://www.pygame.org/) (see requirements.txt)

## Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Controls

- **Arrow Keys**: Move paddle left/right
- **Space**: Launch ball (when glued) or start game/return to title
- **M**: Mute/unmute sounds
- **F**: Fire lasers (when laser power-up is active)
- **Mouse**: Click level preview to select level in level select screen
- **1-9, 0**: Select level by number in level select screen
- **P**: Pause/unpause the game (shows 'PAUSED')

## Power-ups

- **Grow (G)**: Paddle grows larger
- **Laser (L)**: Enables laser cannons (press F to fire)
- **Glue (C)**: Ball sticks to paddle on hit
- **Slow (S)**: Ball moves slower
- **Multi (M)**: Splits ball into two
- **Life (+)**: Gain an extra life
- **Shrink (-)**: Paddle shrinks

## How to Run

1. **Make sure you have installed the requirements above**
2. **Run the game**:
   ```bash
   python main.py
   ```

## Assets

- All images and sounds are included in the `assets/` and `levels/` folders.
- Make sure these folders are in the same directory as `main.py`.

## Credits

- Developed for Phase 12 Homework
- Powered by [PyGame](https://www.pygame.org/)
- Sound and image assets: see `assets/images` and `assets/sounds`

## License

This project is for educational purposes.
