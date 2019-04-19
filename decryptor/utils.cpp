#include <stdio.h>
#include <string.h>
#include "utils.h"

int get_file_size(const char *filename) // path to file
{
        FILE *p_file = NULL;
        p_file = fopen(filename, "rt");
        fseek(p_file, 0, SEEK_END);
        int size = ftell(p_file);
        fclose(p_file);
        return size;
}

void fill_longest_prefix_suffix(char *pattern, int M, int *lps) {
        int len = 0, i = 1;
        lps[0] = 0;

        char *patt_end = &pattern[len];
        char *patt_start = &pattern[i];

        while (i < M) {
                if (*patt_end == *patt_start) {
                        len++;
                        lps[i] = len;
                        i++;
                        patt_end++;
                        patt_start++;
                } else {
                        if (len != 0) {
                                len = lps[len - 1];
                        } else {
                                lps[i] = 0;
                                i++;
                                patt_start++;
                        }
                }
        }
}

/*
        KMP algorithm that gives the first occurence of a substring
*/
long get_first_occurence(char *source, char *what) {
        long M = strlen(what);
        long N = strlen(source);

        int lps[M];
        fill_longest_prefix_suffix(what, M, lps);

        char *src = &source[0];
        char *patt = &what[0];

        long i = 0, j = 0;
        while (i < N) {
                if (*patt == *src) {
                        i++;
                        j++;
                        src++;
                        patt++;
                }

                if (j == M ) {
                        return i - j;
                } else if (i < N && *src != *patt) {
                        if (j != 0) {
                                j = lps[j - 1];
                                patt = &what[j];
                        } else {
                                i++;
                                src++;
                        }
                }
        }

        return -1;
}

long get_first_occurence(char *source, char what) {
        long len = strlen(source);
        char *src = source;
        for (long i = 0; i < len; i++) {
                if (what == *src) {
                        return i;
                }
                src++;
        }

        return -1;
}
