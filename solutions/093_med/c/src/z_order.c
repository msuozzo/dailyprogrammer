#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>


typedef struct string {
    char *data;
    size_t length;
} string;


string *read_file(const char *fname, string *out_file) {
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


unsigned z_order(unsigned ind, unsigned bits) {
    unsigned row = ind / (1 << bits);
    unsigned col = ind % (1 << bits);
    unsigned ret = 0;
    unsigned offset, op, bit;
    for (int i = 2 * bits - 1; i >= 0; --i) {
        op = (i % 2) ? row : col;
        offset = i / 2;
        bit = ((op & (1 << offset)) >> offset);
        ret |= bit << i;
    }
    return ret;
}


unsigned pad_length(string *to_pad) {
    unsigned dim = 1, bits = 0;
    while (to_pad->length > (dim * dim)) {
        dim <<= 1;
        bits++;
    }
    unsigned padded_length = dim * dim;

    to_pad->data = realloc(to_pad->data, padded_length + 1);
    memset(to_pad->data + to_pad->length, ' ', padded_length - to_pad->length);
    to_pad->data[padded_length] = '\0';

    to_pad->length = padded_length;
    return bits;
}


int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "USAGE: %s {input_fname}\n", argv[0]);
        return 1;
    }
    // Read input
    string input_file = {0, 0};
    if (!read_file(argv[1], &input_file)) {
        fprintf(stderr, "Failed to read file");
        return 1;
    } else if (!input_file.length) {
        fprintf(stderr, "No input provided.");
        return 1;
    }
    // Pad the buffer
    unsigned bits = pad_length(&input_file);

    // Create the output buffer
    char *output = (char *) malloc(input_file.length);

    // Populate the output buffer with the Z order indices
    for (int i = 0; i < input_file.length; ++i) {
        unsigned z = z_order(i, bits);
        output[i] = input_file.data[z];
    }
    output[input_file.length] = '\0';
    // Print encrypted text
    for (int i = 0; i < input_file.length; ++i) {
        printf("%c", output[i]);
        if ((i + 1) % (1 << bits) == 0) {
            printf("\n");
        }
    }

    free(output);
    free(input_file.data);

    return 1;
}
