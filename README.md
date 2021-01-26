# Boardgame Challenge
* 그냥 내가 혼자서 여러 종류의 보드게임들을 직접 구현해보는 챌린지
* 오목(렌주룰)을 시작으로 체스, 장기, 바둑, 고스톱, 모노폴리, 스플렌더 등등을 시간나는 대로 도전할 예정

## Renju
* 오목의 규칙 중 하나로, 흑에게만 33/44/장목의 금수 제한을 두는 규칙
* 금수를 구현하는데 애로사항이 있어서 
<a href="https://blog.naver.com/PostView.nhn?blogId=dnpc7848&logNo=221506783416&parentCategoryNo=&categoryNo=15&viewDate=&isShowPopularPosts=false&from=postView">여기</a>에 있는 코드를 참고함
* 좌클릭으로 착수, 우클릭으로 수를 무를 수 있음
* 게임이 종료되면 우클릭으로 게임을 재시작할 수 있음

- 흑의 금수 표시
<img src="https://user-images.githubusercontent.com/67459853/105721194-a5a11680-5f67-11eb-9d85-0b98ca36c87d.png">

- 게임 종료
<img src="https://user-images.githubusercontent.com/67459853/105721191-a46fe980-5f67-11eb-9fc1-f376b412d132.png">

## Chess
* 좌클릭으로 착수, 우클릭으로 수를 무를 수 있음
* 게임이 종료되면 우클릭으로 게임을 재시작할 수 있음
* 아직 무승부는 구현하지 않음(기물 부족 무승부, 3수 동형 무승부, 50수 무승부, 스테일메이트 등)

- 기물을 선택하면 행마가 가능한 칸을 표시함
<img src="https://user-images.githubusercontent.com/67459853/105721198-a6d24380-5f67-11eb-8388-66ec48613ace.png">

- 캐슬링
<img src="https://user-images.githubusercontent.com/67459853/105721807-4e4f7600-5f68-11eb-86ab-68901514195e.png">

- 앙파상
<img src="https://user-images.githubusercontent.com/67459853/105721210-a89c0700-5f67-11eb-9990-b98abe73200a.png">

- 프로모션
<img src="https://user-images.githubusercontent.com/67459853/105721207-a8037080-5f67-11eb-840f-1c7553219b42.png">

- 게임 종료
<img src="https://user-images.githubusercontent.com/67459853/105721214-a9349d80-5f67-11eb-8328-1937a476348b.png">
