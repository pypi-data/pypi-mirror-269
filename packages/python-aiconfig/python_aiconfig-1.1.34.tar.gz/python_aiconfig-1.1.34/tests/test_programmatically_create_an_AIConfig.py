import pytest
from aiconfig.Config import AIConfigRuntime
from aiconfig.util.config_utils import extract_override_settings

from aiconfig.schema import (
    AIConfig,
    ConfigMetadata,
    ExecuteResult,
    ModelMetadata,
    Prompt,
    PromptMetadata,
)


@pytest.fixture
def ai_config_runtime():
    runtime = AIConfigRuntime.create("Untitled AIConfig")
    return runtime


def test_create_empty_config_with_defaults(ai_config_runtime):
    """
    Test creating an empty AIConfig with default values.
    """
    config: AIConfig = ai_config_runtime

    # Ensure the AIConfig is created with default values
    assert config.metadata == ConfigMetadata()
    assert config.prompt_index == {}
    assert config.prompts == []
    assert config.schema_version == "latest"
    assert config.name == "Untitled AIConfig"


def test_add_model_to_config(ai_config: AIConfig):
    """
    Test adding a new model to the config's metadata.
    """
    model_name = "new_model"
    model_settings = {"setting1": "value1", "setting2": "value2"}

    ai_config.add_model(model_name, model_settings)

    # Ensure the model is added to the config's metadata
    assert model_name in ai_config.metadata.models
    assert ai_config.metadata.models[model_name] == model_settings


def test_delete_model_from_config(ai_config):
    """
    Test deleting an existing model.
    """
    model_name = "existing_model"
    model_settings = {"setting1": "value1", "setting2": "value2"}

    ai_config.add_model(model_name, model_settings)

    ai_config.delete_model(model_name)

    # Ensure the model is deleted from the config's metadata
    assert model_name not in ai_config.metadata.models


def test_delete_nonexistent_model(ai_config: AIConfig):
    """
    Test deleting a non-existent model (expect an exception).
    """
    non_existent_model = "non_existent_model"

    # Ensure trying to delete a non-existent model raises an exception
    with pytest.raises(
        Exception, match=f"Model '{non_existent_model}' does not exist."
    ):
        ai_config.delete_model(non_existent_model)


def test_add_prompt_to_config(ai_config_runtime: AIConfigRuntime):
    """
    Test adding a prompt to the AIConfig.
    """
    config = ai_config_runtime

    prompt_data = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )

    config.add_prompt("prompt1", prompt_data)

    # Ensure the prompt is added correctly
    assert config.prompt_index["prompt1"].name == "prompt1"
    assert config.prompt_index["prompt1"].input == "This is a prompt"
    assert config.prompt_index["prompt1"].metadata.model == "fakemodel"

    # Ensure prompt list is in sync with prompt index
    assert config.prompts[0] == config.prompt_index["prompt1"]


def test_delete_prompt_from_config(ai_config_runtime):
    """
    Test deleting a prompt from the AIConfig.
    """
    config = ai_config_runtime

    prompt_data = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )

    config.add_prompt("prompt1", prompt_data)
    assert len(config.prompt_index) == 1
    assert len(config.prompts) == 1

    config.delete_prompt("prompt1")

    # Ensure the prompt is deleted correctly
    assert config.prompt_index == {}
    assert config.prompts == []
    assert len(config.prompt_index) == 0


def test_update_prompt_in_config(ai_config_runtime):
    """
    Test updating a prompt in the AIConfig.
    """
    config: AIConfig = ai_config_runtime

    prompt_data = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )

    config.add_prompt("prompt1", prompt_data)

    updated_prompt_data = Prompt(
        name="prompt1",
        input="Updated prompt",
        metadata=PromptMetadata(model="updatedmodel"),
    )

    config.update_prompt("prompt1", updated_prompt_data)

    # Ensure the prompt is updated correctly
    assert config.prompt_index["prompt1"].input == "Updated prompt"
    assert config.prompt_index["prompt1"].metadata.model == "updatedmodel"
    # Ensure prompt list is in sync with prompt index
    assert config.prompts[0] == config.prompt_index["prompt1"]


def test_create_config_with_name():
    """
    Test creating an AIConfig with a specific name.
    """
    config_runtime = AIConfigRuntime.create("My AIConfig")

    config = config_runtime

    assert config.name == "My AIConfig"


