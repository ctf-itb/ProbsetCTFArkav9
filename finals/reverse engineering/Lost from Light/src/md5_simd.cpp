#include <array>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <immintrin.h>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

class MD5
{
  public:
    MD5()
    {
        init();
    }

    static std::string hash(const std::string &input)
    {
        MD5 md5;
        md5.digest(input.data(), input.size());
        return md5.getHashString();
    }

    static std::array<uint8_t, 16> hash_u8(const std::string &input)
    {
        MD5 md5;
        md5.digest(input.data(), input.size());
        return md5.getHash();
    }

    void digest(const void *buffer, size_t size)
    {
        const uint8_t *bytes = static_cast<const uint8_t *>(buffer);
        uint64_t message_bits = size * 8;

        __m128i current_state = _mm_loadu_si128(reinterpret_cast<const __m128i *>(state.data()));

        size_t num_full_blocks = size / 64;
        if (num_full_blocks > 0)
        {
            processBlocks(bytes, num_full_blocks, current_state);
            bytes += num_full_blocks * 64;
            size -= num_full_blocks * 64;
        }

        _mm_storeu_si128(reinterpret_cast<__m128i *>(state.data()), current_state);

        std::array<uint8_t, 128> scratch{};
        memcpy(scratch.data(), bytes, size);

        scratch[size] = 0x80;
        if (size >= 56)
        {
            transformBlock(scratch.data());
            memset(scratch.data(), 0, 56);
        }

        memcpy(scratch.data() + 56, &message_bits, 8);

        transformBlock(scratch.data());
    }

    std::array<uint8_t, 16> getHash() const
    {
        std::array<uint8_t, 16> result;
        memcpy(result.data(), state.data(), 16);
        return result;
    }

    std::string getHashString() const
    {
        auto bytes = getHash();
        std::stringstream ss;
        ss << std::hex << std::setfill('0');

        for (auto byte : bytes)
        {
            ss << std::setw(2) << static_cast<int>(byte);
        }

        return ss.str();
    }

    void init()
    {
        state[0] = 0x67452301;
        state[1] = 0xEFCDAB89;
        state[2] = 0x98BADCFE;
        state[3] = 0x10325476;
    }

  private:
    alignas(16) std::array<uint32_t, 4> state;

    alignas(32) static constexpr uint32_t K[64] = {
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391};

    alignas(32) static constexpr uint8_t S[64] = {7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                                                  5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20,
                                                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                                                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};

    alignas(32) static constexpr uint8_t X_INDEX[64] = {0, 1, 2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15,
                                                        1, 6, 11, 0,  5,  10, 15, 4,  9,  14, 3,  8,  13, 2,  7,  12,
                                                        5, 8, 11, 14, 1,  4,  7,  10, 13, 0,  3,  6,  9,  12, 15, 2,
                                                        0, 7, 14, 5,  12, 3,  10, 1,  8,  15, 6,  13, 4,  11, 2,  9};

    void processBlocks(const uint8_t *data, size_t numBlocks, __m128i &state_vec)
    {
        for (size_t i = 0; i < numBlocks; i++)
        {
            transformBlockSIMD(data + i * 64, state_vec);
        }
    }

