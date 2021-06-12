class StateMachine:
    """
    Generic State Machine
    """

    def __init__(self):
        self.registered_states = {}
        self.current_time = None
        self.current_state = None
        self.state_name = None
        self.registered_data = {}
        pass

    def setup_state_machine(self, current_time, registered_states, start_state_name):
        self.registered_states = registered_states
        self.current_time = current_time
        self.change_state(start_state_name)

    def register_data(self, key, value):
        self.registered_data[key] = value

    def get_data(self, key):
        if key in self.registered_data:
            return self.registered_data[key]

        return None

    def change_state(self, next_state_name):
        previous = self.state_name
        self.state_name = next_state_name
        persist = {} if self.current_state is None else self.current_state.exit()
        self.current_state = self.registered_states[self.state_name]
        self.current_state.previous = previous
        self.current_state.enter(persisted_data=persist, current_time=self.current_time)
        pass

    def handle_events(self, events):
        """
        Feed events to current state
        :param events:
        :return:
        """
        self.current_state.handle_events(events)

    def update(self, current_time):
        self.current_time = current_time
        self.current_state.update(self.current_time)
        pass

    def get_surfaces(self):
        self.current_state.get_surfaces()


class AbstractState:
    """
    Base State for all Concrete States to Inherit from.
    HandleEvents, Enter, Exit and Update should be overloaded.
    """

    def __init__(self, state_machine):
        self.data_to_persist = {}
        self.state_machine = state_machine
        self.previous = None
        self.surfaces = []
        pass

    def handle_events(self, events):
        """
        Handle Events passed in from the main game loop
        :param events:
        :return:
        """
        pass

    def enter(self, persisted_data, current_time):
        self.data_to_persist = persisted_data
        self.current_time = current_time
        pass

    def exit(self):
        """
        Handle exit logic and return any data that should persist to the next state
        :return:
        """
        return self.data_to_persist

    def get_surfaces(self):
        return self.surfaces

    def update(self, current_time):
        pass
