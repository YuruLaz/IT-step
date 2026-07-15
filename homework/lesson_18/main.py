class MethodChecker(type):
    def __new__(cls, name, bases, attrs):

        for attr_name, attr_value in attrs.items():

            # ვამოწმებთ მხოლოდ მეთოდებს
            if callable(attr_value):

                # სპეციალური მეთოდები (__init__, __str__ და ა.შ) გამოვტოვოთ
                if attr_name.startswith("__") and attr_name.endswith("__"):
                    continue

                if not attr_name.startswith("_"):
                    raise ValueError(
                        f"Method '{attr_name}' must start with '_'"
                    )

        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MethodChecker):
    name = "jclass"

    def _test(self):   # ვალიდურია
        pass

    def test(self):    # გამოიწვევს ValueError-ს
        pass