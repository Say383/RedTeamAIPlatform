import os
import json
import logging

# Initialize the logger
logging.basicConfig(filename='report_generator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to generate a report from test results
def generate_report(test_results, report_format="json", output_dir="reports"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        report = None

        if report_format == "json":
            report = generate_json_report(test_results)
        # Add support for more report formats here (e.g., HTML, PDF).

        if report:
            report_filename = f"{output_dir}/test_report.{report_format}"
            with open(report_filename, 'w') as file:
                file.write(report)

            logging.info(f"Generated {report_format} report: {report_filename}")
            return report_filename
        else:
            logging.error(f"Unsupported report format: {report_format}")
            raise Exception(f"Unsupported report format: {report_format}")
    except Exception as e:
        logging.error(f"Failed to generate report. Error: {str(e)}")
        raise Exception("Failed to generate the report")

# Function to generate a JSON report
def generate_json_report(test_results):
    try:
        report = {
            "timestamp": get_current_timestamp(),
            "results": test_results
        }
        return json.dumps(report, indent=4)
    except Exception as e:
        logging.error(f"Failed to generate JSON report. Error: {str(e)}")
        raise Exception("Failed to generate the JSON report")

# Function to get the current timestamp
def get_current_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

