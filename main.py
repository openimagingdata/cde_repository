import logging
import json
import os
from api_caller import APICaller
from jsonschema import validate, ValidationError
from logger_config import setup_logger

def main():
    logger = setup_logger()
    try:
        api_url = "https://api3.rsna.org/radelement/v1/sets"
        temp_dir = "temp_data"
        os.makedirs(temp_dir, exist_ok=True)
        output_json_file = os.path.join(temp_dir, "api_data.json")
        api_caller = APICaller(api_url, output_json_file, logger)
        api_caller.fetch_and_store_api_data()

        log_total_items(output_json_file)

        # Call clean_data function
        input_file = output_json_file
        output_file = os.path.join(temp_dir, "clean_api_data.json")
        clean_data(input_file, output_file)
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")


def log_total_items(json_file):
    logger = logging.getLogger(__name__)
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            total_items = len(data)
            logger.info(f"Total number of items: {total_items}")
    except Exception as e:
        logger.error(f"An error occurred while reading {json_file}: {e}")


def clean_data(input_file: str, output_file: str):
    # Read the existing JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Remove items with an empty list of index_codes
    cleaned_data = [item for item in data if item.get('index_codes')]

    # Write the cleaned data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    # Log the total item count of the cleaned data
    logging.info(f'Total items after cleaning: {len(cleaned_data)}')

    # Create directories if they don't exist
    os.makedirs('cde_sets', exist_ok=True)
    os.makedirs('cde_sets_docs', exist_ok=True)
    os.makedirs('invalid_cde_sets', exist_ok=True)

    # Load the schema from the cde_schema directory
    with open(os.path.join('cde_schema', 'cde.schema.json'), 'r') as schema_file:
        schema = json.load(schema_file)

    # Create separate JSON and Markdown files for each valid item
    for item in cleaned_data:
        item_id = item.get('id')
        if item_id:
            try:
                # Validate the item against the schema
                validate(instance=item, schema=schema)
                item_json_file = os.path.join('cde_sets', f"{item_id}.json")
                item_md_file = os.path.join('cde_sets_docs', f"{item_id}.md")

                # Write the item data to a JSON file
                with open(item_json_file, 'w') as f:
                    json.dump(item, f, indent=4)
                logging.info(f"Created JSON file for item ID: {item_id}")

                # Write the item data to a Markdown file
                with open(item_md_file, 'w') as f:
                    f.write(f"# Item ID: {item_id}\n\n")
                    f.write(f"- **Name**: {item.get('name', 'N/A')}\n")
                    f.write(f"- **Number**: {item.get('number', 'N/A')}\n\n")
                    f.write("## Metadata\n\n")
                    f.write(f"- **Type**: {item.get('type', 'N/A')}\n")
                    f.write(
                        f"- **Category**: {item.get('category', 'N/A')}\n\n")
                    f.write("## Elements\n\n")
                    elements = item.get('elements', [])
                    for idx, element in enumerate(elements, start=1):
                        f.write(f"{idx}. {element}\n")
                    f.write("\n[JSON File](../cde_sets/{item_id}.json)\n")
                logging.info(f"Created Markdown file for item ID: {item_id}")
            except ValidationError as e:
                # Handle validation errors
                invalid_json_file = os.path.join(
                    'invalid_cde_sets', f"{item_id}.json")
                error_file = os.path.join('invalid_cde_sets', f"{item_id}.txt")

                # Write the invalid item data to a JSON file
                with open(invalid_json_file, 'w') as f:
                    json.dump(item, f, indent=4)
                logging.error(f"Validation failed for item ID: {item_id}")

                # Write the validation error to a text file
                with open(error_file, 'w') as f:
                    f.write(f"Validation error for item ID: {item_id}\n")
                    for error in e.schema_path:
                        f.write(f"Error in property: {error}\n")
                    f.write(str(e))
                logging.info(f"Created error file for item ID: {item_id}")


if __name__ == "__main__":
    main()
