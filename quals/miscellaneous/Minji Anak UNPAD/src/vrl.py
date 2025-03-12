import base64, os, json, hmac, hashlib, asyncio, socket

FLAG = "ARKAV{mmm_hmm_wh4t's_y0ur_ET4?!}"
FLAG_BYTES = FLAG.encode()
ROTATIONS = 3

class PAD:
    def __init__(self, data: bytes):
        self.data = data
        self.key_schedule = []

    def generate_key_schedule(self, seed: bytes):
        keys = []
        current = seed

        for _ in range(ROTATIONS):
            h = hmac.new(current, self.data, hashlib.sha256)
            derived_key = h.digest()[:len(self.data)]
            keys.append(derived_key)
            current = derived_key

        return keys

    def encrypt(self):
        seed = os.urandom(32)
        self.key_schedule = self.generate_key_schedule(seed)

        result = self.data
        for round_key in self.key_schedule:
            result = bytes(a ^ b for a, b in zip(result, round_key))
            rotation = (round_key[0] % (len(result) - 1)) + 1
            result = result[rotation:] + result[:rotation]

        if any(x == p for x, p in zip(result, self.data)):
            raise AssertionError("Direct leak found")

        return result

def encrypt_flag():
    encryptor = PAD(FLAG_BYTES)
    return encryptor.encrypt()

class Challenge:
    def __init__(self):
        self.before_input = b"Give me your favorite songs!\n"
        self.exit = False

    async def handle_request(self, reader, writer):
        writer.write(self.before_input)
        await writer.drain()

        data = await reader.read(1024)
        message = data.decode().strip()

        try:
            input_json = json.loads(message)
            if input_json == {"msg": "request"}:
                try:
                    ciphertext = encrypt_flag()
                    response = {"ciphertext": base64.b64encode(ciphertext).decode()}
                except AssertionError:
                    response = {"error": "Encryption failed - leak detected"}
            else:
                response = {"error": "Invalid request"}
        except json.JSONDecodeError:
            response = {"error": "Invalid input"}

        writer.write((json.dumps(response) + "\n").encode())
        await writer.drain()
        writer.close()

async def main():
    host = socket.gethostbyname(socket.gethostname())
    port = 8090

    server = await asyncio.start_server(
        Challenge().handle_request, host, port
    )
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())