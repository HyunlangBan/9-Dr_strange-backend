# introduction

* 영국 60년 정통 패션 브랜드 샌들, 슈즈, 부츠 등을 취급하는 세계적인 의류 기업 닥터마틴 클론 프로젝트
* 개발기간 : 2020.06.22 ~ 2020.07.03(약 2주)
* 개발인원 : 3 Front-end(강솔미, 전성현, 한수민), 3 Back-end(김동건, 반현랑, 정나온)
* [Front-end Github](https://github.com/wecode-bootcamp-korea/9-Dr_strange-frontend)
* [Back-end Github](https://github.com/wecode-bootcamp-korea/9-Dr_strange-backend)

# Demo
[![](https://images.velog.io/images/dgk089/post/a9f911a0-60f9-475b-9082-b44bb7712fa0/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7,%202020-07-04%2016-47-47.png)](https://youtu.be/x_OftNpGTy0)

# Model

![Model](https://images.velog.io/images/dgk089/post/5dbf5268-d445-4705-9e9c-27d3de238379/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7,%202020-07-04%2011-16-00.png)

# Technologies

* Python
* Django
* Beautifulsoup, Selenium
* Bcrypt
* JWT
* MySQL
* CORS headers
* Git, Github

# Features

* users
   - 유저정보저장
   - 회원가입 / 로그인
     - 회원가입시 유효성 검사
     - 회원가입시 패스워드 암호화
     - 로그인시 JWT Access 토큰 발행
   - 로그인 상태인지 확인하는 데코레이터 함수
   - 마이페이지
   
* product_app
   - 상품 리스트 구현
   - 상품 상세정보 구현
   - 상품 검색 구현
   - 상품 베스트셀러 구현
   
* cart_app
   - 장바구니 구현
      - 장바구니 추가 / 보기 / 삭제

# API Documentation

https://documenter.getpostman.com/view/9451840/T17FBoMA
