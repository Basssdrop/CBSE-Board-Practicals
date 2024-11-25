import sqlite3
from typing import List, Tuple


class InsufficientFundsError(Exception):
    # Exception is raised when user is trying to withdraw more than account balance
    pass


class AccountNotFoundError(Exception):
    # Exception is raised when the user input account does not exist
    pass


class LoanNotFoundError(Exception):
    # Exception raised when the loan does not exist in the system
    pass


class Bank:
    def __init__(self, db_name: str = "bank_system.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._initialize_database()

    def _initialize_database(self):
        # Create the accounts and loans tables if they do not exist
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY,
            account_holder TEXT NOT NULL,
            balance REAL NOT NULL CHECK(balance >= 0)
        )
        """
        )
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number INTEGER NOT NULL,
            loan_amount REAL NOT NULL CHECK(loan_amount > 0),
            remaining_amount REAL NOT NULL CHECK(remaining_amount >= 0),
            FOREIGN KEY(account_number) REFERENCES accounts(account_number)
        )
        """
        )
        self.connection.commit()

    def create_account(
        self, account_number: int, account_holder: str, initial_balance: float = 0.0
    ):
        # Create a new account in the system
        try:
            self.cursor.execute(
                """
            INSERT INTO accounts (account_number, account_holder, balance)
            VALUES (?, ?, ?)
            """,
                (account_number, account_holder, initial_balance),
            )
            self.connection.commit()
            print(
                f"Account {account_number} created for {account_holder} with balance {initial_balance}."
            )
        except sqlite3.IntegrityError:
            raise ValueError(f"Account with number {account_number} already exists.")

    def deposit_to_account(self, account_number: int, amount: float):
        """Deposit an amount into the specified account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        account = self._get_account(account_number)
        new_balance = account[2] + amount
        self.cursor.execute(
            """
        UPDATE accounts SET balance = ? WHERE account_number = ?
        """,
            (new_balance, account_number),
        )
        self.connection.commit()
        print(
            f"Deposited {amount} to account {account_number}. New balance: {new_balance}."
        )

    def withdraw_from_account(self, account_number: int, amount: float):
        """Withdraw an amount from the specified account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        account = self._get_account(account_number)
        if account[2] < amount:
            raise InsufficientFundsError("Insufficient funds for this withdrawal.")
        new_balance = account[2] - amount
        self.cursor.execute(
            """
        UPDATE accounts SET balance = ? WHERE account_number = ?
        """,
            (new_balance, account_number),
        )
        self.connection.commit()
        print(
            f"Withdrew {amount} from account {account_number}. New balance: {new_balance}."
        )

    def check_account_balance(self, account_number: int) -> float:
        """Check the balance of the specified account."""
        account = self._get_account(account_number)
        print(f"Account {account_number} balance: {account[2]}")
        return account[2]

    def apply_for_loan(self, account_number: int, loan_amount: float):
        """Apply for a loan for the specified account."""
        if loan_amount <= 0:
            raise ValueError("Loan amount must be positive.")
        self._get_account(account_number)  # Ensure account exists
        self.cursor.execute(
            """
        INSERT INTO loans (account_number, loan_amount, remaining_amount)
        VALUES (?, ?, ?)
        """,
            (account_number, loan_amount, loan_amount),
        )
        self.connection.commit()
        print(f"Loan of {loan_amount} approved for account {account_number}.")

    def repay_loan(self, account_number: int, repayment_amount: float):
        """Repay a loan for the specified account."""
        if repayment_amount <= 0:
            raise ValueError("Repayment amount must be positive.")
        self.cursor.execute(
            """
        SELECT loan_id, remaining_amount FROM loans
        WHERE account_number = ? AND remaining_amount > 0
        ORDER BY loan_id LIMIT 1
        """,
            (account_number,),
        )
        loan = self.cursor.fetchone()
        if not loan:
            raise LoanNotFoundError(
                f"No active loans found for account {account_number}."
            )
        loan_id, remaining_amount = loan
        if repayment_amount > remaining_amount:
            raise ValueError(
                f"Repayment amount exceeds the remaining loan balance of {remaining_amount}."
            )
        new_remaining = remaining_amount - repayment_amount
        self.cursor.execute(
            """
        UPDATE loans SET remaining_amount = ? WHERE loan_id = ?
        """,
            (new_remaining, loan_id),
        )
        self.connection.commit()
        print(
            f"Repayment of {repayment_amount} made for loan ID {loan_id}. Remaining loan balance: {new_remaining}."
        )

    def view_loans(self, account_number: int) -> List[Tuple[int, float, float]]:
        """View all loans for the specified account."""
        self.cursor.execute(
            """
        SELECT loan_id, loan_amount, remaining_amount FROM loans
        WHERE account_number = ?
        """,
            (account_number,),
        )
        loans = self.cursor.fetchall()
        if not loans:
            print(f"No loans found for account {account_number}.")
        else:
            print("\nLoans for Account Number:", account_number)
            for loan in loans:
                print(
                    f"Loan ID: {loan[0]}, Total Loan: {loan[1]}, Remaining Amount: {loan[2]}"
                )
        return loans

    def _get_account(self, account_number: int) -> Tuple[int, str, float]:
        """Retrieve account details from the database."""
        self.cursor.execute(
            """
        SELECT * FROM accounts WHERE account_number = ?
        """,
            (account_number,),
        )
        account = self.cursor.fetchone()
        if not account:
            raise AccountNotFoundError(
                f"Account with number {account_number} not found."
            )
        return account

    def list_all_accounts(self) -> List[Tuple[int, str, float]]:
        """Retrieve all accounts in the database."""
        self.cursor.execute(
            """
        SELECT * FROM accounts
        """
        )
        accounts = self.cursor.fetchall()
        return accounts

    def close(self):
        """Close the database connection."""
        self.connection.close()


