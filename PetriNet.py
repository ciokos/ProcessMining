from components import Place, Transition, Edge


class PetriNet:

    def __init__(self):
        self.places = []
        self.transitions = []
        self.edges = []
        self.starting_places = []
        self.final_places = []

    def add_place(self, id):
        self.places.append(Place(id))

    def add_transition(self, name, id):
        self.transitions.append(Transition(name, id))

    def add_edge(self, source, target):
        s = self.__get_component(source)
        t = self.__get_component(target)
        self.edges.append(Edge(s, t))
        return self

    def get_tokens(self, place):
        return self.__get_component(place).tokens

    def is_enabled(self, transition):
        for e in self.edges:
            if e.target.id == transition:
                if e.source.tokens < 1:
                    return False
        return True

    def enable(self, transition):
        missing = 0
        for e in self.edges:
            if e.target.id == transition:
                if e.source.tokens < 1:
                    e.source.tokens = 1
                    missing += 1
        return missing

    def add_marking(self, place):
        self.__get_component(place).tokens += 1

    def fire_transition(self, transition):
        consumed = 0
        produced = 0
        for e in self.edges:
            if e.target.id == transition:
                e.source.tokens -= 1
                consumed += 1
            elif e.source.id == transition:
                e.target.tokens += 1
                produced += 1
        return consumed, produced

    def __get_component(self, id):
        if id > 0:
            return next((p for p in self.places if p.id == id), None)
        else:
            return next((t for t in self.transitions if t.id == id), None)

    def transition_name_to_id(self, name):
        for transition in self.transitions:
            if transition.name == name:
                return transition.id

    def reset(self):
        for place in self.places:
            if place.id != 1:
                place.tokens = 0
            else:
                place.tokens = 1

    def get_remaining_tokens(self):
        remaining = 0
        for place in self.places:
            if place.id != 2:
                remaining += place.tokens
        return remaining

    def get_last_token(self):
        for place in self.places:
            if place.id == 2:
                return place.tokens

    def print_model(self):
        for edge in self.edges:
            if edge.source.id > 0:
                print("(id: {},tokens: {}) -> {}".format(edge.source.id, edge.source.tokens, edge.target.name))
            else:
                print("{} -> (id: {},tokens: {})".format(edge.source.name, edge.target.id, edge.target.tokens))
