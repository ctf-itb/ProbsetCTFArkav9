#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>

#include "md5_simd.cpp"

using namespace std;

array<uint8_t, 56> flag;
array<uint8_t, 16> flag_hash = {${flag_hash}};

int main()
{
    try
    {
        cout << "Flag: ";
        string input;
        cin >> input;
        memcpy(flag.data(), input.data(), flag.size());
        auto digest = MD5::hash_u8(input.substr(0, flag.size()));
        if (digest == flag_hash)
        {
            cout << "Correct\n";
        }
        else
        {
            __asm__ volatile(
                ".cfi_escape 0x16,0x10,${dwarfs}"
            );
            throw 0;
        }
    }
    catch (int i)
    {
        cout << "Wrong\n";
    }
}
