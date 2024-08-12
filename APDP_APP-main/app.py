import os
import csv
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Constants for file names
USERS_FILE = "users.csv"
BRANCHES_FILE = "branches.csv"
PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"

########## Factory Pattern ##########

# Interface for data loaders
class DataLoader:
    def load_data(self):
        raise NotImplementedError

# CSV loader implementation
class CSVDataLoader(DataLoader):
    def __init__(self, file_name):
        self.file_name = file_name
    
    def load_data(self):
        data = []
        if os.path.exists(self.file_name):
            with open(self.file_name, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    data.append(row)
        return data

# Factory to create loaders
class DataLoaderFactory:
    @staticmethod
    def create_loader(file_name):
        if file_name.endswith('users.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('branches.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('products.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('sales.csv'):
            return CSVDataLoader(file_name)
        else:
            raise ValueError("Unsupported file type")

########## Command Pattern ##########

# Base command interface
class Command:
    def execute(self):
        raise NotImplementedError

# Concrete command to add a new branch
class AddBranchCommand(Command):
    def execute(self):
        print("\n///// Add New Branch /////")
        branches_data = load_data(BRANCHES_FILE)
        
        branch_id = input("Enter Branch ID: ")
        branch_name = input("Enter Branch Name: ")
        location = input("Enter Location: ")

        new_branch = [branch_id, branch_name, location]
        branches_data.append(new_branch)

        os.remove(BRANCHES_FILE)

        headers = ['Branch ID', 'Branch Name', 'Location']
        save_data(BRANCHES_FILE, branches_data, headers=headers)
        print(f"Branch {branch_name}  successfully added.")

# Concrete command to add a new sale
class AddSaleCommand(Command):
    def execute(self):
        print("\n///// Add New Sale /////")
        sales_data = load_data(SALES_FILE)
        
        branch_id = input("Enter Branch ID: ")
        product_id = input("Enter Product ID: ")
        amount_sold = input("Enter Amount Sold: ")

        new_sale = [branch_id, product_id, amount_sold, datetime.now().strftime('%Y-%m-%d')]
        sales_data.append(new_sale)

        os.remove(SALES_FILE)

        headers = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
        save_data(SALES_FILE, sales_data, headers=headers)
        print(" Successfully sale added.")

# Concrete command for monthly sales analysis of a specific branch
class MonthlySalesAnalysisCommand(Command):
    def __init__(self, branch_id):
        self.branch_id = branch_id
    
    def execute(self):
        perform_monthly_sales_analysis(self.branch_id)

# Concrete command for price analysis of a specific product
class PriceAnalysisCommand(Command):
    def __init__(self, product_id):
        self.product_id = product_id
    
    def execute(self):
        perform_price_analysis(self.product_id)

# Concrete command for weekly sales analysis of the supermarket network
class WeeklySalesAnalysisCommand(Command):
    def execute(self):
        perform_weekly_sales_analysis()

# Concrete command for total sales amount analysis
class TotalSalesAmountAnalysisCommand(Command):
    def execute(self):
        perform_total_sales_amount_analysis()

# Concrete command for monthly sales analysis of all branches
class AllBranchesMonthlySalesAnalysisCommand(Command):
    def execute(self):
        perform_all_branches_monthly_sales_analysis()

########## Utility Functions ##########

# Function to load data from CSV file
def load_data(file_name):
    loader = DataLoaderFactory.create_loader(file_name)
    return loader.load_data()

# Function to save data to CSV file
def save_data(file_name, data, headers=None):
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerows(data)

# Function for user login
def user_login():
    print("///// Login /////")
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# Function for monthly sales analysis of a specific branch
def perform_monthly_sales_analysis(branch_id):
    print(f"\n///// Analysis Monthly Sales - Branch {branch_id} /////")
    sales_data = load_data(SALES_FILE)
    branch_sales = [int(sale[2]) for sale in sales_data if sale[0] == branch_id]

    if not branch_sales:
        print(f"Branch ID cannot be identified in the sales data. {branch_id}.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(branch_sales, bins=10, edgecolor='black')
    plt.title(f'Monthly Sales Analysis - Branch {branch_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Function for price analysis of a specific product
def perform_price_analysis(product_id):
    print(f"\n///// Price Analysis - Product {product_id} /////")
    sales_data = load_data(SALES_FILE)
    product_sales = [int(sale[2]) for sale in sales_data if sale[1] == product_id]

    if not product_sales:
        print(f"No sales data found for Product ID {product_id}.")
        return

    average_price = np.mean(product_sales)
    max_price = np.max(product_sales)
    min_price = np.min(product_sales)
    median_price = np.median(product_sales)

    print(f"Average Price: {average_price} LKR")
    print(f"Maximum Price: {max_price} LKR")
    print(f"Minimum Price: {min_price} LKR")
    print(f"Median Price: {median_price} LKR")

    # Plotting boxplot for price distribution
    plt.figure(figsize=(8, 5))
    plt.boxplot(product_sales, vert=False)
    plt.title(f'Price Distribution - Product {product_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.grid(True)
    plt.show()

# Function for weekly sales analysis of the supermarket network
def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data '{date_str}' does not match any known format")

def perform_weekly_sales_analysis():
    print("\n///// Weekly Sales Analysis - Supermarket Network /////")
    sales_data = load_data(SALES_FILE)

    # Example: Analyze sales for the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_sales = [int(sale[2]) for sale in sales_data
                    if start_of_week <= parse_date(sale[3]) <= end_of_week]

    total_sales = sum(weekly_sales)
    average_sales = np.mean(weekly_sales) if weekly_sales else 0

    print(f"Total Sales for the Week: {total_sales} LKR")
    print(f"Average Daily Sales: {average_sales} LKR")

# Function for total sales amount analysis
def perform_total_sales_amount_analysis():
    print("\n///// Analysis Total Sales Amount  /////")
    sales_data = load_data(SALES_FILE)
    total_sales = sum([int(sale[2]) for sale in sales_data])

    print(f"Sales Total Amount: {total_sales} LKR")

# Function for monthly sales analysis of all branches
def perform_all_branches_monthly_sales_analysis():
    print("\n///// Monthly Sales Analysis of All Branches /////")
    sales_data = load_data(SALES_FILE)
    branches_data = load_data(BRANCHES_FILE)
    
    monthly_sales = {branch[0]: 0 for branch in branches_data}
    
    for sale in sales_data:
        branch_id = sale[0]
        monthly_sales[branch_id] += int(sale[2])
    
    
    branch_ids, sales_amounts = zip(*monthly_sales.items())
    
    plt.figure(figsize=(10, 6))
    plt.bar(branch_ids, sales_amounts)
    plt.title('Monthly Sales Analysis of All Branches')
    plt.xlabel('Branch ID')
    plt.ylabel('Total Sales (LKR)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

########## Main Program ##########

# Main program loop with command execution
def main():
    # Ensure CSV files exist with headers
    headers_users = ['Username', 'Password']
    if not os.path.exists(USERS_FILE):
        save_data(USERS_FILE, [], headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    if not os.path.exists(BRANCHES_FILE):
        save_data(BRANCHES_FILE, [], headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    if not os.path.exists(PRODUCTS_FILE):
        save_data(PRODUCTS_FILE, [], headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    if not os.path.exists(SALES_FILE):
        save_data(SALES_FILE, [], headers=headers_sales)

    # Login loop
    while True:
        if user_login():
            print(" Successful Login !")
            break
        else:
            print("Invalid login. Please try again.")

    # Command map
    command_map = {
        '1': AddBranchCommand,
        '2': AddSaleCommand,
        '3': MonthlySalesAnalysisCommand,
        '4': PriceAnalysisCommand,
        '5': WeeklySalesAnalysisCommand,
        '6': TotalSalesAmountAnalysisCommand,
        '7': AllBranchesMonthlySalesAnalysisCommand,
        '8': lambda: print("Logged out.")
    }

    # Main menu
    while True:
        print("\n///// Main Menu /////")
        print("1. Register a New Branch")
        print("2. Record a New Sale")
        print("3. Analyze Monthly Sales for a Specific Branch")
        print("4. Examine Price Data for a Specific Product")
        print("5. Review Weekly Sales for the Supermarket Network")
        print("6. Analysis Total Sales Amounts")
        print("7. Monthly Sales Analysis of All Branches")
        print("8. Sign out")

        choice = input("Choose an option (1-8): ")

        if choice in command_map:
            if choice == '8':
                command_map[choice]()  # Log out directly
                break
            else:
                if choice in ['3', '4']:
                    param = input(f"Enter {'Branch ID' if choice == '3' else 'Product ID'}: ")
                    command = command_map[choice](param)
                else:
                    command = command_map[choice]()
                command.execute()
        else:
            print("Not a suitable choice. Type a number between 1 and 8 please.")

# Execute the main program
main()
