#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import time
import sys
if sys.version_info >= (3,):
    import configparser
else:
    import ConfigParser


class BasePlugin:
    '''
    Abstract class for plugins
    '''
    __name__ = ''

    def __init__(self, moniza_cache=[]):
        if isinstance(moniza_cache, list):
            self.moniza_cache = moniza_cache
        else:
            raise TypeError('Type of moniza_cache have to be list')

        # if not self.__name__:
        #     self.__name__ = os.path.splitext(os.path.basename(__file__))[0]

    def run(self, config=None):
        '''
        Virtual method for running the plugin
        '''
        pass

    def execute(self):
        '''
        Execution wrapper for the plugin
        argv[1]: ini_file
        '''
        config = None
        if len(sys.argv) > 1:
            if sys.version_info >= (3,):
                config = configparser.RawConfigParser(defaults)
            else:
                config = ConfigParser.RawConfigParser(defaults)
            config.read(sys.argv[1])
        pickle.dump(self.run(config), sys.stdout.buffer)

    def get_moniza_cache(self):
        '''
        Return moniza cached value for this specific plugin.
        '''
        try:
            return self.moniza_cache[0]
        except Exception:
            return {}

    def set_moniza_cache(self, cache):
        '''
        Set moniza cache value previously passed to this plugin instance.
        To enable caching existing moniza_cache list have to be passed
        to Plugin on initialization.
        Minimally it should be list().
        moniza will be able to see only changes in zero element of moniza_cache, so
        do not manually override self.moniza_cache, othervice cache will not be saved!

        If self.moniza_cache is not a list appropriate exception will be raised.
        '''
        try:
            self.moniza_cache[0] = cache
        except IndexError:
            self.moniza_cache.append(cache)

    def absolute_to_per_second(self, key, val, prev_cache):
        try:
            if val >= prev_cache[key]:
                value = \
                    (val - prev_cache[key]) / \
                    (time.time() - prev_cache['ts'])
            else:  # previous cached value should not be higher than current value (service was restarted?)
                value = val / \
                    (time.time() - prev_cache['ts'])
        except Exception:  # No cache yet, can't calculate
            value = 0
        return value
