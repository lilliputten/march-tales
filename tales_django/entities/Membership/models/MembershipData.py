class MembershipData:
    data = [
        {
            'tag': 'ACADEMIC',
            'label': 'Academic',
            'price': 25,
            'currency': 'EUR',
        },
        {
            'tag': 'NORMAL',
            'label': 'Normal',
            'price': 50,
            'currency': 'EUR',
            'default': True,
        },
        {
            'tag': 'HONORARY',
            'label': 'Honorary',
            'price': 0,
            'currency': 'EUR',
        },
    ]
    default = 'NORMAL'
    available = {'NORMAL', 'ACADEMIC'}

    def __getitem__(self, key: str) -> dict:
        dct = {o['tag']: o for o in self.data}
        return dct[key]

    @property
    def choices(self):
        return [(o['tag'], o['label']) for o in self.data]

    @property
    def public_choice_field_with_prices(self):
        return [
            (
                obj['tag'],
                '{} ({} {})'.format(obj['label'], obj['price'], obj['currency']),
            )
            for obj in self.data
            if obj['tag'] in self.available
        ]
