nums = [1, 2, 4, 5]
missing_number = []
for i in range(len(nums)):
    if (i+1) != nums[i]:
        missing_number.append(i+1)
        
print(missing_number)
