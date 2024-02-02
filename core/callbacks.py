import logging


class Callbacks:
    _player_list={}
    _player_list_initialized=False

    def announce_player(self, con, response):
        """announce joining or leaving players

        Args:
            con (instance): Instance of the RCON class
            response (str): Response with all players from the gameserver
        """
        new_player_list = self._palworld_extract_playerlist(response)
        # check for players that joined our server
        for player in new_player_list:
            if not player in self._player_list:
                self._player_list[player] = new_player_list[player]
                if self._player_list_initialized:
                    cmd = con.command('broadcast ' + "{} has joined the server :)".format(
                        self._player_list[player]['name']
                    ).replace(' ', '_'))
                    logging.info(cmd.replace("\n",""))
        # check for players that have left our server
        for player in self._player_list.copy():
            if not player in new_player_list:
                if self._player_list_initialized:
                    cmd = con.command('broadcast ' + "{} has left the server ...".format(
                        self._player_list[player]['name']
                    ).replace(' ', '_'))
                    logging.info(cmd.replace("\n",""))
                del self._player_list[player]
        if not self._player_list_initialized:
            self._player_list_initialized = True

    def _palworld_extract_playerlist(self, response):
        """extracts players from the showplayers response

        Args:
            response (str): Response with all players from the gameserver

        Returns:
            _type_: _description_
        """
        # Split the data into lines and discard the header
        lines = response.strip().split('\n')[1:]
        players = {}
        for line in lines:
            parts = line.rsplit(',', 2)
            if len(parts) == 3:
                name, playeruid, steamid = parts
                players[steamid] = {
                    'name': name,
                    'playeruid': playeruid,
                    'steamid': steamid
                }
        return players