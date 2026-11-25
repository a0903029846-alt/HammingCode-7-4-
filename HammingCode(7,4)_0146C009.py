class Hamming74:

    def calculate_redundant_bits(self, m):
        r = 0

        while 2 ** r < m + r + 1:
            r += 1

        return r

    def calculate_parity(self, data):
        code = [0] * 8

        code[3] = int(data[0])
        code[5] = int(data[1])
        code[6] = int(data[2])
        code[7] = int(data[3])

        code[1] = code[3] ^ code[5] ^ code[7]
        code[2] = code[3] ^ code[6] ^ code[7]
        code[4] = code[5] ^ code[6] ^ code[7]

        return code

    def encode(self, data):
        code = self.calculate_parity(data)
        return code[1:]

    def create_error(self, code, error_position):
        received = code.copy()
        received[error_position - 1] ^= 1
        return received

    def check_error(self, received):
        code = [0] + received

        s1 = code[1] ^ code[3] ^ code[5] ^ code[7]
        s2 = code[2] ^ code[3] ^ code[6] ^ code[7]
        s4 = code[4] ^ code[5] ^ code[6] ^ code[7]

        error_position = s1 + s2 * 2 + s4 * 4

        return s1, s2, s4, error_position

    def correct_error(self, received, error_position):
        corrected = received.copy()
        corrected[error_position - 1] ^= 1
        return corrected

    def decode(self, code):
        data = [
            code[2],
            code[4],
            code[5],
            code[6]
        ]

        return ''.join(str(bit) for bit in data)


if __name__ == "__main__":

    ham = Hamming74()

    print("=" * 45)
    print("       Hamming (7,4) Error Correction")
    print("=" * 45)

    while True:
        data = input("\nEnter the Data to be transmitted (4 bits): ")

        if len(data) == 4 and all(bit in "01" for bit in data):
            break

        print("Error! Please enter exactly 4 binary digits.")

    print("\nOriginal Data:", data)

    m = len(data)
    r = ham.calculate_redundant_bits(m)

    print("\n[Step 2] Calculate Redundant Bits")
    print("Number of data bits (m):", m)
    print("Number of redundant bits (r):", r)
    print("Formula: 2^r >= m + r + 1")
    print(f"Total bits = {m} + {r} = {m + r}")

    encoded = ham.encode(data)

    print("\n[Step 3] Determine Parity Bits (Even Parity)")
    print("P1 =", encoded[0])
    print("P2 =", encoded[1])
    print("P4 =", encoded[3])

    print("\nBit Position:")
    print("1  2  3  4  5  6  7")
    print("P1 P2 D1 P4 D2 D3 D4")

    print("\nEncoded Data:")
    print("".join(map(str, encoded)))

    print("\n[Step 4] Create Error Data for Testing")
    print("Enter 1~7 = Flip the corresponding bit")

    while True:
        try:
            error_position = int(
                input("\nWhich bit do you want to change? (1~7): ")
            )

            if 1 <= error_position <= 7:
                break

            print("Please enter a number from 1 to 7.")

        except ValueError:
            print("Please enter a valid integer.")

    received = ham.create_error(encoded, error_position)

    print("\nTransmitted Data:")
    print("".join(map(str, encoded)))

    print("\nReceived Data:")
    print("".join(map(str, received)))

    print("\n[Step 5] Check for Errors")

    s1, s2, s4, detected_position = ham.check_error(received)

    print("\nSyndrome:")
    print(f"S1 = {s1}")
    print(f"S2 = {s2}")
    print(f"S4 = {s4}")
    print(f"Syndrome = {s1}{s2}{s4}")

    print("\n[Step 6] Error Correction")

    if detected_position == 0:
        print("No error detected.")
        corrected = received.copy()
    else:
        print("Error detected!")
        print("Error position:", detected_position)

        corrected = ham.correct_error(
            received,
            detected_position
        )

        print("Error corrected.")

    print("\nCorrected Data:")
    print("".join(map(str, corrected)))

    print("\n[Step 7] Decode")

    original = ham.decode(corrected)

    print("Decoded Data:", original)

    print("\n" + "=" * 45)
    print("             Final Result")
    print("=" * 45)

    print("Original Data :", data)
    print("Encoded Data  :", "".join(map(str, encoded)))
    print("Received Data :", "".join(map(str, received)))
    print("Corrected Data:", "".join(map(str, corrected)))
    print("Decoded Data  :", original)

    if original == data:
        print("\nTransmission successful!")
    else:
        print("\nTransmission failed!")

    print("=" * 45)