def test_create_config_with_schema_version():
    """
    Test creating an AIConfig with a specific schema version.
    """
    config_runtime = AIConfigRuntime.create(
        "AIConfig with Schema", schema_version="v1"
    )

    config = config_runtime

    assert config.schema_version == "v1"


def test_add_prompt_with_duplicate_name(ai_config_runtime: AIConfigRuntime):
    """
    Test adding a prompt with a duplicate name.
    """
    config = ai_config_runtime

    prompt_data1 = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )
    prompt_data2 = Prompt(
        name="prompt1",
        input="Duplicate prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )

    config.add_prompt("prompt1", prompt_data1)

    # Ensure adding a prompt with a duplicate name raises an exception
    with pytest.raises(
        Exception, match=r"Prompt with name prompt1 already exists."
    ):
        config.add_prompt("prompt1", prompt_data2)


def test_update_nonexistent_prompt(ai_config_runtime: AIConfigRuntime):
    """
    Test updating a nonexistent prompt.
    """
    config = ai_config_runtime
    nonexistent_prompt_name = "nonexistent_prompt"

    prompt_data = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )

    # Ensure updating a nonexistent prompt raises an exception
    with pytest.raises(
        IndexError,
        match=f"Prompt '{nonexistent_prompt_name}' not found in config",
    ):
        config.update_prompt(nonexistent_prompt_name, prompt_data)


def test_delete_nonexistent_prompt(ai_config_runtime: AIConfigRuntime):
    """
    Test deleting a nonexistent prompt.
    """
    config = ai_config_runtime
    prompt_name = "nonexistent_prompt"

    # Ensure deleting a nonexistent prompt raises an exception
    with pytest.raises(
        IndexError, match=f"Prompt '{prompt_name}' not found in config"
    ):
        config.delete_prompt(prompt_name)


def test_get_metadata_with_nonexistent_prompt(
    ai_config_runtime: AIConfigRuntime,
):
    """
    Test the retrieval of metadata from a non-existent prompt.
    """
    config = ai_config_runtime
    prompt_name = "nonexistent_prompt"

    # Ensure that attempting to retrieve metadata for a non-existent prompt raises an exception
    with pytest.raises(
        IndexError, match=f"Prompt '{prompt_name}' not found in config"
    ):
        config.get_metadata(prompt_name)


@pytest.fixture
def ai_config():
    config = AIConfig(
        name="Untitled AIConfig",
        schema_version="latest",
        metadata=ConfigMetadata(),
        prompts=[],
    )
    return config


def test_load_saved_config(tmp_path):
    """
    Test loading a saved AIConfig from a JSON file.
    """
    config_runtime = AIConfigRuntime.create("My AIConfig")

    # Create a configuration-level parameter
    config_runtime.set_parameter(
        "config_param", "config_value", prompt_name=None
    )

    # Create a sample prompt for testing
    prompt_data = Prompt(
        name="prompt1",
        input="This is a prompt",
        metadata=PromptMetadata(model="fakemodel"),
    )
    config_runtime.add_prompt("prompt1", prompt_data)

    # Set a prompt-level parameter
    config_runtime.set_parameter(
        "prompt_param", "prompt_value", prompt_name="prompt1"
    )

    json_config_filepath = tmp_path / "my_aiconfig.json"
    config_runtime.save(json_config_filepath)

    loaded_config = AIConfigRuntime.load(json_config_filepath)

    # Ensure the loaded AIConfig contains the expected data
    assert loaded_config.name == "My AIConfig"
    assert loaded_config.metadata.parameters == {
        "config_param": "config_value"
    }
    assert "prompt1" in loaded_config.prompt_index
    assert loaded_config.prompt_index["prompt1"].metadata is not None
    assert loaded_config.prompt_index["prompt1"].metadata.parameters == {
        "prompt_param": "prompt_value"
    }


def test_set_config_name(ai_config_runtime: AIConfigRuntime):
    ai_config_runtime.set_name("My AIConfig")
    assert ai_config_runtime.name == "My AIConfig"


def test_set_description(ai_config_runtime: AIConfigRuntime):
    ai_config_runtime.set_description("This is a description")
    assert ai_config_runtime.description == "This is a description"


