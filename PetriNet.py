from components import Place, Transition, Edge


class PetriNet:

    def __init__(self):
        self.places = []
        self.transitions = []
        self.edges = []

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

    def add_marking(self, place):
        self.__get_component(place).tokens += 1

    def fire_transition(self, transition):
        for e in self.edges:
            if e.target.id == transition:
                e.source.tokens -= 1
            elif e.source.id == transition:
                e.target.tokens += 1

    def __get_component(self, id):
        if id > 0:
            return next((p for p in self.places if p.id == id), None)
        else:
            return next((t for t in self.transitions if t.id == id), None)

    def transition_name_to_id(self, name):
        for transition in self.transitions:
            if transition.name == name:
                return transition.id
