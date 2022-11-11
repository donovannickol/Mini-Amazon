#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

char **firstnames = NULL;
int num_firstnames = 18239;

char **lastnames = NULL;
int num_lastnames = ;

char **emaildomains = NULL;
int num_emaildomains = 0;

typedef struct Profile {
    char *fullname;
    char *firstname;
    char *lastname;
    char *email;
    int age;
    char *address;
    char *city;
    char *state;
}

/*********

UTILITY FUNCTIONS

********/

/*
Extract substring of original string from start index (inclusive) to end index (exclusive)
*/
char *splice_string(char *original, int start_index, int end_index) {
    int subsize = end_index - start_index;
    char *outputstring = (char *) malloc(sizeof(subsize));
    memcpy(outputstring, &original[start_index], subsize);
    outputstring[subsize] = '\0';
    return outputstring;
}

/*
Given a year, determine if it is a leap year
*/
int is_leap_year(int year) {
    if (year % 400 == 0) {
        return 1;
    } else if (year % 100 == 0) {
        return 0;
    } else if (year % 4 == 0) {
        return 1;
    } else {
        return 0;
    }
}

/*
Return an integer value contained within a stirng
*/
int get_val(char *int_string) {
    return atoi(int_string);
}

/*
Given a year and a month, return how many days are in that month.
If it is a leap year, there rae 29 days in february, otherwise 28.
*/
int num_days_in_month(int year, int month) {
    if(month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
        return 31;
    } else if(month == 4 || month == 6 || month == 9 || month == 11) {
        return 30;
    } else if(is_leap_year(year)) {
        return 29;
    } else {
        return 28;
    }
}


/*
Generate a random number in a given range
https://stackoverflow.com/questions/822323/how-to-generate-a-random-int-in-c
*/
int random_number(int min_num, int max_num)
{
    int result = 0, low_num = 0, hi_num = 0;

    if (min_num < max_num)
    {
        low_num = min_num;
        hi_num = max_num + 1;
    } else {
        low_num = max_num + 1;
        hi_num = min_num;
    }

    srand(time(NULL));
    result = (rand() % (hi_num - low_num)) + low_num;
    return result;
}

/* Returns a random line (w/o newline) from the file provided */
char* choose_random_word(const char *filename) {
    FILE *f;
    size_t lineno = 0;
    size_t selectlen;
    char selected[256]; /* Arbitrary, make it whatever size makes sense */
    char current[256];
    selected[0] = '\0'; /* Don't crash if file is empty */

    f = fopen(filename, "r"); /* Add your own error checking */
    while (fgets(current, sizeof(current), f)) {
        if (drand48() < 1.0 / ++lineno) {
            strcpy(selected, current);
        }
    }
    fclose(f);
    selectlen = strlen(selected);
    if (selectlen > 0 && selected[selectlen-1] == '\n') {
        selected[selectlen-1] = '\0';
    }
    return strdup(selected);
}

char **readwords(char *filename) {
    int max_line_size = 100;
    FILE *fp = fopen(filename, "r");
    int num_lines = 0;
    for (char c = getc(fp); c != EOF; c = getc(fp)) {
        if (c == '\n')  {
            num_lines += 1;
        }
    }
    fclose(fp);
    char **output_words = (char**) (malloc(sizeof(char)*num_lines));

    fp = fopen(filename, "r");
    for(int i = 0; i < num_lines; i++) {
        output_words[i] = (char *) malloc(sizeof(char)*num_lines);
        fscanf(fp, "%s", output_words[i]);
    }
    return output_words;
}

/***

APIs

***/


/*
Get a random date between start and end dates, both inclusive. 
*/
char* date_between(char *start_date, char *end_date) {
    char *start_year_string = splice_string(start_date, 0, 4);
    char *start_month_string = splice_string(start_date, 5,7);
    char *start_day_string = splice_string(start_date, 8,10);
    int start_year = get_val(start_year_string);
    int start_month = get_val(start_month_string);
    int start_day = get_val(start_day_string);
    start_year_string = NULL;
    start_month_string = NULL;
    start_day_string = NULL;
    free(start_year_string);
    free(start_month_string);
    free(start_day_string);

    char *end_year_string =splice_string(end_date, 0, 4);
    char *end_month_string = splice_string(end_date, 5,7);
    char *end_day_string = splice_string(end_date, 8,10);
    int end_year = get_val(end_year_string);
    int end_month = get_val(end_month_string);
    int end_day = get_val(end_day_string);
    end_year_string = NULL;
    end_month_string = NULL;
    end_day_string = NULL;
    free(end_year_string);
    free(end_month_string);
    free(end_day_string);

    if(start_year > end_year) {
        int temp = end_year;
        end_year = start_year;
        start_year = temp;
    }
    if(start_year == end_year && start_month > end_month) {
        int temp = end_month;
        end_month = start_month;
        start_month = temp;
    }
    if(start_year == end_year && start_month == end_month && start_day >= end_day) {
        if(start_day == end_day) {
            return start_date;
        } else{
            int temp = end_day;
            end_day = start_day;
            start_day = temp;
        }
    }

    int output_year = random_number(start_year, end_year);
    int output_month;
    if(output_year == end_year && output_year == start_year) {
        output_month = random_number(start_month, end_month);
    } else if(output_year == start_year) {
        output_month = random_number(start_month, 12);
    } else if(output_year == end_year) {
        output_month = random_number(1,end_month);
    } else {
        output_month = random_number(1,12);
    }

    int max_num_days = num_days_in_month(output_year, output_month);
    int output_day;
    if(output_month == start_month && output_month == start_month) {
        output_day = random_number(start_day, end_day);
    } else if(output_month == start_month) {
        output_day = random_number(start_day,max_num_days);
    } else if(output_month == end_month) {
        output_day = random_number(1, end_day);
    } else {
        output_day = random_number(1,max_num_days);
    }

    char output_year_string[5];
    sprintf(output_year_string, "%d", output_year); 
    char output_month_string[3];
    sprintf(output_month_string, "%d", output_month); 
    char output_day_string[3];
    sprintf(output_day_string, "%d", output_day); 

    char *output_date_string = (char *) malloc(sizeof(char)*11);
    strcpy(output_date_string, output_year_string);
    strcat(output_date_string, "-");
    strcat(output_date_string, output_month_string);
    strcat(output_date_string, "-");
    strcat(output_date_string, output_day_string);
    output_date_string[10] = '\0';
    return output_date_string;
}


/*
Return a random date
*/
char *date() {
    char *default_start = "1974-01-01";
    char *default_end = "2022-11-10";
    return date_between(default_start, default_end);
}


/*
Return a random date starting from a given date
*/
char *date_from(char *start_date) {
    char *default_end = "2022-11-10";
    return date_between(start_date, default_end);
}

/*
Return a random date before a given date
*/
char *date_before(char *end_date) {
    char *default_start = "1974-01-01";
    return date_between(default_start, end_date);
}


char *firstname() {
    if (firstnames == NULL) {
        firstnames = readwords("names/firstnames.txt");
    }
    int index = random_number(0, num_firstnames - 1);
    return NULL;
}

char *lastname() {
    if (lastnames == NULL) {
        lastnames = readwords("names/lastnames.txt");
    }
    return NULL;
}

char *emaildomain() {
    if (lastnames == NULL) {
        emaildomains = readwords("emaildomains.txt");
    }
    return NULL;
}




// int main() {
//     // printf("%s\n", date());
//     readwords("names/firstnames.txt");
// }