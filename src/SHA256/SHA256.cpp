#include "SHA256.h"

int main(int argc, char* argv[]) {
	if (argc != 2) {
		cout << "Usage: program_name <input_string>" << std::endl;
		return 1;
	}
	string msg = argv[1];
	SHA256 ctx;
	cout << ctx.getHash(msg);
	return 0;
}