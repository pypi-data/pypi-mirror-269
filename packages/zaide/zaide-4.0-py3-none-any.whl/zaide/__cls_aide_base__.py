import datetime
import time
import sys
import os
import socket

import json

import inspect


class _cls_frame_func:
    @staticmethod
    def get_current_function_name():
        frame = inspect.currentframe()
        func_name = frame.f_back.f_code.co_name
        return func_name

    @staticmethod
    def is_directly_called(func):
        current_frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(current_frame)
        for frame in outer_frames:
            if frame[3] != func.__name__:
                return False
        return True


class _cls_process_bars:
    @staticmethod
    def count_down(title: str = "Waiting for next check",
                                    time_sec: int = 10,
                                    progress_symbol: str = "▋",
                                    count_only: bool = True,
                                    end: str = "\n"):

        start = time.perf_counter()

        if count_only:
            title = ""
            progress_symbol = None
        else:
            if title is None or title == "":
                title = ""
            else:
                title = title + ":"

            if progress_symbol is None or progress_symbol == "":
                progress_symbol = None
            else:
                pass

        for i in range(1, 101):
            dur = int(time.perf_counter() - start)

            if progress_symbol is None:
                print(f"\r{title}{i:3}% {dur}s ", end="")
            else:
                print(f"\r{title}{i:3}% {progress_symbol * (i // 2):progress_symbol_length}{dur}s ", end="")

            sys.stdout.flush()

            time.sleep(time_sec / 99)

        print("", end=end)


