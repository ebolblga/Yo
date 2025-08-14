from typing import List, Tuple


def write_output(pairs: List[Tuple[str, str, int]], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(
            "| Index | Word with 'ё' | Word with 'е' | Combined Frequency |\n"
        )
        f.write('|-|-|-|-|\n')
        for idx, (yo, e, freq) in enumerate(pairs, 1):
            f.write(f'| {idx} | {yo} | {e} | {freq} |\n')
