import csv
import datetime
import re

date_regex = re.compile(r"(^\d{2}/\d{2}/\d{4})")

# import transaction data for receipts
nationbuilder_transactions_export_csv = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/nationbuilder-financialtransactions-export-109-2024-10-06.csv",
    "r",
)

reader = csv.DictReader(nationbuilder_transactions_export_csv)

# create results file for receipts
receipts_for_idis = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/output_data/receipts_export.csv",
    "w",
)
receipts_headers = ["type", "date", "amount", "received_from"]
receipts_writer = csv.DictWriter(receipts_for_idis, fieldnames=receipts_headers)
receipts_writer.writeheader()

## will need to import list of existing donors at some point, but this is fine to start
receipts_list = []
for row in reader:
    name_regex = re.compile(r"(^[\w,']+) ([\w,']+$)")
    given_name = name_regex.match(row["recruiter_name"]).group(1)
    surname = name_regex.match(row["recruiter_name"]).group(2)
    donor_data = {
        "type": "Individual Contribution",
        "date": date_regex.match(row["created_at"]).group(1),
        "amount": row["amount"].replace("$", ""),
        "received_from": surname + ", " + given_name,
    }

    receipts_list.append(donor_data)
    receipts_writer.writerow(donor_data)

print(f"Finished processing receipts\n")

# import payouts data for compiling expenditures

payouts_filenames = [
    "nationbuilder-payouts-export-105-2024-10-06.csv",
    "nationbuilder-payouts-export-107-2024-10-06.csv",
    "nationbuilder-payouts-export-106-2024-10-06.csv",
    "nationbuilder-payouts-export-108-2024-10-06.csv",
]

payouts_data = {}

for file in payouts_filenames:
    payouts_csv = open(
        "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/"
        + file,
        "r",
    )
    reader = csv.DictReader(payouts_csv)

    for row in reader:
        if row["transaction_type"] != "fee":
            continue

        transformed_date = date_regex.match(row["created_date"]).group(1)
        amount = round(float(row["amount"]), 2)
        if payouts_data.get(transformed_date, None) is not None:
            payouts_data[transformed_date] = round(
                (payouts_data[transformed_date] + amount), 2
            )
        else:
            payouts_data[transformed_date] = amount

print(f"finished compiling expenditures\n")
# create results file for expenditures
expenditures_for_idis_export = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/output_data/expenditures_export.csv",
    "w",
)
expenditures_headers = ["date", "amount", "expended_to", "purpose"]
expenditures_writer = csv.DictWriter(
    expenditures_for_idis_export, fieldnames=expenditures_headers
)
expenditures_writer.writeheader()


for date, amount in payouts_data.items():
    expense_data = {
        "date": date,
        "amount": amount,
        "expended_to": "NationBuilder - PO Box 811428, Los Angeles, CA",
        "purpose": "Processing fees",
    }
    expenditures_writer.writerow(expense_data)

print("Finished processing expenditures")
