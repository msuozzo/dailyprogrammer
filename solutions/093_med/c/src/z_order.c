#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>


typedef struct file_data {
    char *data;
    size_t length;
} file_data;

file_data *read_file(const char *fname, file_data *out_file) {
    FILE *f = fopen(fname, "r");
    if (ferror(f)) {
        perror("Error opening file");
        return NULL;
    }
    out_file->data = malloc(BUFSIZ);
    size_t capacity = BUFSIZ;
    unsigned bytes_read;
    while ((bytes_read = fread(out_file->data + out_file->length, 1, BUFSIZ, f)) == BUFSIZ) {
        out_file->length += bytes_read;
        if (capacity < out_file->length) {
            capacity <<= 1;
            out_file->data = realloc(out_file->data, capacity);
        }
    }
    out_file->length += bytes_read;
    if (ferror(f)) {
        perror("Error reading file");
        return NULL;
    }
    return out_file;
}


void print_n_bits(unsigned input, unsigned num_bits) {
    for (int j = num_bits; j >= 0; j--) {
        printf("%d", (input & (1 << j)) >> j);
    }
}


unsigned z_order(unsigned row, unsigned col, unsigned dim) {
    unsigned ret = 0;
    unsigned offset, op, bit;
    for (int i = 2 * dim - 1; i >= 0; --i) {
        op = (i % 2) ? row : col;
        offset = i / 2;
        bit = ((op & (1 << offset)) >> offset);
        ret |= bit << i;
    }
    return ret;
}


int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "USAGE: %s {input_fname}\n", argv[0]);
        return 1;
    }
    // Read input
    file_data input_file = {0, 0};
    if (!read_file(argv[1], &input_file)) {
        fprintf(stderr, "Failed to read file");
        return 1;
    }
    printf(input_file.data);
    printf("\n%lu\n", input_file.length);
    if (!input_file.length) {
        fprintf(stderr, "No input provided.");
        return 1;
    }
    unsigned dim = 1, bits = 1;
    while (input_file.length > (dim * dim)) {
        dim <<= 1;
        bits++;
    }
    // Pad input
    unsigned padded_length = dim * dim;
    input_file.data = realloc(input_file.data, padded_length + 1);
    memset(input_file.data + input_file.length, ' ', padded_length - input_file.length);
    input_file.data[padded_length] = '\0';
    input_file.length = padded_length;

    char *output = (char *) malloc(dim * dim);

    for (int i = 0; i < input_file.length; ++i) {
        unsigned z = z_order(i / dim, i % dim, bits);
        output[i] = input_file.data[z];
        printf("%d, %d\t==>\t", i / dim, i % dim);
        print_n_bits(z, 8);
        printf("\n");

    }
    printf("INPUT: %s\n", input_file.data);
    printf("BOXED: \n");
    for (int i = 0; i < input_file.length; ++i) {
        printf("%c", input_file.data[i]);
        if ((i + 1) % dim == 0) {
            printf("\n");
        }
    }
    printf("\n");
    printf("ENCRYPTED: \n");
    for (int i = 0; i < dim * dim; ++i) {
        printf("%c", output[i]);
        if ((i + 1) % dim == 0) {
            printf("\n");
        }
    }

    free(output);
    free(input_file.data);

    return 1;
}
