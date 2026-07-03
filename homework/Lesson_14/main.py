import csv
import os

# os.path.abspath(__file__) gvibrunebs am failis absolitur paths saidanac ar unda gaeshvas programa.
# os.path.dirname() gvibrunebs absolitur path im direqtoriis sadac es faili ari motavsebuli
ROOT = os.path.dirname(os.path.abspath(__file__))
# aseve shemedzlo gamomeyena pathlib modulis Path funqcia
# ROOT = pathlib.Path(__file__).resolve().parent
# igive shedegi

def davaleba_1():
    '''უსასრულოდ შეეკითხება სახელს და გვარს სანამ არ შევიყვანთ "stop"-ს.  name-surname.txt ამავე დირექტორიაში'''

    # os.path.join() aertebs chven ROOT file paths da gadacemul fails -> ROOT + file.txt
    # .join aseve xvdeba operatiul sistemas da tviton abams /-linux,mac  an \-windows
    file_path = os.path.join(ROOT, "name-surname.txt")

    try:
        with open(file_path, "r") as f:
            # tito iteraciaze gvadzlevs int 1 da ramdenjerac datrialdeba vajamebt sum()
            counter = sum(1 for _ in f) + 1
            # programa ramdenjerac ar unda gaitishos da gaeshvas count rcheba swori

    except FileNotFoundError:
        counter = 1


    with open(file_path, "a") as f:
        while True:
            name: str = input("Enter your first name or 'stop': ").strip()

            if name == "stop":
                break
            if not name:
                print("Name cannot be empty!")
                continue

            lastname: str = input("Enter your last name: ").strip()
            
            if not lastname:
                print("Last name cannot be empty!")
                continue
            
            #tu name an lastname blank f.write agar eshveba
            f.write(f"{counter}. {name} {lastname}\n")
            counter += 1



def davaleba_2():
    '''ვფილტრავთ დიდ და პატარა ასკიან ადამინაებს. ვინახავთ young-old დირექტორიაში'''
    new_dir = os.path.join(ROOT, "young-old")
    # sad unda sheiqmnas axali directoria
    os.makedirs(new_dir, exist_ok=True)
    # exist_ok= parametri, tu arsebobs ukve aseti dir - errori ar mogvces

    input_path = os.path.join(ROOT, "material", "persons.txt")
    young_path = os.path.join(ROOT, "young-old", "younger_than_50.txt")
    old_path   = os.path.join(ROOT, "young-old", "older_than_50.txt")

    with (
        open(input_path, "r") as f,
        open(young_path, "w") as young,
        open(old_path, "w") as old,
    ):
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                age = int(line.split(", ")[1])
                # split to list, [1] asakis poziciistvis

            except (ValueError, IndexError):
                continue

            if age < 50:
                young.write(f"{line}\n")
            else:                              
                old.write(f"{line}\n")


# davaleba 3-istvis
def write_people(n):
    new_dir = os.path.join(ROOT, "people")
    os.makedirs(new_dir, exist_ok=True) #vqmni directorias sadac iqneba shenauxli people.csv
    file_path = os.path.join(new_dir, "people.csv")

    fieldnames = ["ID", "first_name", "last_name", "age"]
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, n + 1):
            # n -- parametri
            print(f"\n--- Person {i} ---")
            first = input("First name: ").strip()
            last  = input("Last name: ").strip()

            while True:
                # try, except validuri int-intistvis
                try:
                    age = int(input("Age: ").strip())
                    if age > 110:
                        print("input a valid age")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid whole number!")

            writer.writerow({
                "ID": i,
                "first_name": first,
                "last_name": last,
                "age": age,
            })


def davaleba_3():
    '''ვეკითხებით რამდენჯერ უნდა შეიყვანოს ადამიანი. ვინახავთ name-surname დირექტორიაში'''
    while True:
        try:
            n = int(input("How many people do you want to enter? ").strip())
            break
        except ValueError:
            print("Please enter a valid whole number!")

    write_people(n)



def davaleba_4():
    '''ვფილტრავთ მაღალ და დადაბალ ქულიან სტუდენტებს. ვინახავთ passed-failed დირექტორიაში'''
    new_dir = os.path.join(ROOT, "passed-failed")
    os.makedirs(new_dir, exist_ok=True)

    with open(os.path.join(ROOT, "material", "students.csv"), "r", newline="") as f:
        data = csv.DictReader(f)
        with (
            # vqmni axal direcotrias da mand vushveb failed passed studentebis csv files
            open(os.path.join(new_dir, "passed_students.csv"), "w", newline="") as p,
            open(os.path.join(new_dir, "failed_students.csv"), "w", newline="") as fl,
            # newline= parametri carieli rows asacileblad
        ):
            writer = csv.DictWriter(p, fieldnames=data.fieldnames)
            writer.writeheader()
            # fieldnames= igive columnebis shesadgenad rac ari data-shi 
            writer_2 = csv.DictWriter(fl, fieldnames=data.fieldnames)
            writer_2.writeheader()

            for row in data:
                # try, except blocki erroris shemowmebisatvis
                try:
                    grade = int(row["Grade"])
                except (ValueError, KeyError):
                    print(f"Skipping bad row: {row}")
                    continue

                if grade >= 50:
                    writer.writerow(row)
                else:
                    writer_2.writerow(row)


def main():
    '''მთავარი'''

    davalebebi = {
        "1": davaleba_1,
        "2": davaleba_2,
        "3": davaleba_3,
        "4": davaleba_4,
    }

    while True:
        choice = input("\nChoose (1, 2, 3, 4) or 'q': ").strip()
        
        if choice == "q":
            break

        # magalitad choice = "2"
        # viyenebt .get() rom avigot swori davaleba dictidan - choice = "2" -> action(cvladi) = value: davaleba_2 
        action = davalebebi.get(choice)

        if action:
            # action = davaleba_2 vushvebt davaleba_2 + () da eshveba funqcia 
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()