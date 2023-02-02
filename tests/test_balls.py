import logging
from collections import namedtuple
from os import chdir
from pathlib import Path

import pandas as pd
import pandas.testing as pd_testing
from pytest_cases import THIS_MODULE, fixture, parametrize_with_cases

from bbv.ball import ball_map

cases = THIS_MODULE

__author__ = "Kevin Steptoe"
__copyright__ = "Kevin Steptoe"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

TestData = namedtuple("TestData", ["input_files", "Sheet_Name", "expected_files"])


def case_v21WIP():
    return TestData(
        ("Freya_pkg_spec__release_v2.1_WIP.xlsx",),
        ("Ball Map (2)",),
        ("ball.pcl",),
    )


@fixture
@parametrize_with_cases("td", cases=".")
def build_env(td, datadir_copy):
    for l_of_files in [td.input_files, td.expected_files]:
        for f in l_of_files:
            s_file = datadir_copy[f]
    datadir = Path(s_file.dirname)
    with (datadir) as f:
        chdir(f)
    yield td


def test_balls(build_env):
    """API Tests"""

    input_path = [Path(i) for i in build_env.input_files]
    sheet_name = [i for i in build_env.Sheet_Name]
    gold_path = [Path(i) for i in build_env.expected_files]
    results = list(zip(input_path, sheet_name, gold_path))
    output_filename = None
    loglevel = None

    for input_file, sheet_name, golden_pcl in results:
        produced = ball_map(input_file, sheet_name, output_filename, loglevel)
        _logger.info(f"Reading Golden pickle file {str(golden_pcl.absolute())}")
        golden = pd.read_pickle(golden_pcl)
        _logger.info(f"Comparing {str(produced)} and {str(gold_path)}")
        pd_testing.assert_frame_equal(golden, produced)
        _logger.info("Comparison Complete")
