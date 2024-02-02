import logging
from mcrcon import MCRcon
import schedule
import time
import yaml

class PalworldRCON:
    config = None

    def __init__(self):
        """initialize class
        """
        self._set_logging()
        self._load_config()
        self._create_schedules()
        self.loop()

    def _set_logging(self):
        """set basic logging
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
            handlers=[logging.StreamHandler()],
        )

    def _load_config(self):
        """load yaml config
        """
        logging.info(f"loading config file")
        try:
            with open("./config.yaml", "r") as file:
                self.config = yaml.safe_load(file)
        except BaseException as error:
            logging.error(f"could not load config file: {error}")
            quit()

    def _create_schedules(self):
        """iterate through the config file and create all schedules to run
        """
        for server in self.config:
            server = self.config[server][0]
            logging.info(f"create schedules for {server['ip']}:{server['query_port']}")
            # config to pass to each schedule
            server_config = {
                "ip": server["ip"],
                "port": server["query_port"],
                "password": server["rcon_password"],
            }
            # iterate through all commands
            for command in server['schedules']:
                chain = getattr(schedule, "every")
                for attribute, value in command["every"][0].items():
                    if isinstance(value, list) and 'at' in value[0]:
                        # run function e.g. "day"
                        chain = getattr(chain(), attribute)
                        # run function "at"
                        if isinstance(value[0]["at"], list):
                            chain = getattr(chain, "at")(*value[0]["at"])
                        else:
                            chain = getattr(chain, "at")(str(value[0]["at"]))
                    else:
                        chain = getattr(chain(value if value else None), attribute)
                # start schedule
                chain.do(
                    self.run_command,
                    config=server_config,
                    command=command["command"],
                    arguments=command["arguments"] if "arguments" in command else None
                )

    def run_command(self, config, command, arguments):
        """connects to the palworld server and executes a command

        Args:
            config (dict): configuration data to connect to the server
            command (string): the command to run
            arguments (string): the arguments to add to the command
        """
        logging.info("running command {} with parameter {}".format(command, arguments))
        try:
            with MCRcon(host=config["ip"], port=config["port"], password=config["password"], timeout=5) as con:
                response = con.command('ShowPlayers')
                print(response)
        except BaseException as e:
            logging.error(f"could not run command: {e}")

    def loop(self):
        """run endless loop to check for tasks
        """
        logging.info("waiting for schedules")
        while True:
            schedule.run_pending()
            time.sleep(1)
    
if __name__ == '__main__':
    PalworldRCON()
