# -*- coding:utf-8 -*-
import os
import subprocess
import sys
import signal

__all__  = ["mkdirs", "check_file", "run_cmd"]

class TimeoutExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutExpired

def mkdirs(file_path):
    """
    判断文件路径所在的目录是否存在，如果不存在则创建目录
    :param file_path: 文件路径
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_file(path):
    """
    This function checks if a file path exists and returns the type of the path.

    :param path: The path to the file.
    :type path: str
    :return: A string indicating the type of path. Possible values are 'File', 'Directory', or ''.
    :rtype: str
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            return "File"
        elif os.path.isdir(path):
            return "Directory"
    else:
        return "NotExists"

def run_cmd(
        cmd,
        deamon=False,
        timeout=None,
        return_list=True,
        encoding="utf-8"):
    """
    执行系统命令, 并获取返回值

    :param cmd: str, 要执行的命令
    :param deamon: bool, 是否以守护进程的方式运行命令
    :param timeout: float, 命令执行的最长时间
    :param return_list: bool, 是否返回list类型的结果
    :param encoding: str, 命令执行结果的编码方式，默认为utf-8
    :return: list/str/Popen, 返回命令执行结果，如果deamon=True，则返回Popen对象
    """
    if sys.version_info.major == 2:
        subp = subprocess.Popen(['/bin/sh', '-c', cmd],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    else:
        subp = subprocess.Popen(['/bin/sh', '-c', cmd],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding=encoding)
    if deamon:
        return subp
    out = communicate(subp, timeout)
    if return_list:
        return out[0].split("\n")
    # out format: (stdout_data, stderr_data)
    return out


def communicate(subp, timeout=None):
    if sys.version_info[0] >= 3:
        expired = False
        try:
            return subp.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
        if expired:
            raise TimeoutExpired("Command timed out after {} seconds".format(timeout))

    # Set up a SIGALRM handler to raise an exception after the specified timeout
    if timeout is not None:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)
    try:
        # Write the input data to stdin and read the output from stdout and stderr
        out, err = subp.communicate()
    except TimeoutExpired:
        # If the timeout was reached, kill the child process and raise a TimeoutError
        subp.kill()
        raise TimeoutExpired("Command timed out after {} seconds".format(timeout))
    finally:
        # Reset the SIGALRM handler to its default behavior
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    # Return the output and error as strings
    return out.decode(), err.decode()
