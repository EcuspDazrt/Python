import time
import os

# Define the Spider-Man dance frames
frames = [
    r"""
     (\(\
    ( -.-)
   o_(")(")   🕷️ Spider-Man Dancing - Pose 1
    """,
    r"""
     (\_/) 
    ( o.o )
    > ^ <   🕷️ Spider-Man Dancing - Pose 2
    """,
    r"""
     (\_/)
    ( •_•)
    / >🕸️>  Spider-Man Shooting Web - Pose 3
    """,
    r"""
     (\_/)
    ( •_•)
    <🕸️< \  Spider-Man Shooting Web - Pose 4
    """
]

# Loop to animate
try:
    while True:
        for frame in frames:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
            print(frame)
            time.sleep(0.5)  # Delay between frames
except KeyboardInterrupt:
    print("\n🕸️ Spider-Man dance stopped.")
