from datetime import datetime

my_birthdate = 2003
my_name = "ლაზარე"
my_surname = "შარაშენიძე"

current_weliwadi = datetime.now().year

my_age = current_weliwadi - my_birthdate

print(f"ჩემი სახელია {my_name} {my_surname}")
print(f"მე ვარ {my_age} წლის")
print(f"დაბადებული ვარ {my_birthdate} წელს")
print("\nპროგრამის დასასრული")