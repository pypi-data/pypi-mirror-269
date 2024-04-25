# coding: utf-8

import unittest
import pandas as pandas
from snakemake.io import Wildcards


class TestSoftwareVersions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_diffent_string_versions(self):
        from hydra_genetics.utils.software_versions import _create_container_name_version_string

        self.assertEqual(_create_container_name_version_string("docker://hydragenetics/common:1.10.2"),
                         "common_1.10.2")
        self.assertEqual(_create_container_name_version_string("docker://fred2/optitype"),
                         "optitype_NoVersion")
        self.assertEqual(_create_container_name_version_string("/test/tgs/hydragenetics__common_1.10.2.sif"),
                         "common_1.10.2")
        self.assertEqual(_create_container_name_version_string("/test/tgs/common"),
                         "common_NoVersion")
