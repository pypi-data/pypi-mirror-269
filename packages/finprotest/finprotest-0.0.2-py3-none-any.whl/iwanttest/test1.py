# list를 입력받아 합을 반환
def add(l):
    ans = sum(l)
    return ans

# list를 입력받아 곱을 반환
def mul(l):
    ans = 1
    for i in l:
        ans*=i
    return ans