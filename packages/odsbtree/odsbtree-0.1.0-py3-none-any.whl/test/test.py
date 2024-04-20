class ObliviousStack:
    def __init__(self):
        self.stack = []  # 用于模拟栈的列表
        self.top = -1  # 栈顶位置，初始为-1表示栈为空

    def next_id(self):
        # 生成下一个节点的唯一标识符
        return len(self.stack)

    def start(self):
        # 初始化或重置操作
        pass

    def access(self, operation, id=None, data=None):
        if operation == 'Insert':
            self.stack.append(data)  # 将数据节点插入栈中
            self.top += 1
        elif operation == 'Read':
            if 0 <= id < len(self.stack):
                return self.stack[id]  # 返回指定ID的数据节点
            else:
                return None
        elif operation == 'Del':
            if 0 <= id < len(self.stack):
                self.stack[id] = None  # 删除指定ID的数据节点
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def finalize(self, top, padVal=1):
        # 结束操作，可以在这里进行任何清理工作或安全措施
        pass

    def push(self, data_node):
        self.start()
        id = self.next_id()
        self.access('Insert', id, (data_node, self.top))
        self.top = id
        self.finalize(self.top)

    def pop(self):
        if self.top == -1:
            return None  # 栈为空时返回None
        self.start()
        data_node, next_id = self.access('Read', self.top)
        self.access('Del', self.top)
        self.top = next_id
        self.finalize(self.top)
        return data_node

# 示例使用
ods_stack = ObliviousStack()
ods_stack.push("first")
ods_stack.push("second")
print(ods_stack.pop())  # 应该输出 "second"
print(ods_stack.pop())  # 应该输出 "first"
