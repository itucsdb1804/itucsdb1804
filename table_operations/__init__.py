import os

all_pys = list(filter(lambda x: (x[-3:] == ".py" and x != "__init__.py" and x != "baseClass.py"), os.listdir(os.path.dirname(os.path.realpath(__file__)))))

__all__ = list(map(lambda y: y[:-3], all_pys))
