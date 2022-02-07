import re

def _load_highscores(self):
        """Load in any HighScores from previous games."""
        highscore_regex = re.compile(r"Highscore: .*")
        # Try to open the file and extract highscore info.
        try:
            with open('Space_Invaders\game_data.txt') as data_object:
                data = data_object.read()
                highscore_regex = re.compile(r"Highscore: .*")
                content = highscore_regex.findall(data)
            highscore = str(content)
            data_object.close()

        
        except FileNotFoundError:
            # If the game data file doesn't exist create on and set the highscore to zero.
            with open('Space_Invaders\game_data.txt', 'w') as data_object:
                highscore = '0'

                data_object.write(f'Highscore: {highscore}')
            data_object.close()
