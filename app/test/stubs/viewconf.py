''' Stubs for model testing '''
from service.viewconf_reader import ViewConfReader

class StubViewConfReader(ViewConfReader):
    ''' Fake repo to test instance methods '''
    @staticmethod
    def get_dimension_descriptor(language, observatory, scope, dimension):
        ''' Overriding method outside test scope '''
        yaml_collection = {
            "empty": None,
            "no_sections": {},
            "no_cards": {"secoes": []},
            "empty_cards": {"secoes": [{"cards": []}]},
            "card_not_found": {"secoes": [{"cards": [{"id": "wrong"}]}]},
            "card_exists": {"secoes": [
                {"cards": [{"id": "wrong"}]},
                {"cards": [{"id": "wrong"}, {"id": "right"}, {"id": "wrong"}]}
            ]}
        }
        return yaml_collection.get(dimension)
