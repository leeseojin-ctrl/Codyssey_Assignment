import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.img = cv2.imread(self.file_path)
        if self.img is None:
            raise ValueError('이미지를 찾을 수 없습니다.')

    def _show_images(self, title, images_dict, cmap=None):
        '''시각화를 위한 내부 헬퍼 함수'''
        num_images = len(images_dict)
        fig, axes = plt.subplots(1, num_images, figsize=(5 * num_images, 5))
        fig.suptitle(title, fontsize=16)

        if num_images == 1:
            axes = [axes]

        for ax, (name, img_data) in zip(axes, images_dict.items()):
            ax.set_title(name)
            if len(img_data.shape) == 3:
                # BGR을 RGB로 변환하여 출력
                ax.imshow(cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB))
            else:
                ax.imshow(img_data, cmap=cmap if cmap else 'gray')
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()

    def task_1_transform(self):
        '''1. 이미지 반전·회전 기초 (보너스 포함)'''
        img_original = self.img.copy()
        
        # 반전 및 회전
        img_flip_ud = cv2.flip(img_original, 0)
        img_flip_lr = cv2.flip(img_original, 1)
        img_rot_90 = cv2.rotate(img_original, cv2.ROTATE_90_CLOCKWISE)
        img_rot_180 = cv2.rotate(img_original, cv2.ROTATE_180)
        
        # 보너스: 업샘플링 (2배)
        img_upsampled = cv2.resize(img_original, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

        self._show_images('Task 1: Rotate & Flip', {
            'Original': img_original,
            'Up-Down Flip': img_flip_ud,
            'Left-Right Flip': img_flip_lr,
            'Rotate 90': img_rot_90,
            'Rotate 180': img_rot_180
        })
        print(f'보너스 과제 (업샘플링 사이즈): {img_upsampled.shape}')

    def task_2_resize_crop(self):
        '''2. 이미지 리사이즈·스케일링·크롭 (보너스 포함)'''
        img_original = self.img.copy()
        
        # 사이즈 변환
        img_640 = cv2.resize(img_original, (640, 480))
        img_1024 = cv2.resize(img_original, (1024, 768))
        
        # 비율 변환
        img_ratio = cv2.resize(img_original, None, fx=0.3, fy=0.7)
        
        # 특정 부분 크롭 (깊은 복사)
        crop_img = img_original[50:200, 50:200].copy()

        # 보너스: 여러 사람 개별 크롭 (임의의 바운딩 박스 가정)
        person_1 = img_original[10:100, 10:100].copy()
        person_2 = img_original[100:200, 100:200].copy()

        self._show_images('Task 2: Resize & Crop', {
            '640x480': img_640,
            'Ratio (fx=0.3, fy=0.7)': img_ratio,
            'Cropped Area': crop_img,
            'Bonus: Person 1': person_1,
            'Bonus: Person 2': person_2
        })

    def task_3_color_invert(self):
        '''3. 색상 변환과 역상 처리 (보너스 포함)'''
        img_original = self.img.copy()
        
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        img_inverse = cv2.bitwise_not(img_original)

        self._show_images('Task 3: Color & Invert', {
            'Original': img_original,
            'Gray': img_gray,
            'Inverse': img_inverse
        })

        # 보너스: 히스토그램 출력
        hist_original = cv2.calcHist([img_original], [0], None, [256], [0, 256])
        hist_inverse = cv2.calcHist([img_inverse], [0], None, [256], [0, 256])
        
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.plot(hist_original, color='blue')
        plt.title('Original Histogram (Blue Channel)')
        plt.subplot(1, 2, 2)
        plt.plot(hist_inverse, color='red')
        plt.title('Inverse Histogram (Blue Channel)')
        plt.show()

    def task_4_filters(self):
        '''4. 이미지 이진화·에지 검출·블러링 (보너스 포함)'''
        img_original = self.img.copy()
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        
        # 이진화
        _, img_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        
        # 에지 검출
        img_sobel = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
        img_sobel = cv2.convertScaleAbs(img_sobel)
        img_laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
        img_laplacian = cv2.convertScaleAbs(img_laplacian)
        img_canny = cv2.Canny(img_gray, 100, 200)
        
        # 흐림 효과 (전체)
        img_blur = cv2.GaussianBlur(img_original, (15, 15), 0)
        
        # 보너스: 특정 부분만 흐림 효과 (ROI Blurring)
        img_roi_blur = img_original.copy()
        roi = img_roi_blur[50:200, 50:200]
        img_roi_blur[50:200, 50:200] = cv2.GaussianBlur(roi, (25, 25), 0)

        self._show_images('Task 4: Binary & Edges', {
            'Binary': img_binary,
            'Sobel': img_sobel,
            'Laplacian': img_laplacian,
            'Canny': img_canny
        })
        self._show_images('Task 4: Blurring', {
            'Full Blur': img_blur,
            'ROI Blur (Bonus)': img_roi_blur
        })

    def task_5_hsv_split(self):
        '''5. 이미지 HSV 변환·H/S/V 채널 출력 (보너스 포함)'''
        img_original = self.img.copy()
        
        # HSV 변환 및 분리
        img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(img_hsv)
        
        self._show_images('Task 5: HSV Channels', {
            'H Channel': h,
            'S Channel': s,
            'V Channel': v
        })

        # 보너스: BGR 채널 분리 기법과 비교
        b, g, r = cv2.split(img_original)
        self._show_images('Task 5 Bonus: BGR Channels', {
            'B Channel': b,
            'G Channel': g,
            'R Channel': r
        })

    def task_6_object_labeling(self):
        '''6. 객체 표시와 라벨링 (사각형·텍스트·연결선) (보너스 포함)'''
        img_original = self.img.copy()
        
        # 텍스트와 사각형 위치 설정
        rect_start = (50, 50)
        rect_end = (150, 150)
        text_pos = (200, 30)
        
        # 1. 빨간색 사각형 표시
        cv2.rectangle(img_original, rect_start, rect_end, (0, 0, 255), 2)
        
        # 2. 텍스트 작성
        cv2.putText(img_original, 'Object 1', text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # 3. 텍스트와 사각형을 잇는 빨간색 연결선
        line_start = (150, 100)
        line_end = (200, 25)
        cv2.line(img_original, line_start, line_end, (0, 0, 255), 2)

        # 보너스: 다른 형태의 도형 그리기 (삼각형, 원형)
        # 원형 표시
        cv2.circle(img_original, (250, 100), 40, (0, 255, 0), 2)
        cv2.putText(img_original, 'Circle Obj', (230, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 삼각형 표시
        triangle_pts = np.array([[350, 150], [400, 50], [450, 150]], np.int32)
        triangle_pts = triangle_pts.reshape((-1, 1, 2))
        cv2.polylines(img_original, [triangle_pts], True, (255, 0, 0), 2)
        cv2.putText(img_original, 'Triangle Obj', (360, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        self._show_images('Task 6: Object Labeling & Bonus Shapes', {
            'Labeled Objects': img_original
        })


def main():
    # 사용자가 지정한 파일 이름
    file_name = '공원.jpg'
    
    try:
        # ImageProcessor 클래스 초기화
        processor = ImageProcessor(file_name)
    except ValueError:
        print('에러: 이미지를 찾을 수 없습니다.')
        print('코랩 좌측 탭의 폴더 아이콘을 눌러 \'공원.jpg\' 파일을 업로드한 후 다시 실행해 주세요.')
        return
    
    print('--- 1. 이미지 반전·회전 기초 ---')
    processor.task_1_transform()
    
    print('--- 2. 이미지 리사이즈·스케일링·크롭 ---')
    processor.task_2_resize_crop()
    
    print('--- 3. 색상 변환과 역상 처리 ---')
    processor.task_3_color_invert()
    
    print('--- 4. 이미지 이진화·에지 검출·블러링 ---')
    processor.task_4_filters()
    
    print('--- 5. 이미지 HSV 변환·H/S/V 채널 출력 ---')
    processor.task_5_hsv_split()
    
    print('--- 6. 객체 표시와 라벨링 ---')
    processor.task_6_object_labeling()

if __name__ == '__main__':
    main()
