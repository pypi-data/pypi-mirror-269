"""
Longitudinal redundancy check implementation
"""

import random

def encode_lrc(message_1, message_2, message_3, message_4):
    lrc = ""
    for i in range(len(message_1)):
        message_1_int = int(message_1[i])
        message_2_int = int(message_2[i])
        message_3_int = int(message_3[i])
        message_4_int = int(message_4[i])
        zminna = message_1_int ^ message_2_int ^ message_3_int ^ message_4_int
        lrc += str(zminna)
    return lrc

def generate_blocks(num_blocks, num_messages, message_length):
    blocks = []
    for _ in range(num_blocks):
        block = []
        for _ in range(num_messages):
            message = "".join(str(random.randint(0, 1)) for _ in range(message_length))
            block.append(message)
        blocks.append(block)
    return blocks

def introduce_errors(blocks, error_probability):
    new_blocks = []
    for block in blocks:
        new_block = []
        for message in block:
            new_message = ""
            for i in range(len(message)):
                if random.random() < error_probability:
                    new_message += "0" if message[i] == "1" else "1"
                else:
                    new_message += message[i]
            new_block.append(new_message)
        new_blocks.append(new_block)
    return new_blocks

def detect_errors(block_with_errors, lrc):
    new_lrc = ""
    for i in range(len(block_with_errors[0])):
        message_1_int = int(block_with_errors[0][i])
        message_2_int = int(block_with_errors[1][i])
        message_3_int = int(block_with_errors[2][i])
        message_4_int = int(block_with_errors[3][i])
        zminna = message_1_int ^ message_2_int ^ message_3_int ^ message_4_int
        new_lrc += str(zminna)

    for i in range(len(lrc)):
        if lrc[i] != new_lrc[i]:
            return "Error occured", lrc[i], i


if __name__ == "__main__":
	message_1 = "11100111"
	message_2 = "11011101"
	message_3 = "00111001"
	message_4 = "10101001"
	lrc = encode_lrc(message_1, message_2, message_3, message_4)
	print(lrc)

	num_blocks = 10000
	num_messages = 4
	message_length = 8

	blocks = generate_blocks(num_blocks, num_messages, message_length)
	print("Generated blocks:")
	for block in blocks[:3]:
		print(block)
	
	blocks = generate_blocks(num_blocks, num_messages, message_length)
	print("Generated blocks:")
	for block in blocks[:3]:
		print(block)

	error_probability = 0.3
	block_with_errors = introduce_errors(blocks, error_probability)

	print("Перший блок після введення помилок:")
	for block in block_with_errors[:3]:
		print(block)
	
	for k, block in enumerate(blocks):
		for i in range(0, len(block), 4):
			lrc = encode_lrc(block[i], block[i + 1], block[i + 2], block[i + 3])
			errors = detect_errors(block_with_errors[k], lrc)
			print(errors)
	
	NUM_OF_BLOCKS = 10000
	NUM_OF_MESSAGES_PER_BLOCK = 4
	MESSAGE_LEN = 8

	BLOCKS = generate_blocks(NUM_OF_BLOCKS, NUM_OF_MESSAGES_PER_BLOCK, MESSAGE_LEN)

	ERROR_PROB = 0.3

	BLOCKS_WITH_ERRORS = introduce_errors(BLOCKS, ERROR_PROB)

	for k, block in enumerate(BLOCKS):
		for i in range(0, len(block), 4):
			lrc = encode_lrc(block[i], block[i + 1], block[i + 2], block[i + 3])
			errors = detect_errors(BLOCKS_WITH_ERRORS[k], lrc)
			print(errors)
