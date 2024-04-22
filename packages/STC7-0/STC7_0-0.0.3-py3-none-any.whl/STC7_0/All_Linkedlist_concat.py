
class ListNode:
	def __init__(self, newItem, nextNode:'ListNode'):
		self.item = newItem
		self.next = nextNode

## 링크리스트의 기본이 되는 ListNode 정의
## self.item은 생성자 인자의 newitem
## self.next는 생성자 인자의 nextNode 주소값 리턴

class BidirectNode:
    def __init__(self, x, prevNode:'BidirectNode', nextNode:'BidirectNode'):
        self.item = x
        self.prev = prevNode
        self.next = nextNode

## 양방향 링크리스트의 기본이 되는 BidirectNode 정의
## self.item은 생성자 인자의 newitem
## self.이전노드주솟값는 이전노드로 설정
## self.다음노드주솟값은 다음노드로 설정



class LinkedListBasic:
	def __init__(self):
		self.__head = ListNode('dummy', None)
		self.__numItems = 0

##self._head는 첫 노드 레퍼런스, ListNode를 통해 dummy 노드 생성
##self.__numItem은 항목의 수 설정


	def __getNode(self, i:int) -> ListNode:
		curr = self.__head # 더미 헤드, index: -1
		for index in range(i+1):
			curr = curr.next
		return curr

 ##i번째의 노드의 주솟값을 찾는 함수, 반환시 ListNode 형태의 클래스 반환
 ##내가 원하는 i번쨰 노드의 주소를 찾기위한 for 반복문 설정
 ##현재노드를 다음노드로 이동
 ##리턴


	def insert(self, i:int, newItem):
		if i >= 0 and i <= self.__numItems:
			prev = self.__getNode(i - 1)
			newNode = ListNode(newItem, prev.next)
			prev.next = newNode
			self.__numItems += 1
		else:
			print("index", i, ": out of bound in insert()")

## 노드를 집어넣는 함수 생성
## if i >= 0 and i <= self.__numItems: 는 인덱스의 유효상태 확인하는 코드
## prev 에 개체의 getNode를 통한 i 번째 전 이전노드의 주솟값 설정
## newNode에 listNode의 클래스 생성을 통해 리턴
## prev의 다음노드 주솟값은 newNode라는 주솟값 초기화
## 항목 추가


	# [알고리즘 5-3] 구현: 연결 리스트의 원소 삭제하기
	def pop(self, i:int):   # i번 노드 삭제. 고정 파라미터
		if (i >= 0 and i <= self.__numItems-1):
			prev = self.__getNode(i - 1)
			curr = prev.next
			prev.next = curr.next
			retItem = curr.item
			self.__numItems -= 1
			return retItem
		else:
			return None

## i번째의 노드의 item을 리턴하고 , 노드를 삭제하는 함수
## if i >= 0 and i <= self.__numItems: 는 인덱스의 유효상태 확인하는 코드
## prev 에 개체의 getNode를 통한 i 번째 전 이전노드의 주솟값 설정
## 현대노드의 위치를 이전노드의 다음노드의 위치로 레퍼런스 설정
## 이전노드의 다음노드의 주솟값을 현대노드의 다음노드의 주솟값으로 초기화하여, i번째 현재노드를 삭제
## 삭제노드의 Item을 retItem 에 반환
## 노드가 삭제되었으므로 개체의 전체 항목수 -1
## Item 리턴


	def isEmpty(self) -> bool:
		return self.__numItems == 0
## 노드가 비어있는지 확인하는 함수
## 개체의 항목수가 0이면 true 아니면 false 리턴

	def size(self) -> int:
		return self.__numItems
## 개체의 항목수 반환하는 함수
## 개체항목수 리턴

	def clear(self):
		self.__head = ListNode("dummy", None)
		self.__numItems = 0

## 모든 개체 초기화 함수
## 헤더노드를 dummy헤더노드로 설정, 다음노드 레퍼런스 X
## 항목수 0


	def reverse(self):
		a = LinkedListBasic()
		for index in range(self.__numItems):
			a.insert(0, self.get(index))
		self.clear()
		for index in range(a.size()):
			self.append(a.get(index))

## 노드의 순서를 역순으로 연결하는 함수
## a 에 링크리스트 클래스의 새로운객체로 초기화
## 현재객체의 항목수만큼 a객체에 0번째 index로 현재객체의 값 삽입
## 현재객체는 삭제
## a객체의 항목수만큼 그전 현재객체에 a객체노드의 값을 맨 마지막에 삽입


	def printList(self):
		curr = self.__head.next=
		while curr != None:
			print(curr.item, end = ' ')
			curr = curr.next
		print()