class jsonDate(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class __cls_base__:
    def __init__(self):
        pass

    @staticmethod
    def Cbool(value, set_non_ture_as_false: bool = True):
        if value is None:
            output = None
        elif isinstance(value, bool):
            output = value
        elif isinstance(value, int):
            if value == 1:
                output = True
            elif value == 0:
                output = False
            else:
                output = None
        elif isinstance(value, str):
            if value.strip().upper() in ["1", "YES", "ON", "TRUE"]:
                output = True
            elif value.strip().upper() in ["0", "NO", "OFF", "FALSE"]:
                output = False
            else:
                output = None
        else:
            output = None

        if output is None:
            if set_non_ture_as_false is True:
                return False
            else:
                return output
        else:
            return output

    @property
    def slash(self):
        if os.name == 'nt':
            return '\\'
        else:
            return '/'

    class cls_dict:
        def __init__(self):
            self.__my_dict = {}

        def add(self, new_key, new_value=None):
            self.__my_dict[new_key] = new_value

        def get(self, my_key):
            return self.__my_dict[my_key]

    @staticmethod
    def unix_timestamp_to_time_str(target_unix_timestamp: int):
        time0 = time.localtime(target_unix_timestamp)
        time0 = time.strftime("%Y-%m-%d %H:%M:%S", time0)

        return time0

    @staticmethod
    def hostname():
        return socket.gethostname()

    @property
    def ip(self):
        return socket.gethostbyname(self.hostname())

    @staticmethod
    def CrLf():
        return "\r\n"

    @staticmethod
    def cjson(data):
        return json.dumps(data, ensure_ascii=False, cls=jsonDate)

    @staticmethod
    def none_to_blank(value):
        if value is None:
            return ''
        else:
            return value

    @staticmethod
    def str_to_json(data):
        return json.loads(data)

    @staticmethod
    def dict_to_str(my_dict: dict,
                    split_key: str = "",
                    next_row_key: str = "\r\n",
                    pass_none: bool = False,
                    list_pass_name: list = None):
        s = None
        for key in my_dict:
            if list_pass_name is None or key not in list_pass_name:
                if s is None:
                    s = key + split_key + str(my_dict[key])
                else:
                    value = my_dict[key]

                    if value is None and pass_none is True:
                        pass
                    else:
                        if value is None:
                            value = ''
                        else:
                            value = str(value)

                        s = s + next_row_key + key + split_key + value
            else:
                pass
        return s

    @staticmethod
    def list_to_str(my_list, split_key: str = "", next_row_key: str = "\r\n", show_index_id: bool = True):
        s = None
        for i in my_list:

            if i is None:
                i = ''
            else:
                i = str(i)

            if s is None:
                if show_index_id is True:
                    s = str(i.index) + split_key + i
                else:
                    s = i

            else:
                if show_index_id is True:
                    s = s + str(i.index) + split_key + i
                else:
                    s = s + next_row_key + i
        return s

    @staticmethod
    def append(s, key, new_s):
        # print(s,new_s)
        # str_append = ""
        if s is None or s == "":
            if new_s is None or new_s == "":
                str_append = ""
            else:
                str_append = new_s
        else:
            if new_s is None or new_s == "":
                str_append = s
            else:
                str_append = str(s) + key + str(new_s)
        # print(str_append)
        if str_append is None:
            str_append = ""
        else:
            pass

        return str_append

    @staticmethod
    def is_ip(value):
        if not isinstance(value, str):
            return False
        else:
            pass

        if len(value) < 7 or len(value) > 15:
            # print(1)
            return False
        else:
            pass

        list_value = value.split(".")

        if len(list_value) != 4:
            # print(2)
            return False
        else:
            pass

        for s in list_value:
            if not s.isalnum():
                # print(3)
                return False
            else:
                if int(s) > 255 or int(s) < 0:
                    # print(4)
                    return False
                else:
                    pass

        if list_value[3] == '0':
            return False
        else:
            pass

        return True

    def find_ip(self, value: str, split_key: str = " "):
        ip = None
        if value is None:
            return None
        else:
            arr = value.split(split_key)

            for s in arr:
                if self.is_ip(s):
                    ip = s
                    return ip
                else:
                    pass

            return ip

    @staticmethod
    def first(my_value: str, my_split_key: str = ","):
        arr = str(my_value).split(my_split_key)
        return arr[0]

    def rcut(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):
        # print(start_key,start_correction)
        start_index = self.rfindx(str0, start_key, start_count) + start_correction

        end_index = self.rfindx(str0, end_key, end_count) + end_correction

        # print(start_index, end_index)

        str_cut = str0[start_index:end_index]

        return str_cut

    @staticmethod
    def rfindx(str_source: str, str_key: str, count: int = 1):
        if str_key is None:
            return len(str_source)
        else:
            count0 = 1
            index = str_source.rfind(str_key)
            if index != -1:

                while count0 < count:
                    index = str_source[:index].rfind(str_key)
                    count0 = count0 + 1
                    # print(index, count0, count)
                    if index == -1:
                        return index
                    else:
                        pass

                return index
            else:
                return index

    @staticmethod
    def __cut_from_the_x_key_to_the_rest_first_key(str0: str,
                                                   start_key: str, start_key_order: int,
                                                   end_key: str,
                                                   include_start_key: bool = False, include_end_key: bool = False):
        if start_key == '':
            start_index = 0
        else:
            if start_key_order == 1:
                start_index = str0.find(start_key)
            elif start_key_order == -1:
                start_index = str0.rfind(start_key)
            else:
                start_index = str0.rfind(start_key)

        if include_start_key is False:
            start_index = start_index + len(start_key)
        else:
            pass

        str0 = str0[start_index:]

        end_index = str0.find(end_key)

        if include_end_key is False:
            pass
        else:
            end_index = end_index + len(end_key)

        str0 = str0[:end_index]

        return str0

    def cut_from_the_first_key_to_the_rest_first_key(self, str0: str,
                                                     start_key: str, end_key: str,
                                                     include_start_key: bool = False, include_end_key: bool = False):
        return self.__cut_from_the_x_key_to_the_rest_first_key(str0=str0,
                                                               start_key=start_key,
                                                               start_key_order=1,
                                                               end_key=end_key,
                                                               include_start_key=include_start_key,
                                                               include_end_key=include_end_key)

    def cut_from_the_last_key_to_the_rest_first_key(self, str0: str,
                                                    start_key: str, end_key: str,
                                                    include_start_key: bool = False, include_end_key: bool = False):
        return self.__cut_from_the_x_key_to_the_rest_first_key(str0=str0,
                                                               start_key=start_key,
                                                               start_key_order=-1,
                                                               end_key=end_key,
                                                               include_start_key=include_start_key,
                                                               include_end_key=include_end_key)

    def cut(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):
        start_index = self.findx(str0, start_key, start_count) + start_correction

        end_index = self.findx(str0, end_key, end_count) + end_correction

        # print('start_key=', start_key)
        # print('start_index=', start_index,'end_index=', end_index)

        # print("se:", start_index, end_index)

        str_cut = str0[start_index:end_index]

        return str_cut

    def cut2(self, str0: str, start_key, start_count, start_correction, end_key, end_count, end_correction):
        start_index = self.findx(str0, start_key, start_count) + start_correction

        str1 = str0[start_index + len(start_key):]

        if end_count == 0:
            end_index = len(str1)
        elif end_count < 0:
            end_index = self.rfindx(str1, end_key, 0 - end_count) + end_correction
        else:
            end_index = self.findx(str1, end_key, end_count) + end_correction
        # print("se:", start_index, end_index)

        str_cut = str1[:end_index]

        # print('start_key=', start_key)
        # print('start_index=', start_index, 'end_index=', end_index)
        # print('str1=', str1)
        # print('str_cut=', str_cut)
        return str_cut

    @staticmethod
    def findx(str0: str, str1: str, count: int = 1):
        count0 = 1

        index = str0.find(str1)

        index_rst = index

        if index != -1:
            while count0 < count:
                # print(count0, "-", index_rst)

                index = str0[index_rst + len(str1):].find(str1)

                # print(count0, "--", index)

                if index == -1:
                    return index_rst
                else:
                    index_rst = index_rst + len(str1) + index

                    # print(count0, "---", index_rst)

                count0 = count0 + 1
            return index_rst
        else:
            return index_rst

    @property
    def no_such_key(self):
        return 'NoSuchKey'

    @staticmethod
    def get_dict_value(my_dict: dict, key: str, miss_key_default: str = "@#$"):
        if my_dict.__contains__(key):
            value = my_dict[key]
        else:
            if miss_key_default == "@#$":
                value = None
            else:
                value = miss_key_default
        return value
