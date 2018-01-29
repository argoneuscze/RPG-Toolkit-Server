import json

from game.item import Item, ItemContainer, ItemTemplate


class ItemManager:
    def __init__(self):
        self.item_templates = dict()

    def new_item(self, item_short_name):
        template = self.item_templates.get(item_short_name)
        if template is None:
            return None
        if template.is_container:
            return ItemContainer(template)
        else:
            return Item(template)

    def construct_loaded_items(self, item_list):
        ret = []
        for item in item_list:
            if isinstance(item, dict):
                for container, contents in item.items():
                    item_container = self.new_item(container)
                    for item_contents in self.construct_loaded_items(contents):
                        item_container.add_item(item_contents)
                    ret.append(item_container)
            else:
                ret.append(self.new_item(item))
        return ret

    def create_item_template(self, short_name, full_name, description, is_container):
        self.item_templates[short_name] = ItemTemplate(short_name, full_name, description, is_container)

    def load_item_templates(self, gamedir):
        data = json.load(open("{}/item_list.json".format(gamedir)))
        for template in data:
            t = ItemTemplate(template['short_name'], template['long_name'],
                             template['description'], template["is_container"])
            self.item_templates[template['short_name']] = t

    def save_item_templates(self, gamedir):
        with open('{}/item_list.json'.format(gamedir), 'w') as outfile:
            json.dump([template.as_dict() for template in self.item_templates.values()], outfile)

    def __eq__(self, other):
        return self.item_templates == other.item_templates
