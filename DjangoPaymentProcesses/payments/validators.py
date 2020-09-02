from django.core.exceptions import ValidationError
from datetime import datetime

def sum_digits(digit):
    if digit < 10:
        return digit
    else:
        sum = (digit % 10) + (digit // 10)
        return sum

def creditcard_validator(value):

    # check for letters
    for c in value:
        if c.isalpha():
            raise ValidationError(('Card number must not contain letters!'),
                                  code='model_invalid1',
                                  params={
                                      'value': value},
                                  )

    # reverse the credit card number
    cc_num = value[::-1]
    # convert to integer list
    cc_num = [int(x) for x in cc_num]
    # double every second digit
    doubled_second_digit_list = list()
    digits = list(enumerate(cc_num, start=1))
    for index, digit in digits:
        if index % 2 == 0:
            doubled_second_digit_list.append(digit * 2)
        else:
            doubled_second_digit_list.append(digit)

    # add the digits if any number is more than 9
    doubled_second_digit_list = [sum_digits(x) for x in doubled_second_digit_list]
    # sum all digits
    sum_of_digits = sum(doubled_second_digit_list)
    # return True or False
    if sum_of_digits % 10 != 0:
        raise ValidationError(('Invalid card number!'),
                                  code='model_invalid2',
                                  params={
                                      'value': value},
                                  )
  
def date_validator(value):
    
    d = datetime.now()
    if value <= datetime.date(d):
       raise ValidationError(('Expiry date must be set in the future!'),
                                  code='model_invalid1',
                                  params={
                                      'value': value},
                                  )

def security_validator(value):
    
    if len(value) < 3:
        raise ValidationError(('Security code must be three numbers!'),
                                  code='model_invalid1',
                                  params={
                                      'value': value},
                                  )
    if not value.isdigit():
        raise ValidationError(('Security code must be all numbers!'),
                                  code='model_invalid2',
                                  params={
                                      'value': value},
                                  )
def amount_validator(value):
    
    if value <= 0:
        raise ValidationError(('Amount must not be negative or zero!'),
                                  code='model_invalid1',
                                  params={
                                      'value': value},
                                  )