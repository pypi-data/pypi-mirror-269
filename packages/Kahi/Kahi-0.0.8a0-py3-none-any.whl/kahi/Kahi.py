import yaml
from importlib import import_module
import pkgutil
from collections import OrderedDict
from pymongo import MongoClient
from time import time


class OrderedLoader(yaml.SafeLoader):
    def __init__(self, *args, **kwargs):
        super(OrderedLoader, self).__init__(*args, **kwargs)

        def construct_dict_order(self, data):
            return OrderedDict(self.construct_pairs(data))
        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_dict_order)


class Kahi:
    def __init__(self, workflow_file, verbose=0, use_log=True):
        self.plugin_prefix = "kahi_"
        self.workflow_file = workflow_file
        self.workflow = None
        self.config = None
        self.plugins = {}

        self.client = None

        self.log_db = None
        self.log = None
        self.use_log = use_log
        self.verbose = verbose

    def load_workflow(self):
        """
        Loads the workflow from file
        """
        with open(self.workflow_file, "r") as stream:
            data = yaml.load(stream, Loader=OrderedLoader)
            self.workflow = data["workflow"]
            self.config = data["config"]
            self.client = MongoClient(self.config["database_url"])
            if self.verbose > 4:
                print(data)

    def load_plugins(self, verbose=0):
        """
        Loads all plugins available in the system
        """
        discovered_plugins = {
            name: import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith(self.plugin_prefix + "_")
        }
        self.discovered_plugins = discovered_plugins

    def retrieve_logs(self):
        """
        Retrieves the logs from the database
        """

        self.log_db = self.client[self.config["log_database"]]
        log = list(self.log_db[self.config["log_collection"]].find())
        if log:
            self.log = log

        if self.verbose > 1:
            print("Log retrieved from database")
        if self.verbose > 4:
            print(log)

    def run(self):
        if not self.workflow:
            self.load_workflow()
        if not self.log:
            self.retrieve_logs()

        # import modules
        for module_name in self.workflow.keys():
            if self.verbose > 4:
                print("Loading plugin: " + self.plugin_prefix + module_name)
            if len(module_name.split("/")) > 1:
                module_name = module_name.split("/")[0]
            try:
                self.plugins[module_name] = import_module(
                    self.plugin_prefix + module_name + "." + self.plugin_prefix.capitalize() + module_name)
                self.plugins[module_name + "._version"] = import_module(
                    self.plugin_prefix + module_name + "._version")
            except ModuleNotFoundError as e:
                if self.verbose > 0 and self.verbose < 5:
                    print(e)
                    print("Plugin {} not found.\nTry\n\tpip install {}".format(
                        module_name,
                        self.plugin_prefix + module_name
                    ))
                    return None
                if self.verbose > 4:
                    raise

        # run workflow
        for log_id, params in self.workflow.items():
            executed_module = False
            log_split = log_id.split("/")
            if len(log_split) > 1:
                module_name = log_split[0]
                params["task"] = log_split[1]
            else:
                module_name = log_id
            if self.use_log:
                if self.log:
                    for log in self.log:
                        if log["_id"] == log_id:
                            if log["status"] == 0:
                                executed_module = True
                                break
            if executed_module:
                if self.verbose > 4:
                    print("Skipped plugin: " + self.plugin_prefix + log_id)
                continue
            if self.verbose > 4:
                print("Running plugin: " + self.plugin_prefix + log_id)

            plugin_class = getattr(
                self.plugins[module_name],
                self.plugin_prefix.capitalize() + module_name)

            plugin_class_version = getattr(
                self.plugins[module_name + "._version"], "get_version")

            plugin_config = self.config.copy()
            plugin_config[module_name] = self.workflow[log_id]
            if isinstance(plugin_config[module_name], list):
                for i in range(len(plugin_config[module_name])):
                    plugin_config[module_name][i]["task"] = params["task"] if "task" in params else None
            else:
                plugin_config[module_name]["task"] = params["task"] if "task" in params else None
            plugin_instance = plugin_class(config=plugin_config)

            run = getattr(plugin_instance, "run")
            try:
                time_start = time()
                status = run()
                time_elapsed = time() - time_start
                if self.verbose > 4:
                    print("Plugin {} finished in {} seconds".format(
                        log_id,
                        time_elapsed
                    ))
                if self.use_log:
                    if self.log_db[self.config["log_collection"]
                                   ].find_one({"_id": log_id}):
                        self.log_db[self.config["log_collection"]].update_one(
                            {
                                "_id": log_id
                            },
                            {"$set":
                                {
                                    "plugin_version": plugin_class_version(),
                                    "config": plugin_config[module_name],
                                    "time": int(time_start),
                                    "status": status,
                                    "message": "ok",
                                    "time_elapsed": int(time_elapsed)
                                }
                             }
                        )
                    else:
                        self.log_db[self.config["log_collection"]].insert_one(
                            {
                                "_id": log_id,
                                "plugin_version": plugin_class_version(),
                                "config": plugin_config[module_name],
                                "time": int(time_start),
                                "status": status,
                                "message": "ok",
                                "time_elapsed": int(time_elapsed)
                            }
                        )
            except Exception as e:
                if self.use_log:
                    if self.log_db[self.config["log_collection"]
                                   ].find_one({"_id": log_id}):
                        self.log_db[self.config["log_collection"]].update_one(
                            {
                                "_id": log_id
                            },
                            {"$set":
                                {
                                    "plugin_version": plugin_class_version(),
                                    "config": plugin_config[module_name],
                                    "time": int(time()),
                                    "status": 1,
                                    "message": str(e),
                                    "time_elapsed": 0
                                }
                             }
                        )
                    else:
                        self.log_db[self.config["log_collection"]].insert_one(
                            {
                                "_id": log_id,
                                "plugin_version": plugin_class_version(),
                                "config": plugin_config[module_name],
                                "time": int(time()),
                                "status": 1,
                                "message": str(e),
                                "time_elapsed": 0
                            }
                        )
                print("Plugin {} failed".format(log_id))
                raise
        if self.verbose > 0:
            print("Workflow finished")