    void transformBlockSIMD(const uint8_t *block, __m128i &state_vec)
    {
        assert(block != nullptr);

        __m128i abcd = state_vec;

        uint32_t a = _mm_extract_epi32(abcd, 0);
        uint32_t b = _mm_extract_epi32(abcd, 1);
        uint32_t c = _mm_extract_epi32(abcd, 2);
        uint32_t d = _mm_extract_epi32(abcd, 3);

        __m256i X_0_7 = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(block));
        __m256i X_8_15 = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(block + 32));

        alignas(32) uint32_t X[16];
        _mm256_store_si256(reinterpret_cast<__m256i *>(&X[0]), X_0_7);
        _mm256_store_si256(reinterpret_cast<__m256i *>(&X[8]), X_8_15);

        __m256i K_0_7 = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(&K[0]));
        __m256i K_8_15 = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(&K[8]));

        for (int i = 0; i < 64; i++)
        {
            uint32_t f;
            uint32_t g;

            if (i < 16)
            {
                f = (b & c) | (~b & d);
                g = i;
            }
            else if (i < 32)
            {
                f = (b & d) | (c & ~d);
                g = (5 * i + 1) % 16;
            }
            else if (i < 48)
            {
                f = b ^ c ^ d;
                g = (3 * i + 5) % 16;
            }
            else
            {
                f = c ^ (b | ~d);
                g = (7 * i) % 16;
            }

            uint32_t temp = d;
            d = c;
            c = b;
            b = b + leftRotate((a + f + K[i] + X[g]), S[i]);
            a = temp;
        }

        __m128i transformed = _mm_set_epi32(d, c, b, a);
        state_vec = _mm_add_epi32(state_vec, transformed);
    }

    void transformBlock(const uint8_t *block)
    {
        assert(block != nullptr);

        uint32_t a = state[0];
        uint32_t b = state[1];
        uint32_t c = state[2];
        uint32_t d = state[3];

        alignas(32) uint32_t X[16];
        memcpy(X, block, 64);

        for (int i = 0; i < 64; i++)
        {
            uint32_t f;
            uint32_t g;

            if (i < 16)
            {
                f = (b & c) | (~b & d);
                g = i;
            }
            else if (i < 32)
            {
                f = (b & d) | (c & ~d);
                g = (5 * i + 1) % 16;
            }
            else if (i < 48)
            {
                f = b ^ c ^ d;
                g = (3 * i + 5) % 16;
            }
            else
            {
                f = c ^ (b | ~d);
                g = (7 * i) % 16;
            }

            uint32_t temp = d;
            d = c;
            c = b;
            b = b + leftRotate((a + f + K[i] + X[g]), S[i]);
            a = temp;
        }

        state[0] += a;
        state[1] += b;
        state[2] += c;
        state[3] += d;
    }

    void processBlocksAVX2(const uint8_t *blocks, size_t numBlocks)
    {
        if (numBlocks < 8)
        {
            for (size_t i = 0; i < numBlocks; i++)
            {
                transformBlock(blocks + i * 64);
            }
            return;
        }

        size_t fullChunks = numBlocks / 8;

        __m256i a_vec = _mm256_set1_epi32(state[0]);
        __m256i b_vec = _mm256_set1_epi32(state[1]);
        __m256i c_vec = _mm256_set1_epi32(state[2]);
        __m256i d_vec = _mm256_set1_epi32(state[3]);

        for (size_t chunk = 0; chunk < fullChunks; chunk++)
        {
            const uint8_t *chunk_blocks = blocks + chunk * 8 * 64;

            __m256i aa = a_vec;
            __m256i bb = b_vec;
            __m256i cc = c_vec;
            __m256i dd = d_vec;

            alignas(32) uint32_t X[8][16];

            for (int i = 0; i < 8; i++)
            {
                memcpy(X[i], chunk_blocks + i * 64, 64);
            }

            for (int i = 0; i < 64; i++)
            {
                __m256i f_vec;
                int g;

                if (i < 16)
                {
                    f_vec = _mm256_or_si256(
                        _mm256_and_si256(b_vec, c_vec),
                        _mm256_and_si256(_mm256_xor_si256(b_vec, _mm256_set1_epi32(0xFFFFFFFF)), d_vec));
                    g = i;
                }
                else if (i < 32)
                {
                    f_vec = _mm256_or_si256(
                        _mm256_and_si256(b_vec, d_vec),
                        _mm256_and_si256(c_vec, _mm256_xor_si256(d_vec, _mm256_set1_epi32(0xFFFFFFFF))));
                    g = (5 * i + 1) % 16;
                }
                else if (i < 48)
                {
                    f_vec = _mm256_xor_si256(_mm256_xor_si256(b_vec, c_vec), d_vec);
                    g = (3 * i + 5) % 16;
                }
                else
                {
                    f_vec = _mm256_xor_si256(
                        c_vec, _mm256_or_si256(b_vec, _mm256_xor_si256(d_vec, _mm256_set1_epi32(0xFFFFFFFF))));
                    g = (7 * i) % 16;
                }

                __m256i X_g = _mm256_setr_epi32(X[0][g], X[1][g], X[2][g], X[3][g], X[4][g], X[5][g], X[6][g], X[7][g]);

                __m256i temp = d_vec;
                d_vec = c_vec;
                c_vec = b_vec;

                __m256i sum = _mm256_add_epi32(a_vec, f_vec);
                sum = _mm256_add_epi32(sum, _mm256_set1_epi32(K[i]));
                sum = _mm256_add_epi32(sum, X_g);

                __m256i rotated = leftRotate256(sum, S[i]);
                b_vec = _mm256_add_epi32(b_vec, rotated);

                a_vec = temp;
            }

            a_vec = _mm256_add_epi32(a_vec, aa);
            b_vec = _mm256_add_epi32(b_vec, bb);
            c_vec = _mm256_add_epi32(c_vec, cc);
            d_vec = _mm256_add_epi32(d_vec, dd);
        }

        for (size_t i = fullChunks * 8; i < numBlocks; i++)
        {
            transformBlock(blocks + i * 64);
            return;
        }

        alignas(32) uint32_t a_out[8], b_out[8], c_out[8], d_out[8];

        _mm256_store_si256(reinterpret_cast<__m256i *>(a_out), a_vec);
        _mm256_store_si256(reinterpret_cast<__m256i *>(b_out), b_vec);
        _mm256_store_si256(reinterpret_cast<__m256i *>(c_out), c_vec);
        _mm256_store_si256(reinterpret_cast<__m256i *>(d_out), d_vec);

        state[0] = a_out[0];
        state[1] = b_out[0];
        state[2] = c_out[0];
        state[3] = d_out[0];
    }

    static inline uint32_t leftRotate(uint32_t x, uint32_t c)
    {
        return (x << c) | (x >> (32 - c));
    }

    static inline __m256i leftRotate256(__m256i x, uint32_t c)
    {
        return _mm256_or_si256(_mm256_slli_epi32(x, c), _mm256_srli_epi32(x, 32 - c));
    }

    void unpackBlocks(const uint8_t *blocks, uint32_t X[][16], int numBlocks)
    {
        for (int b = 0; b < numBlocks; b++)
        {
            const uint32_t *block_words = reinterpret_cast<const uint32_t *>(blocks + b * 64);
            for (int w = 0; w < 16; w++)
            {
                X[b][w] = block_words[w];
            }
        }
    }
};
