

import os

__all__ = ["blueprints"]
blueprints = []

for fname in os.listdir(os.path.dirname(__file__)):
    if fname.endswith(".py") and not fname.startswith("__init__"):
        view = __import__("distributed.views.%s" % fname.rstrip(".py"),
                          globals(), locals(), ["blueprint", "routes"], -1)
        blueprints.append((view.blueprint, view.routes))
