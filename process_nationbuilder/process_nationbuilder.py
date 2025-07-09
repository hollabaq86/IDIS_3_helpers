import csv
import re
from datetime import datetime

date_regex = re.compile(r"(^\d{2}/\d{2}/\d{4})")

# import transaction data for receipts
nationbuilder_transactions_export_csv = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/nationbuilder-financialtransactions-export-109-2024-10-06.csv",
    "r",
)

# create or load donor csv file

reader = csv.DictReader(nationbuilder_transactions_export_csv)

# create results file for donors if it doesn't exist
donor_length_check = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/donors.csv",
    "r",
)
#print(len(existing_donors_for_idis.readlines()))
number_existing_donors = len(donor_length_check.readlines())
print("number existing numbers: " + str(number_existing_donors))
donor_length_check.close()

existing_donors_for_idis = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/donors.csv",
    "r",
)
donors_reader = csv.DictReader(existing_donors_for_idis)
donors_writer = None
donors_headers = ["received_from", "billing_address1", "billing_address2", "billing_city", "billing_state", "billing_zip", "occupation", "employer", "date_added"]
new_donors_for_idis = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/input_data/donors.csv",
    "a",
)
donors_writer = csv.DictWriter(new_donors_for_idis, fieldnames=donors_headers)

if number_existing_donors == 0:
    print("creating donor file to write")
    donors_writer.writeheader()
else:
    print("re-using donor file to write")
existing_donors = [row["received_from"] for row in donors_reader]
existing_donors = list(set(existing_donors))
working_donors = existing_donors.copy()

# create results file for receipts
receipts_for_idis = open(
    "/Users/hollystotelmyer/IDIS_3_helpers/process_nationbuilder/output_data/receipts_export.csv",
    "w",
)
receipts_headers = ["type", "date", "amount", "received_from"]
receipts_writer = csv.DictWriter(receipts_for_idis, fieldnames=receipts_headers)
receipts_writer.writeheader()

## will need to import list of existing donors at some point, but this is fine to start

for row in reader:
    name_regex = re.compile(r"(^[A-zÀ-ÿ,']+) ([A-zÀ-ÿ,' ]*?)([A-zÀ-ÿ,'-]+$)")
    given_name = name_regex.match(row["recruiter_name"]).group(1)
    surname = name_regex.match(row["recruiter_name"]).group(3)
    donor_name = surname + ", " + given_name
    donation_data = {
        "type": "Individual Contribution",
        "date": date_regex.match(row["created_at"]).group(1),
        "amount": row["amount"].replace("$", ""),
        "received_from": donor_name,
    }
    donor_data = {
        "received_from": donor_name,
        "billing_address1": row["billing_address1"],
        "billing_address2": row["billing_address2"],
        "billing_city": row["billing_city"],
        "billing_state": row["billing_state"],
        "billing_zip": row["billing_zip"],
        "occupation": row["signup_occupation"],
        "employer": row["signup_employer"],
        "date_added": datetime.today(),
    }
    if donor_name not in existing_donors and donor_name not in working_donors:
        print("Adding a donor! " + donor_name)
        donors_writer.writerow(donor_data)
        working_donors.append(donor_name)
    receipts_writer.writerow(donation_data)

print("Finished processing receipts\n")

# import payouts data for compiling expenditures

payouts_filenames = [
    "nationbuilder-payouts-export-240-2025-07-08.csv",
    "nationbuilder-payouts-export-239-2025-07-08.csv",
    "nationbuilder-payouts-export-238-2025-07-08.csv",
    "nationbuilder-payouts-export-237-2025-07-08.csv",
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

print("finished compiling expenditures\n")
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
