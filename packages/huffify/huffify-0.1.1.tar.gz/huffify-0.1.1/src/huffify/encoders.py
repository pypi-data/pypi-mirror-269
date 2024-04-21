from huffify.abstract import IEncoder


class MVPEncoder(IEncoder):
    def _build_bytes_string_from_table(
        self, encoding_table: dict[str, str], message: str
    ) -> str:
        bytes_string = "".join([encoding_table[char] for char in message])
        return bytes_string

    def _make_bytes_partition(self, bytes_string: str) -> bytearray:
        encoded_stream = ["0"]
        if not bytes_string:
            return bytearray((0,))
        elif len(bytes_string) < 8:
            additional_len = len(bytes_string) % 8
            byte = (additional_len, int(bytes_string, 2))
            return bytearray(byte)
        additional_len = len(bytes_string) % 8
        required_len = len(bytes_string) - additional_len
        for i in range(0, required_len, 8):
            encoded_stream.append(bytes_string[i : i + 8])
        if additional_len:
            encoded_stream[0] = bin(additional_len)[2:]
            encoded_stream.append(bytes_string[-additional_len:])
        return bytearray(map(lambda x: int(x, 2), encoded_stream))

    def encode_string(self, encoding_table: dict[str, str], message: str) -> bytearray:
        bytes_string = self._build_bytes_string_from_table(encoding_table, message)
        encoded_message = self._make_bytes_partition(bytes_string)
        return encoded_message

    def decode_string(self, encoding_table: dict[str, str], encoded_message: bytearray) -> str:
        encoding_table = {code: char for char, code in encoding_table.items()}
        bytes_container: list[str] = []
        external_byte_count = encoded_message[0]
        if external_byte_count:
            _encoded_message = encoded_message[1:-1]
        else:
            _encoded_message = encoded_message[1:]
        for byte in _encoded_message:
            bin_repr = bin(byte)[2:]
            missing_zeros = 0
            if len(bin_repr) != 8:
                missing_zeros = 8 - len(bin_repr) % 8
            byte_str = "0" * missing_zeros + bin_repr
            bytes_container.append(byte_str)
        if external_byte_count:
            byte_str = bin(encoded_message[-1])[2:]
            additional_zeroes = external_byte_count - len(byte_str)
            if len(byte_str) != external_byte_count:
                byte_str = additional_zeroes * "0" + byte_str
            bytes_container.append(byte_str)
        bytes_string = "".join(bytes_container)
        current_code = ""
        decoded_message = ""
        for num in bytes_string:
            current_code += num
            if encoding_table.get(current_code):
                decoded_message += encoding_table[current_code]
                current_code = ""

        return decoded_message
