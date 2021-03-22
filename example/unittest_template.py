import unittest
import requests


class TestStringMethods(unittest.TestCase):
    {%- for config in configs %}
    def test_{{ config.name }}(self):
        {% if config.arg_num == 0 or ("Request" in config.arg_types and config.arg_num == 1)%}resp = requests.{{ config.method }}("{{ config.url }}")
        {% else %}data = 
        resp = requests.{{ config.method }}("{{ config.url }}", data=data)
        {% endif %}
        self.assertEqual(resp.status_code, 200)
    {% endfor %}


if __name__ == "__main__":
    unittest.main()
