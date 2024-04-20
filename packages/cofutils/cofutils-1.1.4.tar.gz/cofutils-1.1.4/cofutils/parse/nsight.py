#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Aditya Agrawal.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


class Nsight(object):
    """
	This class gets kernel information from the SQL (nvvp) database.
	"""

    #driverT = "CUPTI_ACTIVITY_KIND_DRIVER"
    runtimeT = "CUPTI_ACTIVITY_KIND_RUNTIME"
    kernelT = "CUPTI_ACTIVITY_KIND_KERNEL"
    markerT = "NVTX_EVENTS"
    stringT = "StringIds"

    def __init__(self, db):
        self.db = db
        self.markerId = 0

        

    def getProfileStart(self):
        """
		Get the profile start time
		"""
        profStart = sys.maxsize
        #for table in [self.driverT, self.runtimeT, self.kernelT, self.markerT]:
        for table in [self.runtimeT, self.kernelT, self.markerT]:
            colname = "start"
            cmd = "select {} from {} ORDER BY {} ASC LIMIT 1".format(colname, table, colname)
            result = self.db.select(cmd)
            assert (len(result) <= 1)
            if (len(result) == 1):
                assert (colname in result[0])
                t = result[0][colname]
                if (t < profStart):
                    profStart = t
        assert (profStart < sys.maxsize)
        return profStart

    def createMarkerTable(self):
        """
		Create a temporary table and index it to speed up repeated SQL quesries.
		"""
        cmd = 'CREATE TEMPORARY TABLE marker AS SELECT * FROM {}'.format(self.markerT)
        self.db.execute(cmd)

        self.db.execute('CREATE INDEX start_index ON marker (start)')
        self.db.execute('CREATE INDEX end_index ON marker (end)')
        
        #self.db.execute('CREATE INDEX id_index ON marker (id)')

    def encode_object_id(self, info):
        # Nothing to do for nsight. objId comes out of database
        assert 'objId' in info

    def getKernelInfo(self):
        """
		Get GPU kernel info
		"""
        cmd = (
            "SELECT "
            "demangledName as kNameId, "
            "strings.value as name, "
            "runtime.start as rStart, "
            "runtime.end as rEnd, "
            "runtime.globalTid as objId, "
            "runtime.globalTid / 0x1000000 % 0x1000000 AS pid, "
            "runtime.globalTid % 0x1000000 AS tid, "
            "kernels.globalPid / 0x1000000 % 0x1000000 AS kpid, "
            "kernels.correlationId,kernels.start,kernels.end,deviceId,streamId,"
            "gridX,gridY,gridZ,blockX,blockY,blockZ "
            "FROM {} AS kernels "
            "JOIN {} AS strings ON (kNameId = strings.Id) "
            "JOIN {} AS runtime ON (kernels.correlationId = runtime.correlationId AND kpid = pid) "
        ).format(self.kernelT, self.stringT, self.runtimeT)
        result = self.db.select(cmd)
        return result

    def getMarkerInfo(self, objId, startTime, endTime):
        """
		This function first finds all NVTX markers encapsulating
		a runtime / driver kernel launch.
		It then splits the markers into many lists.
			layerMarkers : User added NVTX markers
			traceMarkers : Call trace markers (inserted by pyprof)
			reprMarkers  : Markers containing the extra_repr() of a module (inserted by pyprof)
			pyprofMarkers: Markers containing args and kwargs (tensor shape, datatype etc.)
			seqMarkers   : Markers containing PyTorch internal sequence markers (inserted by PyTorch)
			altSeqMarkers: Markers inserted by PyTorch between two kernel launches. Needs better explanation.
			otherMarkers : Markers not in either of the above categories.

		We extract seqId from the seq and altSeq markers. The seqId is used in bprop.
		We also extract information from the layerMarkers.
		"""

        layerMarkers = []
        traceMarkers = []
        reprMarkers = []
        pyprofMarkers = []
        seqMarkers = []
        otherMarkers = []
        altSeqMarkers = []
        bprop = False

        #Helper functions

        def delete(objId, sTime):
            """
			Delete rows from the temporary SQL table which are no longer required.
			This speeds up future queries.
			"""
            margin = 0
            cmd = 'DELETE FROM marker WHERE globalTid = {} AND end < {}'.format(objId, sTime - margin)
            #cmd = 'DELETE FROM marker WHERE end < {}'.format(sTime - margin)
            self.db.execute(cmd)

        def getLayerName(mlist):
            """
			Get layer names from layer marker list.
			"""
            layers = []
            assert (type(mlist) == list)
            for m in mlist:
                assert ("layer:" in m)
                l = m.split(":")[1]
                layers.append(l)
            return layers

        def getSeqId(mlist):
            """
			Get sequence ids from seq / alt seq marker list.
			"""
            ids = []
            assert (type(mlist) == list)
            for m in mlist:
                assert (", seq = " in m)
                seq = int(m.split("=")[1])
                ids.append(seq)

            #Remove duplicates
            ids = list(set(ids))
            ids.sort()
            return ids

        def filterTrace(mlist):
            """
			Filter trace markers to remove certain file names.
			"""
            assert (type(mlist) == list)
            if len(mlist) == 0:
                return mlist
            mlist = mlist[-1]  #The last stack trace will be a super set.
            mlist = eval(mlist)
            mlist = mlist['traceMarker']
            assert (type(mlist) == list)
            mlist = list(filter(lambda x: "/torch/nn/modules/" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/nn/functional.py" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/tensor.py" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/autograd/__init__.py" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/_jit_internal.py" not in x, mlist))
            mlist = list(filter(lambda x: "/pyprof/nvtx/nvmarker.py" not in x, mlist))
            mlist = list(filter(lambda x: "/apex/optimizers/" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/_utils.py" not in x, mlist))
            mlist = list(filter(lambda x: "/torch/optim/" not in x, mlist))
            return mlist

        #Find all encapsulating markers
        cmd = 'SELECT text from marker where \
				start < {} and \
				end >= {} \
				ORDER BY start ASC'.format(startTime, endTime)
        # cmd = 'SELECT text from marker where \
		# 		globalTid = {} and \
		# 		start < {} and \
		# 		end > {} \
		# 		ORDER BY start ASC'.format(objId, startTime, endTime)
        result = self.db.select(cmd)
        for r in result:
            m = r['text']
            if m is not None:
                if 'DeepSpeedEngine.forward' in m:
                    otherMarkers.append('DeepSpeedEngine.forward')
                elif 'DeepSpeedEngine.backward' in m:
                    otherMarkers.append('DeepSpeedEngine.backward')
        delete(objId, startTime)

        return layerMarkers, filterTrace(
            traceMarkers
        ), reprMarkers, pyprofMarkers, seqMarkers, otherMarkers, altSeqMarkers, getSeqId(seqMarkers), getSeqId(
            altSeqMarkers
        ), getLayerName(layerMarkers)
