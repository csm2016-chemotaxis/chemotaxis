import numpy as np
from util import Error

class Model:
    # A reference to the singleton object
    __instance = None

    def __init__(self, dt, source_position, source_strength, source_decay_rate):
        """Model ctor, not meant to be called by the user

        By convention, always call get_instance() when you want a valid
        reference to the singleton Model. Never call the constructor
        explicitly.
        """
        self.time = 0
        self.dt = dt
        self.source_position = source_position
        self.source_strength = source_strength
        self.source_decay_rate = source_decay_rate
        self.sim_objs = []
        self.larvae = []
        self.arena = None
        # TODO: add other model objects and params (arena, etc)
        self.views = []
    
    @staticmethod
    def get_instance(dt=0.1, source_position=np.array([0,0]), source_strength=10, source_decay_rate=5):
        if not Model.__instance:
            Model.__instance = Model(dt, source_position, source_strength, source_decay_rate)
        return Model.__instance

    def add_larva(self, l):
        self.larvae.append(l)
        self.sim_objs.append(l)

    def add_arena(self, a):
        self.arena = a
        # Add the arena to the top of the simulation object list, so that it
        # always gets updated first
        self.sim_objs.insert(0, a)

    def get_arena(self):
        if not self.arena:
            raise Error('Must create the Arena!')
        return self.arena

    def update(self):
        """Increment the time and tell all objects to update themselves"""
        for obj in self.sim_objs:
            obj.update()
        self.time += self.dt

    # View Services
    def attach(self, view):
        """Attaching a view to the model

        Attaching a view adds it to the container and causes it to be updated
        with all current Larva state information.
        """
        self.views.append(view)

    # TODO: possibly add a way to detach a view, maybe not necessary. Maybe
    # when you add a view, it is permanent. If you don't want it anymore,
    # just don't draw it.

    def notify_state(self, state, head_loc, joint_loc, velocity, head_angle):
        """Notify the views about Larva state changes
        """
        for v in self.views:
            v.update_view(self.time, state, head_loc, joint_loc, velocity, head_angle, self.source_position)