## 노드의 값을 출력하는 함수
## curr 변수에 더미헤드 다음노드를 가리키는 레퍼런스 설정
## while 현대노드의 값이 None 아닐때동안 반복설정
## curr.item 출력 , 현재노드를 다음노드로 이동


class CircularLinkedList :
	def __init__(self) :
		self.__tail = ListNode("dummy", None)
		self.__tail.next = self.__tail
		self.__numItems = 0

## 원형링크리스트를 설정하는 클래스
## 생성자
## 객체의 __tail(마지막노드)에 ListNode클래스를 통한 더미헤드 레퍼런스(주솟값) 설정
## 객체의 tail의 다음노드를 자기자신의 주솟값으로 설정
## 객체의 항목수는 0

	def C_insert(self, i:int, newItem) -> None:
		if (i >= 0 and i <= self.__numItems):
			prev = self.getNode(i - 1)
			newNode = ListNode(newItem, prev.next)
			prev.next = newNode
			if i == self.__numItems:
				self.__tail = newNode
			self.__numItems += 1
		else:
			print("index", i, ": out of bound in insert()")

## 원형 리스트의 노드를 삽입하는 함수
## if i >= 0 and i <= self.__numItems: 는 인덱스의 유효상태 확인하는 코드
## prev 에 개체의 getNode를 통한 i 번째 전 이전노드의 주솟값 설정
## newNode에 listNode의 클래스 생성을 통해 리턴
## prev의 다음노드 주솟값은 newNode라는 주솟값 초기화
## 추가: i가 항목수(맨 마지막) 이라면 __tail노드에 새 노드 삽입(맨 마지막에 넣고 싶을때)
## 항목 추가

	def C_append(self, newItem) -> None:
		newNode = ListNode(newItem, self.__tail.next)
		self.__tail.next = newNode
		self.__tail = newNode
		self.__numItems += 1

## 원형 리스트의 노드를 맨 마지막에 삽입하는 함수
## newNode변수에 리스트노드 삽입(다음노드의 주소는 __tail의 다음노드 설정)
## __tail의 다음노드는 newNode로 주솟값 리턴
## __tail의 레퍼런스를 newNode로 설정
## 항목 추가


	def C_pop(self, *args):
		if self.isEmpty():
			return None
		if len(args) != 0:
			i = args[0]
		if len(args) == 0 or i == -1:
			i = self.__numItems - 1
		if (i >= 0 and i <= self.__numItems - 1):
			prev = self.getNode(i - 1)
			retItem = prev.next.item
			prev.next = prev.next.next
			if i == self.__numItems - 1:
				self.__tail = prev
			self.__numItems -= 1
			return retItem
		else:
			return None

## i번째 원소를 리턴하고 노드삭제하는 함수
## 가변 파라미터. 인자가 없거나 -1이면 마지막 원소로 처리하기 위함.
## 인덱스 i 결정
## pop(k)과 같이 인자가 있으면 i = k 할당
## pop()에 인자가 없거나 pop(-1)이면 i에 맨 끝 인덱스 할당
## i번 원소 삭제
## 인덱스의 유효한지 확인하는 코드
## if i >= 0 and i <= self.__numItems: 는 인덱스의 유효상태 확인하는 코드
## prev 에 개체의 getNode를 통한 i 번째 전 이전노드의 주솟값 설정
## 현대노드의 위치를 이전노드의 다음노드의 위치로 레퍼런스 설정
## 이전노드의 다음노드의 주솟값을 현대노드의 다음노드의 주솟값으로 초기화하여, i번째 현재노드를 삭제
## 삭제노드의 Item을 retItem 에 반환
## 노드가 삭제되었으므로 개체의 전체 항목수 -1
## Item 리턴


	def C_get(self, *args):
		if self.isEmpty():
			return None
		if len(args) != 0:
			i = args[0]
		if len(args) == 0 or i == -1:
			i = self.__numItems - 1
		if (i >= 0 and i <= self.__numItems - 1):
			return self.getNode(i).item
		else:
			return None

##원형리스트의 i번째 노드의 값을 리턴하는 함수
## i번째 원소를 리턴하고 노드삭제하는 함수
## 가변 파라미터. 인자가 없거나 -1이면 마지막 원소로 처리하기 위함.
## 인덱스 i 결정
## pop(k)과 같이 인자가 있으면 i = k 할당
## pop()에 인자가 없거나 pop(-1)이면 i에 맨 끝 인덱스 할당
## i번 원소 삭제
## 인덱스의 유효한지 확인하는 코드
## 객체의 i번째 getNode의 item을 리턴


	def C_clear(self):
		self.__tail = ListNode("dummy", None)
		self.__tail.next = self.__tail
		self.__numItems = 0

