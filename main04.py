class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def insert(self, position, data):
        if position < 0 or position > self.count:
            return False

        new_node = Node(data)

        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self.count += 1
        return True

    def delete(self, data):
        current = self.head
        previous = None

        while current is not None:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self.count -= 1
                return True
            previous = current
            current = current.next
        return False

    def get_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


class CircularList:
    def __init__(self):
        self.head = None
        self.current_node = None
        self.count = 0

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
        self.count += 1

    def delete(self, data):
        if not self.head:
            return False

        current = self.head
        previous = None
        found = False

        for _ in range(self.count):
            if current.data == data:
                found = True
                break
            previous = current
            current = current.next

        if found:
            if self.count == 1:
                self.head = None
                self.current_node = None
            else:
                if current == self.head:
                    last = self.head
                    while last.next != self.head:
                        last = last.next
                    self.head = current.next
                    last.next = self.head
                else:
                    previous.next = current.next
                
                if self.current_node == current:
                    self.current_node = self.head
            
            self.count -= 1
            return True
        return False

    def get_next(self):
        if not self.head:
            return None
        if self.current_node is None:
            self.current_node = self.head
        else:
            self.current_node = self.current_node.next
        return self.current_node.data

    def search(self, data):
        if not self.head:
            return False
        current = self.head
        for _ in range(self.count):
            if current.data == data:
                return True
            current = current.next
        return False


if __name__ == '__main__':
    linkedlist = LinkedList()
    linkedlist.insert(0, 'Hype Boy')
    linkedlist.insert(1, 'Ditto')
    linkedlist.insert(1, 'OMG')
    print('LinkedList:', linkedlist.get_list())
    
    linkedlist.delete('OMG')
    print('After Delete:', linkedlist.get_list())

    circularlist = CircularList()
    songs = ['song1.mp3', 'song2.mp3', 'song3.mp3']
    for s in songs:
        circularlist.insert(s)
        
    print('Search song2.mp3:', circularlist.search('song2.mp3'))
    
    for i in range(5):
        print(f'Playing {i + 1}: {circularlist.get_next()}')