def test_get_prompt_existing(ai_config_runtime: AIConfigRuntime):
    """Test retrieving an existing prompt by name."""
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    retrieved_prompt = ai_config_runtime.get_prompt("GreetingPrompt")
    assert retrieved_prompt == prompt


def test_get_prompt_after_deleting_previous(
    ai_config_runtime: AIConfigRuntime,
):
    prompt1 = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    prompt2 = Prompt(
        name="GoodbyePrompt",
        input="Goodbye, see you later!",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt1.name, prompt1)
    ai_config_runtime.add_prompt(prompt2.name, prompt2)
    ai_config_runtime.delete_prompt("GreetingPrompt")
    retrieved_prompt = ai_config_runtime.get_prompt("GoodbyePrompt")
    assert retrieved_prompt == prompt2


def test_get_prompt_nonexistent(ai_config_runtime: AIConfigRuntime):
    with pytest.raises(
        IndexError, match=r"Prompt 'GreetingPrompt' not found in config"
    ):
        ai_config_runtime.get_prompt("GreetingPrompt")


def test_update_model_for_ai_config(ai_config_runtime: AIConfigRuntime):
    """Test updating model without a specific prompt."""
    # New model name, new settings --> update
    model_name = "testmodel"
    settings = {"topP": 0.9}
    ai_config_runtime.update_model(model_name, settings)
    pytest.warns(
        match=f"No prompt name was given to update the model name to '{model_name}'."
    )
    assert ai_config_runtime.metadata.models is not None
    assert ai_config_runtime.metadata.models[model_name] == settings

    # Existing model name, no settings --> no-op
    ai_config_runtime.update_model(model_name)
    pytest.warns(
        match=f"No prompt name was given to update the model name to '{model_name}'."
    )
    assert ai_config_runtime.metadata.models is not None
    assert ai_config_runtime.metadata.models[model_name] == settings

    # Existing model name, new settings --> update
    new_settings = {"topP": 0.75}
    ai_config_runtime.update_model(model_name, new_settings)
    pytest.warns(
        match=f"No prompt name was given to update the model name to '{model_name}'."
    )
    assert ai_config_runtime.metadata.models is not None
    assert ai_config_runtime.metadata.models[model_name] == new_settings

    # New model name, no settings --> update
    new_model_name = "testmodel_without_settings"
    ai_config_runtime.update_model(new_model_name)
    pytest.warns(
        match=f"No prompt name was given to update the model name to '{new_model_name}'."
    )
    assert ai_config_runtime.metadata.models is not None
    assert ai_config_runtime.metadata.models[new_model_name] == {}


def test_update_model_for_prompt(ai_config_runtime: AIConfigRuntime):
    """Test updating model for a specific prompt."""
    # New model name, new settings, no prompt metadata --> update
    prompt1 = Prompt(name="GreetingPrompt", input="Hello, how are you?")
    ai_config_runtime.add_prompt(prompt1.name, prompt1)
    model_name = "testmodel"
    settings = {"topP": 0.9}
    ai_config_runtime.update_model(model_name, settings, prompt1.name)
    prompt = ai_config_runtime.get_prompt(prompt1.name)
    assert prompt.metadata is not None
    assert prompt.metadata.model == ModelMetadata(
        name=model_name, settings=settings
    )

    # New model name, no settings --> update name only
    new_model_name = "testmodel_new_name"
    ai_config_runtime.update_model(new_model_name, None, prompt1.name)
    prompt = ai_config_runtime.get_prompt(prompt1.name)
    assert prompt.metadata is not None
    assert prompt.metadata.model == ModelMetadata(
        name=new_model_name, settings=settings
    )

    # Same model name, new settings --> update settings only
    settings = {"topP": 0.9}
    ai_config_runtime.update_model(new_model_name, settings, prompt1.name)
    prompt = ai_config_runtime.get_prompt(prompt1.name)
    assert prompt.metadata is not None
    assert prompt.metadata.model == ModelMetadata(
        name=new_model_name, settings=settings
    )

    # New name, no settings, prompt with model name as string --> update
    prompt2 = Prompt(
        name="GreetingPromptModelAsStr",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="some_random_model"),
    )
    ai_config_runtime.add_prompt(prompt2.name, prompt2)
    new_name_again = "testmodel_new_name_model_as_str"
    ai_config_runtime.update_model(new_name_again, None, prompt2.name)
    prompt = ai_config_runtime.get_prompt(prompt2.name)
    assert prompt.metadata is not None
    assert prompt.metadata.model == ModelMetadata(
        name=new_name_again, settings={}
    )

    # New name, no settings, prompt with metadata but no model --> update
    tags = ["my_fancy_tags"]
    prompt3 = Prompt(
        name="GreetingsNumber3",
        input="Hello, how are you?",
        metadata=PromptMetadata(tags=tags),
    )
    ai_config_runtime.add_prompt(prompt3.name, prompt3)
    new_name_3 = "new_name_number_3"
    ai_config_runtime.update_model(new_name_3, None, prompt3.name)
    prompt = ai_config_runtime.get_prompt(prompt3.name)
    assert prompt.metadata is not None
    assert prompt.metadata.model == ModelMetadata(name=new_name_3, settings={})
    assert prompt.metadata.tags == tags


