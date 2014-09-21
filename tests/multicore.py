
import sys
import radical.pilot as rp

#------------------------------------------------------------------------------
#
def pilot_state_cb (pilot, state) :
    """ this callback is invoked on all pilot state changes """

    print "[Callback]: ComputePilot '%s' state: %s." % (pilot.uid, state)

    if  state == rp.FAILED :
        sys.exit (1)


#------------------------------------------------------------------------------
#
def unit_state_change_cb (unit, state) :
    """ this callback is invoked on all unit state changes """

    print "[Callback]: ComputeUnit  '%s' state: %s." % (unit.uid, state)

    if  state == rp.FAILED :
        sys.exit (1)


#------------------------------------------------------------------------------
#
if __name__ == "__main__":

    session = rp.Session()

    # Create a new session. A session is the 'root' object for all other
    # RADICAL-Pilot objects. It encapsualtes the MongoDB connection(s) as
    # well as security crendetials.

    # Add an ssh identity to the session.
    c = rp.Context('ssh')
    session.add_context(c)

    # Add a Pilot Manager. Pilot managers manage one or more ComputePilots.
    pmgr = rp.PilotManager(session=session)

    # Register our callback with the PilotManager. This callback will get
    # called every time any of the pilots managed by the PilotManager
    # change their state.
    pmgr.register_callback(pilot_state_cb)

    # Define a pilot on stampede of in total 32 cores that spans two nodes,
    # runs for 15 mintutes and uses $HOME/radical.pilot.sandbox as sandbox directory.
    pdesc = rp.ComputePilotDescription()
    pdesc.resource  = "india.futuregrid.org"
    pdesc.runtime   = 15 # minutes
    pdesc.cores     = 32 

    # Launch the pilot.
    pilot = pmgr.submit_pilots(pdesc)

    # Number of cores for respective task
    #task_cores = [1 for _ in range(32)]
    task_cores = [3 for _ in range(32)]
    #task_cores = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    # Seconds of sleep for respective task
    task_sleep = [30 for _ in range(32)]

    compute_unit_descriptions = []
    for unit_no in range(32):
        cud = rp.ComputeUnitDescription()
        cud.executable  =  "/bin/sh"
        cud.arguments   = ["-c", "/bin/sleep %d && /bin/date > unit-%s.dat" % (task_sleep[unit_no], unit_no)]
        cud.cores       = task_cores[unit_no]

        compute_unit_descriptions.append(cud)

    # Combine the ComputePilot, the ComputeUnits and a scheduler via
    # a UnitManager object.
    umgr = rp.UnitManager(
        session=session,
        scheduler=rp.SCHED_DIRECT_SUBMISSION)

    # Register our callback with the UnitManager. This callback will get
    # called every time any of the units managed by the UnitManager
    # change their state.
    umgr.register_callback(unit_state_change_cb)

    # Add the previously created ComputePilot to the UnitManager.
    umgr.add_pilots(pilot)

    # Submit the previously created ComputeUnit descriptions to the
    # PilotManager. This will trigger the selected scheduler to start
    # assigning ComputeUnits to the ComputePilots.
    units = umgr.submit_units(compute_unit_descriptions)

    # Wait for all compute units to reach a terminal state (DONE or FAILED).
    umgr.wait_units()

    for unit in units:
        print "* Task %s (executed @ %s) state: %s, exit code: %s, started: %s, finished: %s, output: %s" \
            % (unit.uid, unit.execution_locations, unit.state, unit.exit_code, unit.start_time, unit.stop_time,
               unit.stdout)

    # always clean up the session
    session.close()

# ------------------------------------------------------------------------------
