import json
import queue
import requests


BASE_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
UID = "404751330"


class HttpHandler:


    def __init__(self, base_url, uid):
        self._base_url = base_url
        self._uid = uid
        while True:
            response = requests.post(self._base_url + "/session", data={"uid": self._uid}, headers={"content-type": "application/x-www-form-urlencoded"})
            if response.status_code == requests.codes["OK"]:
                break
        self._token = json.loads(response.text)["token"]


    def get_game_state(self):
        while True:
            response = requests.get(self._base_url + "/game?token=" + self._token)
            if response.status_code == requests.codes["OK"]:
                break
        return json.loads(response.text)


    def post_action(self, action):
        while True:
            response = requests.post(self._base_url + "/game?token=" + self._token, data={"action": action})
            if response.status_code == requests.codes["OK"]:
                break
        return json.loads(response.text)["result"]


class Game:


    def __init__(self):
        self.h = HttpHandler(BASE_URL, UID)
        self.get_next_maze()


    def get_next_maze(self):
        state = self.h.get_game_state()
        dimensions = state["maze_size"]
        if dimensions != None:
            self.width, self.height = dimensions
        start_position = state["current_location"]
        if start_position != None:
            self.col, self.row = start_position
        self.status = state["status"]
        self.levels_completed = state["levels_completed"]
        self.total_levels = state["total_levels"]
        


    def move(self, action):
        result = self.h.post_action(action)
        if result == "SUCCESS":
            if action == "UP":
                self.row -= 1
            elif action =="DOWN":
                self.row += 1
            elif action == "LEFT":
                self.col -= 1
            elif action == "RIGHT":
                self.col += 1
        return result


class MazeSolver:

    _directions = ["UP","DOWN","LEFT","RIGHT"]
    _opposite = {"UP":"DOWN", "DOWN":"UP", "LEFT":"RIGHT", "RIGHT":"LEFT"}

    def __init__(self):
        self._visited = set()

    def _solve_maze_helper(self, game):
        
        self._visited.add((game.row, game.col))

        for dir in self._directions:
            result = game.move(dir)
            if result == "END":
                return True
            if result == "SUCCESS":
                if (game.row, game.col) not in self._visited and self._solve_maze_helper(game):
                    return True
                game.move(self._opposite[dir])

        return False


    def solve_maze(self, game):
        print("Solving maze {0} of {1} with size {2} x {3} ...".format(game.levels_completed + 1, game.total_levels, game.height, game.width))
        if self._solve_maze_helper(game):
            print("Maze {0} completed".format(game.levels_completed + 1))
            self._reset()
        else:
            print("Could not solve maze")


    def _reset(self):
        self._visited = set()


def main():

    g = Game()
    ms = MazeSolver()

    while g.status != "FINISHED" and g.status != None:
        ms.solve_maze(g)
        g.get_next_maze()

    print(g.status)


if __name__ == "__main__":
    main()