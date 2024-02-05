import logging
from mcrcon import MCRcon
from pydoc import locate
import schedule
import time
import yaml

class PalworldRCON:
    callbacks = {}
    config = None

    def __init__(self):
        """initialize class
        """
        self._load_config()
        self._set_logging()
        self._create_schedules()
        self.loop()

    def _set_logging(self):
        """set basic logging
        """
        if "app" in self.config and "log_level" in self.config["app"]:
            if hasattr(logging, str(self.config["app"]["log_level"]).upper()):
                level = getattr(logging, str(self.config["app"]["log_level"]).upper())
        else:
            level = logging.DEBUG
        logging.basicConfig(
            level=level,
            format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
            handlers=[logging.StreamHandler()],
        )

    def _load_config(self):
        """load yaml config
        """
        try:
            with open("./config.yaml", "r") as file:
                self.config = yaml.safe_load(file)
        except BaseException as error:
            logging.error(f"could not load config file: {error}")
            quit()

    def _create_schedules(self):
        """iterate through the config file and create all schedules to run
        """
        for server in self.config["gameserver"]:
            logging.info(f"create schedules for {server['ip']}:{server['query_port']}")
            # config to pass to each schedule
            server_config = {
                "ip": server["ip"],
                "port": server["query_port"],
                "password": server["rcon_password"],
            }
            # iterate through all commands
            for command in server['schedules']:
                for entry in command["every"]:
                    chain = getattr(schedule, "every")
                    for attribute, value in entry.items():
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
                        arguments=command["arguments"] if "arguments" in command else None,
                        callback=command["callback"] if "callback" in command else None
                    )

    def run_command(self, config, command, arguments, callback):
        """connects to the palworld server and executes a command

        Args:
            config (dict): configuration data to connect to the server
            command (string): the command to run
            arguments (string): the arguments to add to the command
            callback (string): the callback to run if exists
        """
        logging.debug("running command {} with parameter {}".format(command, arguments))
        try:
            with MCRcon(host=config["ip"], port=config["port"], password=config["password"], timeout=5) as con:
                if arguments:
                    response = con.command(command + " " + arguments)
                else:
                    response = con.command(command)
                if callback:
                    try:
                        cb_split = callback.split(".")
                        if len(cb_split) == 2:
                            # check if class got loaded already
                            if str(cb_split[0]).lower() + "." + str(cb_split[0]).lower().capitalize() in self.callbacks:
                                module = self.callbacks[str(cb_split[0]).lower() + "." + str(cb_split[0]).lower().capitalize()]
                            else:
                                # try to load class (from plugins.test import Test)
                                module = locate(f"plugins." + str(cb_split[0]).lower() + "." + str(cb_split[0]).lower().capitalize())
                                # load plugin
                                module = module()
                            # check if plugin has the given function
                            if hasattr(module, cb_split[1]):
                                # run the function
                                func = getattr(module, cb_split[1])
                                func(con, response)
                    except BaseException as e:
                        logging.error(f"could not load module {callback}: {e}")
                else:
                    logging.info(response.replace("\n",""))
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
    try:
        PalworldRCON()
    except KeyboardInterrupt:
        logging.info("Exiting due to KeyboardInterrupt (e.g. STRG+C)")
        quit()
