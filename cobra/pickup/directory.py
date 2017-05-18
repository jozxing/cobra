# -*- coding: utf-8 -*-

"""
    pickup.directory
    ~~~~~~~~~~~~~~~~

    Implements various directory

    :author:    Feei <feei@feei.cn>
    :homepage:  https://github.com/wufeifei/cobra
    :license:   MIT, see LICENSE for more details.
    :copyright: Copyright (c) 2017 Feei. All rights reserved
"""
import time
import os
from cobra.utils.log import logger


class Directory(object):
    def __init__(self, path):
        self.path = path

    file_id = 0
    type_nums = {}
    result = {}
    file = []

    def files(self, directory, level=1):
        if level == 1:
            logger.debug(directory)
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)

            # Directory Structure
            # logger.debug('|  ' * (level - 1) + '|--' + filename)
            if os.path.isdir(path):
                self.files(path, level + 1)
            if os.path.isfile(path):
                # Statistic File Type Count
                file_name, file_extension = os.path.splitext(path)
                self.type_nums.setdefault(file_extension.lower(), []).append(filename)

                path = path.replace(self.path, '')
                self.file.append(path)
                self.file_id += 1
                logger.debug("{0}, {1}".format(self.file_id, path))

    """
    :return {'file_nums': 50, 'collect_time': 2, '.php': {'count': 2, 'list': ['/path/a.php', '/path/b.php']}}
    """

    def collect_files(self):
        t1 = time.clock()
        self.files(self.path)
        self.result['no_extension'] = {'count': 0, 'list': []}
        for extension, values in self.type_nums.items():
            extension = extension.strip()
            self.result[extension] = {'count': len(values), 'list': []}
            # .php : 123
            logger.debug('{0} : {1}'.format(extension, len(values)))
            for f in self.file:
                es = f.split(os.extsep)
                if len(es) >= 2:
                    # Exists Extension
                    # os.extsep + es[len(es) - 1]
                    if f.endswith(extension):
                        self.result[extension]['list'].append(f)
                else:
                    # Didn't have extension
                    self.result['no_extension']['count'] = int(self.result['no_extension']['count']) + 1
                    self.result['no_extension']['list'].append(f)
        t2 = time.clock()
        return self.result, self.file_id, t2 - t1
