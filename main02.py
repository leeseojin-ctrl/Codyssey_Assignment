import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def set_matplotlib_korean_font():
    '''코랩 환경에서 그래프 한글 깨짐 방지를 위한 폰트 설정'''
    font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
    try:
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
    except FileNotFoundError:
        plt.rc('font', family='NanumBarunGothic')
    plt.rc('axes', unicode_minus=False)


def load_and_preprocess_data(file_name):
    '''CSV 파일을 읽고 일반가구원 외 컬럼 삭제 및 전처리를 수행한다.'''
    try:
        df = pd.read_csv(file_name, encoding='utf-8')
    except (UnicodeDecodeError, UnicodeError):
        df = pd.read_csv(file_name, encoding='cp949')

    # 컬럼명 정리
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")

    # [수행과제] 일반가구원을 제외한 나머지 컬럼들을 모두 삭제한다.
    # 분석에 필수적인 식별 정보(성별, 연령별, 시점)와 '일반가구원'만 남깁니다.
    essential_cols = ['성별', '연령별', '시점', '일반가구원']
    df = df[essential_cols].copy()

    # 데이터 타입 정제
    df['시점'] = pd.to_numeric(df['시점'], errors='coerce')
    if '일반가구원' in df.columns:
        df['일반가구원'] = pd.to_numeric(
            df['일반가구원'].astype(str).str.replace(',', ''),
            errors='coerce'
        )

    # 2015년 이후 데이터 필터링
    df = df[df['시점'] >= 2015].dropna(subset=['일반가구원'])

    return df


def print_gender_stats(df):
    '''남자 및 여자의 연도별 일반가구원 통계 출력'''
    print('### [2015년 이후 남자 및 여자의 연도별 일반가구원 통계] ###')
    mask = (df['연령별'].str.strip() == '합계') & (df['성별'].str.strip() != '계')
    pivot_gender = df[mask].pivot_table(
        index='시점',
        columns='성별',
        values='일반가구원',
        aggfunc='sum'
    )
    print(pivot_gender)
    print('\n')


def print_age_stats(df):
    '''연도별 연령별 일반가구원 데이터 통계 출력'''
    print('### [2015년 이후 연도별 연령별 일반가구원 통계] ###')
    # 요약 항목 제외 (합계 및 대분류 제외)
    exclude_list = ['합계', '15~64세', '65세이상']
    mask = (df['성별'].str.strip() == '계') & (~df['연령별'].str.strip().isin(exclude_list))
    pivot_age = df[mask].pivot_table(
        index='시점',
        columns='연령별',
        values='일반가구원',
        aggfunc='sum'
    )

    # 연령대 정렬 순서 정의
    age_order = [
        '15세미만', '15~19세', '20~24세', '25~29세', '30~34세', '35~39세',
        '40~44세', '45~49세', '50~54세', '55~59세', '60~64세', '65~69세',
        '70~74세', '75~79세', '80~84세', '85세이상'
    ]
    actual_cols = [age for age in age_order if age in pivot_age.columns]
    print(pivot_age[actual_cols])
    print('\n')


def draw_population_chart(df):
    '''성별 및 연령별 일반가구원 데이터 통계를 꺾은선 그래프로 표현'''
    set_matplotlib_korean_font()
    
    # 그래프 크기 및 스타일 설정
    plt.figure(figsize=(16, 10))
    
    # 시각적 가독성을 위해 주요 연령대 그룹만 선택하거나 선의 굵기를 조절함
    # 여기서는 모든 연령대를 그리되, 성별에 따라 선 스타일을 명확히 구분함
    exclude_list = ['합계', '15~64세', '65세이상']
    plot_df = df[(df['성별'].str.strip() != '계') & (~df['연령별'].str.strip().isin(exclude_list))]

    age_order = [
        '15세미만', '20~24세', '30~34세', '40~44세', 
        '50~54세', '60~64세', '70~74세', '85세이상'
    ]

    for age in age_order:
        for gender in ['남자', '여자']:
            subset = plot_df[
                (plot_df['연령별'].str.strip() == age) &
                (plot_df['성별'].str.strip() == gender)
            ]
            if not subset.empty:
                # 남자는 실선(-), 여자는 점선(--)으로 표현하여 가독성 증대
                line_style = '-' if gender == '남자' else '--'
                plt.plot(
                    subset['시점'],
                    subset['일반가구원'],
                    marker='o',
                    label=f'{gender}_{age}',
                    linestyle=line_style,
                    linewidth=2,
                    markersize=5
                )

    plt.title('2015-2024 성별 및 주요 연령별 일반가구원 변화 추이', fontsize=18, pad=20)
    plt.xlabel('연도', fontsize=12)
    plt.ylabel('일반가구원 수 (명)', fontsize=12)
    
    # 범례를 우측 외부로 빼서 그래프를 가리지 않게 함
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(df['시점'].unique()) # 연도가 정수로 깔끔하게 나오도록 설정
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    TARGET_FILE = 'kosis.csv'

    try:
        # 데이터 전처리
        population_data = load_and_preprocess_data(TARGET_FILE)

        # 1. 성별 연도별 통계 출력
        print_gender_stats(population_data)

        # 2. 연령별 연도별 통계 출력
        print_age_stats(population_data)

        # 3. 꺾은선 그래프 시각화
        draw_population_chart(population_data)

    except FileNotFoundError:
        print(f"오류: '{TARGET_FILE}' 파일을 찾을 수 없습니다.")
    except Exception as error:
        print(f'실행 중 오류 발생: {error}')
