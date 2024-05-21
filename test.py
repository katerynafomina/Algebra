import networkx as nx
import matplotlib.pyplot as plt

# Визначення матриці суміжності
matrix_data = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 0]
]

# Створення графа з матриці суміжності
G = nx.Graph()
size = len(matrix_data)

for i in range(size):
    for j in range(i+1, size):  # Використовуємо тільки верхню трикутну частину матриці
        if matrix_data[i][j] == 1:
            G.add_edge(i, j)

# Візуалізація графа
pos = nx.spring_layout(G)  # Використовуємо алгоритм розкладки "spring" для позиціонування вузлів
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', font_weight='bold')

# Показуємо графік
plt.show()
