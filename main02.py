import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def set_matplotlib_korean_font():
    font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
    try:
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
    except FileNotFoundError:
        plt.rc('font', family='NanumBarunGothic')
    plt.rc('axes', unicode_minus=False)


def load_and_preprocess_data(file_name):
    try:
        df = pd.read_csv(file_name, encoding='utf-8')
    except (UnicodeDecodeError, UnicodeError):
        df = pd.read_csv(file_name, encoding='cp949')

    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")
    
    # 일반가구원 제외 나머지 컬럼 삭제
    essential_cols = ['성별', '연령별', '시점', '일반가구원']
    df = df[essential_cols].copy()

    df['시점'] = pd.to_numeric(df['시점'], errors='coerce')
    if '일반가구원' in df.columns:
        df['일반가구원'] = pd.to_numeric(
            df['일반가구원'].astype(str).str.replace(',', ''),
            errors='coerce'
        )

    return df[df['시점'] >= 2015].dropna(subset=['일반가구원'])


def print_gender_stats(df):
    print('### [2015년 이후 남녀 연도별 일반가구원 통계] ###')
    mask = (df['연령별'].str.strip() == '합계') & (df['성별'].str.strip() != '계')
    print(df[mask].pivot_table(index='시점', columns='성별', 
                               values='일반가구원', aggfunc='sum'), '\n')


def print_age_stats(df):
    print('### [2015년 이후 연도별 연령별 일반가구원 통계] ###')
    exclude = ['합계', '15~64세', '65세이상']
    mask = (df['성별'].str.strip() == '계') & (~df['연령별'].str.strip().isin(exclude))
    pivot_age = df[mask].pivot_table(index='시점', columns='연령별', 
                                     values='일반가구원', aggfunc='sum')
    
    age_order = ['15세미만', '15~19세', '20~24세', '25~29세', '30~34세', '35~39세',
                 '40~44세', '45~49세', '50~54세', '55~59세', '60~64세', '65~69세',
                 '70~74세', '75~79세', '80~84세', '85세이상']
    actual_cols = [age for age in age_order if age in pivot_age.columns]
    print(pivot_age[actual_cols], '\n')


def draw_population_chart(df):
    set_matplotlib_korean_font()
    plt.figure(figsize=(16, 10))
    
    exclude = ['합계', '15~64세', '65세이상']
    plot_df = df[(df['성별'].str.strip() != '계') & (~df['연령별'].str.strip().isin(exclude))]
    
    # 주요 연령대 선정 (가독성 최적화)
    age_order = ['15세미만', '20~24세', '30~34세', '40~44세', 
                 '50~54세', '60~64세', '70~74세', '85세이상']

    for age in age_order:
        for gender in ['남자', '여자']:
            subset = plot_df[(plot_df['연령별'].str.strip() == age) & 
                             (plot_df['성별'].str.strip() == gender)]
            if not subset.empty:
                plt.plot(subset['시점'], subset['일반가구원'], marker='o', 
                         label=f'{gender}_{age}', linewidth=2,
                         linestyle='-' if gender == '남자' else '--')

    plt.title('2015-2024 성별/연령별 일반가구원 추이', fontsize=18, pad=20)
    plt.xlabel('연도', fontsize=12)
    plt.ylabel('일반가구원 수 (명)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(df['시점'].unique())
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    TARGET = 'kosis.csv'
    try:
        population_data = load_and_preprocess_data(TARGET)
        print_gender_stats(population_data)
        print_age_stats(population_data)
        draw_population_chart(population_data)
    except Exception as error:
        print(f'오류 발생: {error}')
