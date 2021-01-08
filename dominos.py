from pizza_order import order, print_vouchers, get_vouchers

street_no = ''
street = ''
suburb = ''
state = ''
postcode = ''
order_option = 'delivery'  # or pickup

pizza1 = 'FIRE BREATHER'
pizza2 = 'GODFATHER'
pizza3 = 'SUPREME'

name = "Caleb"
phone = ""
email = ''

payment_method = 'paypal'  # instagift, cash, creditcard

voucher_id = 2

print('+' + '='*93 + '+')
for i in range(1, 3):
    print('|' + ' '*93 + '|')
    if i == 1:
        print('|' + ' '*39 + '=DOMINOS ORDER=' + ' '*39 + '|')
print('+' + '='*93 + '+')

user_details_option = input(
    'Use Pre-entered Details: (y/n) ').lower()

if user_details_option == 'n':
    print('')
    street_no = input('Enter House Number: ')
    street = input('Enter Street: ').upper()
    suburb = input('Enter Suburb: ').upper()
    state = input('Enter State: ').upper()
    postcode = input('Enter Postcode: ')
    print('')
    # delivery or pickup
    order_option = input('Order type: ').lower()
    print('')
    pizza1 = input('Enter Pizza #1: ').upper()
    pizza2 = input('Enter Pizza #2: ').upper()
    pizza3 = input('Enter Pizza #3: ').upper()
    print('')
    name = input('Enter your name: ')
    phone = input('Enter your phone number: ')
    email = input('Enter your email: ')
    print('')
    # instagift, cash, creditcard, paypal
    payment_method = input('Enter payment method: ').lower()
    print('')
elif user_details_option not in ['n', 'y']:
    exit()


# Print Vouchers
print_vouchers()
voucher_id = input('Enter voucher ID: ')

# Select Voucher
voucher = get_vouchers()
code = voucher[int(voucher_id)][0]

order(street_no, street, suburb, state, postcode, order_option,
      code, pizza1, pizza2, pizza3, name, phone, email, payment_method)
