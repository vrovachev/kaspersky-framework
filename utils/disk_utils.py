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

if float(sys.version[:2]) >= 3:
    from functools import reduce


def check_free_space(func):
    def _check(self, *args, **kwargs):
        if self.all_free_disk_space_gb() < self.WRITE_MB/1024:
            raise AssertionError(
                "Need more {}MB free disk space. Free {}MB".format(
                    self.WRITE_MB, self.all_free_disk_space_gb()*1024))
        return func(self, *args, **kwargs)
    return _check


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
    def write_get(io_file, block_size, blocks_count, show_progress=True):
        """
        Tests write speed by writing random blocks, at total quantity
        of blocks_count, each at size of block_size bytes to disk.
        Function returns a list of write times in sec of each block.
        """
        f = os.open(io_file, os.O_CREAT | os.O_WRONLY, 0o777)
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
        os.close(f)
        return took

    @staticmethod
    def read_get(io_file, block_size, blocks_count, write_block_kb,
                 read_block_b, show_progress=True):
        """
        Performs read speed test by reading random offset blocks from
        file, at maximum of blocks_count, each at size of block_size
        bytes until the End Of File reached.
        Returns a list of read times in sec of each block.
        """
        f = os.open(io_file, os.O_RDONLY, 0o777)
        # generate random read positions
        offsets = list(range(0, blocks_count * block_size, block_size))
        shuffle(offsets)

        took = []
        for i, offset in enumerate(offsets, 1):
            if show_progress and i % int(
                                    write_block_kb*1024/read_block_b) == 0:
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
        os.close(f)
        return took

    @check_free_space
    def io_calculate(self):
        wr_blocks = int(self.WRITE_MB * 1024 / self.WRITE_BLOCK_KB)
        rd_blocks = int(self.WRITE_MB * 1024 * 1024 / self.READ_BLOCK_B)

        write_results = self.write_get(self.FILE, 1024 * self.WRITE_BLOCK_KB,
                                       wr_blocks)
        read_results = self.read_get(self.FILE, self.READ_BLOCK_B, rd_blocks,
                                     self.WRITE_BLOCK_KB, self.READ_BLOCK_B)
        os.remove(self.FILE)

        res = [(self.WRITE_MB / sum(write_results)),
               (self.WRITE_MB / sum(read_results))]
        print('\n\nWritten {} MB in {:.4f} s\nWrite speed is  {:.2f} MB/s\n  '
              'max: {max:.2f}, min: {min:.2f}\n'.format(
                  self.WRITE_MB, sum(write_results), res[0],
                  max=self.WRITE_BLOCK_KB / (1024 * min(write_results)),
                  min=self.WRITE_BLOCK_KB / (1024 * max(write_results))))
        print('\nRead {} x {} B blocks in {:.4f} s\nRead speed is  {:.2f} '
              'MB/s\n  max: {max:.2f}, min: {min:.2f}\n'.format(
                  len(read_results), self.READ_BLOCK_B, sum(read_results),
                  res[1],
                  max=self.READ_BLOCK_B / (1024 * 1024 * min(read_results)),
                  min=self.READ_BLOCK_B / (1024 * 1024 * max(read_results))))
        return res

    def all_free_disk_space_gb(self):
        return reduce(lambda res, x: res+x[1]/1024, self.disks, 0)
