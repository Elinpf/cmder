from cmder.main import get_options

args = get_options()
try:
    args.func(args)
except ValueError as e:
    print("[-] " + repr(e))

except TypeError as e:
    exit()
