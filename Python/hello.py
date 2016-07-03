 # This program says hello and asks for my name.

print('Hello World')
print('What is your name?')      #ask for user's name
myName = input()
print('It is good to meet you, ' + myName)
print('The length of your name is:')
print(len(myName))
myAge = input()
print('You will be ' + str(int(myAge) + 1)+ "in a year.")