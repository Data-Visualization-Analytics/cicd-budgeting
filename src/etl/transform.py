import logging

import pandas as pd

import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Transformer:
    def __init__(self,
                 downloaded_file_path=os.path.abspath('downloads/Budgeting sheet.xlsx'),
                 processed_file_path=os.path.abspath('downloads/income.csv')):
        self.downloaded_file_path = downloaded_file_path
        self.processed_file_path = processed_file_path

    def extract_tables_from_planner(self, file_path, sheet_name="Planner"):

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        tables = []
        current_rows = []

        def is_data_row(row):
            non_null = row.dropna()
            if len(non_null) < 2:
                return False
            has_text = any(isinstance(v, str) for v in non_null)
            has_number = any(isinstance(v, (int, float)) for v in non_null)
            return has_text and has_number

        for _, row in df.iterrows():

            # End table on blank row
            if row.isna().all():
                if current_rows:
                    tables.append(pd.DataFrame(current_rows).dropna(axis=1, how="all"))
                    current_rows = []
                continue

            first_cell = str(row.iloc[0]).lower()

            # End table on subtotal / total
            if "sub total" in first_cell or first_cell.startswith("total"):
                if current_rows:
                    tables.append(pd.DataFrame(current_rows).dropna(axis=1, how="all"))
                    current_rows = []
                continue

            if is_data_row(row):
                current_rows.append(row.tolist())

        # Catch last table
        if current_rows:
            tables.append(pd.DataFrame(current_rows).dropna(axis=1, how="all"))

        return tables

    def mapper(self):
        tables = self.extract_tables_from_planner(os.path.abspath(self.downloaded_file_path))
        expense_table = pd.DataFrame()
        for i, table in enumerate(tables):
            if i == 0:
                table.columns = ['Category','Amount (₹)','% of Total Income']
                expense_table = pd.concat([table, expense_table])
        expense_table.to_csv(os.path.abspath(self.processed_file_path), index=False)




