choice = input("აირჩიეთ ამოცანა 1, 2 ან 3: ")

if choice == "1":
    sentence = input("შეიყვანეთ წინადადება: ")
    first_word = input("რომელი სიტყვა ჩავანაცვლო? ")
    second_word = input("რით ჩავანაცვლო? ")

    new_sentence = sentence.replace(first_word, second_word)

    print("ახალი წინადადება:", new_sentence)


elif choice == "2":
    sentence = input("შეიყვანეთ წინადადება: ")

    words = sentence.split()

    longest_word = max(words, key=len)

    print("ყველაზე გრძელი სიტყვა არის:", longest_word)


elif choice == "3":
    word1 = input("შეიყვანეთ პირველი სიტყვა: ")
    word2 = input("შეიყვანეთ მეორე სიტყვა: ")

    word1 = word1.lower()
    word2 = word2.lower()

    if sorted(word1) == sorted(word2):
        print("ეს სიტყვები ანაგრამებია")
    else:
        print("ეს სიტყვები არ არის ანაგრამები")


else:
    print("გთხოვთ აირჩიოთ მხოლოდ 1, 2 ან 3")