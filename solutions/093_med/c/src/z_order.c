#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>


typedef struct string {
    char *data;
    size_t length;
} string;


string *read_file(const char *fname, string *contents) {
    FILE *f = fopen(fname, "r");
    if (f == NULL || ferror(f)) {
        perror("Error opening file");
        return NULL;
    }
    size_t capacity = BUFSIZ;
    contents->data = realloc(NULL, capacity + 1);
    contents->length = 0;
    unsigned bytes_read;
    while ((bytes_read = fread(contents->data + contents->length, 1, BUFSIZ, f)) == BUFSIZ) {
        contents->length += bytes_read;
        if (capacity < contents->length) {
            capacity <<= 1;
            contents->data = realloc(contents->data, capacity + 1);
        }
    }
    contents->length += bytes_read;
    contents->data[contents->length] = '\0';
    if (ferror(f)) {
        perror("Error reading file");
        return NULL;
    }
    return contents;
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


unsigned z_order_rev(unsigned ind, unsigned bits) {
    unsigned ret = 0;
    unsigned offset, base, bit;
    for (int i = 0; i < 2 * bits; ++i) {
        base = (i % 2) ? bits : 0;
        offset = i / 2;
        bit = ((ind & (1 << i)) >> i);
        ret |= (bit << (base + offset));
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


string *encrypt(string *plaintext, string *ciphertext) {
    // Pad the buffer
    unsigned bits = pad_length(plaintext);

    // Create the ciphertext buffer
    ciphertext->data = (char *) calloc(plaintext->length + 1, 1);
    ciphertext->length = plaintext->length;

    // Populate the ciphertext buffer with the Z order indices
    for (int i = 0; i < plaintext->length; ++i) {
        unsigned z = z_order(i, bits);
        ciphertext->data[i] = plaintext->data[z];
    }

    return ciphertext;
}


string *decrypt(string *ciphertext, string *plaintext) {
    // Determine the box dimensions
    unsigned dim = (int) sqrt(ciphertext->length);
    assert(dim * dim == ciphertext->length);
    unsigned bits = 0;
    while ((1 << ++bits) != dim) ;

    // Create the plaintext buffer
    plaintext->data = (char *) calloc(ciphertext->length, 1);
    plaintext->length = ciphertext->length;

    // Populate the ciphertext buffer with the Z order indices
    for (int i = 0; i < plaintext->length; ++i) {
        unsigned z = z_order_rev(i, bits);
        plaintext->data[i] = ciphertext->data[z];
    }

    return plaintext;
}


int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "USAGE: %s -[e,d] {input_fname}\n\t-e  Encrypt file\n\t-d  Decrypt file\n"
                        "\tinput_fname  File to read. NOTE: trailing newline character is enforced.\n", argv[0]);
        return 1;
    }
    // Validate flag
    if (strncmp(argv[1], "-e", 2) && strncmp(argv[1], "-d", 2)) {
        fprintf(stderr, "Invalid flag provided: %s\n", argv[1]);
        return 1;
    }

    // Read input
    string input_file = {NULL, 0};
    if (!read_file(argv[2], &input_file)) {
        fprintf(stderr, "Failed to read file: %s\n", argv[2]);
        return 1;
    } else if (!input_file.length) {
        fprintf(stderr, "No input provided.\n");
        return 1;
    }

    // Remove the trailing newline
    assert(input_file.data[input_file.length - 1] == '\n');
    input_file.data[input_file.length - 1] = '\0';
    input_file.length -= 1;

    // Perform the operation (encryption or decryption)
    string output = {NULL, 0};
    if (!strncmp(argv[1], "-e", 2)) {
        encrypt(&input_file, &output);
    } else {
        decrypt(&input_file, &output);
    }

    // Print the output
    for (int i = 0; i < output.length; ++i) {
        printf("%c", output.data[i]);
    }
    printf("\n");

    free(output.data);
    free(input_file.data);

    return 0;
}
