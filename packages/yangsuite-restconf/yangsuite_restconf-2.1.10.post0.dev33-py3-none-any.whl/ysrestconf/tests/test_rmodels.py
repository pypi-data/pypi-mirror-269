import os
import json
from unittest import TestCase

from yangsuite.paths import set_base_path
from ysrestconf.restconf import ParseRestconf
from ysyangtree import YSContext
from ysdevices import YSDeviceProfile
from ysfilemanager import YSYangSet


class TestParseRestconf(TestCase):
    """Test ParseRestconf class used for generating OpenAPI documents."""
    @classmethod
    def setUpClass(cls):
        """Set up variables for ParseRestconf object instansiation."""
        # Set base path for the test directory
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        cls.openapi_dir = os.path.join(cls.testdir, 'openapi')
        set_base_path(cls.testdir)

        # User and device variables
        cls.user = 'testrest'
        cls.device_name = 'CSR1K-7'
        cls.host = YSDeviceProfile.get(cls.device_name)
        # Other instantiation variables that can change from test to test
        cls.yang_model = 'test-list'
        cls.yangset_name = 'testlist'
        cls.tags = ['/top-level-list']
        cls.depth_limit = ''
        cls.custom_media_types = []
        # Load YSYangSet and YSContext objects
        cls.yangset = YSYangSet.load(cls.user, cls.yangset_name)
        cls.ctx = YSContext(
            cls.yangset,
            modulenames=[cls.yang_model]
        )

    def test_add_keys_generate_pathname(self):
        """Test add_keys_generate_pathname method which generates pathname
        and set the pathkeys inside the ParseRestconf object."""
        parser = ParseRestconf(
            self.user, self.yang_model, self.ctx,
            self.tags, self.host, self.depth_limit,
            self.custom_media_types,
        )

        # Check for the pathkeys set after add_keys_generate_pathname invocation
        expected_pathkeys = [[
            '/data/test-list:top-level-list',
            '={test-list:top-level-list-first-key},{test-list:top-level-list-second-key}',
            [{
                'name': 'first-key',
                'in': 'path',
                'required': False,
                'schema': {'type': 'string'},
                'pathname': '={test-list:top-level-list-first-key}',
                'paramname': 'test-list:top-level-list-first-key'
            }, {
                'name': 'second-key',
                'in': 'path',
                'required': False,
                'schema': {'type': 'integer', 'format': 'uint32'},
                'pathname': ',{test-list:top-level-list-second-key}',
                'paramname': 'test-list:top-level-list-second-key'
            }]
        ]]
        self.assertEqual(
            json.loads(json.dumps(parser.pathkeys)),
            expected_pathkeys
        )

    def test_add_keys_generate_pathname_negative(self):
        """Test add_keys_generate_pathname method with negative case."""
        yang_model = 'test-container'
        yangset_name = 'testcontainer'
        tags = ['/top-level-container']
        yangset = YSYangSet.load(self.user, yangset_name)
        ctx = YSContext(
            yangset,
            modulenames=[yang_model]
        )
        parser = ParseRestconf(
            self.user, yang_model, ctx,
            tags, self.host, self.depth_limit,
            self.custom_media_types,
        )
        # Expect there are no pathkeys, because XPath is a container
        self.assertEqual(parser.pathkeys, [])
