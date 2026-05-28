import warnings

# '경고 메시지 없이 실행' 제약 조건을 위해 불필요한 UserWarning 숨김 처리
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


class IrisMachineLearning:
    def __init__(self):
        # 1. Scikit-learn 데이터셋 불러오기
        self.iris_dataset = load_iris()
        self.data = self.iris_dataset.data
        self.target = self.iris_dataset.target

        # 데이터 분할 및 모델을 위한 변수 초기화
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.knn_model = None

    def explore_dataset(self):
        # DESCR 출력
        print('--- 1. DESCR (데이터셋 설명) ---')
        print(self.iris_dataset.DESCR)

        # target_names 출력
        print('\n--- 2. target_names ---')
        print(self.iris_dataset.target_names)

        # feature_names 출력
        print('\n--- 3. feature_names ---')
        print(self.iris_dataset.feature_names)

        # 실제 데이터 항목 분석
        print('\n--- 4. Data 항목 분석 ---')
        print(f'모양(shape): {self.data.shape}')
        print(f'차원(ndim): {self.data.ndim}')
        print(f'타입(dtype): {self.data.dtype}')
        print(f'앞에서부터 5개 샘플:\n{self.data[:5]}')

        # target 항목 분석
        print('\n--- 5. Target 항목 분석 ---')
        print(f'모양(shape): {self.target.shape}')
        print(f'차원(ndim): {self.target.ndim}')
        print(f'타입(dtype): {self.target.dtype}')
        print(f'앞에서부터 5개 샘플:\n{self.target[:5]}')

    def draw_distribution_plot(self):
        # [보너스 과제 1] 데이터 분포 그래프 시각화
        # Sepal length와 Sepal width를 기준으로 시각화합니다.
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(
            self.data[:, 0], 
            self.data[:, 1], 
            c=self.target, 
            cmap='viridis'
        )
        
        plt.xlabel(self.iris_dataset.feature_names[0])
        plt.ylabel(self.iris_dataset.feature_names[1])
        plt.title('Iris Data Distribution (Sepal Length vs Width)')
        
        # 범례 추가 (문자열 내 부득이한 경우이므로 " " 사용을 지양하고 ' ' 유지)
        plt.legend(*scatter.legend_elements(), title='Target')
        plt.show()

    def train_and_predict(self):
        # 데이터 분할 (대입문 '=' 앞뒤로 공백 적용)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.data, 
            self.target, 
            random_state=0
        )

        # 분할된 데이터의 모양과 크기 출력
        print('\n--- 6. 데이터 분할 결과 ---')
        print(f'X_train 모양: {self.x_train.shape}, 크기: {self.x_train.size}')
        print(f'X_test 모양: {self.x_test.shape}, 크기: {self.x_test.size}')
        print(f'y_train 모양: {self.y_train.shape}, 크기: {self.y_train.size}')
        print(f'y_test 모양: {self.y_test.shape}, 크기: {self.y_test.size}')

        # n_neighbors=1 로 모델 학습 
        # (PEP 8에 따라 함수 키워드 인자의 '=' 앞뒤에는 공백을 두지 않음)
        self.knn_model = KNeighborsClassifier(n_neighbors=1)
        self.knn_model.fit(self.x_train, self.y_train)

        # 예측 수행
        new_sample = [[5.0, 2.9, 1.0, 0.2]]
        prediction = self.knn_model.predict(new_sample)
        predicted_class_name = self.iris_dataset.target_names[prediction[0]]
        
        print('\n--- 7. 예측 결과 ---')
        print(f'입력 값 {new_sample}에 대한 예측: {prediction[0]} ({predicted_class_name})')

    def evaluate_model(self):
        # [보너스 과제 2] 모델 평가
        train_accuracy = self.knn_model.score(self.x_train, self.y_train)
        test_accuracy = self.knn_model.score(self.x_test, self.y_test)

        print('\n--- 8. 모델 평가 (정확도) ---')
        print(f'Train 스코어: {train_accuracy:.2f}')
        print(f'Test 스코어: {test_accuracy:.2f}')


if __name__ == '__main__':
    # 클래스 인스턴스화 및 메서드 순차 실행
    # = 앞뒤로 공백을 주는 PEP 8 규칙 준수
    ml_task = IrisMachineLearning()
    
    ml_task.explore_dataset()
    ml_task.draw_distribution_plot()
    ml_task.train_and_predict()
    ml_task.evaluate_model()
