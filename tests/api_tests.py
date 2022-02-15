from mock import patch, Mock, MagicMock
import pytest

from market_and_fleet import get_typeid

class Test_API:
    def test_get_typeid(self):
        assert get_typeid('Brutix Blueprint') == '16230'

    @patch('__main__.get_typeid.sourcefile', sourcefile)
    def test_get_type_id_mocked(self):
        get_typeid("beepboop")
            assert get_type_obj