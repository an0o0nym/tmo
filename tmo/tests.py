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
        s = gettext('fav_color', name='John', color=['red', 'blue', 'green'])
        self.assertEqual(s, 'My name is John and my favourite colors is red, blue and green.')

        s = gettext('fav_color#p', name='John', color=['red', 'blue', 'green'])
        self.assertEqual(s, 'My name is John and my favourite colors are red, blue and green.')

        s = gettext('fav_car#p', car=['bmw', 'mercedes'])
        self.assertEqual(s, 'My favourite car is bmw and mercedes.')

        s = gettext('fav_car#p', car=['bmw'])
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext('fav_car#p', car='bmw')
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext('fav_car', car='bmw')
        self.assertEqual(s, 'My favourite car is bmw.')

        s = gettext(
            'fav_game',
            game=['World of Warcraft', 'Dirt4'],
            connector_word=' or '
        )
        self.assertEqual(s, 'I usually play World of Warcraft or Dirt4.')

        s = gettext('fav_number', number=1.21513)
        self.assertEqual(s, 'My favourite number is 1.22.')


if __name__ == '__main__':
    unittest.main()
