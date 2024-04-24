# Copyright Streamsets 2023

# fmt: off
import pytest

# fmt: on


@pytest.mark.parametrize('pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_st_pipeline_builder'])
def test_pipeline_builder_add_stage_stage_exist(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    stage_to_add = "Trash"
    pipeline_builder.add_stage(stage_to_add)
    dummy_pipeline_stage = pipeline_builder._pipeline[pipeline_builder._config_key]['stages'][0]
    assert stage_to_add in dummy_pipeline_stage["instanceName"]


@pytest.mark.parametrize('pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_st_pipeline_builder'])
def test_pipeline_builder_add_stage_stage_does_not_exist(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    fake_stage_name = "Cannot Exist"
    with pytest.raises(Exception) as e:
        pipeline_builder.add_stage(fake_stage_name)
    assert str(e.value) == "Could not find stage ({}).".format(fake_stage_name)


@pytest.mark.parametrize('pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_st_pipeline_builder'])
def test_add_stage_supported_types(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    snowflake_destination = pipeline_builder.add_stage('Snowflake', type='destination')

    assert 'STREAMSETS_SNOWFLAKE' in snowflake_destination.supported_connection_types
