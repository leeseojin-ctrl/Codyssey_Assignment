class StackStructure:
    def __init__(self):
        self.stack = []
        self.limit = 10

    def push(self, data):
        if len(self.stack) >= self.limit:
            print('경고: 스택이 가득 찼습니다. 더 이상 추가할 수 없습니다.')
        else:
            self.stack.append(data)

    def pop(self):
        if self.empty():
            print('경고: 스택이 비어 있습니다. 가져올 내용이 없습니다.')
            return None
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0

    def peek(self):
        if self.empty():
            print('경고: 스택이 비어 있어 마지막 내용을 확인할 수 없습니다.')
            return None
        return self.stack[-1]

    def display_status(self):
        print('\n--- 현재 스택 상태 (시각화) ---')
        if self.empty():
            print('[ Empty ]')
        else:
            for i in range(len(self.stack) - 1, -1, -1):
                print(f'| Index {i}: {self.stack[i]} |')
            print('---------------------------')


# 동작 확인
mystack = StackStructure()

# 1. 데이터 입력 (고유 번호 포함)
print('--- 데이터 입력 시작 ---')
for i in range(1, 12):
    print(f'Push 시도: Data_{i}')
    mystack.push(f'Data_{i}')

# 2. 시각화 확인
mystack.display_status()

# 3. peek 확인
print(f'현재 상단 노드(peek): {mystack.peek()}')

# 4. 데이터 출력 및 빈 상태 확인
print('\n--- 데이터 추출(Pop) 시작 ---')
while not mystack.empty():
    print(f'Pop 결과: {mystack.pop()}')

# 5. 빈 스택에서의 경고 메시지 확인
mystack.pop()
mystack.display_status()
