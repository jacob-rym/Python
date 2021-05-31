PLACEHOLDER = "[name]"

with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter = letter_file.read()

    for name in names:
        formatted_name = name.rstrip()
        new_letter = letter.replace(PLACEHOLDER, formatted_name)
        with open(f"./Output/ReadyToSend/{formatted_name}.txt", mode="w") as completed_letter:
            completed_letter.write(new_letter)
