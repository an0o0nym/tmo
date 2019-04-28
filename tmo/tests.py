import os
import unittest

from tmo.core import tmo_engine
from tmo.core import gettext


class TestTMOEngine(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        TEMPLATES_PATH = os.path.join(BASE_DIR, 'fixtures', 'templates.json')

        tmo_engine.load_templates(TEMPLATES_PATH)

    def test_engine(self):
        # automatically select singular or plural template
        s = gettext('fav_color', name='John', color='red')
        self.assertEqual(s, 'My name is John and my favourite color is red.')

        s = gettext('fav_color', name='John', color=['red'])
        self.assertEqual(s, 'My name is John and my favourite color is red.')

        s = gettext('fav_color', name='John', color=['red', 'blue', 'green'])
        self.assertEqual(s, 'My name is John and my favourite colors are red, blue and green.')

        # there is no plural template - fall back to the singular
        s = gettext('fav_car', car=['bmw', 'mercedes'])
        self.assertEqual(s, 'My favourite car is bmw and mercedes.')

        s = gettext('fav_car#cars', car=['bmw', 'mercedes'])
        self.assertEqual(s, 'My favourite car is bmw and mercedes.')

        s = gettext('fav_car', car=['bmw'])
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext('fav_car', car='bmw')
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext('fav_car', car='bmw')
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext(
            'fav_game',
            game=['World of Warcraft', 'Dirt4'],
        )
        self.assertEqual(s, 'I usually play the World of Warcraft or the Dirt4.')

        s = gettext('fav_number', number=[1.21513, 1.41342])
        self.assertEqual(s, 'My favourite number is 1.22 and 1.41.')

        s = gettext('fav_country', country=['Great Britain', 'USA', 'Czech Republic'])
        self.assertEqual(s, 'My favourite countries are the Great Britain, the USA and the Czech Republic.')


if __name__ == '__main__':
    unittest.main()
