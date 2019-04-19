#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "utils.h"
#include "constants.h"

using namespace std;

long skip_header(char *text) {
        return get_first_occurence(text, "</head>") + 7;
}

long skip_body_tag(char *text) {
        return get_first_occurence(text, ">") + 1;
}

/*
        Function that for a given tag (eg: <sup, <div), builds its
        corresponding closing tag.
        TODO: check if there are any tags without closing pair and consider that
        case
*/
char *build_closing_tag(const char *tag) {
        int len = strlen(tag);
        char *result = (char *) malloc((len + 3) * sizeof(char));

        result[0] = '<';
        result[1] = '/';
        strncpy(result + 2, tag + 1, len - 1);
        result[len + 1] = '>';
        result[len + 2] = '\0';

        return result;
}

/*
        Function that checks if text starts with what
*/
bool compare_next(char *text, char *what) {
        int len = strlen(what);
        char *x = text;
        char *y = what;

        for (int i = 0; i < len; i++) {
                if (*x != *y) {
                        return false;
                }
                x++;
                y++;
        }

        return true;
}

/*
        Given a starting pos in a string, this function will return the
        content of a tag starting at that position. Considering that there
        is no closing tag before the first opening one
*/
char *get_tag_text(char *text, char *tag) {
        char *closing = build_closing_tag(tag);
        char *result;

        int tag_len = strlen(tag);
        int clos_len = strlen(closing);

        long next_pos = get_first_occurence(text + tag_len, tag) + tag_len;
        long close_pos = get_first_occurence(text, closing);
        long tag_end = get_first_occurence(text, '>');
        long len = 0;

        // if there are no more tags like this one
        if (next_pos == -1) {
                len = close_pos - tag_end;
                result = (char *) malloc((len + 1) * sizeof(char));
                strncpy(result, text + tag_end + 1, len - 1);
                result[len] = '\0';
        } else {
                // eg: <div> <div> <div> </div> </div> </div>
                if (next_pos < close_pos) {
                        int no_tags_left = 0; //number of tags - 1 (the first one)

                        while (next_pos < close_pos) {
                                next_pos += get_first_occurence(text + tag_len + next_pos, tag) + tag_len;
                                no_tags_left++;
                        }

                        for (int i = 0; i < no_tags_left; i++) {
                                close_pos += get_first_occurence(text + clos_len + close_pos, closing) + clos_len;
                        }
                }

                len = close_pos - tag_end;
                result = (char *) malloc((len + 1) * sizeof(char));
                strncpy(result, text + tag_end + 1, len - 1);
        }

        free(closing);
        return result;
}

void tests(char *text) {
        /* TEST closing tag */
        cout << "Test closing tags\n===================\n";
        char c1[] = "<h1";
        char c2[] = "<h2";
        char c3[] = "<sup";
        char c4[] = "<span";
        char c5[] = "<div";
        char c6[] = "<table";
        cout << build_closing_tag(c1) << "\n";
        cout << build_closing_tag(c2) << "\n";
        cout << build_closing_tag(c3) << "\n";
        cout << build_closing_tag(c4) << "\n";
        cout << build_closing_tag(c5) << "\n";
        cout << build_closing_tag(c6) << "\n\n";

        /* TEST get text from tag */
        char x1[] = "<title";
        char x2[] = "<script";
        char x3[] = "<div";
        long pos = get_first_occurence(text, x1);
        cout << get_tag_text(text + pos, x1) << "\n";
        pos = get_first_occurence(text, x2);
        cout << get_tag_text(text + pos, x2) << "\n";
        cout << get_tag_text(text + 12309, x3) << "\n";

        cout << get_tag_text(text + 34663, x3) << "\n";
}

int main() {
        FILE *f = fopen("input.html", "rt");

        long size = get_file_size("input.html");
        char *text = (char *) malloc((size + 1) * sizeof( char));

        fread(text, size + 1, 1, f);

        tests(text);

        free(text);
        fclose(f);
        return 0;
}
