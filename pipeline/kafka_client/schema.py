import io
import json
import os

import avro
import avro.io
import avro.schema

script_dir = os.path.dirname(os.path.realpath(__file__))
schema_path = os.path.join(script_dir, "schema.avsc")

schema = avro.schema.parse(open(schema_path).read())


def serialize_avro(data: dict) -> bytes:
    """
    Serialize a dictionary to Avro bytes.
    """
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer = avro.io.DatumWriter(schema)
    writer.write(data, encoder)

    return bytes_writer.getvalue()


def deserialize_avro(raw_bytes: bytes) -> str:
    """
    Deserialize Avro bytes to JSON string.
    """
    try:
        bytes_reader = io.BytesIO(raw_bytes)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        deserialized_data = reader.read(decoder)
        return json.dumps(deserialized_data)
    except Exception as e:
        return json.dumps({"error": str(e)})
