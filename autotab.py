# stdlib
import inspect
import numpy as np
from IPython.extensions.completion import _init_completers
import IPython.core.interactiveshell
from numpydoc import docscrape

__all__ = ['install']

def install(*modules):
    """Install the numpydoc IPython tab completion extension.

    Parameters
    ----------
    *modules : list of modules
        These should be a list of modules that form the namespace in which the
        types in the docstrings can be evaluated. For instance, if your docstrings
        say that something is of type ndarray, you need to pass in the numpy
        module so that we can resolve the string 'ndarray' into np.ndarray
    """
    ipython = IPython.core.interactiveshell.InteractiveShell.instance()
    current = ipython.Completer.TAB_COMPLETION_REGISTRY
    replacement = NumpyDocTabCompleteRegistry()

    if isinstance(current, dict):
        for key, value in current.iteritems():
            replacement[key] = value

    for module in modules:
        replacement.namespace = module.__dict__

    ipython.Completer.TAB_COMPLETION_REGISTRY = replacement


class NumpyDocTabCompleteRegistry(object):
    """
    Dict-like replacement for IPython.core.IPCompleter.TAB_COMPLETION_REGISTRY
    that checks a function's docstring to try to extract tab completion info
    """
    def __init__(self):
        self._attempted_functions = set([])
        self._tab_completions = {}
        self.namespace = {}

    def __setitem__(self, key, value):
        #print 'calling setitem'
        self._tab_completions[key] = value

    def __getitem__(self, key):
        #print 'Calling getitem with key=%s' % key

        if key in self._tab_completions:
            return self._tab_completions[key]
        if key in self._attempted_functions:
            raise KeyError('Sorry boss, no dice.')
        # add to the attempted registry before we do anything else
        self._attempted_functions.add(key)

        doc = inspect.getdoc(key)
        if doc is None:
            # mark our attempt as unsucessfull
            raise KeyError('Sorry boss, no dice. (2)')

        # parse the parameters portion of the docstring
        annotations = {}
        parsed = docscrape.NumpyDocString(doc)
        for param_doc in parsed['Parameters']:
            name = param_doc[0]
            type_name = param_doc[1]
            # if there's a comma, the first element is the type name while
            # the second is a qualifier like "optional"
            if ',' in type_name:
                type_name = type_name.split(',')[0]

            try:
                type = eval(type_name, self.namespace)
            except Exception as e:
                #print 'e1', e
                continue

            if inspect.isclass(type):
                annotations[name] = type
            else:
                pass

        # parse the return value of the docstring
        returns = parsed['Returns']
        if len(returns) == 1:
            type_name = returns[0][1]
            # i can only currently handle single return values
            if ',' not in type_name:
                try:
                    type = eval(type_name, self.namespace)
                    annotations['return'] = type
                except Exception as e:
                    #print 'e2', e
                    pass

        if len(annotations) > 0:
            try:
                # this calls __setitem__ behind the scenes
                _init_completers(key, annotations)
            except ValueError as e:
                pass

        # the return could have been stored in one of two places
        if hasattr(key, '_tab_completions'):
            return key._tab_completions
        return self._tab_completions[key]
