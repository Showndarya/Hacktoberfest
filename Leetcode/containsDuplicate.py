class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        
        if(len(nums)<=1):
            return False
        
        nums.sort()
        
        for i in range(len(nums)-1):
            if(nums[i]==nums[i+1]):
                return True
        
        
        return False