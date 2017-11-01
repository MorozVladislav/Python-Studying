"""
TASK: Create 'foo' object which allows you to run code below and get expected output.

EXPECTED OUTPUT:

Mimosa
Acrux
Acrux
Mimosa
Mimosa
Mimosa
Alpha Centauri
# IndexError
# TypeError
Algol,Polaris
Algol,Polaris
Regulus
"""


class Stars:
    def __init__(self, star_name=None):
        if star_name is not None:
            self.name = star_name
        else:
            self.name = "Acrux"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def func_1():
    return Stars


def func_2():
    return func_1


foo = [
    Stars,
    {
        "Sirius": [
            Stars(),
            Stars
        ]
    },
    {
        "Arcturus": [
            [
                {
                    "Vega": Stars
                }
            ]
        ],
        "Capella": {
            "Rigel": {
                "Procyon": func_1,
                "Achernar": func_2
            }
        }
    },
    ("Alpha Centauri",),
    set(),
    set(),
    "Regulus"
]


if __name__ == '__main__':
    print(foo[0]('Mimosa').name)

    print(foo[1]['Sirius'][0].name)

    print(foo[1]['Sirius'][1]().name)

    print(foo[2]['Arcturus'][0][-1]['Vega']('Mimosa').name)

    print(foo[2]['Capella']['Rigel']['Procyon']()('Mimosa').name)

    print(foo[2]['Capella']['Rigel']['Achernar']()()('Mimosa').name)

    print(foo[3][0])

    try:
        print(foo[3][1])
    except IndexError:
        print('# IndexError')

    try:
        foo[3][0] = 'Deneb'
    except TypeError:
        print('# TypeError')

    foo[4].add('Algol')
    foo[4].add('Polaris')
    foo[4].add('Algol')
    print(','.join(foo[4]))

    foo[5].add(foo[0]('Algol'))
    foo[5].add(foo[0]('Polaris'))
    foo[5].add(foo[0]('Algol'))
    print(','.join(i.name for i in foo[5]))

    print(foo[6][:])
