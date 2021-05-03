from scipy.stats.stats import spearmanr

list_a = [1.0] * 1742
list_b = list(list_a)
for i in range(421):
	list_b[i] = 2.0
print(list_b)
print(spearmanr(list_a, list_b))