## 원형리스트를 초기화하는 함수
## __tail을 ListNode 더미헤더로 레퍼런스 초기화
## tail의 다음주소를 자기자신으로 설정
## 항목수 0


	def C_reverse(self) -> None:
		__head = self.__tail.next  # 더미 헤드
		prev = __head; curr = prev.next; next = curr.next
		curr.next = __head; __head.next = self.__tail; self.__tail = curr
		for i in range(self.__numItems - 1):
			prev = curr; curr = next; next = next.next
			curr.next = prev

## 원형 리스트의 노드의 연결을 역으로 설정하는 함수
## __head에 tail의 다음노드의 위치값으로 초기화(__head <- __tail로 주소값 연결)
## prev변수에 헤더노드 저장, 현재변수에 이전노드의 다음노드 주솟값 리턴, next노드에 현재노드의 다음노드 리턴
## 현재노드의 다음노드는 이전노드로 연결, 이전노드의 다음노드는 tail노드로 연결, tail노드를 현재노드로 연결(역으로 연결)
## 항목수만큼 이전노드는 현재노드로, 현재는 다음노드로 다음노드는 다음노드의 다음으로 초기화
## 현재노드의 다음노드 주솟값은 이전노드로 연결
## 반복


	def C_getNode(self, i:int) -> ListNode:
		curr = self.__tail.next  # 더미 헤드, index: -1
		for index in range(i+1):
			curr = curr.next
		return curr

## 원형 리스트의 노드의 위치를 찾는 함수
## 현재노드를 tail의 다음노드로 설정= 더미헤드
## i+1만큼 현재노드를 다음노드로 설정
## 노드반환

	def C_printList(self) -> None:
		for element in self:
			print(element, end = ' ')
		print()

## 원형 리스트를 출력하는 함수
## 객체의 item(element) 만큼 반복
## item 출력


	def C_printInterval(self, i,j) :
		curr = self.getNode(i)
		for _ in range(j-i+1) :
			print(curr.item)
			curr = curr.next

## 원형 리스트의 i번째에서 j번째까지 출력하는 함수
## 현재노드의 getNode(i) 를 통해 i번째 주솟값 리턴
## j번째 - i번째 -1만큼 반복하여 현재노드의 item출력
## 현재노드를 다음노드로 설정



class CircularDoublyLinkedList:
	def __init__(self):
		self.__head = BidirectNode("dummy", None, None)
		self.__head.prev = self.__head
		self.__head.next = self.__head
		self.__numItems = 0

## 양방향 원형 링크리스트 클래스 설정
## __head에 BidirectNode클래스 객체 더미헤더로 설정
## __head의 이전노드의 주솟값은 자기자신으로 설정
## __head의 다음노드의 주솟값은 자기자신으로 설정
## 항목수는 0


	def B_insert(self, i:int, newItem) -> None:
		if (i >= 0 and i <= self.__numItems):
			prev = self.getNode(i - 1)
			newNode = BidirectNode(newItem, prev, prev.next)
			newNode.next.prev = newNode
			prev.next = newNode
			self.__numItems += 1
		else:
			print("index", i, ": out of bound in insert()")

## 양방향 링크리스트에 노드를 삽입하는 함수
## 인덱스가 유효한지 확인하는 코드
## prev에 getNode를 통해 i번째 이전노드의 주솟값을 저장
## newNode에 BidirecNode클래스 객체로 리턴, 이전노드의 주소는 prev, 다음노드는 prev.next로 리턴
## newNode의 다음노드의 이전노드주솟값은 newNode로 저장
## 이전노드의 다음노드 주솟값은 newNode로 연결
## 항목수는 +1

	def B_append(self, newItem) -> None:
		prev = self.__head.prev
		newNode = BidirectNode(newItem, prev, self.__head)
		prev.next = newNode
		self.__head.prev = newNode
		self.__numItems += 1

## 양방향 링크리스트에 마지막 인덱스에 노드를 삽입하는 함수
## prev에 __head의 이전노드주솟값 저장
## newNode에 BidirectNode의 객체리턴, 이전노드의 주솟값은 prev, 다음노드의 주솟값은 헤더노드 주솟값 리턴
## 이전노드의 다음노드의 주솟값을 새로운 노드에 저장
## 헤더노드의 이전노드의 주솟값을 새로운 노드에 연결
## 항목수 +1

	def B_pop(self, *args):
		if self.isEmpty():
			return None
		if len(args) != 0:
			i = args[0]
		if len(args) == 0 or i == -1:
			i = self.__numItems - 1
		if (i >= 0 and i <= self.__numItems - 1):
			curr = self.getNode(i)
			retItem = curr.item
			curr.prev.next = curr.next
			curr.next.prev = curr.prev
			self.__numItems -= 1
			return retItem
		else:
			return None

