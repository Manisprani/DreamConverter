import sys
def to(log_output, b):
    if b:
        sys.stdout = open(log_output, 'w')
