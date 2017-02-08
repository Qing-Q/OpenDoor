# -*- coding: utf-8 -*-

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Development Team: Stanislav WEB
"""

import os
import fcntl
import termios
import platform
import shlex
import struct
import subprocess


class Terminal(object):
    """ Terminal class"""
    
    def get_ts(self):
        """
        Get width and height of console
        :return: tuple
        """
    
        current_os = platform.system()
        tuple_xy = None
        if current_os == 'Windows':
            tuple_xy = self.__get_ts_windows()
            if tuple_xy is None:
                tuple_xy = self.__get_ts_tput()
        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = self.__get_ts_unix()
        if tuple_xy is None:
            tuple_xy = (80, 25)  # default value
        return tuple_xy
    
    @staticmethod
    def __get_ts_windows():
        """
        Get windows terminal size
        :return: tuple
        """
    
        try:
            from ctypes import windll, create_string_buffer
    
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except Exception:
            pass

    @staticmethod
    def __get_ts_unix():
        """
        Get unix terminal size
        :return tuple
        """
    
        def ioctl_GWINSZ(fd):
            """
            Get  win soize
            :param callback fd:
            :return: tuple
            """
        
            try:

                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr
            except:
                pass
    
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                return None
        return int(cr[1]), int(cr[0])
    
    @staticmethod
    def __get_ts_tput():
        """
        Get terminal height / width
        :return: tuple
        """
    
        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except subprocess.CalledProcessError:
            pass
