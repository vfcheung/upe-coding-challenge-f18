import json
import queue
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
        self.visited = dict()
        self.col = state["current_location"][0]
        self.row = state["current_location"][1]
        self.status = state["status"]
        self.levels_completed = state["levels_completed"]
        self.total_levels = state["total_levels"]


    def move(self, action):
        response = self.h.post_action(action)
        self.update()
        return response["result"]



class MazeSolver:
    

    def __init__(self):
        pass
    

    def solve_maze(self, game):

        q = queue.Queue()
        q.put((game.row, game.col))
        start_row = game.row
        start_col = game.col

        while not q.empty():

            row, col = q.get()
            print("currently searching from", row, col)

            if row != start_row and col != start_col:
                game.move(game.visited[(row, col)])

            response = game.move("UP")
            if response == "END":
                print("Finished maze")
                break
            if response == "SUCCESS" and (game.row, game.col) not in game.visited:
                print("Moving up to", game.row, game.col)
                game.visited[(game.row, game.col)] = "UP"
                q.put((game.row, game.col))
            if response == "SUCCESS":
                game.move("DOWN")
            # else:
            #     game.move("DOWN")

            response = game.move("DOWN")
            if response == "END":
                print("Finished maze")
                break
            if response == "SUCCESS" and (game.row, game.col) not in game.visited:
                print("Moving down to", game.row, game.col)
                game.visited[(game.row, game.col)] = "DOWN"
                q.put((game.row, game.col))
            if response == "SUCCESS":
                game.move("UP")
            # else:
            #     game.move("UP")

            response = game.move("LEFT")
            if response == "END":
                print("Finished maze")
                break
            if response == "SUCCESS" and (game.row, game.col) not in game.visited:
                print("Moving left to", game.row, game.col)
                game.visited[(game.row, game.col)] = "LEFT"
                q.put((game.row, game.col))
            if response == "SUCCESS":
                game.move("RIGHT")
            # else:
            #     game.move("RIGHT")

            response = game.move("RIGHT")
            if response == "END":
                print("Finished maze")
                break
            if response == "SUCCESS" and (game.row, game.col) not in game.visited:
                print("Moving right to", game.row, game.col)
                game.visited[(game.row, game.col)] = "RIGHT"
                q.put((game.row, game.col))
            if response == "SUCCESS":
                game.move("LEFT")
            # else:
            #     game.move("LEFT")



    

def main():
    g = Game()
    ms = MazeSolver()

    # while g.status != "FINISHED":
    #     ms.solve_maze(g)
    #     g.update()

    print(g.width, g.height, g.row, g.col, g.status, g.levels_completed, g.total_levels)

    ms.solve_maze(g)

    print(g.status)


if __name__ == "__main__":
    main()