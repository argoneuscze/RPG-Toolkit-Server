from collections import Counter


class ItemTemplate:
    """Represents an Item's 'blueprint' within the Game.

    Each template has an identifier, a name, description and a flag whether it may contain
    other items or not. Actual items may then be spawned based on this template and placed in rooms
    or given to characters.

    """

    def __init__(self, short_name, long_name, description, is_container):
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.is_container = is_container

    def as_dict(self):
        data = {
            'short_name': self.short_name,
            'long_name': self.long_name,
            'description': self.description,
            'is_container': self.is_container
        }
        return data

    def __eq__(self, other):
        return self.short_name == other.short_name and \
               self.long_name == other.long_name and \
               self.description == other.description and \
               self.is_container == other.is_container

    def __hash__(self):
        return hash((self.short_name, self.long_name, self.description, self.is_container))


class Item:
    """This class represents an actual Item instance within the game world.

    Each Item has its own template which it's based on.

    """

    def __init__(self, item_template):
        self.item_template = item_template

    def get_short_name(self):
        return self.item_template.short_name

    def get_long_name(self):
        return self.item_template.long_name

    def get_description(self):
        return self.item_template.description

    def is_container(self):
        return False

    def is_same_type(self, other_item):
        return self.get_short_name() == other_item.get_short_name()

    def __eq__(self, other):
        return self.item_template == other.item_template

    def __hash__(self):
        return hash(id(self))


class ItemContainer(Item):
    """This is a subclass of Item which represents an Item that may contain other Items."""

    def __init__(self, item_template):
        super().__init__(item_template)
        self.items = Counter()

    def __iter__(self):
        for element in self.get_items():
            yield element
        raise StopIteration

    def is_container(self):
        return True

    def add_item(self, item):
        self.items[item] += 1

    def remove_item(self, item):
        if self.items[item] != 0:
            self.items[item] -= 1

    def get_items(self):
        return self.items.elements()

    def transfer_item(self, template_name, target_container):
        container, item = self.find_item(template_name)
        if container is None:
            # TODO some error if not found
            return None
        container.remove_item(item)
        target_container.add_item(item)

    def find_item(self, template_name):
        for item in self.get_items():
            if item.get_short_name() == template_name:
                return self, item
            if isinstance(item, ItemContainer):
                container, found_item = item.find_item(template_name)
                if container is not None:
                    return container, found_item
        return None, None

    def as_list(self):
        res = []
        for item in self.items.elements():
            if item.is_container():
                res.append({item.get_short_name(): item.as_list()})
            else:
                res.append(item.get_short_name())
        return res

    def __eq__(self, other):
        return self.item_template == other.item_template and self.as_list() == other.as_list()

    def __hash__(self):
        return hash(id(self))


class GenericContainer(ItemContainer):
    """A generic container Item that does not get saved anywhere.

    This container represents a Room's or Character's implicit Item storage.

    """

    def __init__(self):
        super().__init__(ItemTemplate('generic', 'Generic storage', 'You should not see this.', True))
