def main():
    friend_ages = {
        "Rolf": 24,
        "Adam": 30,
        "Anne": 27
    }

    print(friend_ages["Anne"])

    friend_ages["bob"] = 20
    print(friend_ages)
    friend_ages["Rolf"] = 40
    print(friend_ages)


    student_attendance = {
        "Rolf": 60,
        "Bob": 80,
        "Anne": 100
    }

    sum = 0
    avg = 0
    counter = 0
    if "Bob" in student_attendance:
        print("Bob attended")

    for name in student_attendance:
        print(f"{name} {student_attendance[name]}")

    for name, attended in student_attendance.items():
        counter += 1
        sum += attended
        print(f"{name} {attended}")

    avg = sum / counter
    print(f"avrage: {avg}")
    
    friends = [
        {"name": "Rolf", "age": 24},
        {"name": "Adam", "age": 30},
        {"name": "Anne", "age": 27}
    ]

    second_friend = friends[1]

    print(second_friend["name"])
    old_friends = []
    for index, friend in enumerate(friends):
        print(friend)
        if friend["age"] > 25:
            old_friends.append(friends[index])   
    
    print(old_friends)


if __name__ == "__main__":
    main()