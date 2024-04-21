from os import system
from written_number import *


def main():
    yek_dict = {"0":"", "1": "یک", "2": "دو", "3": "سه", "4": "چهار",
                "5": "پنج", "6": "شش", "7": "هفت", "8": "هشت", "9": "نه"}
    dah_dict = {"10": "ده", "11": "یازده", "12": "دوازده", "13": "سیزده", "14": "چهارده",
                "15": "پانزده", "16": "شانزده", "17": "هفده", "18": "هجده", "19": "نوزده"}
    dahh_dict = {"0":"", "2": "بیست", "3": "سی", "4": "چهل", "5": "پنجاه",
                "6": "شصت", "7": "هفتاد", "8": "هشتاد", "9": "نود"}
    sad_dict = {"0":"", "1": "صد", "2": "دویست", "3": "سیصد", "4": "چهارصد",
                "5": "پانصد", "6": "ششصد", "7": "هفتصد", "8": "هشتصد", "9": "نهصد"}

    # region Get number
    user_number = int(input("Enter a number.\n\U0001F449"))
    system("cls")
    user_number = str(f"{user_number:,}")
    user_number_list = user_number.split(sep=",")
    user_number_list[0] = user_number_list[0].zfill(3)
    user_number = "".join(user_number_list)
    # endregion


    # region turn a number into its written form (Persian)
    number_written = ""
    for i in range(len(user_number_list)):

        if user_number[0] == "0":
            if user_number[1] == "0":
                if user_number[2] == "0":
                    user_number = "".join(user_number_list[(i+1):])
                    continue
                else:
                    first_digit = yek_dict.get(user_number[2])
                    number_written = number_written + first_digit + " "
            else:
                if user_number[1] == "1":
                    first_part = dah_dict.get(user_number[1:3])
                    number_written = number_written + first_part + " "
                else:
                    if user_number[2] == "0":
                        second_digit = dahh_dict.get(user_number[1])
                        number_written = number_written + second_digit + " "
                    else:
                        second_digit = dahh_dict.get(user_number[1])
                        third_digit = yek_dict.get(user_number[2])
                        number_written = number_written + "و" + " " + \
                            second_digit + " " + "و " + " " + third_digit + " "
        else:
            first_digit = sad_dict.get(user_number[0])
            number_written = number_written + first_digit + " "
            if user_number[1] == "0" and user_number[2] != "0":
                third_digit = yek_dict.get(user_number[2])
                number_written = number_written + "و" + " " + third_digit + " "
            elif user_number[1] == "1":
                first_part = dah_dict.get(user_number[1:3])
                number_written = number_written + first_part + " "
            elif user_number[1] != "0" and user_number[2] == "0":
                second_digit = dahh_dict.get(user_number[1])
                number_written = number_written + "و" + " " + second_digit
            elif (user_number[1] != "0") and (user_number[2] != "0"):
                second_digit = dahh_dict.get(user_number[1])
                third_digit = yek_dict.get(user_number[2])
                number_written = number_written + "و" + " " + \
                    second_digit + " " + "و " + " " + third_digit + " "
                
        user_number = "".join(user_number_list[(i+1):])

        range_part = True

        if i == len(user_number_list)-1:
            range_part = False

        if range_part:
            all_zero = all_zeros(user_number)
            if all_zero:
                number_range = find_number_range(user_number_list[i:])
                number_written = number_written + number_range
                break
            else:
                number_range = find_number_range(user_number_list[i:])
                number_written = number_written + number_range + " " + "و" + " "
    # endregion

    print(number_written)

if __name__ == "__main__":
    main()