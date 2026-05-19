import cv2
import os
from datetime import datetime


class MediaController:
    # 클래스 이름은 CapWord 방식 사용
    
    def __init__(self):
        # 대입문 = 앞뒤 공백 사용 및 문자열은 ' ' 사용
        self.window_name = 'media_player'

    def process_image(self, image_path):
        # 함수 이름과 변수 이름은 snake_case 방식 사용
        img = cv2.imread(image_path)
        
        if img is not None:
            cv2.imshow(self.window_name, img)
            # 키 입력 대기 33ms 설정
            cv2.waitKey(33)
            # 사진이 출력되면 다시 창 닫기
            cv2.destroyAllWindows()
            print('이미지 출력을 완료하고 창을 닫았습니다.')
        else:
            print('이미지 파일을 열 수 없습니다.')

    def process_camera(self):
        # 카메라 출력을 실시간으로 받아보기
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print('카메라를 열 수 없습니다.')
            return

        # 출력 해상도 640 x 480 설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(self.window_name, frame)
            
            # 33ms 대기 및 ESC(아스키코드 27) 누를 시 종료
            key = cv2.waitKey(33)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_video(self, video_path):
        # 특정 동영상 파일 열어서 재생 및 단축키 제어
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print('동영상 파일을 열 수 없습니다.')
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)

        is_recording = False
        writer_mp4 = None
        writer_avi = None

        print('동영상을 재생합니다. 단축키를 사용할 수 있습니다.')

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print('영상 재생이 완료되었습니다.')
                break

            cv2.imshow(self.window_name, frame)

            # 녹화 중일 경우 프레임 저장
            if is_recording and writer_mp4 is not None and writer_avi is not None:
                writer_mp4.write(frame)
                writer_avi.write(frame)

            # 단축키 입력을 위한 33ms 대기
            key = cv2.waitKey(33)

            if key == 27:
                # ESC: 프로그램 종료
                print('프로그램을 종료합니다.')
                break
                
            elif key == 26:
                # Ctrl+Z: 화면을 이미지로 캡쳐 (아스키코드 26)
                now_str = datetime.now().strftime('%Y_%H-%M-%S')
                image_name = now_str + '_capture.jpg'
                cv2.imwrite(image_name, frame)
                print('이미지가 캡쳐되었습니다:', image_name)
                
            elif key == 24:
                # Ctrl+X: 동영상 녹화 시작 (아스키코드 24)
                if not is_recording:
                    now_str = datetime.now().strftime('%Y_%H-%M-%S')
                    
                    # 보너스 과제: 2가지 코덱(mp4v, XVID) 사용
                    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
                    video_name_mp4 = now_str + '_record.mp4'
                    writer_mp4 = cv2.VideoWriter(video_name_mp4, fourcc_mp4, fps, frame_size)

                    fourcc_avi = cv2.VideoWriter_fourcc(*'XVID')
                    video_name_avi = now_str + '_record.avi'
                    writer_avi = cv2.VideoWriter(video_name_avi, fourcc_avi, fps, frame_size)
                    
                    is_recording = True
                    print('녹화를 시작합니다.')
                    
            elif key == 3:
                # Ctrl+C: 녹화 중지 (아스키코드 3)
                if is_recording:
                    is_recording = False
                    writer_mp4.release()
                    writer_avi.release()
                    print('녹화를 중지하고 파일을 저장했습니다.')

        # 자원 해제
        cap.release()
        if writer_mp4 is not None:
            writer_mp4.release()
        if writer_avi is not None:
            writer_avi.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # 타겟 파일명 설정
    target_video = 'IMG_8511.MOV'
    target_image = 'sample.jpg'
    
    # 컨트롤러 인스턴스 생성
    controller = MediaController()

    # 1. 이미지 출력 테스트 (파일이 존재할 경우에만 실행하여 경고/에러 방지)
    if os.path.exists(target_image):
        controller.process_image(target_image)

    # 2. 동영상 재생 및 단축키 제어 (IMG_8511.MOV)
    if os.path.exists(target_video):
        controller.process_video(target_video)
    else:
        print('해당 경로에 지정한 동영상 파일이 없습니다.')

    # 3. 보너스 과제: 실시간 카메라 출력 (필요 시 주석 해제하여 사용)
    # controller.process_camera()
