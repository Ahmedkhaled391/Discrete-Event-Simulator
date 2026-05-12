# We made sure that A,C,M satisfy the LCG constraints for getting a full period without repitition

# 1. C is relatively prime to M (C is odd)
# 2. Every prime factor of M divides (A - 1)
# 3. If M is divisible by 4, (A - 1) is also divisible by 4
# Now we can get a full period of 2^32, without repititions

A = 1664525
C = 1013904223
M = 2**32
MIN_TIME = 1
MAX_TIME = 10


def next_lcg_value(seed, a=A, c=C, m=M):
    return (a * seed + c) % m


def lcg(seed, count, a=A, c=C, m=M):
    if count < 0:
        raise ValueError("Positive only")

    values = []
    current = seed

    for _ in range(count):
        current = next_lcg_value(current, a, c, m)
        values.append(current)

    return values

#Converts a huge raw LCG number into a smaller usable range.
def scale_to_time(value, min_time=MIN_TIME, max_time=MAX_TIME):
    if min_time > max_time:
        raise ValueError("min time must be <= max time")

    return min_time + (value % (max_time - min_time + 1))


def generate_times(n, seed, min_time=MIN_TIME, max_time=MAX_TIME):
    if n < 0:
        raise ValueError("n must be non-negative")

    # Use a single LCG stream to make it deterministic.
    raw_values = lcg(seed, 2 * n)
    scaled_values = [
        scale_to_time(value, min_time, max_time) for value in raw_values
    ]

    inter_arrival_times = scaled_values[:n]
    service_times = scaled_values[n:]

    return inter_arrival_times, service_times


def print_generated_sequences(inter_arrival_times, service_times):
    print("Generated inter-arrival times:")
    print(inter_arrival_times)
    print("Generated service times:")
    print(service_times)

# generate , print , return inputs 
def prepare_simulation_inputs(n, seed):
    inter_arrival_times, service_times = generate_times(n, seed)
    print_generated_sequences(inter_arrival_times, service_times)
    return inter_arrival_times, service_times



