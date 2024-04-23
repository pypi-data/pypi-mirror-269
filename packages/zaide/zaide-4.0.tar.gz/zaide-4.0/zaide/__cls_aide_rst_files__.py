import datetime
import os
import json
import configparser

from .__cls_aide_base__ import __cls_base__


class SECTION_cfg:
    # section name
    name: str = "Configuration"

    # section.options
    date: str = "date_utc"
    log_level: str = "log_level"
    debug: str = "debug"


class __cls_aide_rst_files__(__cls_base__):
    # noinspection PyMissingConstructor
    def __init__(self, log_level, rst_dir: str = None):
        self.rst_file_folder = rst_dir

        self.cfg_log_level = 0
        self.cfg_is_debug = None

        self.check_path(check_log_file=False, check_config_file=True)

        self.load_conf(log_level=log_level)

    @property
    def cfg_file_path(self):
        return self.rst_file_folder + self.slash + "conf" + self.slash + "rst.cfg"

    @property
    def log_file_path(self):
        return self.rst_file_folder + self.slash + "log" + self.slash + f"rst_{datetime.date.today()}.log"

    def check_path(self, check_config_file: bool = False, check_log_file: bool = True):
        now_path = os.getcwd()

        arr_now_path = now_path.split(self.slash)

        my_dir = None

        for i in arr_now_path:
            dir_name = i
            if dir_name != 'module' and dir_name != 'run':
                if my_dir is None:
                    my_dir = dir_name
                else:
                    my_dir = my_dir + self.slash + dir_name
            else:
                break

        self.rst_file_folder = my_dir + self.slash + "rst"

        if not os.path.exists(self.rst_file_folder):
            os.mkdir(self.rst_file_folder)
            check_config_file = True
            check_log_file = True
        else:
            pass

        if check_config_file:

            path, file_name = os.path.split(self.cfg_file_path)

            if not os.path.exists(path):
                os.mkdir(path)
            else:
                pass

            if not os.path.exists(self.cfg_file_path):
                config = configparser.ConfigParser()

                # config.read(self.cfg_file_path, encoding="utf-8")

                config.add_section(SECTION_cfg.name)

                config.set(SECTION_cfg.name, SECTION_cfg.date, str(datetime.datetime.utcnow()))
                config.set(SECTION_cfg.name, SECTION_cfg.log_level, "1")
                config.set(SECTION_cfg.name, SECTION_cfg.debug, "0")

                config.write(open(self.cfg_file_path, "w"))

                # f = open(self.cfg_file_path, 'a', encoding='utf-8')
                #
                # f.writelines(f"{self.SETTING_DATE}={datetime.datetime.utcnow()}")
                # f.writelines("\n")
                # f.writelines(f"{self.SETTING_LOG_LEVEL}=1")
                # f.writelines("\n")
                # f.writelines(f"{self.SETTING_DEBUG}=0")
                #
                # f.close()
            else:
                pass

        if check_log_file:
            path, file_name = os.path.split(self.log_file_path)

            if not os.path.exists(path):
                os.mkdir(path)
            else:
                pass
        else:
            pass

    def load_conf(self, log_level):
        # check eviroment and set log_level
        config = configparser.ConfigParser()

        config.read(self.cfg_file_path, encoding="utf-8")

        if log_level not in [0, 1, 2, 3]:
            loaded_log_level = config.get(SECTION_cfg.name, SECTION_cfg.log_level)

            self.cfg_log_level = int(loaded_log_level) if loaded_log_level.isdigit() else loaded_log_level
        else:
            self.cfg_log_level = log_level

        self.cfg_is_debug = self.Cbool(config.get(SECTION_cfg.name, SECTION_cfg.debug))

        # check eviroment and set log_level
        # f = open(self.cfg_file_path, 'r')
        #
        # text = f.read()
        #
        # f.close()
        #
        # if log_level not in [0, 1, 2, 3]:
        #     if text.find(f"{self.SETTING_LOG_LEVEL}=0") >= 0:
        #         self.cfg_log_level = 0
        #     elif text.find(f"{self.SETTING_LOG_LEVEL}=1") >= 0:
        #         self.cfg_log_level = 1
        #     elif text.find(f"{self.SETTING_LOG_LEVEL}=2") >= 0:
        #         self.cfg_log_level = 2
        #     else:
        #         self.cfg_log_level = 3
        # else:
        #     self.cfg_log_level = log_level
        #
        # if text.find(f"{self.SETTING_DEBUG}=1") >= 0:
        #     self.cfg_is_debug = True
        # else:
        #     self.cfg_is_debug = False

    def add_log(self, new_log):
        if self.log_file_path is None:
            self.check_path()
        else:
            pass

        try:
            f = open(self.log_file_path, 'a', encoding='utf-8')
            f.writelines("\n")

            log = {'gmt0': datetime.datetime.utcnow(), 'rst': new_log}

            log = self.cjson(log)

            f.writelines(log)

            f.close()
        except Exception as e:
            # self.set_error(e.__str__())
            print("Log Write Error:" + e.__str__())

    @staticmethod
    def add_log_2(new_msg, log_path):
        f = open(log_path, 'a')
        f.writelines("\n")
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        f.writelines(new_msg)
        f.close()

    @staticmethod
    def find_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        return new_msg in open(log_path, 'rt').read()

    @staticmethod
    def replace_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        return new_msg in open(log_path, 'rt').read()

    @staticmethod
    def find_big_log(new_msg, log_path):
        if isinstance(new_msg, dict):
            new_msg = json.dumps(new_msg, ensure_ascii=False)
        with open(log_path, 'rt') as handle:
            for ln in handle:
                if new_msg in ln:
                    return True
                else:
                    return False
