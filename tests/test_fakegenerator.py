import pytest


@pytest.fixture
def seed():
    return "LoR"


@pytest.fixture
def generic(seed):
    from mimesis import Generic

    return Generic("pt-br", seed)


@pytest.fixture
def DataGeneratorClass():
    from datanonymizer.generators import DataGenerator

    return DataGenerator


def test_should_return_anonimized_data(DataGeneratorClass, generic):
    gen = DataGeneratorClass(provider=generic.person.full_name)
    assert gen("A") == "Prado Periordi"


def test_should_return_same_output_given_an_input(DataGeneratorClass, generic):
    gen = DataGeneratorClass(provider=generic.person.full_name)
    assert gen("A") == "Prado Periordi"
    assert gen("A") == "Prado Periordi"
    assert gen("B") == "Tristão Cola"
    assert gen("C") == "Liberal Bolzan"
    assert gen("B") == "Tristão Cola"
    assert gen("C") == "Liberal Bolzan"


def test_should_never_repeat_and_output_for_distinct_inputs(
    DataGeneratorClass, generic
):
    gen = DataGeneratorClass(provider=generic.person.full_name)
    outputs = [gen(x) for x in range(10_000)]  # I've tested with 1_000_000!
    assert len(outputs) == len(set(outputs))
