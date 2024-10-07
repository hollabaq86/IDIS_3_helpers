# IDIS_3_helpers

Helpful scripts for anyone who has to submit reports to the Illinois State Board of Elections IDIS v3.0 system

This repo uses [uv](https://docs.astral.sh/uv/#getting-started)

## process_nationbuilder

Assuming you use Nationbuilder to raise funds for your state-registered committee, process_nationbuilder can read your transactions and payouts exports and generate a results CSV for faster importing to IDIS 3.0

### Pre-requisites
In Nationbuilder, export the transactions and payouts you need, and move those files to the `input_data` folder.

### To run
- in `process_nationbuilder.by` copy the relative paths of your import files to the correct locations (line 5 and 29)

Then run the script

```
$ uv run process_nationbuilder/process_nationbuilder.by
```

in the directory `output_data`, you'll see two CSV files to use to file receipts and expenditures on IDIS 3.0.

## javascript_helper

IN PROGRESS

Hoping to build some scripts or a browser plugin to assist in autocompleting donor data for you via the IDIS 3.0 site.