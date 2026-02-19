from objects.Tank import Tank


class TankMenu:
    def __init__(self):
        self.tank = Tank(start_x=0, start_y=0, load_from_file=True)
        self.running = True
        self.commands = {
            "1": self.show_status,
            "2": self.start_engine,
            "3": self.stop_engine,
            "4": self.move_tank,
            "5": self.shoot_cannon,
            "6": self.refuel_tank,
            "7": self.add_crew_member,
            "8": self.remove_crew_member,
            "9": self.show_crew,
            "10": self.save_game,
            "11": self.load_game,
            "12": self.delete_save,
            "13": self.make_crew_ready, 
            "0": self.exit_program,
        }

    def print_menu(self):
        print("\n OPTIONS:")
        print("=" * 60)
        print(" 1. Show status")
        print(" 2. Start Engine")
        print(" 3. Stop Engine")
        print(" 4. Move to Position")
        print(" 5. Shoot")
        print(" 6. Fefuel the Tank")
        print(" 7. Add a crew member")
        print(" 8. Delete a crew member")
        print(" 9. Show crew members")
        print("10. Save")
        print("11. Load")
        print("12. Delete loading")
        print("13. Board Crew")
        print(" 0. Exit")
        print("=" * 60)

    def show_status(self):
        self.tank.get_status()
        input("\nPress Enter...")

    def start_engine(self):
        if self.tank.start_engine():
            print("Engine is running")
        else:
            print("Fail")
        input("\nPress Enter...")

    def stop_engine(self):
        self.tank.stop_engine()
        print("\nEngine was stopped")
        input("\nPress Enter ...")

    def move_tank(self):
        print("\n:Enter coordinates")
        try:
            x = float(input("X coordinate: "))
            y = float(input("Y coordinate: "))

            if self.tank.move_to(x, y):
                print("Tank moved")
            else:
                print("Failed to move! Check engine and crew.")
        except ValueError:
            print("Enter numbers")
        input("\n Press Enter ...")

    def shoot_cannon(self):
        print(f"There are: {self.tank.ammo} ammos left")
        confirm = input("Shoot? (y/n): ")
        if confirm.lower() == "y":
            self.tank.shoot_cannon()
        input("\nPress Enter...")

    def refuel_tank(self):
        print("\nRefuel:")
        print("1. full refueling")
        print("2. partial refueling")
        choice = input("Choose option (1/2): ")
        if choice == "1":
            self.tank.refuel()
        elif choice == "2":
            try:
                amount = int(input("Enter the number of liters: "))
                self.tank.refuel(amount)
            except ValueError:
                print("Enter a number")
        else:
            print("Fail")
        input("\nPress Enter...")

    def add_crew_member(self):
        name = input("Name: ")
        self.tank.add_member(name)
        input("\nPress Enter...")

    def remove_crew_member(self):
        print("\n👋 Removing a crew member:")
        print("\nCurrent crew:")
        self.tank.show_crew()
        name = input("\n Enter name to delete: ")
        try:
            self.tank.remove_crew_member(name)
        except Exception as e:
            print(f"Error: {e}")
        input("\nPress Enter...")

    def show_crew(self):
        print(self.tank.get_crew_info())
        input("\nPress Enter...")
    def make_crew_ready(self):
        print("\n Boarding crew...")
    
        if self.tank.board_crew():
            print("Crew is in tank! Can ride now!")
        else:
            print(" Something went wrong")
    
        input("\nPress Enter...")

    def save_game(self):
        print("\nSaving...")
        self.tank.save_state()
        input("\nPress Enter...")

    def load_game(self):
        print("\nLoading...")
        self.tank.load_state()
        input("\nPress Enter...")

    def delete_save(self):
        print("\n Delete loadings:")
        confirm = input("Are you sure?(y/n): ")
        if confirm.lower() == "y":
            self.tank.delete_save()
        else:
            print(" Was not confirmed")
        input("\nPress Enter...")

    def exit_program(self):
        print("\nSave?")
        choice = input("y - save, n - exit without saving: ")
        if choice.lower() == "y":
            self.tank.save_state()
        print("\n. Bye")
        self.running = False

    def run(self):
        while self.running:
            print(f"\nPosition: {self.tank.position}")
            print(f" Fuel: {self.tank.fuel_level}l ({self.tank.fuel_percentage:.1f}%)")
            print(f" Ammos: {self.tank.ammo}")
            print(f" Engine: {'running' if self.tank.engine_is_running else 'stop'}")
            self.print_menu()
            choice = input("\nChoose: ")
            if choice in self.commands:
                self.commands[choice]()
            else:
                print("\nTry again")
                input("Press Enter ...")

if __name__ == "__main__":
    menu = TankMenu()
    menu.run()
