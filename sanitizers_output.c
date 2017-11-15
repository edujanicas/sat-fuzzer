#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main(int argc, char const *argv[])
{
	if(argc >= 2){
		int arg = *argv[1];
		if (arg == '0') {
			//ubsan.c:12:8: runtime error: negation of -2147483648 cannot be represented in type 'int [100]'; cast to an unsigned type to negate this value to itself
			printf("Intmin negated\n");
			int i2 = INT_MIN;
			int j = -i2;
		}	
		else if (arg == '1') {
			//ubsan.c:17:17: runtime error: store to null pointer of type 'int'
			//ASAN:SIGSEGV
			printf("nullPointer dereference\n");
			int *nullPointer;
			*nullPointer = 10;
		}
		else if (arg == '2') {
			//ubsan.c:27:6: runtime error: shift exponent 32 is too large for 32-bit type 'int'
			printf("Bit shift\n");
			int i = 23;
			i <<= 32;
		}
		else if (arg == '3') {
			//==8654==ERROR: AddressSanitizer: heap-use-after-free on address 0x61400000fe48 at pc 0x00000040106b bp 0x7ffd981a3f00 sp 0x7ffd981a3ef0
			printf("Use after free\n");
			int *array = malloc(sizeof(int) * 100);
  			free(array);
  			return array[argc];  // BOOM
		}
		else if (arg == '4') {
			//==8673==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61400000ffd8 at pc 0x000000401181 bp 0x7ffe3d8d7d00 sp 0x7ffe3d8d7cf0
			printf("Heap overflow\n");
			int *array = malloc(sizeof(int) * 100);
  			array[0] = 0;
  			int res = array[argc + 100];  // BOOM
			free(array);
		}
		else if (arg == '5') {
			//==8695==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffcb3734bf8 at pc 0x00000040129a bp 0x7ffcb37349e0 sp 0x7ffcb37349d0
			printf("Stack overflow\n");
			int stack_array[100];
  			stack_array[1] = 0;
  			return stack_array[argc + 100];  // BOOM
		}
	}
	return 0;
}