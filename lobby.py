class Lobby:
    def __init__(self, max_size=10) -> None:
        self.__lobby = []
        self.has_pair = False
        self.__max_size = max_size
    
    def __is_user_in_lobby(self, user):
         
        for u in self.__lobby:
            if u[0] == user[0] and u[0] != '127.0.0.1':
                return True
    
    def add(self, user):
        if len(self.__lobby) < self.__max_size and not self.__is_user_in_lobby(user):
            self.__lobby.append(user)
            self.__update_has_pair()
    
    def __update_has_pair(self):
        if len(self.__lobby) >= 2:
            self.has_pair = True
        else:
            self.has_pair = False

    def delete(self, *users):
        for user in users:
            if user in self.__lobby:
                self.__lobby.remove(user)
        self.__update_has_pair()

    def is_empty(self):
        return not self.__lobby

    def pair(self):
        if len(self.__lobby) >= 2:
            players = self.__lobby[0], self.__lobby[1]
            self.delete(self.__lobby[0], self.__lobby[1])
            return players
    
    def __str__(self) -> str:
        return "(Empty)" if len(self.__lobby) == 0 else '\n' + ' | '.join(str(t) for t in self.__lobby)
