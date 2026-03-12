import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class SpaceshipTitanicAnalyzer:
    '''스페이스 타이타닉 데이터를 분석하는 클래스'''

    def __init__(self, train_path, test_path):
        self.train_path = train_path
        self.test_path = test_path
        self.full_data = None

    def load_and_merge_data(self):
        '''csv 모듈을 사용하여 데이터를 읽고 Pandas로 병합'''
        train_list = []
        test_list = []

        # 표준 라이브러리 csv를 사용하여 파일 읽기
        with open(self.train_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                train_list.append(row)

        with open(self.test_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # test 데이터에는 Transported 열이 없으므로 결측치 처리
                if 'Transported' not in row:
                    row['Transported'] = None
                test_list.append(row)

        # Pandas 객체로 변환 및 병합
        df_train = pd.DataFrame(train_list)
        df_test = pd.DataFrame(test_list)
        
        # 데이터 타입 조정 (수치형 데이터 변환)
        for df in [df_train, df_test]:
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            if 'Transported' in df.columns:
                df['Transported'] = df['Transported'].map(
                    {'True': True, 'False': False, None: None}
                )

        self.full_data = pd.concat([df_train, df_test], axis=0).reset_index(drop=True)
        
        print(f'전체 데이터 수량: {len(self.full_data)}개')
        return self.full_data

    def find_high_correlation(self):
        '''Transported 항목과 가장 관련성이 높은 수치 항목 찾기'''
        # 분석을 위해 True/False를 1/0으로 변환한 임시 데이터프레임 생성
        train_only = self.full_data[self.full_data['Transported'].notnull()].copy()
        train_only['Transported'] = train_only['Transported'].astype(int)
        
        # 수치형 데이터만 추출하여 상관관계 계산
        numeric_df = train_only.select_dtypes(include=['float64', 'int64', 'int32'])
        corr_matrix = numeric_df.corr()
        
        target_corr = corr_matrix['Transported'].sort_values(ascending=False)
        print('\n[Transported 항목과의 상관계수]')
        print(target_corr)
        
        return target_corr

    def visualize_age_transported(self):
        '''나이대별 Transported 여부 시각화'''
        # 분석용 데이터 복사 (결측치 제외)
        plot_df = self.full_data[self.full_data['Transported'].notnull()].copy()
        
        # 연령대 구간 설정 (10대 단위)
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
        labels = ['0s', '10s', '20s', '30s', '40s', '50s', '60s', '70s+']
        plot_df['AgeGroup'] = pd.cut(
            plot_df['Age'], bins=bins, labels=labels, right=False
        )

        plt.figure(figsize=(10, 6))
        sns.countplot(data=plot_df, x='AgeGroup', hue='Transported', palette='viridis')
        plt.title('Transported Status by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Passenger Count')
        plt.show()

    def visualize_destination_age_dist(self):
        '''보너스: Destination별 승객 연령대 분포 시각화'''
        plot_df = self.full_data.copy()
        
        # 연령대 생성
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 100]
        labels = ['0s', '10s', '20s', '30s', '40s', '50s', '60s', '70s+']
        plot_df['AgeGroup'] = pd.cut(
            plot_df['Age'], bins=bins, labels=labels, right=False
        )

        plt.figure(figsize=(12, 6))
        sns.countplot(
            data=plot_df, 
            x='Destination', 
            hue='AgeGroup', 
            palette='magma'
        )
        plt.title('Age Distribution by Destination')
        plt.xlabel('Destination')
        plt.ylabel('Passenger Count')
        plt.legend(title='Age Group', loc='upper right')
        plt.show()


def run_analysis():
    '''메인 실행 함수'''
    # 파일 경로 설정
    train_file = 'train.csv'
    test_file = 'test.csv'
    
    # 분석기 인스턴스 생성 (CapWord 규칙 준수)
    analyzer = SpaceshipTitanicAnalyzer(train_file, test_file)
    
    # 1~4. 데이터 로드 및 병합
    analyzer.load_and_merge_data()
    
    # 5. 상관관계 확인
    analyzer.find_high_correlation()
    
    # 6. 연령대별 시각화
    analyzer.visualize_age_transported()
    
    # 7. 보너스 과제
    analyzer.visualize_destination_age_dist()


if __name__ == '__main__':
    run_analysis()