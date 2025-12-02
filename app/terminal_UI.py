import os
import time
import member_functions
import trainer_functions
import admin_functions
from sqlalchemy.orm import Session
from datetime import datetime, date
from models.schemas import Admin, Trainer, Member, RoomBooking, FitnessClass

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
		print("4) Debug Menu (not for production)")
		print("0) Quit")
		c = prompt("Choose role (0-4)")
		if c == "1":
			member_flow(session)
		elif c == "2":
			trainer_flow(session)
		elif c == "3":
			admin_flow(session)
		elif c == "4":
			debug_flow(session)
		elif c == "0":
			print("Bye")
			break
		else:
			print("Invalid choice")
			time.sleep(0.8)

def debug_flow(session: Session):
	while True:
		clear_screen()
		print("Debug Menu")
		print("1) View Members")
		print("2) View Trainers")
		print("3) View Admins")
		print("0) Back")
		c = prompt("Choice")
		if c == "1":
			member_functions.view_members(session)
			input("Press Enter to continue...")
		elif c == "2":
			trainer_functions.view_trainers(session)
			input("Press Enter to continue...")
		elif c == "3":
			admin_functions.view_admins(session)
			input("Press Enter to continue...")
		elif c == "0":
			break
		else:
			print("Invalid")
			input("Press Enter to continue...")

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
			member_functions.register_member(session, name, dob, gender, contact)
		elif choice == "2":
			name = prompt("Enter your username", True)
			member = member_functions.login_member(session, name)
			if member:
				member_dashboard(session, member)
		elif choice == "0":
			break
		else:
			print("Invalid")
			time.sleep(0.6)

def trainer_flow(session: Session):
	while True:
		clear_screen()
		print("Trainer Menu")
		print("1) Register")
		print("2) Login")
		print("0) Back")
		choice = prompt("Choice")
		if choice == "1":
			name = prompt("Enter your name", True)
			trainer_functions.register_trainer(session, name)
		elif choice == "2":
			name = prompt("Enter your username", True)
			trainer_id = trainer_functions.login_trainer(session, name)
			trainer = session.get(Trainer, trainer_id)
			if trainer:
				trainer_dashboard(session, trainer)
		elif choice == "0":
			break
		else:
			print("Invalid")
			time.sleep(0.6)

def member_dashboard(session: Session, member: Member):
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
			member_functions.dashboard(session, member)
		elif c == "2":
			weight = prompt("Enter weight (kg)", required=False)
			height = prompt("Enter height (cm)", required=False)
			heart_rate = prompt("Enter heart rate (bpm)", required=False)
			current_date = datetime.today().isoformat()
			member_functions.input_health_metric(session, member, current_date, weight, height, heart_rate)
		elif c == "3":
			manage_goal_flow(session, member)
		elif c == "4":
			manage_pt_session_flow(session, member)
		elif c == "5":
			register_fitness_class_flow(session, member)
		elif c == "0":
			break
		else:
			print("Invalid")
		input("Press Enter to continue...")

def manage_goal_flow(session: Session, member: Member):
	print("Current Fitness Goals:")
	member_functions.view_fitness_goals(session, member)
	while True:
		choice = prompt("Add a fitness goal? (y/n)", required=True).lower()
		if choice in ("n", "no"):
			break
		if choice in ("y", "yes"):
			description = prompt("Enter goal description", required=True)
			target = prompt("Enter goal target", required=True)
			member_functions.add_fitness_goals(session, member, description, target)
		else:
			print("Invalid")

def manage_pt_session_flow(session: Session, member: Member):
	print("Manage Personal Training Sessions")
	member_functions.view_pt_sessions(session, member)

	while True:
		choice = prompt("Book a PT session? (y/n)", required=True).lower()

		if choice in ("n", "no"):
			break

		if choice in ("y", "yes"):
			print("Available trainers:")
			trainer_functions.view_trainers(session)
			trainer_id = prompt_int("Trainer ID", required=True)
			trainer = session.get(Trainer, trainer_id)
			print("Available room bookings:")
			# assumes this shows future/free bookings, or all bookings
			member_functions.view_room_bookings(session)

			booking_id = prompt_int("Choose a booking ID from the above available room bookings", required=True)
			booking = session.get(RoomBooking, booking_id)
			pt_session = member_functions.book_pt_session(session=session, member=member, trainer=trainer, booking=booking)

			if pt_session:
				print("PT session booked (id:", getattr(pt_session, "session_id", None), ")")
			else:
				print("Unable to book PT session — conflict or error.")
		else:
			print("Invalid")

def register_fitness_class_flow(session: Session, member: Member):
	print("Register for Fitness Classes")
	member_functions.view_available_classes(session)
	while True:
		choice = prompt("Register for a class? (y/n)", required=True).lower()
		if choice in ("n", "no"):
			break
		if choice in ("y", "yes"):
			class_id = prompt_int("Class ID", required=True)
			fitness_class = session.get(FitnessClass, class_id)
			success = member_functions.class_registration(session, member, fitness_class)
			if success:
				print("Registered for class.")
			else:
				print("Unable to register — class may be full")

