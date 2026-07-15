def get_hourly_rate(instance_type, os):

    if instance_type == "t3.micro":
        base_rate = 0.01
    elif instance_type =="m5.large":
        base_rate = 0.10
    elif instance_type == "c5.xlarge":
        base_rate = 0.20
    
    if os == "windows":
        base_rate +=0.05
    
    return base_rate
    
def calculate_total_cost(rate, hours):
    total_cost = rate * hours

    return total_cost


def get_s3_rate(storage_tier):

    if storage_tier == "standard":
        rate = 0.023
    elif storage_tier == "glacier":
        rate = 0.004
    elif storage_tier == "deep_archive":
        rate = 0.00099

    return rate



def calculate_s3_cost(rate, gb):

    total_cost = rate *gb

    return total_cost



    
def run_ec2_calculator():
    print("\n--- EC2 Compute Estimator ---")


    while True:
        instance = input("Type of instance (t3.micro, m5.large, c5.xlarge): ").strip().lower()

        if instance not in ["t3.micro", "m5.large", "c5.xlarge"]:
            print("invalid instance")
            continue
        else:
            break

    while True:
        os_model = input("OS Model (linux, windows): ").strip().lower()
        if os_model not in ["linux","windows"]:
            print("invalid model")
            continue
        else:
            break

    while True:

        hours =(input("how many hours will it be running? "))

        if hours.isdigit():
            hours= float(hours)
            break
        elif hours.count(".")==1:
            left, right = hours.split(".")
            if left.isdigit() and right.isdigit():
                hours =float(hours)
                break
            else:
                print("invalid hours")
        else:
            print("invalid hourse")
        
    rate = get_hourly_rate(instance, os_model)

    print(f"your rate: ${rate:.2f}")

    total = calculate_total_cost(rate, hours)

    print(f"your total: ${total:.2f}")



def run_s3_calculator():
    print("\n--- S3 Storage Estimator ---")

    while True:


        storage = input("Enter the storage tier (standard, glacier, deep_archive): ").strip().lower()

        if storage not in ["standard", "glacier", "deep_archive"]:

            print("invalid storage\n")
            continue
        else:
            break

    while True:
        data_size = input("how many GB do you want to store: ")

        if data_size.isdigit():
            data_size = float(data_size)
            break
        elif data_size.count(".")== 1:
            left, right = data_size.split(".")
            if left.isdigit() and right.isdigit():
                data_size = float(data_size)
                break
            else:
                print("invalid size")
        else:
            print("invalid size")


    rate = get_s3_rate(storage)

    print(f"Your rate: ${rate:.2f}")

    total = calculate_s3_cost(rate, data_size)

    print(f"your total: {total:.2f}")


def main():
    while True:
        print("=== Welcome to the AWS Cloud Estimator ===")
        print("1. Calculate EC2 Compute Costs")
        print("2. Calculate S3 Storage Costs")
        print("3. Quit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            run_ec2_calculator()
        elif choice == "2":
            run_s3_calculator()
        elif choice == "3":
            print("Exiting calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please type 1, 2, or 3.\n")

if __name__=="__main__":
    main()
