import random
import string


def rand_str(length=12):
	return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
