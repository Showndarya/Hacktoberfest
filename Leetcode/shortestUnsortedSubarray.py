nums=list(map(int,input().split()))

temp=sorted(nums)

start,end=-1,-1

for i in range(len(nums)):
	if(nums[i]!=temp[i]):
		start=i
		break

for i in range(len(nums)-1,-1,-1):
	if(nums[i]!=temp[i]):
		end=i
		break

if(start==-1 or end==-1):
	print("0")
else:
	print(end-start+1)