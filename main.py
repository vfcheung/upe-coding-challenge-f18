import json
import requests


BASE_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
UID = "404751330"


class HttpHandler:


    def __init__(self, base_url, uid):
        self.base_url = base_url
        self.uid = uid
        self.token = json.loads(requests.post(self.base_url + "/session", data={"uid": self.uid}, headers={"content-type": "application/x-www-form-urlencoded"}).text)["token"]


    def get_game_state(self):
        state = json.loads(requests.get(self.base_url + "/game?token=" + self.token).text)
        return state

    
    def post_action(self, action):
        payload = {"action": action}
        response = json.loads(requests.post(self.base_url + "/game?token=" + self.token, data=payload).text)
        return response


class Game:

    def __init__(self):
        self.h = HttpHandler(BASE_URL, UID)
        self.update()


    def update(self):
        state = self.h.get_game_state()
        self.width = state["maze_size"][0]
        self.height = state["maze_size"][1]
        self.maze = [[0] * self.width for _ in range(self.height)]
        self.col = state["current_location"][0]
        self.row = state["current_location"][1]
        self.status = state["status"]
        self.levels_completed = state["levels_completed"]
        self.total_levels = state["total_levels"]


    def move(self, action):
        response = self.h.post_action(action)
        return response["result"]



class MazeSolver:
    

    def __init__(self):
        pass
    

    def solve_maze(self, game, result="SUCCESS"):

        # if game.status != "PLAYING":
        #     return

        if result == "END":
            print("Maze completed")
            return True

        if result == "WALL" or result == "OUT_OF_BOUNDS":
            return False

        if game.col < 0 or game.col >= game.width or game.row < 0 or game.row >= game.height:
            return False
        
        if game.maze[game.row][game.col] == 1:
            return False

        curr_row = game.row
        curr_col = game.col

        game.maze[curr_row][curr_col] = 1

        game.row, game.col = curr_row - 1, curr_col
        if self.solve_maze(game, game.move("UP")):
            return True

        game.row, game.col = curr_row + 1, curr_col
        if self.solve_maze(game, game.move("DOWN")):
            return True

        game.row, game.col = curr_row, curr_col - 1
        if self.solve_maze(game, game.move("LEFT")):
            return True

        game.row, game.col = curr_row, curr_col + 1
        if self.solve_maze(game, game.move("RIGHT")):
            return True

        return False




    

def main():
    g = Game()
    ms = MazeSolver()

    while g.status != "FINISHED":
        ms.solve_maze(g)
        g.update()

    print(g.status)


if __name__ == "__main__":
    main()