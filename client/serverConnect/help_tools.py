import sys
from itertools import product
from random import randrange

sys.path.insert(0, "/home/utyfull/Desktop/projects/tgBotWithApi/client/serverConnect")
from dbConnect import connect_to_Server


class helping_methods:
    def new_key():
        alphabet = '123456!@#$%^&*'
        key_list = list(product(alphabet, repeat=6))
        index = randrange(0, 5000)
        key = ''.join(i for i in key_list[index])
        if connect_to_Server.check_key(key) == "YES":
            return helping_methods.new_key()
        else:
            return key

    def check_team_valid(self, team):
        pass

