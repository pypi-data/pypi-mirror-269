class ObliviousDataStructure:
    def __init__(self):
        self.cache = {}  # 用于临时存储节点数据
        self.rootPos = None  # 根节点位置

    def start(self, rootPos):
        # 初始化操作，更新缓存以包含根位置
        self.rootPos = rootPos

    def access(self, op, id, data=None):
        # 根据操作类型处理数据
        if op == 'Insert':
            # 插入操作：在缓存中插入新节点，位置和子节点位置映射稍后更新
            self.cache[id] = {'data': data, 'pos': None, 'childrenPos': None}
        elif op == 'Read':
            # 读取操作：如果缓存中有该节点，直接返回；否则，模拟从存储中读取
            if id in self.cache:
                return self.cache[id]['data']
            else:
                # 这里简化处理，假设每次读取都成功，并将节点添加到缓存中
                self.cache[id] = {'data': data, 'pos': 'simulated_pos', 'childrenPos': {}}
                return data
        elif op == 'Write':
            # 写入操作：更新节点数据，如果节点不在缓存中，先模拟读取
            if id not in self.cache:
                self.access('Read', id, data)
            self.cache[id]['data'] = data
        elif op == 'Del':
            # 删除操作：如果缓存中有该节点，直接移除；否则，模拟读取后移除
            if id not in self.cache:
                self.access('Read', id)
            del self.cache[id]

    def finalize(self, rootID, padVal):
        # 完成操作：更新节点位置，执行必要的填充，并将所有更改写回存储
        # 这里简化处理，不实现真正的填充和写回逻辑
        print(f"Finalizing with rootID {rootID} and padVal {padVal}")
        self.cache.clear()

# 示例使用
ods = ObliviousDataStructure()
ods.start('root_pos')
ods.access('Insert', 'id1', 'data1')
data = ods.access('Read', 'id1')
print(f"Read data: {data}")
ods.access('Write', 'id1', 'new_data1')
data = ods.access('Read', 'id1')
print(f"Read updated data: {data}")
ods.finalize('new_root_id', 1)

class BPlusTreeNode:
    def __init__(self, is_leaf=True, keys=None, children=None):
        self.is_leaf = is_leaf
        self.keys = keys or []
        self.children = children or []

class ODSBPlusTree:
    def __init__(self, degree):
        self.root = "root_id"  # 根节点ID
        self.degree = degree
        self.ods = ObliviousDataStructure()  # 创建ODS实例
        self.ods.start(self.root)  # 初始化ODS，设置根位置
        # 初始化根节点
        self.ods.access('Insert', self.root, {'data': BPlusTreeNode(is_leaf=True), 'pos': None, 'childrenPos': None})

    def insert(self, key, value=None):
        # 递归地插入键值对
        self._insert(self.root, key, value)
        # 注意：这里可能需要处理根节点分裂的情况

    def _insert(self, node_id, key, value):
        # 通过ODS访问节点数据
        node_data = self.ods.access('Read', node_id)
        node = node_data['data']
        if node.is_leaf:
            # 在叶子节点插入键值对
            index = 0
            while index < len(node.keys) and node.keys[index][0] < key:
                index += 1
            node.keys.insert(index, (key, value))
            # 通过ODS更新节点数据
            self.ods.access('Write', node_id, {'data': node, 'pos': node_data['pos'], 'childrenPos': node_data['childrenPos']})
        # 处理非叶子节点的插入逻辑...
        # 注意：这里的实现被简化了，需要完整地处理节点分裂等情况

    def search(self, node_id, key):
        # 递归搜索键
        node_data = self.ods.access('Read', node_id)
        node = node_data['data']
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i][1]  # 找到键，返回值
        elif node.is_leaf:
            return None  # 叶子节点未找到键
        else:
            # 搜索子节点
            child_id = node.children[i]  # 子节点ID
            return self.search(child_id, key)

# 示例使用
bpt = ODSBPlusTree(degree=3)
bpt.insert(1, "One")
bpt.insert(2, "Two")
print(bpt.search(bpt.root, 1))  # 应该输出 "One"
print(bpt.search(bpt.root, 3))  # 应该输出 None