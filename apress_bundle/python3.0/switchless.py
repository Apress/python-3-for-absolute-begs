#! /usr/bin/python3.0

scope = {'potrzebie':'fershlugginer',
        'brian':'very naughty boy',
        'is':'='}
keywords = {'quit':'break',
            'scope':'print scope',
	    'vars': 'print vars()',
	    'globals':'print globals()',
	    'locals':'print locals()'}
while True:
    command = eval(input(':-> '))
    try:
        exec(keywords[command.lower()])
    except SyntaxError as msg:
        print(("Syntax Error:", msg))
    except:
        try:
            command, args = command.split(" ",1)
        except ValueError as msg:
            print(("Value Error:", msg))
        else:
            args = args.split()
        try:
            exec('print ' + repr(scope[command]), scope)
        except KeyError:
                print("Huh?")


