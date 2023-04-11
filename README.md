# tic-tac-toe-panel-library
Tic Tac Toe game ( User vs Computer ) using [Panel library](https://panel.holoviz.org/index.html)

Some features of this implementation:
1. Game supports 3 difficulty levels.
2. Game allows user to choose X or O as their move for a game.
3. Game switches first move between User and Computer after every reset and after every configuration change to ensure fairness for both players.


The app is converted to webassembly and deployed to https://2598nitz.github.io/tic-tac-toe-panel-library/ .
Known [issue](https://github.com/pyodide/pyodide/issues/97) with pyodide, hence not showing delay added for Computer move when converted to Webassembly.

To run the app locally:
1. Clone this repository.
2. Make sure dependecies mentioned in [requirements.txt](/requirements.txt) file are installed by pip or conda.
3. Run command: panel serve app.py --show --autoreload

Some screenshots of the application:

<img width="520" alt="image" src="https://user-images.githubusercontent.com/35998771/231260643-0ddf0f71-a65a-4005-8a6d-9b07ab661bfc.png">
<img width="552" alt="image" src="https://user-images.githubusercontent.com/35998771/231260876-4091bdc6-eec2-412f-a405-b1665b299edf.png">
<img width="510" alt="image" src="https://user-images.githubusercontent.com/35998771/231261241-8b3583cf-3047-454c-b7da-41eb03132d1b.png">

