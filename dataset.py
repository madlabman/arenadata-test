# Minimal valid dataset with no data
yaml_empty_template = [[]]

# Empty object
yaml_empty_object_template = {}

# Not array
yaml_not_an_array_template = {
    'id': 'some-id',
    'label': 'Button label. Mandatory',
    'link': 'Web link. Optional',
    'depends': 'Id of parent element. Optional'
}

# Missed `id` field
yaml_no_id_template = [
    {
        'label': 'Button label. Mandatory',
        'link': 'Web link. Optional',
        'depends': 'Id of parent element. Optional'
    }
]

# Missed `label` field
yaml_no_label_template = [
    {
        'id': 'some-id',
        'link': 'Web link. Optional',
        'depends': 'Id of parent element. Optional'
    }
]

# Element is a parent of itself
yaml_item_is_parent_of_itself_template = [
    {
        'id': 'same-id',
        'label': 'Button label. Mandatory',
        'depends': 'same-id'
    }
]

# Same ids for items
yaml_items_with_the_same_ids_template = [
    {
        'id': 'same-id',
        'label': 'Button label. Mandatory'
    },
    {
        'id': 'same-id',
        'label': 'Button label. Mandatory'
    }
]

# Item depends on non-existent item
yaml_item_depends_on_non_existent_item_template = [
    {
        'id': 'some-id',
        'label': 'Button label. Mandatory',
        'depends': 'non-existent-id'
    }
]

# Data for creating valid template files
yaml_valid_data = [
    # One item depends on another
    # Buttons have to be disabled
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
    # Item with link
    [
        {
            'id': 'some-id',
            'label': 'Label One',
            'link': 'https://yandex.ru'
        }
    ],
    # Just another one valid example
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
