import datetime
import queue
import random
import threading
import time
import sqlite3

try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

sensorQ = queue.Queue()
stop_flag = False

db_conn = None
db_cursor = None


def init_db():
    global db_conn, db_cursor
    
    if HAS_MYSQL:
        try:
            db_conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='password',
                database='smart_farm'
            )
            db_cursor = db_conn.cursor()
            db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS parm_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_name VARCHAR(20),
                    input_time DATETIME,
                    temperature INT,
                    illuminance INT,
                    humidity INT
                )
            ''')
            print('MySQL 데이터베이스 연결 및 테이블 준비 완료.')
            return
        except Exception as e:
            print(f'MySQL 연결 실패({e}). 기본 제공되는 SQLite3로 대체 실행합니다.')
            db_conn = None

    if db_conn is None:
        db_conn = sqlite3.connect(':memory:', check_same_thread=False)
        db_cursor = db_conn.cursor()
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS parm_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_name TEXT,
                input_time DATETIME,
                temperature INTEGER,
                illuminance INTEGER,
                humidity INTEGER
            )
        ''')
        print('SQLite3 메모리 데이터베이스 준비 완료.')


class DataFrame:
    def __init__(self):
        self.rows = []

    def append(self, row_data):
        self.rows.append(row_data)

    def print_5min_average(self):
        print('\n--- [보너스 1] DataFrame 5분 단위(누적) 평균 데이터 ---')
        sensor_sums = {}
        for row in self.rows:
            name = row['name']
            if name not in sensor_sums:
                sensor_sums[name] = {'count': 0, 'temp': 0, 'light': 0, 'humi': 0}
            
            sensor_sums[name]['count'] += 1
            sensor_sums[name]['temp'] += row['temp']
            sensor_sums[name]['light'] += row['light']
            sensor_sums[name]['humi'] += row['humi']

        for name in sorted(sensor_sums.keys()):
            data = sensor_sums[name]
            c = data['count']
            if c > 0:
                avg_t = data['temp'] / c
                avg_l = data['light'] / c
                avg_h = data['humi'] / c
                print(f'{name} - 평균 온도: {avg_t:.1f}, 평균 조도: {avg_l:.1f}, 평균 습도: {avg_h:.1f}')


class ParmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.illuminance = 0
        self.humidity = 0

    def set_data(self):
        self.temperature = random.randint(20, 30)
        self.illuminance = random.randint(5000, 10000)
        
        if random.random() > 0.9:
            self.humidity = random.randint(91, 100)
        else:
            self.humidity = random.randint(40, 70)

    def get_data(self):
        return self.temperature, self.illuminance, self.humidity


def insert_sensor_data(sensor_name, input_time, temp, light, humi):
    if db_conn is None:
        return

    is_sqlite = 'sqlite3' in str(type(db_conn))
    placeholder = '?' if is_sqlite else '%s'
    
    sql = f'''
        INSERT INTO parm_data 
        (sensor_name, input_time, temperature, illuminance, humidity) 
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
    '''
    
    try:
        db_cursor.execute(sql, (sensor_name, input_time, temp, light, humi))
        db_conn.commit()
    except Exception as e:
        print(f'데이터베이스 입력 오류: {e}')


def get_sensor_data():
    if db_conn is None:
        return []

    sql = 'SELECT sensor_name, input_time, temperature, humidity FROM parm_data ORDER BY input_time ASC'
    try:
        db_cursor.execute(sql)
        return db_cursor.fetchall()
    except Exception as e:
        print(f'데이터 조회 오류: {e}')
        return []


def process_queue():
    while not stop_flag or not sensorQ.empty():
        while not sensorQ.empty():
            data = sensorQ.get()
            insert_sensor_data(data[0], data[1], data[2], data[3], data[4])
        
        time.sleep(1)