## i번째 원소를 리턴하고 노드삭제하는 함수
## 가변 파라미터. 인자가 없거나 -1이면 마지막 원소로 처리하기 위함.
## 인덱스 i 결정
## pop(k)과 같이 인자가 있으면 i = k 할당
## pop()에 인자가 없거나 pop(-1)이면 i에 맨 끝 인덱스 할당
## i번 원소 삭제
## 인덱스의 유효한지 확인하는 코드
## 현재노드를 getNode(i) 번째로 레퍼런스 저장
## 현재노드의 item을 저장
## 현재노드의 이전노드의 다음노드의 주솟값을 현재노드의 다음노드의 주솟값으로 연결
## 현재노드의 다음노드의 이전노드의 주솟값을 현재노드의 이전노드의 주솟값으로 연결
## 항목수 -1

	def B_get(self, *args):
		if self.isEmpty(): return None
		if len(args) != 0:
			i = args[0]
		if len(args) == 0 or i == -1:
			i = self.__numItems - 1
		if (i >= 0 and i <= self.__numItems - 1):
			return self.getNode(i).item
		else:
			return None

## i번째 원소를 리턴하고 노드삭제하는 함수
## 가변 파라미터. 인자가 없거나 -1이면 마지막 원소로 처리하기 위함.
## 인덱스 i 결정
## pop(k)과 같이 인자가 있으면 i = k 할당
## pop()에 인자가 없거나 pop(-1)이면 i에 맨 끝 인덱스 할당
## i번 원소 삭제
## 인덱스의 유효한지 확인하는 코드
## 객체의 getNode를 통해 i번쨰 item을 리턴

	def B_clear(self):
		self.__head = BidirectNode("dummy", None, None)
		self.__head.prev = self.__head
		self.__head.next = self.__head
		self.__numItems = 0

## 양방향 링크리스트 초기화 함수
## head부분은 BidirectNode의 dummy노드로 초기화
## __head의 이전노드의 주솟값은 자기자신으로 설정
## __head의 다음노드의 주솟값은 자기자신으로 설정
## 항목수 0


	def B_reverse(self) -> None:
		prev = self.__head; curr = prev.next; next = curr.next
		self.__head.next = prev.prev; self.__head.prev = curr
		for i in range(self.__numItems):
			curr.next = prev; curr.prev = next
			prev = curr; curr = next; next = next.next

## 양방향 링크리스트의 노드순서를 역으로 설정하는 함수
## prev를 헤더노드로 , curr를 이전노드의 다음노드로, 다음노드는 현재의 다음노드로 레퍼런스 저장
## 헤더노드의 다음노드의 주솟값 현재노드의 이전노드로 연결, 헤더노드의 이전노드의 주솟값은 현재노드로 연결
## 항목수만큼 현재노드의 다음노드의 주솟값은 이전노드로 연결, 현재노드의 이전노드의 주솟값은 다음노드로 연결
## 이전노드 현재노드로, 현재는 다음, 다음노드는 다음다음노드로 설정

	def B_getNode(self, i:int) -> BidirectNode:
		curr = self.__head  # 더미 헤드, index: -1
		for index in range(i + 1):
			curr = curr.next
		return curr

## 양방향 링크 리스트의 원하는 노드를 찾는 함수
## curr에 더미헤드의 주솟값 리턴
## i번째 + 1만큼 현재노드가 다음노드로 이동
## curr 리턴

	def B_printList(self) -> None:
		for element in self:
			print(element, end = ' ')
		print()

## 양방향 링크 리스트를 출력하는 함수
## 객체의 item(element) 만큼 반복
## item 출력

	def B_printInterval(self, i, j) -> None:
		index = 0;
		for element in self:
			if (i <= index and index <=j):
				print(element, end = ' ')
			if (j == index):
				break
			index += 1
		print()

## 양방향 링크리스트의 i번째에서 j번째까지 출력하는 함수
## 인덱스 0, 객체의 item(element) 만큼 반복
## i 가 index보다 작거나 같거나, j가 index보다 높으면 element 출력
## if j가 index와 비슷하다면 반복 취소(index가 끝가지 감)
