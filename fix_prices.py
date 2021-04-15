from main import load_and_calc_container_sum, fix_prices
from pathlib import Path
import re


def main():
    files = [f.name for f in Path('.').glob('*_container_data_with_prices.json')]
    age_to_filename_mapping = {int(re.findall(r'^([0-9]*)', f)[0]): f for f in files}
    latest_file_index = sorted(age_to_filename_mapping)[-1]
    file_name_to_process = age_to_filename_mapping[latest_file_index]

    before = load_and_calc_container_sum(file_name_to_process)
    fix_prices(file_name_to_process)
    after = load_and_calc_container_sum(file_name_to_process)
    print('file_name_to_process', file_name_to_process)
    print('before', before)
    print('after', after)


if __name__ == '__main__':
    main()
