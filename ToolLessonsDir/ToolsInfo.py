from Tools import multiply

multiply_tool = {
    'type': 'function',
    'function': {
        'name': 'multiply',
        'description': 'Multiplies two integers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'integer',
                    'description': 'First integer',
                },
                'b': {
                    'type': 'integer',
                    'description': 'Second integer',
                }
            },
            'required': ['a','b'],
            'additionalProperties': False
        }
    }
}

tools = {
    'multiply': multiply
}

