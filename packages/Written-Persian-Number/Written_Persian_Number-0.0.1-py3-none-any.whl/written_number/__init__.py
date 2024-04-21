"""Needed Functions"""

def find_number_range(user_number_list: list) -> str:
    """ Get number range

    Args:
        user_number_list (list): Number is divided into 3 value groups

    Returns:
        str: Number range
    """
    if 35 <= len(user_number_list) <= ((10**100)/3)+1:
        number_range = "گوگول"
    else:
        index = len(user_number_list)-2
        number_range_tuple = ("هزار", "میلیون", "میلیارد", "بیلیون", "بیلیارد", "تریلیون", "تریلیارد", "کوآدریلیون", "کادریلیارد",
                          "کوینتیلیون", "کوانتینیارد", "سکستیلیون", "سکستیلیارد", "سپتیلیون", "سپتیلیارد", "اکتیلیون", "اکتیلیارد",
                          "نانیلیون", "نانیلیارد", "دسیلیون", "دسیلیارد", "آندسیلیون", "آندسیلیارد", "دودسیلیون", "دودسیلیارد", 
                          "تریدسیلیون", "تریدسیلیارد", "کوادردسیلیون", "کوادردسیلیارد", "کویندسیلیون", "کویندسیلیارد", "سیدسیلیون",
                          "سیدسیلیارد")
        number_range = number_range_tuple[index]
    return number_range
    

def all_zeros(string: str) -> bool:
    """ Ckeck all values of a number

    Args:
        string (str): Number

    Returns:
        bool: True: All values are zero
              False: The number has at least one non-zero value
    """
    for char in string:
        if char != '0':
            return False
    return True