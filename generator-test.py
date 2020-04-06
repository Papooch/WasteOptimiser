def generate(nums):
   for num in nums:
      yield num

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

generator = generate(numbers)

def a2g(arr): return (n for n in arr)

numbers = iter(numbers)

for g in numbers:
   print(g)
   if g == 4:
      print("next is", next(numbers), "and", next(numbers))


for g in numbers:
   print(g)
   if g == 4:
      print("aaaa is", next(numbers), "and", next(numbers))