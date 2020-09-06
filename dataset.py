yaml_empty_set = [[]]

# Data for creating malformed template files
yaml_invalid_data = [
    # Empty object
    {},
    # Not array
    {
        'id': 'some-id',
        'label': 'Button label. Mandatory',
        'link': 'Web link. Optional',
        'depends': 'Id of parent element. Optional'
    },
    # Missed `id` field
    [
        {
            'label': 'Button label. Mandatory',
            'link': 'Web link. Optional',
            'depends': 'Id of parent element. Optional'
        }
    ],
    # Missed `label` field
    [
        {
            'id': 'some-id',
            'link': 'Web link. Optional',
            'depends': 'Id of parent element. Optional'
        }
    ],
    # Element is a parent of itself
    [
        {
            'id': 'same-id',
            'label': 'Button label. Mandatory',
            'depends': 'same-id'
        }
    ],
    # Same ids for items
    [
        {
            'id': 'same-id',
            'label': 'Button label. Mandatory'
        },
        {
            'id': 'same-id',
            'label': 'Button label. Mandatory'
        }
    ],
    # Item depends on non-existent item
    [
        {
            'id': 'some-id',
            'label': 'Button label. Mandatory',
            'depends': 'non-existent-id'
        }
    ]
]

# Data for creating valid template files
yaml_valid_data = [
    [],
    [
        {
            'id': 'parent-id',
            'label': 'Label One',
        },
        {
            'id': 'child-id',
            'label': 'Label Two',
            'depends': 'parent-id'
        }
    ],
    [
        {
            'id': 'some-id',
            'label': 'Label One',
            'link': 'https://yandex.ru'
        }
    ],
    [
        {
            'id': 'parent-id',
            'label': 'Label One',
            'link': 'https://yandex.ru'
        },
        {
            'id': 'child-id',
            'label': 'Label One',
            'link': 'https://google.ru',
            'depends': 'parent-id'
        }
    ]
]