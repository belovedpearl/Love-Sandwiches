import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
'''
sales = SHEET.worksheet('sales')
data = sales.get_all_values()
print(data)
'''

def get_sales_data():
    '''
    Get sales figure input from user
    Run a while loop to repeatedly as for input until
    the correct one is provided
    '''
    while True:
        print("Please enter sales from the last market")
        print("Data should be six numbers")
        print("Example: 10,20,30,40,50,60\n")
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(',')
    
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data

def validate_data(values):
    '''
    Validate data input from user
    '''
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data {e}, please try again")
        return False
    return True

"""
def update_sales_data(data):
    
    Update sales worksheet, add data into rows with list provided
    

    print("Updating worksheet...")
    
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)

    print("Update complete.")

def update_surplus_worksheet(data):
    
    # Update surplus worksheet, add data into rows with list provided
    
    print("Updating surplus worksheet")
   
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    
    print("Surplus worksheet update complete")
"""

def update_worksheet(data, worksheet):
    """
    Update the required worksheet, add data into rows with list provided
    """
    print(f"Updating {worksheet} worksheet...\n")
   
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    
    print(f"{worksheet} worksheet update complete...\n") 


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus
    The surplus is defined as the sales minus stock
    -Positive surplus indicate waste
    -Negative surplus indicate extra made when stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row_int = [int(num) for num in stock_row]
    
    surplus_data = []
    for stock, sales in zip(stock_row_int,sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)

    return surplus_data






def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
   

print("Welcome to love sandwiches automation")
main()