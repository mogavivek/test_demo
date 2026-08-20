from src.system import MachineSystem


def test_temperature_is_valid():
    system = MachineSystem(
        temperature=25,
        pressure=101,
        position=10
    )

    assert system.is_temperature_valid()


def test_pressure_is_valid():
    system = MachineSystem(
        temperature=25,
        pressure=101,
        position=10
    )

    assert system.is_pressure_valid()


def test_position_is_valid():
    system = MachineSystem(
        temperature=25,
        pressure=101,
        position=10
    )

    assert system.is_position_valid()


def test_complete_system():
    system = MachineSystem(
        temperature=25,
        pressure=101,
        position=10
    )

    assert system.system_status()