#
#                                                                            */
#                               utils.py                                     */
#                                                                            */
#                             Espaces Project                                */
#                                                                            */
# -------------------------------------------------------------------------- */


# All units in International System of Units (SI)

import os
import sys

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def open_osx(*args):
    """ """
    if sys.platform=='darwin':
        for arg in args:
            os.system("open %s" % arg)
    else:
        raise StandardError("open_osx only implemente for mac osx")
