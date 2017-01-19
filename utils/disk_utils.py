# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT

import os
import psutil
import sys

from random import shuffle

if float(sys.version[:3]) >= 3.3:
    from time import perf_counter as time
else:
    from time import time


class DiskIO(object):

    def __init__(self):
        self.WRITE_MB = 128
        self.WRITE_BLOCK_KB = 1024
        self.READ_BLOCK_B = 512
        self.FILE = r'/tmp/disk_test'
        self.disks = [(i.mountpoint,
                       float(psutil.disk_usage(
                           i.mountpoint).free)/1024/1024)
                      for i in psutil.disk_partitions()]

    @staticmethod
    def write_test(file, block_size, blocks_count, show_progress=True):
        """
        Tests write speed by writing random blocks, at total quantity
        of blocks_count, each at size of block_size bytes to disk.
        Function returns a list of write times in sec of each block.
        """
        with os.open(file, os.O_CREAT | os.O_WRONLY, 0o777) as f:
            took = []
            for i in range(blocks_count):
                if show_progress:
                    # dirty trick to actually print progress on each iteration
                    sys.stdout.write('\rWriting: {:.2f} %'.format(
                        (i + 1) * 100 / blocks_count))
                    sys.stdout.flush()
                buff = os.urandom(block_size)
                start = time()
                os.write(f, buff)
                os.fsync(f)  # force write to disk
                t = time() - start
                took.append(t)
        return took

    @staticmethod
    def read_test(file, block_size, blocks_count, WRITE_BLOCK_KB,
                  READ_BLOCK_B, show_progress=True):
        """
        Performs read speed test by reading random offset blocks from
        file, at maximum of blocks_count, each at size of block_size
        bytes until the End Of File reached.
        Returns a list of read times in sec of each block.
        """
        with os.open(file, os.O_RDONLY, 0o777) as f:
            # generate random read positions
            offsets = list(range(0, blocks_count * block_size, block_size))
            shuffle(offsets)

            took = []
            for i, offset in enumerate(offsets, 1):
                if show_progress and i % int(
                                        WRITE_BLOCK_KB*1024/READ_BLOCK_B) == 0:
                    # read is faster than write,
                    # so try to equalize print period
                    sys.stdout.write('\rReading: {:.2f} %'.format(
                        (i + 1) * 100 / blocks_count))
                    sys.stdout.flush()
                start = time()
                os.lseek(f, offset, os.SEEK_SET)  # set position
                buff = os.read(f, block_size)  # read from position
                t = time() - start
                if not buff:
                    break  # if EOF reached
                took.append(t)
        return took
