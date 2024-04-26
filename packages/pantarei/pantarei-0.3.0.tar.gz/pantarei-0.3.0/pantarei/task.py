"""
Task
"""
import os
import time
from .helpers import actual_kwargs, all_actual_kwargs, rmd, rmf, tag_function
from .cache import default_cache


class Task:

    """Cached execution of function"""

    def __init__(self, func, cache=None, done=None, clear=None, ignore=None,
                 artifacts=None, tag="", clear_first=False):
        """
        :param func: function to be executed and/or cached
        :param cache: cache instance to use (default: use a default cache)
        :param done: optional function to tell whether task is done
        :param clear: optional function to execute to clear the task
        :param ignore: 
        :param artifacts: sequence of paths of task artifacts
        :param tag: string description of the task
        :param clear_first: clear task cache and artifacts before execution
        """
        # We assume that done and cache receive only the kwargs of the function
        # If we assume the kwargs are the full signature, then the function is not
        # needed anymore and this simplifies the interface. Check if we may need it.
        self.func = func
        self.cache = cache
        self._done = done
        self._clear = clear
        self.ignore = ignore
        self.artifacts = artifacts
        self.__name__ = func.__name__
        self.tag = tag
        if self.cache is None:
            self.cache = default_cache
        self.clear_first = clear_first

    def __call__(self, *args, **kwargs):
        all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        kwargs = actual_kwargs(self.func, *args, **kwargs)
        name = self.qualified_name(**kwargs)

        # Clear cache before calling function if requested
        if self.clear_first:
            self.clear(*args, **kwargs)

        # Store all argments as metadata, even default ones
        self.cache.setup(name, **all_kwargs)
        if self.done(**kwargs):
            # Task found in cache
            results = self.cache.read(name)
        else:
            # Execute task
            # The logging is identical to job, the latter may be avoided?
            hostname = 'unknown'
            if 'HOSTNAME' in os.environ:
                hostname = os.environ['HOSTNAME']
            path = os.path.join(self.cache.path, name)
            fh = open(os.path.join(path, 'task.yaml'), 'a')
            print('task_node:', hostname, file=fh, flush=True)
            print('task_start:', time.time(), file=fh, flush=True)
            try:
                results = self.func(**kwargs)
                print('task_end:', time.time(), file=fh, flush=True)
            finally:
                fh.close()
            self.cache.write(name, results)
        # Check whether task returned an artifacts entry and if so, store it
        try:
            self.artifacts = results['artifacts']
        except:
            pass
        return results

    def qualified_name(self, **kwargs):
        """Unique name of task"""
        from hashlib import md5
        if self.ignore is None:
            selected_kwargs = kwargs
        else:
            selected_kwargs = {}
            for key in kwargs:
                if key not in self.ignore:
                    selected_kwargs[key] = kwargs[key]

        # Sort dict keys else the fqn is not permutation invariant
        # TODO: how to deal with rounding of floats? One option is to use
        # numpy.format_float_scientific() but it only works with scalars
        selected_kwargs = {key: selected_kwargs[key] for key in sorted(selected_kwargs)}
        hash_args = md5(str(selected_kwargs).encode()).hexdigest()
        func_name = self.func.__name__
        if len(self.tag) > 0:
            return f'{func_name}-{self.tag}/{hash_args}'
        else:
            return f'{func_name}/{hash_args}'

    def name(self):
        """Name of task"""
        return self.__name__

    def clear(self, *args, **kwargs):
        """Remove task data from cache and its artifacts"""
        if len(args) == len(kwargs) == 0:
            self.clear_all()
            return
        all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        kwargs = actual_kwargs(self.func, *args, **kwargs)
        name = self.qualified_name(**kwargs)
        self.cache.clear(name)
        # Clear task artifacts
        if self.artifacts is not None:
            # Assume it is a single folder
            # artifact_path = all_kwargs[self.artifacts]
            # artifact_path = artifact_path.format(**all_kwargs)
            if os.path.exists(self.artifacts):
                rmf(self.artifacts)
                rmd(self.artifacts)
            else:
                for path in self.artifacts:
                    rmf(path)
                    rmd(path)

        # Additional clear function
        if self._clear is not None:
            self._clear(**all_kwargs)

    def clear_all(self, warn=True):
        """Clear all data in cache for this task"""
        import time
        func_name = self.func.__name__
        path = func_name
        if len(self.tag) > 0:
            path = f'{func_name}-{self.tag}'
        path = os.path.join(self.cache.path, path)
        if warn:
            print(f'WARNING: deleting data in cache for {path} in 5 sec...')
            time.sleep(5)
        rmd(path)
        # TODO: clear artifacts too (requires a database)

    def done(self, *args, **kwargs):
        """
        Return True is task has been already execution with given position
        and keyword arguments
        """
        all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)
        kwargs = actual_kwargs(self.func, *args, **kwargs)
        name = self.qualified_name(**kwargs)
        if self.clear_first:
            # In this case, we will always call the function again
            return False

        if self._done is None:
            return self.cache.found(name)
        else:
            return self._done(**all_kwargs) and self.cache.found(name)
