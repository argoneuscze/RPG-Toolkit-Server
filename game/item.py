from collections import Counter


class ItemTemplate:
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
    def __init__(self, item_template):
        super().__init__(item_template)
        self.items = Counter()

    def is_container(self):
        return True

    def add_item(self, item):
        self.items[item] += 1

    def remove_item(self, item):
        if self.items[item] != 0:
            self.items[item] -= 1

    def get_items(self):
        return self.items.elements()

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
    def __init__(self):
        super().__init__(ItemTemplate('generic', 'Generic storage', 'You should not see this.', True))
