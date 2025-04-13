 from collections import defaultdict
from typing import List, Tuple, Dict, Optional


class SensorProcessor:
    """
    Клас для обробки даних датчиків із журналу.
    """

    def __init__(self):
        self.all_sensors: set[str] = set()
        self.big_messages: int = 0
        self.good_ids: set[str] = set()
        self.bad_ids: set[str] = set()
        self.errors_detail: Dict[str, List[str]] = {}
        self.count_per_id: defaultdict[str, int] = defaultdict(int)

    def process_line(self, line: str) -> Optional[Tuple[str, str, str, str]]:
        """
        Обробляє рядок тексту та витягує необхідні дані датчика.

        Аргументи:
            line (str): Рядок для обробки.

        Повертає:
            tuple: (sensor_id, state, sp1, sp2) якщо рядок правильний, інакше None.
        """
        if '> ' not in line or 'BIG;' not in line:
            return None

        # Витягування корисної частини рядка після '> '
        parts = line.split('>')[-1].strip().strip("'").strip('"')

        if not parts.startswith("BIG;"):
            return None

        splited_parts = parts.split(';')

        if len(splited_parts) < 18:
            return None

        sensor_id = splited_parts[2]
        state = splited_parts[17].strip().upper()
        sp1 = splited_parts[6]
        sp2 = splited_parts[13]

        return sensor_id, state, sp1, sp2

    def process_errors(self, sp1: str, sp2: str) -> List[str]:
        """
        Обробляє два стани та визначає на основі бітів помилки пристрою.

        Аргументи:
            sp1 (str): Перша частина флагів стану.
            sp2 (str): Друга частина флагів стану.

        Повертає:
            list: Список помилок пристрою.
        """
        concat_sp = str(sp1)[:-1] + str(sp2)
        pairs_lst = [concat_sp[i:i + 2] for i in range(0, len(concat_sp), 2)]
        bin_pairs = [bin(int(pair))[2:].zfill(8) for pair in pairs_lst]
        fifth_bits = [b[4] for b in bin_pairs]

        errors = []
        if fifth_bits[0] == '1':
            errors.append('Battery device error')
        if fifth_bits[1] == '1':
            errors.append('Temperature device error')
        if fifth_bits[2] == '1':
            errors.append('Threshold central error')

        return errors if errors else ["Unknown device error"]

    def process_file(self, file_path: str) -> None:
        """
        Обробляє файл журналу, категоризуючи датчики за їх станом (хороші або погані).

        Аргументи:
            file_path (str): Шлях до файлу для обробки.
        """
        with open(file_path) as f:
            for line in f:
                processed = self.process_line(line)
                if not processed:
                    continue

                self.big_messages += 1
                sensor_id, state, sp1, sp2 = processed
                self.all_sensors.add(sensor_id)
                self.update_sensor_state(sensor_id, state, sp1, sp2)

    def update_sensor_state(self, sensor_id: str, state: str, sp1: str, sp2: str) -> None:
        """
        Оновлює стан датчика на основі його статусу.

        Аргументи:
            sensor_id (str): Ідентифікатор датчика.
            state (str): Стан датчика.
            sp1 (str): Перша частина стану.
            sp2 (str): Друга частина стану.
        """
        if sensor_id in self.bad_ids:
            return

        if state == 'DD':
            self.bad_ids.add(sensor_id)
            self.good_ids.discard(sensor_id)
            self.errors_detail[sensor_id] = self.process_errors(int(sp1), int(sp2))
            self.count_per_id.pop(sensor_id, None)
        elif state == '02' and sensor_id not in self.bad_ids:
            self.good_ids.add(sensor_id)
            self.count_per_id[sensor_id] += 1

    def print_results(self) -> None:
        """
        Виводить результати обробки в консоль.
        """
        print(f"ALL big messages: {self.big_messages}")
        print(f"BIG messages (distinct sensors): {len(self.all_sensors)}")
        print(f"Successful big messages: {len(self.good_ids)}")
        print(f"Failed big messages: {len(self.bad_ids)}\n")

        for dev_id, errors in self.errors_detail.items():
            print(f"{dev_id}: {', '.join(errors)}")

        print(f"\nSuccess messages count: {len(self.count_per_id)}")
        for dev_id in sorted(self.count_per_id):
            print(f"{dev_id}: {self.count_per_id[dev_id]}")


# Використання:
processor = SensorProcessor()
processor.process_file('app_2.log')
processor.print_results()
