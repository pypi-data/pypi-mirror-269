import pytest
import numpy as np
from numpy.typing import NDArray
from AES_Python import AES


@pytest.mark.parametrize("data,key,expected", [
    # 128 bit
    ("6bc1bee22e409f96e93d7e117393172a", "2b7e151628aed2a6abf7158809cf4f3c", "3ad77bb40d7a3660a89ecaf32466ef97"),
    ("ae2d8a571e03ac9c9eb76fac45af8e51", "2b7e151628aed2a6abf7158809cf4f3c", "f5d3d58503b9699de785895a96fdbaaf"),
    ("30c81c46a35ce411e5fbc1191a0a52ef", "2b7e151628aed2a6abf7158809cf4f3c", "43b1cd7f598ece23881b00e3ed030688"),
    ("f69f2445df4f9b17ad2b417be66c3710", "2b7e151628aed2a6abf7158809cf4f3c", "7b0c785e27e8ad3f8223207104725dd4"),
    # 192 bit
    ("6bc1bee22e409f96e93d7e117393172a", "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "bd334f1d6e45f25ff712a214571fa5cc"),
    ("ae2d8a571e03ac9c9eb76fac45af8e51", "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "974104846d0ad3ad7734ecb3ecee4eef"),
    ("30c81c46a35ce411e5fbc1191a0a52ef", "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "ef7afd2270e2e60adce0ba2face6444e"),
    ("f69f2445df4f9b17ad2b417be66c3710", "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "9a4b41ba738d6c72fb16691603c18e0e"),
    # 256 bit
    ("6bc1bee22e409f96e93d7e117393172a", "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "f3eed1bdb5d2a03c064b5a7e3db181f8"),
    ("ae2d8a571e03ac9c9eb76fac45af8e51", "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "591ccb10d410ed26dc5ba74a31362870"),
    ("30c81c46a35ce411e5fbc1191a0a52ef", "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "b6ed21b99ca6f4f9f153e7b1beafed1d"),
    ("f69f2445df4f9b17ad2b417be66c3710", "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "23304b7a39f9f3ff067d8d8f9e24ecc7"),
])
def test_enc_schedule(data, key: str, expected: str) -> None:
    # Formats input data
    data = np.frombuffer(bytes.fromhex(data), dtype=np.uint8).reshape(4, 4)

    # Creates round keys
    round_keys: NDArray[np.uint8] = AES.key_expand(key)

    # Runs decryption
    result: NDArray[np.uint8] = AES()._AES__enc_schedule(data, round_keys)  # type: ignore

    result_formatted = result.astype(np.uint8).tobytes().hex()

    # Evaluates result
    assert result_formatted == expected


@pytest.mark.parametrize("data,key,expected", [
    # 128 bit
    ('1234567890', "2b7e151628aed2a6abf7158809cf4f3c",
     b'|\xc2\x94\x18\xc3\x8f\x1c\xc3\xb0\xc3\xaf\xc2\xa0\xc3\xbf\xc2\xa4\xc2\xbb\xc3\xa9\xc3\x98\xc2\x8am\xc2\xa4'),
    ('1234567890123456', "2b7e151628aed2a6abf7158809cf4f3c",
     b'(>\xc2\xa4JH\xc3\x97\x18\xc2\xa2\xc3\x81\xc3\xb7\xc2\xb7\xc3\xa3\xc2\xbbKJ\xc3\xb8'),
    # 192 bit
    ('1234567890', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     b'K\xc2\x9d\xc3\xa5\xc3\xa9l8&\xc3\x9alO\xc2\xbb\xc3\x83\xc3\xb2\xc3\x83*\xc3\xb2'),
    ('1234567890123456', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     b'\xc3\xb9\x01\xc3\x97\xc3\xa8\xc3\x9c\xc3\xb7\\\xc3\x80\xc3\x88\xc2\xa1*>t\xc2\xabA\xc3\x98'),
    # 256 bit
    ('1234567890', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     b'2 ?\xc3\xabm\xc3\xb5o\xc3\x82\xc2\x8b\xc2\x90\xc2\x80\xc2\x84 D\xc3\x84\xc2\x95'),
    ('1234567890123456', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     b"\xc2\x8cc'\xc3\x88d\xc2\x82\xc2\xb3\xc2\x8cj\xc3\x92\\\xc2\xaa\xc2\x96\xc3\xb1\xc3\xbfi")
])
def test_enc_ecb(data, key, expected):
    aes = AES(key=key)

    assert bytes(aes.enc(data_string=data), "utf-8") == expected


@pytest.mark.parametrize("data,key,iv,expected", [
    # 128 bit
    ('6bc1bee22e409f96e93d7e117393172a', "2b7e151628aed2a6abf7158809cf4f3c",
     "000102030405060708090a0b0c0d0e0f", "7649abac8119b246cee98e9b12e9197d"),
    ('ae2d8a571e03ac9c9eb76fac45af8e51', "2b7e151628aed2a6abf7158809cf4f3c",
     "7649ABAC8119B246CEE98E9B12E9197D", "5086cb9b507219ee95db113a917678b2"),
    ('30c81c46a35ce411e5fbc1191a0a52ef', "2b7e151628aed2a6abf7158809cf4f3c",
     "5086CB9B507219EE95DB113A917678B2", "73bed6b8e3c1743b7116e69e22229516"),
    ('f69f2445df4f9b17ad2b417be66c3710', "2b7e151628aed2a6abf7158809cf4f3c",
     "73BED6B8E3C1743B7116E69E22229516", "3ff1caa1681fac09120eca307586e1a7"),
    # 192 bit
    ('6bc1bee22e409f96e93d7e117393172a', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "000102030405060708090A0B0C0D0E0F", "4f021db243bc633d7178183a9fa071e8"),
    ('ae2d8a571e03ac9c9eb76fac45af8e51', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "4F021DB243BC633D7178183A9FA071E8", "b4d9ada9ad7dedf4e5e738763f69145a"),
    ('30c81c46a35ce411e5fbc1191a0a52ef', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "B4D9ADA9AD7DEDF4E5E738763F69145A", "571b242012fb7ae07fa9baac3df102e0"),
    ('f69f2445df4f9b17ad2b417be66c3710', "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
     "571B242012FB7AE07FA9BAAC3DF102E0", "08b0e27988598881d920a9e64f5615cd"),
    # 256 bit
    ('6bc1bee22e409f96e93d7e117393172a', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "000102030405060708090A0B0C0D0E0F", "f58c4c04d6e5f1ba779eabfb5f7bfbd6"),
    ('ae2d8a571e03ac9c9eb76fac45af8e51', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "F58C4C04D6E5F1BA779EABFB5F7BFBD6", "9cfc4e967edb808d679f777bc6702c7d"),
    ('30c81c46a35ce411e5fbc1191a0a52ef', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "9CFC4E967EDB808D679F777BC6702C7D", "39f23369a9d9bacfa530e26304231461"),
    ('f69f2445df4f9b17ad2b417be66c3710', "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
     "39F23369A9D9BACFA530E26304231461", "b2eb05e2c39be9fcda6c19078c6a9d1b"),
])
def test_enc_cbc(data, key, iv, expected):
    aes = AES(running_mode="CBC", key=key, iv=iv)

    data = "".join([chr(i) for i in bytes.fromhex(data)])

    enc_data = aes.enc(data_string=data)

    assert bytearray([ord(i) for i in enc_data]).hex() == expected
