import datetime

from .__cls_aide_base__ import __cls_base__
from .__cls_aide_rst_files__ import __cls_aide_rst_files__


class _cls_aide_rst_base(__cls_base__):
    # noinspection PyMissingConstructor
    def __init__(self, module: str, log_level: int = -1):
        self.start_time = self.now()

        self.__dict_rst = {"state": False,
                           "msg": None,
                           "data": None,
                           "process": "INIT",
                           "module": module,
                           "dur": None}

        self.__terse_keys = ["state", "msg", "data"]

        self.__last_process = None

        # Level define for print and log
        # 0 No action
        # 1 False
        # 2 False and Warning
        # 3 False and Warning and Information
        # 4 ALL
        self.state_True = True
        self.state_False = False
        self.state_Warning = "Warning"
        self.state_Info = "Info"

        self.file = __cls_aide_rst_files__(log_level=log_level)

        self.__log_level = self.file.cfg_log_level

        self.__is_debug = self.file.cfg_is_debug

    @staticmethod
    def now():
        return datetime.datetime.now()

    def start(self):
        self.start_time = self.now()

    @property
    def dur(self,
            my_time_earlier: datetime.datetime = None,
            my_time_later: datetime.datetime = None):

        if my_time_later is None:
            my_time_later = datetime.datetime.now()
        else:
            pass

        if my_time_earlier is None:
            if isinstance(self.start_time, datetime.datetime):
                my_time_earlier = self.start_time
            else:
                return None
        else:
            pass

        diff = (my_time_later - my_time_earlier)
        diff = f"{diff.seconds}.{diff.microseconds}"

        return diff

    @staticmethod
    def __get_dict_value(my_dict_rst, my_key):
        if my_dict_rst.__contains__(my_key):
            return my_dict_rst[my_key]
        else:
            return None

    @property
    def state(self):
        return self.__get_dict_value(self.__dict_rst, "state")

    def set_state(self, new_state: bool = False):
        self.__dict_rst["state"] = new_state

        self.__dict_rst["dur"] = self.dur

        if self.__log_level == 0:
            pass
        elif self.__log_level == 1 and new_state in [self.state_False]:
            self.add_log()
        elif self.__log_level == 2 and new_state in [self.state_False, self.state_Warning]:
            self.add_log()
        elif self.__log_level == 3 and new_state in [self.state_False, self.state_Warning, self.state_Info]:
            self.add_log()
        elif self.__log_level == 4:
            self.add_log()
        else:
            pass

    @property
    def msg(self):
        return self.__get_dict_value(self.__dict_rst, "msg")

    def set_msg(self, new_msg: object = None):
        self.__dict_rst["msg"] = new_msg

    @property
    def data(self):
        return self.__get_dict_value(self.__dict_rst, "data")

    def set_data(self, new_data: object = None):
        self.__dict_rst["data"] = new_data

    @property
    def process(self):
        return self.__get_dict_value(self.__dict_rst, "process")

    def set_process(self, new_process_name: str = None):
        self.__last_process = self.process
        self.__dict_rst["process"] = new_process_name

    def set_process_back(self):
        self.__dict_rst["process"] = self.__last_process

    def set(self, new_state: object, new_msg: object = None, new_data: object = None, new_process: str = None):

        if isinstance(new_state, dict):
            state = new_state["state"]
            msg = new_state["msg"]
            data = new_state["data"]
        else:
            state = new_state
            msg = new_msg
            data = new_data

        self.set_msg(msg)
        self.set_data(data)

        if new_process is not None:
            self.set_process(new_process)
        else:
            if state == self.state_True:
                if self.__last_process is not None:
                    self.set_process_back()
                else:
                    pass
            else:
                self.set_process(f"{self.__last_process}.{self.process}")

        # fang zai zui hou ,chu fa ri zhi
        self.set_state(state)

    @property
    def _all(self):
        my_dict = self.__dict_rst.copy()

        my_dict["start_time"] = str(self.start_time)
        my_dict["end_time"] = str(self.now())

        my_dict["log_level"] = self.__log_level
        my_dict["is_debug"] = self.__is_debug
        my_dict["rst_file_folder"] = self.file.rst_file_folder

        return my_dict

    @property
    def all(self):
        return self.__dict_rst
        # self.__terse_keys = ["log_level", "is_debug"]
        # return {key: self.__dict_rst[key] for key in self.__dict_rst.keys() if key not in self.__hidden_keys}

    @property
    def terse(self):
        return {key: self.__dict_rst[key] for key in self.__terse_keys}

    @property
    def json(self, show_all: bool = False):
        if show_all is True:
            return self.cjson(self.all)
        else:
            return self.cjson(self.terse)

    # def _print(self):
    #     print(self._all)

    def print(self):
        # \033[32m ,set color
        # \033[0m ,clear color to protect follow print
        if self.state is self.state_True:
            # # Green Dark
            # print(f"\033[32m{self.all}\033[0m")
            # Green Light
            print(f"\033[92m{self.all}\033[0m")
        elif self.state is self.state_False:
            # Red Light
            print(f"\033[91m{self.all}\033[0m")
        elif self.state is self.state_Warning:
            # Yellow Light
            print(f"\033[93m{self.all}\033[0m")
        elif self.state is self.state_Info:
            # Blue Light
            print(f"\033[94m{self.all}\033[0m")
        else:
            print(f"{self.all} ")

    def add_log(self):
        self.file.add_log(self.all)
        if self.__is_debug:
            self.print()
        else:
            pass
