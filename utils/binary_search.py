def binary_search_nearest(sequence, target, get_val_func=None):
	"""
	:param sequence: сортированная по неубыванию последовательность
	:param target: искомое значение
	:param get_val_func: Функция от 1 аргумента (элемента из sequence),
		возвращающая значение сопоставленное этому элементу
	:return: индекс, (True, если точное значение, False, если ближайшее к искомому)
	"""
	min_idx, max_idx = 0, len(sequence) - 1
	best_ind, exact = min_idx, False

	while min_idx <= max_idx:
		mid_idx = min_idx + (max_idx - min_idx) // 2

		if get_val_func:
			val = get_val_func(sequence[mid_idx])
		else:
			val = sequence[mid_idx]

		if val < target:
			min_idx = mid_idx + 1
		elif val > target:
			max_idx = mid_idx - 1
		else:
			best_ind = mid_idx
			exact = True
			break

		if abs(val - target) <= abs(val - target):
			best_ind = mid_idx

	return best_ind, exact
