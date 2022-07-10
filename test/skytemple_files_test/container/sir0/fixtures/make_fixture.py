from typing import Optional, Tuple, List

from range_typed_integers import u8, u16, u32

from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.test.fixture import DummySir0Serializable


class Dummy2(Sir0Serializable):
    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        return bytes([1, 2, 3, 4]), [], None

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> Sir0Serializable:
        raise NotImplementedError()


class Dummy3(Sir0Serializable):
    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        return bytes([32, 32, 32, 32, 34, 34, 34, 34]), [u32(0), u32(4)], None

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> Sir0Serializable:
        raise NotImplementedError()


if __name__ == "__main__":
    models = [
        Dummy2(),
        Dummy3(),
        DummySir0Serializable(u8(1), u8(2), u8(3), u8(4), u16(0)),
        DummySir0Serializable(u8(12), u8(34), u8(56), u8(78), u16(1234)),
    ]
    for i, model in enumerate(models):
        m = Sir0Handler.load_python_model()(*model.sir0_serialize_parts())

        with open(f"./{i}.bin", "wb") as f:
            f.write(Sir0Handler.load_python_writer()().write(m))