def main():
    bank = Bank()
    print("Welcome to the Bank Management System with Loans")

    while True:
        print("\n1: Create Account")
        print("2: Deposit")
        print("3: Withdraw")
        print("4: Check Balance")
        print("5: Apply for Loan")
        print("6: Repay Loan")
        print("7: View Loans")
        print("8: List All Accounts")
        print("9: Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                account_number = int(input("Enter account number: "))
                account_holder = input("Enter account holder name: ")
                initial_balance = float(input("Enter initial balance: "))
                bank.create_account(account_number, account_holder, initial_balance)

            elif choice == "2":
                account_number = int(input("Enter account number: "))
                amount = float(input("Enter amount to deposit: "))
                bank.deposit_to_account(account_number, amount)

            elif choice == "3":
                account_number = int(input("Enter account number: "))
                amount = float(input("Enter amount to withdraw: "))
                bank.withdraw_from_account(account_number, amount)

            elif choice == "4":
                account_number = int(input("Enter account number: "))
                bank.check_account_balance(account_number)

            elif choice == "5":
                account_number = int(input("Enter account number: "))
                loan_amount = float(input("Enter loan amount: "))
                bank.apply_for_loan(account_number, loan_amount)

            elif choice == "6":
                account_number = int(input("Enter account number: "))
                repayment_amount = float(input("Enter repayment amount: "))
                bank.repay_loan(account_number, repayment_amount)

            elif choice == "7":
                account_number = int(input("Enter account number: "))
                bank.view_loans(account_number)

            elif choice == "8":
                accounts = bank.list_all_accounts()
                print("\nAll Accounts:")
                for acc in accounts:
                    print(
                        f"Account Number: {acc[0]}, Holder: {acc[1]}, Balance: {acc[2]}"
                    )

            elif choice == "9":
                print("Exiting the system.")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Input error: {e}")
        except InsufficientFundsError as e:
            print(e)
        except AccountNotFoundError as e:
            print(e)
        except LoanNotFoundError as e:
            print(e)
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    bank.close()


if __name__ == "__main__":
    main()
