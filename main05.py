class Node:
    """트리의 각 노드를 표현하는 클래스입니다."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    """이진 탐색 트리 클래스입니다."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        """새로운 원소를 트리에 추가합니다."""
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_node(self.root, key)

    def _insert_node(self, node, key):
        """내부적으로 노드를 재귀적으로 찾아 삽입하는 헬퍼 함수입니다."""
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_node(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_node(node.right, key)
        # 이미 존재하는 값인 경우 중복 삽입을 하지 않습니다.

    def find(self, key):
        """원하는 값의 존재 유무를 확인하여 True/False를 반환합니다."""
        return self._find_node(self.root, key)

    def _find_node(self, node, key):
        """내부적으로 노드를 탐색하는 헬퍼 함수입니다."""
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._find_node(node.left, key)
        else:
            return self._find_node(node.right, key)

    def delete(self, key):
        """특정 원소를 트리에서 삭제합니다."""
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, node, key):
        """내부적으로 노드를 삭제하고 트리를 재구성하는 헬퍼 함수입니다."""
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # 삭제할 노드를 찾은 경우 (key == node.key)
            
            # 자식이 하나이거나 없는 경우
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # 자식이 둘인 경우: 오른쪽 서브트리에서 가장 작은 값을 찾아 대체
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete_node(node.right, temp.key)

        return node

    def _get_min_value_node(self, node):
        """서브트리에서 최솟값을 가진 노드를 반환합니다."""
        current = node
        while current.left is not None:
            current = current.left
        return current


# 지시사항에 따라 인스턴스(객체)의 이름을 binarytree로 생성
binarytree = BinarySearchTree()

# --- 실행 및 테스트 코드 (확인용) ---
if __name__ == '__main__':
    # 원소 추가 테스트
    binarytree.insert(50)
    binarytree.insert(30)
    binarytree.insert(20)
    binarytree.insert(40)
    binarytree.insert(70)
    binarytree.insert(60)
    binarytree.insert(80)

    # 문자열 홑따옴표(' ') 원칙 준수
    print('--- 탐색(find) 테스트 ---')
    print('20 존재 유무:', binarytree.find(20))
    print('90 존재 유무:', binarytree.find(90))

    # 원소 삭제 테스트
    print('\n--- 삭제(delete) 테스트 ---')
    print('20 삭제 수행')
    binarytree.delete(20)
    print('20 존재 유무:', binarytree.find(20))

    print('30 삭제 수행')
    binarytree.delete(30)
    print('30 존재 유무:', binarytree.find(30))

    print('50 (루트 노드) 삭제 수행')
    binarytree.delete(50)
    print('50 존재 유무:', binarytree.find(50))
    print('70 존재 유무:', binarytree.find(70))