# Trainer UI
def trainer_dashboard(session: Session, trainer: Trainer):
	while True:
		clear_screen()
		print("Trainer Menu")
		print("1) Manage Availability")
		print("2) View Schedule")
		print("3) Member Lookup")
		print("0) Back")
		c = prompt("Choice")
		if c == "1":
			availability_flow(session, trainer)
		elif c == "2":
			trainer_functions.schedule_view(session, trainer)
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

def availability_flow(session: Session, trainer: Trainer):
	print("Current Availability:")
	trainer_functions.view_availability(session, trainer)
	while True:
		more = prompt("Add more availability? (y/n)", required=True).lower()
		if more in ("n", "no"):
			break
		if more in ("y", "yes"):
			start_time = prompt("Start (YYYY-MM-DD HH:MM)")
			end_time = prompt("End (YYYY-MM-DD HH:MM)")
			rec = prompt("Recurring? (y/n)", required=True).lower() in ("y", "yes")
			trainer_functions.set_availability(session, trainer, start_time, end_time, rec)
		else:
			print("Invalid")
		input("Press Enter to continue...")

def admin_flow(session: Session):
	while True:
		clear_screen()
		print("Admin Menu")
		print("1) Register")
		print("2) Login")
		print("0) Back")
		choice = prompt("Choice")
		if choice == "1":
			name = prompt("Enter your name", True)
			admin_functions.register_admin(session, name)
		elif choice == "2":
			name = prompt("Enter your username", True)
			admin = admin_functions.login_admin(session, name)
			if admin:
				admin_dashboard(session, admin)
		elif choice == "0":
			break
		else:
			print("Invalid")
			time.sleep(0.6)

# Admin UI
def admin_dashboard(session: Session, admin: Admin):
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
			room_booking_flow(session, admin)
		elif c == "2":
			equipment_maintenance_flow(session, admin)
		elif c == "3":
			class_management_flow(session, admin)
		elif c == "4":
			billing_management_flow(session)
		elif c == "0":
			break
		else:
			print("Invalid")
			input("Press Enter to continue...")

def room_booking_flow(session: Session, admin: Admin):
	print("All room bookings:")
	admin_functions.view_room_bookings(session)
	while True:
		more = prompt("Add a room booking? (y/n)", required=True).lower()
		if more in ("n", "no"):
			break
		if more in ("y", "yes"):
			print("Available rooms:")
			admin_functions.view_rooms(session)
			room_name = prompt("Room name")
			start_date = prompt("Start date (YYYY-MM-DD)")
			end_date = prompt("End date (YYYY-MM-DD)")
			start_time = prompt("Start time (HH:MM)")
			end_time = prompt("End time (HH:MM)")
			rb = admin_functions.room_booking(session, admin, room_name, start_date, start_time, end_date, end_time)
			if rb:
				print("Room booked (booking id:", getattr(rb, "booking_id", None), ")")
			else:
				print("Unable to book room — conflict or error.")
		else:
			print("Invalid")
		input("Press Enter to continue...")
		
def equipment_maintenance_flow(session: Session, admin: Admin):
	while True:
		print("All equipment maintenance records:")
		print("Equipement ID | Admin ID | Operation | Status")
		admin_functions.view_equipment_maintenance(admin)
		print("1) Add record")
		print("2) Edit record")
		print("3) Go back")

		c = prompt("Choice")
		if c == "1":
			op = prompt("Operation description", required=True)
			status = prompt("Status (open/closed)", required=True)
			admin_functions.add_equipment_maintenance(session, admin, op, status=status)
		elif c == "2":
			print("Edit equipment maintenance record:")
			equipment_id = prompt_int("Equipment ID", required=True)
			status = prompt("New status (open/closed)", required=True)
			admin_functions.edit_equipment_maintenance(session, equipment_id, status=status)
		elif c == "3":
			break
		else:
			print("Invalid")
		input("Press Enter to continue...")

def class_management_flow(session: Session, admin: Admin):
	print("All classes:")
	admin_functions.view_fitness_classes(session)
	while True:
		more = prompt("Add a fitness class? (y/n)", required=True).lower()
		if more in ("n", "no"):
			break
		if more in ("y", "yes"):
			trainer_functions.view_trainers(session)
			trainer_id = prompt_int("Trainer ID")
			trainer = session.get(Trainer, trainer_id)
			class_name = prompt("Class name")
			capacity = prompt_int("Capacity")
			admin_functions.view_rooms(session)
			room_name = prompt("Room name")
			start_date = prompt("Start date (YYYY-MM-DD)")
			start_time = prompt("Start time (HH:MM)")
			end_date = prompt("End date (YYYY-MM-DD)")
			end_time = prompt("End time (HH:MM)")
			admin_functions.add_fitness_class(session, admin, trainer, class_name, capacity, room_name, start_date, start_time, end_date, end_time)

def billing_management_flow(session: Session):
	print("1) Create invoice")
	print("2) Record payment")
	sub = prompt("Choice")
	if sub == "1":
		member_id = prompt_int("Member ID")
		member = session.get(Member, member_id)
		type_b = prompt("Type of billing")
		amount = prompt("Amount ($)")
		amount_s = (amount or "").strip()
		if amount_s.replace('.', '', 1).lstrip('+-').isdigit():
			amount_f = float(amount_s)
		else:
			amount_f = 0.0
		bp = admin_functions.billing_and_payments(session, action = "create", member = member, type_of_billing = type_b, amount = amount_f)
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