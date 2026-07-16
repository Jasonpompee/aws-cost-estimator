storage_prices = {
    "standard": 0.023,
    "intelligent-tiering": 0.025,
    "standard-ia": 0.0125,
    "one-zone-ia": 0.01,
    "glacier-instant": 0.004
}


def calculate_storage_cost(storage_class,number_gb, num_month,storage_prices):
    rate = storage_prices[storage_class]
    total_cost = rate * number_gb *num_month
    return total_cost



def main():



    while True:
        try:
            budget = float(input("enter your budget $"))
            if budget <=0:
                print("budget must be greader than zero")
                continue
            else:
                break
        
        except ValueError:
            print("Please enter a number")

    while True:
        try:


            storage_class = input("enter the storage class: ")
            if storage_class not in storage_prices:
                print("must be a valid storage class")
                continue
            else:
                break

        except EOFError:
            print()
            return
             
             
    while True:
        try:
            data_size = (input("enter the number of GB: "))

            if data_size.isdigit():
                data_size=float(data_size)
                if data_size <= 0:
                    print("data size must be greater than zero")
                    continue
                else:

                 break

            if data_size.count(".")== 1:
                left, right = data_size.split(".")
                if left.isdigit() and right.isdigit():
                    data_size=float(data_size)

                    if data_size <= 0:
                        print("data size must be greater than zero")
                    else:

                     break
                else:
                    print("invalid size")
                    continue
            else:
                print("invalid size")
                continue
        except ValueError:
            print("must be a number ")
            continue

    while True:

        try:

            num_month = input("enter the number of month: ")
            num_month = float(num_month)

            if num_month <= 0:
                raise ValueError
            
            else:
                break
                  
        except ValueError:
            print("must be a number greater than zero")
            continue


    total_cost = calculate_storage_cost(storage_class,data_size,num_month,storage_prices)

    print(f"Storage cost: ${total_cost:.2f}" )

    

    if total_cost > budget:
        amount_over = total_cost - budget
        print(f"Warning: You are over budget by ${amount_over:.2f}")
    else:
        remainder = budget - total_cost
        print(f"You are within budget. ${remainder:.2f} left")


main()