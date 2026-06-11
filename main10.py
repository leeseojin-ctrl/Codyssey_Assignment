import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler

# ==========================================
# 1. 파일 읽기 및 정식 DataFrame 객체 생성
# ==========================================

# abalone_attributes.txt에서 컬럼명 파싱 (첫 줄 출처 태그 예외 처리)
columns_list = []
with open('abalone_attributes.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line_clean = line.strip()
        if line_clean:
            if ']' in line_clean:
                line_clean = line_clean.split(']')[-1].strip()
            columns_list.append(line_clean)

# abalone.txt 읽기 (첫 줄 출처 태그 처리 및 정식 DataFrame 빌드)
with open('abalone.txt', 'r', encoding='utf-8') as f:
    file_content = f.read()

# 만약 데이터 첫머리에 태그가 있다면 제거
if file_content.strip().startswith('['):
    file_content = file_content.split(']', 1)[-1].strip()

# StringIO를 이용해 데이터프레임으로 변환
import io
df = pd.read_csv(io.StringIO(file_content), header=None, names=columns_list)

# 성별(Sex) 컬럼을 label 객체로 분리 후 기존 DataFrame에서 삭제
label = df['Sex']
data = df.drop(columns=['Sex'])

print('--- [Pandas DataFrame 로드 결과 확인] ---')
print(f'추출된 컬럼명: {df.columns.tolist()}')
print(f'data 객체 크기 (성별 제외): {data.shape}')
print(f'label 객체 크기 (성별 분리): {label.shape}\n')


# ==========================================
# 2. Sklearn 패키지를 이용한 Scaling 비교
# ==========================================
min_max_scaler = MinMaxScaler()
standard_scaler = StandardScaler()

data_min_max_pkg = min_max_scaler.fit_transform(data)
data_standard_pkg = standard_scaler.fit_transform(data)


# ==========================================
# 3. Imblearn 패키지를 이용한 Sampling 비교 (Over/Under/SMOTE)
# ==========================================
ros = RandomOverSampler(random_state=42)
rus = RandomUnderSampler(random_state=42)
smote = SMOTE(random_state=42, k_neighbors=2)

x_ros, y_ros = ros.fit_resample(data_min_max_pkg, label)
x_rus, y_rus = rus.fit_resample(data_min_max_pkg, label)
x_smote, y_smote = smote.fit_resample(data_min_max_pkg, label)

print('--- [Sklearn & Imblearn 패키지 처리 결과] ---')
print(f'원본 첫 샘플 Min-Max 스케일링 값: \n{np.round(data_min_max_pkg[0], 4)}')
print(f'Random Over Sampling 적용 후 행 수: {x_ros.shape[0]}')
print(f'Random Under Sampling 적용 후 행 수: {x_rus.shape[0]}')
print(f'SMOTE Sampling 적용 후 행 수: {x_smote.shape[0]}')