def test_update_model_with_invalid_arguments(
    ai_config_runtime: AIConfigRuntime,
):
    """Test trying to update model with invalid arguments."""
    with pytest.raises(
        ValueError,
        match=r"Cannot update model. Either model name or model settings must be specified.",
    ):
        ai_config_runtime.update_model(model_name=None, settings=None)

    with pytest.raises(
        ValueError,
        match=r"Cannot update model. There are two things you are trying:",
    ):
        ai_config_runtime.update_model(
            model_name=None, settings={"top": 0.9}, prompt_name=None
        )


def test_set_and_delete_metadata_ai_config(ai_config_runtime: AIConfigRuntime):
    """Test deleting an existing metadata key at the AIConfig level."""
    ai_config_runtime.set_metadata("testkey", "testvalue")

    assert ai_config_runtime.get_metadata().testkey == "testvalue"

    ai_config_runtime.delete_metadata("testkey")

    assert hasattr(ai_config_runtime.get_metadata(), "testkey") is False


def test_set_and_delete_metadata_ai_config_prompt(
    ai_config_runtime: AIConfigRuntime,
):
    """Test deleting a non-existent metadata key at the AIConfig level."""
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    ai_config_runtime.set_metadata("testkey", "testvalue", "GreetingPrompt")

    assert (
        ai_config_runtime.get_prompt("GreetingPrompt").metadata.testkey
        == "testvalue"
    )

    ai_config_runtime.delete_metadata("testkey", "GreetingPrompt")

    assert (
        hasattr(
            ai_config_runtime.get_prompt("GreetingPrompt").metadata, "testkey"
        )
        is False
    )


def test_add_output_existing_prompt_no_overwrite(
    ai_config_runtime: AIConfigRuntime,
):
    """Test adding an output to an existing prompt without overwriting."""
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    test_result = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output",
        metadata={
            "raw_response": {"role": "assistant", "content": "test output"}
        },
    )
    ai_config_runtime.add_output("GreetingPrompt", test_result)

    assert ai_config_runtime.get_latest_output("GreetingPrompt") == test_result

    test_result2 = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output",
        metadata={
            "raw_response": {
                "role": "assistant",
                "content": "test output for second time",
            }
        },
    )

    ai_config_runtime.add_output("GreetingPrompt", test_result2)
    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt") == test_result2
    )

    ai_config_runtime.delete_output("GreetingPrompt")
    assert ai_config_runtime.get_latest_output("GreetingPrompt") == None


def test_add_outputs_existing_prompt_no_overwrite(
    ai_config_runtime: AIConfigRuntime,
):
    """Test adding outputs to an existing prompt without overwriting."""
    original_result = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="original result",
        metadata={
            "raw_response": {"role": "assistant", "content": "original result"}
        },
    )
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
        outputs=[original_result],
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)

    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt")
        == original_result
    )

    test_result1 = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output 1",
        metadata={
            "raw_response": {"role": "assistant", "content": "test output 1"}
        },
    )
    test_result2 = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output 2",
        metadata={
            "raw_response": {"role": "assistant", "content": "test output 2"}
        },
    )
    ai_config_runtime.add_outputs(
        "GreetingPrompt", [test_result1, test_result2]
    )

    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt") == test_result2
    )
    assert prompt.outputs == [original_result, test_result1, test_result2]


