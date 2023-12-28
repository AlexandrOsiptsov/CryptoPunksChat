#ifndef SHA256_H
#define SHA256_H
#include <cstring>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <cstdint>

// Циклический сдвиг 32-битного бинарного слова a на кол-во бит b
#define ROTRIGHT(a, b) (((a) >> (b)) | ((a) << (32 - (b))))

// Ниже определены функции, используемые алгоритмом

// Ch(X, Y, Z) = (X ^ Y) +(X ^ Z)
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
// Maj(X, Y, Z) = (X ^ Y) +(X ^ Z) +(Y ^ Z)
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
// Σ0(X) = RotR(X, 2) + RotR(X, 13) + RotR(X, 22)
#define EP0(x) (ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22))
// Σ1(X) = RotR(X, 6) + RotR(X, 11) + RotR(X, 25)
#define EP1(x) (ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25))
// σ0(X) = RotR(X, 7) + RotR(X, 18) + ShR(X, 3)
#define SIG0(x) (ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ ((x) >> 3))
// σ1(X) = RotR(X, 17) + RotR(X, 19) + ShR(X, 10)
#define SIG1(x) (ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ ((x) >> 10))

using namespace std;

class SHA256
{
public:
	SHA256() {}
	~SHA256() {}

	// Функционирование объекта класса сводится к воспроизведению
	// одной последовательности действий для каждого нового потока
	// входных данных
	string getHash(const string &data)
	{

		// Инициализация производится в теле фун-ии getHash() с целью
		// обновления конфигурации алгоритма для каждого нового потока
		// входных данных
		blocklen = 0;
		bitlen = 0;
		state[0] = 0x6a09e667;
		state[1] = 0xbb67ae85;
		state[2] = 0x3c6ef372;
		state[3] = 0xa54ff53a;
		state[4] = 0x510e527f;
		state[5] = 0x9b05688c;
		state[6] = 0x1f83d9ab;
		state[7] = 0x5be0cd19;

		compact(data);

		// объявление массива, для хранения в нем значения хэша
		uint8_t *uint_hash = new uint8_t[32];

		// Чтобы убедиться, что входные данные имеют длину, кратную 512 битам, используем паддинг
		pad();

		revert(uint_hash);

		stringstream string_hash;
		string_hash << setfill('0') << std::hex;

		for (uint8_t i = 0; i < 32; i++)
		{
			string_hash << std::setw(2) << (uint32_t)uint_hash[i];
		}
		delete[] uint_hash;
		blocklen = 0;
		bitlen = 0;
		return string_hash.str();
	}

private:
	uint8_t data[64];
	uint32_t blocklen;
	uint64_t bitlen;
	uint32_t state[8];

	uint32_t K[64] = {
		0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

	void compact(const string &data)
	{
		const uint8_t *uint_data = reinterpret_cast<const uint8_t *>(data.c_str());
		int length = data.size();
		for (size_t i = 0; i < length; i++)
		{
			this->data[blocklen++] = uint_data[i];
			if (blocklen == 64)
			{
				transform();

				// End of the block
				bitlen += 512;
				blocklen = 0;
			}
		}
	}

	void transform()
	{
		uint32_t maj, xorA, ch, xorE, sum, newA, newE, m[64];
		uint32_t state[8];

		for (uint8_t i = 0, j = 0; i < 16; i++, j += 4)
		{ // Разделяем данные на 32-битные блоки для 16 первых слов
			m[i] = (this->data[j] << 24) | (this->data[j + 1] << 16) | (this->data[j + 2] << 8) | (this->data[j + 3]);
		}

		for (uint8_t k = 16; k < 64; k++)
		{ // Оставшиеся 48 блоков
			m[k] = SIG1(m[k - 2]) + m[k - 7] + SIG0(m[k - 15]) + m[k - 16];
		}

		for (uint8_t i = 0; i < 8; i++)
		{
			state[i] = this->state[i];
		}
		/*Ниже описаны 64 раунда действий в следующей последовательности :
			T1 = h + Σ1(e) + Ch(e, f, g) + Ki + Wi
			T2 = Σ0(a) + M aj(a, b, c)
			h = g
			g = f
			f = e
			e = d + T1
			d = c
			c = b
			b = a
			a = T1 + T2*/

		for (uint8_t i = 0; i < 64; i++)
		{
			maj = MAJ(state[0], state[1], state[2]);
			xorA = ROTRIGHT(state[0], 2) ^ ROTRIGHT(state[0], 13) ^ ROTRIGHT(state[0], 22);

			ch = CH(state[4], state[5], state[6]);

			xorE = ROTRIGHT(state[4], 6) ^ ROTRIGHT(state[4], 11) ^ ROTRIGHT(state[4], 25);

			sum = m[i] + K[i] + state[7] + ch + xorE;
			newA = xorA + maj + sum;
			newE = state[3] + sum;

			state[7] = state[6];
			state[6] = state[5];
			state[5] = state[4];
			state[4] = newE;
			state[3] = state[2];
			state[2] = state[1];
			state[1] = state[0];
			state[0] = newA;
		}

		// Контактенация частей хеша
		for (uint8_t i = 0; i < 8; i++)
		{
			this->state[i] += state[i];
		}
	}

	void pad()
	{

		// Чтобы убедиться, что входные данные имеют длину, кратную 512 битам:
		//		1)сначала добавляется бит 1,
		//		2)затем добавляется k битов 0, причем k - наименьшее целое положительное число, такое, что l + 1 + k ≡ 448
		//	 mod 512, где l - длина в битах исходного сообщения,
		//		3)Когда длина l < 2^64,исходное сообщение представляется
		//   ровно 64 битами, и эти биты добавляются в конец сообщения.

		uint64_t i = blocklen;
		uint8_t end = blocklen < 56 ? 56 : 64;

		data[i++] = 0x80; // 1)
		while (i < end)
		{
			this->data[i++] = 0x00; // 2)
		}

		if (blocklen >= 56)
		{
			transform();
			memset(this->data, 0, 56);
		}

		// 3)
		bitlen += blocklen * 8;
		this->data[63] = bitlen;
		this->data[62] = bitlen >> 8;
		this->data[61] = bitlen >> 16;
		this->data[60] = bitlen >> 24;
		this->data[59] = bitlen >> 32;
		this->data[58] = bitlen >> 40;
		this->data[57] = bitlen >> 48;
		this->data[56] = bitlen >> 56;
		transform();
	}

	void revert(uint8_t *hash)
	{
		// SHA использует упорядочивание байтов в формате big endian
		// Алгоритм ниже упорядочивает байты в обратном порядке
		for (uint8_t i = 0; i < 4; i++)
		{
			for (uint8_t j = 0; j < 8; j++)
			{
				hash[i + (j * 4)] = (state[j] >> (24 - i * 8)) & 0x000000ff;
			}
		}
	}
};

#endif // SHA256_H