#include <stdio.h>
#include <stdlib.h>


/*
ASCII lower case letters are stored in the format 0bXX0XXXXX
whereas uppercase letters in the format 0bXX1XXXXX
where all X's held the same, the 6th bit simply determines the case of the letter.
This code converts a letter to lowercase by utilizing this property.
*/
char toLowerCase(char c) {
    if(c < 65 || c > 90) {
        return c;
    }
    char mask = 1;
    mask <<= 5;
    return c | mask;
}

/*
ASCII lower case letters are stored in the format 0bXX0XXXXX
whereas uppercase letters in the format 0bXX1XXXXX
where all X's held the same, the 6th bit simply determines the case of the letter.
This code converts a letter to uppercase by utilizing this property.
*/
char toUpperCase(char c) {
    if(c < 97 || c > 122) {
        return c;
    } 
    char mask = 1;
    mask <<= 5;
    return c ^ mask;
}

/*
Given a char array of a single word, convert it to upper camel case, that is, capitalize the first letter of the first word
and lowercase all else.
*/
char *stringToCamelCase(char *string, int length) {
    char *output = malloc(sizeof(char)*length);
    for(int i = 0; i < length; i++) {
        char c = string[i];
        if (c == '\0') {
            break;
        }
        if(i == 0) {
            output[i] = toUpperCase(c);
        } else {
            output[i] = toLowerCase(c);
        }
    }
    return output;
}




int main() {

}