def test_add_outputs_existing_prompt_with_overwrite(
    ai_config_runtime: AIConfigRuntime,
):
    """Test adding outputs to an existing prompt with overwriting."""
    original_result = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="original result",
        metadata={
            "raw_response": {"role": "assistant", "content": "original result"}
        },
    )
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
        outputs=[original_result],
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)

    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt")
        == original_result
    )

    test_result1 = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output 1",
        metadata={
            "raw_response": {"role": "assistant", "content": "test output 1"}
        },
    )
    test_result2 = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="test output 2",
        metadata={
            "raw_response": {"role": "assistant", "content": "test output 2"}
        },
    )
    ai_config_runtime.add_outputs(
        "GreetingPrompt", [test_result1, test_result2], True
    )

    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt") == test_result2
    )
    assert prompt.outputs == [test_result1, test_result2]


def test_add_undefined_outputs_to_prompt(ai_config_runtime: AIConfigRuntime):
    """Test for adding undefined outputs to an existing prompt with/without overwriting. Should result in an error."""
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    assert ai_config_runtime.get_latest_output("GreetingPrompt") == None
    # Case 1: No outputs, overwrite param not defined
    with pytest.raises(
        ValueError,
        match=r"Cannot add outputs. No outputs provided for prompt 'GreetingPrompt'.",
    ):
        ai_config_runtime.add_outputs("GreetingPrompt", [])
    # Case 2: No outputs, overwrite param set to True
    with pytest.raises(
        ValueError,
        match=r"Cannot add outputs. No outputs provided for prompt 'GreetingPrompt'.",
    ):
        ai_config_runtime.add_outputs("GreetingPrompt", [], True)


def test_add_output_existing_prompt_overwrite(
    ai_config_runtime: AIConfigRuntime,
):
    """Test adding an output to an existing prompt with overwriting."""
    original_output = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="original output",
        metadata={
            "raw_response": {"role": "assistant", "content": "original output"}
        },
    )
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
        outputs=[original_output],
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    # check that the original_output is there
    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt")
        == original_output
    )
    expected_output = ExecuteResult(
        output_type="execute_result",
        execution_count=0,
        data="original output",
        metadata={
            "raw_response": {"role": "assistant", "content": "original output"}
        },
    )
    # overwrite the original_output
    ai_config_runtime.add_output("GreetingPrompt", expected_output, True)
    assert (
        ai_config_runtime.get_latest_output("GreetingPrompt")
        == expected_output
    )


def test_add_undefined_output_to_prompt(ai_config_runtime: AIConfigRuntime):
    """Test for adding an undefined output to a prompt with/without overwriting. Should result in an error."""
    prompt = Prompt(
        name="GreetingPrompt",
        input="Hello, how are you?",
        metadata=PromptMetadata(model="fakemodel"),
    )
    ai_config_runtime.add_prompt(prompt.name, prompt)
    # Case 1: No output, overwrite param not defined
    with pytest.raises(
        ValueError,
        match=r"Cannot add output to prompt 'GreetingPrompt'. Output is not defined.",
    ):
        ai_config_runtime.add_output("GreetingPrompt", None)
    # Case 2: No output, overwrite param set to True
    with pytest.raises(
        ValueError,
        match=r"Cannot add output to prompt 'GreetingPrompt'. Output is not defined.",
    ):
        ai_config_runtime.add_output("GreetingPrompt", None, True)


def test_extract_override_settings(ai_config_runtime: AIConfigRuntime):
    initial_settings = {"topP": 0.9}

    # Test Case 1: No global setting, Expect an override
    override = extract_override_settings(
        ai_config_runtime, initial_settings, "testmodel"
    )
    assert override == {"topP": 0.9}

    # Test Case 2: Global Settings differ, expect override
    ai_config_runtime.add_model("testmodel", {"topP": 0.8})
    override = extract_override_settings(
        ai_config_runtime, initial_settings, "testmodel"
    )
    assert override == {"topP": 0.9}

    # Test Case 3: Global Settings match settings, expect no override
    ai_config_runtime.update_model(
        model_name="testmodel", settings={"topP": 0.9}
    )
    override = extract_override_settings(
        ai_config_runtime, initial_settings, "testmodel"
    )
    assert override == {}

    # Test Case 4: Global settings defined and empty settings defined. Expect no override
    override = extract_override_settings(ai_config_runtime, {}, "testmodel")
    assert override == {}