def run_sensor(sensor, dataframe):
    while not stop_flag:
        sensor.set_data()
        t, l, h = sensor.get_data()
        
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')

        print(f'{time_str} {sensor.name} — temp {t:02d}, light {l:04d}, humi {h:02d}')

        sensorQ.put((sensor.name, time_str, t, l, h))
        dataframe.append({'time': now, 'name': sensor.name, 'temp': t, 'light': l, 'humi': h})

        for _ in range(10):
            if stop_flag:
                break
            time.sleep(1)


def print_db_statistics():
    if db_conn is None:
        return

    print('\n--- [보너스 2] 센서별 데이터베이스 통계 (시간대별 평균) ---')
    is_sqlite = 'sqlite3' in str(type(db_conn))
    
    if is_sqlite:
        sql = '''
            SELECT sensor_name, COUNT(*), strftime('%H', input_time) as hr,
                   AVG(temperature), AVG(illuminance), AVG(humidity)
            FROM parm_data
            GROUP BY sensor_name, hr
        '''
    else:
        sql = '''
            SELECT sensor_name, COUNT(*), HOUR(input_time) as hr,
                   AVG(temperature), AVG(illuminance), AVG(humidity)
            FROM parm_data
            GROUP BY sensor_name, hr
        '''

    try:
        db_cursor.execute(sql)
        rows = db_cursor.fetchall()
        for row in rows:
            print(f'[{row[0]}] 건수: {row[1]}건, 시간대: {row[2]}시, '
                  f'평균 온도: {row[3]:.1f}, 평균 조도: {row[4]:.1f}, 평균 습도: {row[5]:.1f}')
    except Exception as e:
        print(f'통계 조회 오류: {e}')


def draw_graph():
    print('\n--- [Task 3] 센서별 시간별 온도 평균 그래프 (습도 90% 초과 시 붉은색 표시) ---')
    data = get_sensor_data()
    if not data:
        print('그래프를 그릴 데이터가 없습니다.')
        return

    grouped = {}
    for row in data:
        s_name = row[0]
        input_time = row[1]
        temp = row[2]
        humi = row[3]

        if isinstance(input_time, str):
            dt = datetime.datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
        else:
            dt = input_time
            
        hour_str = dt.strftime('%Y-%m-%d %H시')

        if s_name not in grouped:
            grouped[s_name] = {}
        if hour_str not in grouped[s_name]:
            grouped[s_name][hour_str] = {'temp': [], 'humi': []}

        grouped[s_name][hour_str]['temp'].append(temp)
        grouped[s_name][hour_str]['humi'].append(humi)

    color_red = '\033[91m'
    color_reset = '\033[0m'

    for s_name in sorted(grouped.keys()):
        print(f'\n[{s_name}]')
        for hour_str, values in grouped[s_name].items():
            avg_temp = sum(values['temp']) / len(values['temp'])
            max_humi = max(values['humi'])

            bar_len = int(avg_temp)
            bar_text = '*' * bar_len

            if max_humi > 90:
                bar_text = f'{color_red}{bar_text} (경고: 해당 시간대 최대 습도 {max_humi}% 도달){color_reset}'

            print(f'{hour_str} | 평균 {avg_temp:4.1f}°C | {bar_text}')


def main():
    global stop_flag
    print('스마트 팜 센서 시뮬레이션을 시작합니다 (약 60초간 동작)...\n')
    
    init_db()
    df = DataFrame()

    sensors = [ParmSensor(f'Parm-{i}') for i in range(1, 6)]
    threads = []

    consumer_t = threading.Thread(target=process_queue)
    consumer_t.daemon = True
    consumer_t.start()

    for sensor in sensors:
        t = threading.Thread(target=run_sensor, args=(sensor, df))
        t.daemon = True
        t.start()
        threads.append(t)

    time.sleep(62)
    stop_flag = True

    for t in threads:
        t.join()

    while not sensorQ.empty():
        time.sleep(0.5)

    print('\n센서 데이터 수집이 완료되었습니다.')

    df.print_5min_average()
    print_db_statistics()
    draw_graph()

    print('\n모든 과제 수행이 성공적으로 완료되었습니다.')


if __name__ == '__main__':
    main()
