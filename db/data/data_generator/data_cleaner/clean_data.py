from parsers import address_reformatter, scraped_data_cleaner

source_file = "raw_data"
dest_file = "cleaned_data"
delimiter = "^"


def clean_data():
    address_reformatter.clean_json(source_file, dest_file, delimiter)
    scraped_data_cleaner.clean_scraped_data(source_file, dest_file, delimiter)

clean_data()