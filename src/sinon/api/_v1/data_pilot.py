

import pilot       as p
import sinon._api  as sa


# ------------------------------------------------------------------------------
#
class DataPilot (p.Pilot, sa.Pilot) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid) : 

        p.Pilot.__init__ (self, pid)


# ------------------------------------------------------------------------------
#

