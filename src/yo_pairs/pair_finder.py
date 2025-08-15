from typing import Dict, List, Tuple


def find_yo_pairs(freq_map: Dict[str, int]) -> List[Tuple[str, str, int]]:
    result = []
    for word, cnt_yo in freq_map.items():
        if 'ё' in word or 'Ё' in word:
            e_var = word.replace('ё', 'е').replace('Ё', 'Е')
            if e_var in freq_map:
                result.append((word, e_var, cnt_yo + freq_map[e_var]))
    return sorted(result, key=lambda x: x[2], reverse=True)
