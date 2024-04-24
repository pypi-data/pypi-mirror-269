"""
     implementation
"""

import typing as _typing
import random as _random


class CRC:
    """
    Cyclic Redundancy Check class
    """
    def __init__(self, message: str, key: str) -> None:
        """
        __init__ method
        """
        self.message = message
        self.key = key
    
    def _xor(self, data_1: str, data_2: str) -> str:
        """
        Find XOR between two massages
        """
        return ''.join(['0' if data_1[i] == data_2[i] else '1' for i in range(1, len(data_2))])

    def _mod_2_div(self, dividend: str) -> str:
        """
        Find mod 2
        """
        pick = len(self.key)
        tmp = dividend[0:pick]

        while pick < len(dividend):
            if tmp[0] == '1':
                tmp = self._xor(self.key, tmp) + dividend[pick]
            else:
                tmp = self._xor('0' * pick, tmp) + dividend[pick]
            pick += 1
        if tmp[0] == '1':
            tmp = self._xor(self.key, tmp)
        else:
            tmp = self._xor('0' * pick, tmp)
        checkword = tmp
        return checkword

    def _encode_data(self) -> _typing.Tuple[str, str]:
        """
        Encode process
        """
        l_key = len(self.key)

        appended_data = self.message + '0' * (l_key - 1)
        remainder = self._mod_2_div(appended_data)

        codeword = self.message + remainder
        return (codeword, remainder)

    def _decode_data(self, encoded_data: str) -> _typing.Tuple[str, str]:
        """
        Decode process
        """
        l_key = len(self.key)

        remainder = self._mod_2_div(encoded_data)
        return (encoded_data[:(len(encoded_data) - len(remainder))], remainder)
    
    def _display(self) -> None:
        """
        Display results
        """
        encoded_data_items = self._encode_data()
        encoded_data, encoded_reminder = encoded_data_items[0], encoded_data_items[1]

        decoded_data_items = self._decode_data(encoded_data)
        decoded_data, decoded_reminder = decoded_data_items[0], decoded_data_items[1]
        print(f'Inner data = {self.message}\nKey = {self.key}\nEncoded data = {encoded_data}\nEncode reminder = {encoded_reminder}\nDecoded data = {decoded_data}\nDecoded reminder = {decoded_reminder}\n{"Data transmitted correctly" if all(i == '0' for i in decoded_reminder) else "Data transmitted corrupt"}')
        return encoded_data

if __name__ == "__main__":
    # text_messgae = "hello"
    # key = "s"
    # crc = CRC(text_messgae, key)
    # encoded_data = crc._display()
    # print()
    # print(crc._bits_message_to_string())
    pass
