counter = -1


def get_unique_id():
    global counter
    counter += 1
    return counter


entities = []


class Entity:
    def __init__(self, components):
        self.id = get_unique_id()
        self.components = components

    def get_component(self, component_name):
        return self.components.get(component_name)

    def has_components(self, *component_names):
        available_component_names = self.components.keys()

        for name in component_names:
            if name not in available_component_names:
                return False

        return True


def get_entities_with(entities, *args):
    entities_with = []
    for entity in entities:
        if entity.has_components(*args):
            entities_with.append(entity)

    return entities_with
