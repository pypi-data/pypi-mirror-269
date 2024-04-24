#  This file is part of the CoverageControl library
#
#  Author: Saurav Agarwal
#  Contact: sauravag@seas.upenn.edu, agr.saurav1@gmail.com
#  Repository: https://github.com/KumarRobotics/CoverageControl
#
#  Copyright (c) 2024, Saurav Agarwal
#
#  The CoverageControl library is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  The CoverageControl library is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  CoverageControl library. If not, see <https://www.gnu.org/licenses/>.

import tempfile
import warnings
import numpy as np
import coverage_control as cc

def test_env_io():
    params = cc.Parameters()
    env = cc.CoverageSystem(params)
    world_idf1 = env.GetWorldIDFObject()
    world_map = world_idf1.GetWorldMap()

    with tempfile.TemporaryDirectory() as tmp_dir:
        env.WriteEnvironment(tmp_dir + "/env.pos", tmp_dir + "/env.idf")
        world_idf2 = cc.WorldIDF(params, tmp_dir + "/env.idf")
        env2 = cc.CoverageSystem(params, world_idf2, tmp_dir + "/env.pos")
        map2 = world_idf2.GetWorldMap()
    is_close = np.allclose(world_map, map2)
    if not is_close:
        diff = np.abs(world_map - map2).max()
    assert is_close
    is_equal = np.array_equal(world_map, map2)
    if not is_equal and is_close:
        diff = np.abs(world_map - map2).max()
        print("Max difference: ", diff)
        warnings.warn("Not all elements are equal, but all elements are close")
