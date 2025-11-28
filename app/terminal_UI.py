import os
import time
import member_functions
import trainer_functions
import admin_functions
from sqlalchemy.orm import Session

def clear_screen():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def prompt(text, required=True):
	while True:
		val = input(f"{text}: ").strip()
		if not val and required:
			print("Required.")
			continue
		return val

def prompt_int(text, required=True):
	while True:
		val = prompt(text, required)
		if not val and not required:
			return None
		if val.lstrip('-').isdigit():
			return int(val)
		print("Enter a valid integer.")

def main_menu(session: Session = None):
	print("Welcome to the Health & Fitness Club Management System!")
	while True:
		clear_screen()
		print("Health & Fitness Club")
		print("1) Member")
		print("2) Trainer")
		print("3) Admin")
		print("0) Quit")
		c = prompt("Choose role (0-3)")
		if c == "1":
			member_flow(session)
		elif c == "2":
			trainer_flow(session)
		elif c == "3":
			admin_flow(session)
		elif c == "0":
			print("Bye")
			break
		else:
			print("Invalid choice")
			time.sleep(0.8)

# Member UI
def member_flow(session: Session):
	while True:
		clear_screen()
		print("Member Menu")
		print("1) Register")
		print("2) Login")
		print("0) Back")
		choice = prompt("Choice")
		if choice == "1":
			name = prompt("Enter your name", True)
			dob = prompt("Enter your date of birth (ex: YYYY-MM-DD)")
			gender = prompt("What is your gender?")
			contact = prompt("Enter your contact details")
			member_functions.register_user(session, name, dob, gender, contact)
		elif choice == "2":
			name = prompt("Enter your username", True)
			member_id = member_functions.login_user(session, name)
			if member_id:
				member_dashboard(session, member_id)
		elif choice == "0":
			break
		else:
			print("Invalid")
			time.sleep(0.6)

def member_dashboard(session: Session, member_id: int):
	while True:
		clear_screen()
		print("Member Dashboard")
		print("1) View / Edit Profile")
		print("2) Manage Health Metrics")
		print("3) Manage Goals")
		print("4) Manage PT Session")
		print("5) Manage Classes")
		print("0) Logout")
		c = prompt("Choice")
		if c == "1":
			print("[PLACEHOLDER] Edit profile — implement in member module")
		elif c == "2":
			print("[PLACEHOLDER] Add health metric — implement in member module")
		elif c == "3":
			print("[PLACEHOLDER] View health history — implement in member module")
		elif c == "4":
			print("[PLACEHOLDER] Manage PT sessions — implement in scheduling module")
		elif c == "5":
			print("[PLACEHOLDER] Register for class — implement in classes module")
		elif c == "0":
			break
		else:
			print("Invalid")
		input("Press Enter to continue...")

# Trainer UI
def trainer_flow(session: Session):
	while True:
		clear_screen()
		print("Trainer Menu")
		print("1) Set Availability")
		print("2) View Schedule")
		print("3) Member Lookup")
		print("0) Back")
		c = prompt("Choice")
		if c == "1":
			trainer_id = prompt_int("Trainer ID")
			start_time = prompt("Start (YYYY-MM-DD HH:MM)")
			end_time = prompt("End (YYYY-MM-DD HH:MM)")
			rec = prompt("Recurring? (y/n)", required=True).lower() in ("y", "yes")
			trainer_functions.set_availability(session, trainer_id, start_time, end_time, rec)
			print("Availability set.")
			input("Press Enter to continue...")
		elif c == "2":
			trainer_id = prompt_int("Trainer ID")
			trainer_functions.schedule_view(session, trainer_id)
			input("Press Enter to continue...")
		elif c == "3":
			name = prompt("Member name to lookup")
			trainer_functions.member_lookup(session, name)
			input("Press Enter to continue...")
		elif c == "0":
			break
		else:
			print("Invalid")
			input("Press Enter to continue...")

# Admin UI
def admin_flow(session: Session):
	while True:
		clear_screen()
		print("Admin Menu")
		print("1) Room Booking")
		print("2) Equipment Maintenance")
		print("3) Class Management")
		print("4) Billing & Payment")
		print("0) Back")
		c = prompt("Choice")
		if c == "1":
			admin_id = prompt_int("Admin ID")
			room_name = prompt("Room name")
			start_date = prompt("Start date (YYYY-MM-DD)")
			start_time = prompt("Start time (HH:MM)")
			end_date = prompt("End date (YYYY-MM-DD)")
			end_time = prompt("End time (HH:MM)")
			rb = admin_functions.room_booking(session, admin_id, room_name, start_date, start_time, end_date, end_time)
			if rb:
				print("Room booked (booking id:", getattr(rb, "booking_id", None), ")")
			else:
				print("Unable to book room — conflict or error.")
			input("Press Enter to continue...")
		elif c == "2":
			admin_id = prompt_int("Admin ID")
			op = prompt("Operation description")
			em = admin_functions.equipment_maintenance(session, admin_id, op)
			print("Equipment maintenance record created (id:", getattr(em, "equipment_id", None), ")")
			input("Press Enter to continue...")
		elif c == "3":
			admin_id = prompt_int("Admin ID")
			trainer_id = prompt_int("Trainer ID")
			class_name = prompt("Class name")
			capacity = prompt_int("Capacity")
			room_name = prompt("Room name")
			start_date = prompt("Start date (YYYY-MM-DD)")
			start_time = prompt("Start time (HH:MM)")
			end_date = prompt("End date (YYYY-MM-DD)")
			end_time = prompt("End time (HH:MM)")
			fc = admin_functions.class_management(session, admin_id, trainer_id, class_name, capacity, room_name, start_date, start_time, end_date, end_time)
			if fc:
				print("Class created (id:", getattr(fc, "class_id", None), ")")
			else:
				print("Unable to create class — room conflict or error.")
			input("Press Enter to continue...")
		elif c == "4":
			print("1) Create invoice")
			print("2) Record payment")
			sub = prompt("Choice")
			if sub == "1":
				member_id = prompt_int("Member ID")
				type_b = prompt("Type of billing")
				amount = prompt("Amount ($)")
				amount_s = (amount or "").strip()
				if amount_s.replace('.', '', 1).lstrip('+-').isdigit():
					amount_f = float(amount_s)
				else:
					amount_f = 0.0
				bp = admin_functions.billing_and_payments(session, action = "create", member_id = member_id, type_of_billing = type_b, amount = amount_f)
				print("Invoice created (id:", getattr(bp, "billing_id", None), ")")
				input("Press Enter to continue...")
			elif sub == "2":
				billing_id = prompt_int("Billing ID")
				method = prompt("Payment method")
				bp = admin_functions.billing_and_payments(session, action = "pay", billing_id = billing_id, payment_method = method)
				if bp:
					print("Payment recorded.")
				else:
					print("Billing record not found.")
				input("Press Enter to continue...")
		elif c == "0":
			break
		else:
			print("Invalid")
			input("Press Enter to continue...")
