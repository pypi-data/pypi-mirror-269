# Copyright 2022 StreamSets Inc.
# fmt: off
import time

import pytest

from streamsets.sdk.utils import get_random_string

# fmt: on


@pytest.fixture(scope="module")
def simple_pipeline_draft(sch, sch_authoring_sdc_id):
    """A trivial pipeline:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple_draft_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline, draft=True)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def simple_draft_run(sch, sch_authoring_sdc_id, simple_pipeline_draft):
    """A trivial draft run:"""
    pipeline = simple_pipeline_draft
    draft_run_id = sch.start_draft_run(pipeline).response.json()["jobId"]
    time.sleep(5)
    draft_run_obj = sch.draft_runs.get(search="id=='{}'".format(draft_run_id))

    try:
        yield draft_run_obj
    finally:
        sch.stop_draft_run(draft_run_obj)
        sch.delete_draft_run(draft_run_obj)


def test_draft_runs(sch, simple_pipeline_draft):
    pipeline = simple_pipeline_draft
    draft_run_id = sch.start_draft_run(pipeline).response.json()["jobId"]
    try:
        draft_run = sch.draft_runs.get(search="id=='{}'".format(draft_run_id))
        assert draft_run is not None
    finally:
        sch.stop_draft_run(draft_run)
        sch.delete_draft_run(draft_run)


def test_draft_run_snapshot(sch, simple_draft_run):
    draft_run = simple_draft_run
    draft_run.capture_snapshot()
    assert draft_run.snapshots[0].name == "Snapshot1"
    assert draft_run.snapshots[-1].batches is not None
    draft_run.capture_snapshot()
    assert len(draft_run.snapshots) == 2
    assert draft_run.snapshots[-1].id is not None
    assert draft_run.snapshots[1].time_stamp > draft_run.snapshots[0].time_stamp
    draft_run.remove_snapshot(draft_run.snapshots[0])
    assert len(draft_run.snapshots) == 1
    draft_run.remove_snapshot(draft_run.snapshots[0])
    assert len(draft_run.snapshots) == 0


def test_draft_run_logs(sch, simple_draft_run):
    draft_run = simple_draft_run
    logs = draft_run.get_logs()
    assert logs is not None
