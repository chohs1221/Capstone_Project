# 2021 Capstone Project
### 접촉·비접촉 쇼핑카트 살균, 소독 및 케어 로봇
Team. SCCR   
<img src="/img4README/img_software.JPG" width="720px" height="540px"></img><br/>
## Contents
* [Introduction](https://github.com/chohs1221/Capstone_Project/#Introduction)
* [System Architecture](https://github.com/chohs1221/Capstone_Project/#System-Architecture)
* [Algorithm](https://github.com/chohs1221/Capstone_Project/#Algorithm)
* [Hardware](https://github.com/chohs1221/Capstone_Project/#Hardware)
* [Software](https://github.com/chohs1221/Capstone_Project/#Software)
  * [View Code](https://github.com/chohs1221/Capstone_Project/blob/master/run.py)
  * [Cart Handle Detection](https://github.com/chohs1221/Capstone_Project/#1-Cart-Handle-Detection)
  * [GUI](https://github.com/chohs1221/Capstone_Project/#2-GUI)
  * [Serial Port & Protocol](https://github.com/chohs1221/Capstone_Project/#3-Serial-Port-&-Protocol)
* [Experiment](https://github.com/chohs1221/Capstone_Project/#Experiment)
* [Conclusion](https://github.com/chohs1221/Capstone_Project/#Conclusion)
* [References](https://github.com/chohs1221/Capstone_Project/#References)


## Introduction   
<img src="/img4README/img_survey.jpg" width="920px" height="240px"></img><br/>
코로나 장기전으로 인해 마트 방문 시 대량구매를 하는 사람들이 증가하는 추세이다. 뿐만 아니라 집에서 밥을 해먹는 집콕족, 홈파티족들의 등장으로 인해 오히려 마트의 매출은 상승세를 보이고 있다. 기존에도 마트는 하루에도 수백 명에서 많게는 수천 명이 오고 가는 시설이었지만, 코로나의 지속으로 지금은 더욱 늘어나고 있다. 마트 이용객의 증가는 곧 쇼핑카트 사용자의 증가를 뜻한다. 많은 사람들이 접촉하는 쇼핑카트는 코로나 및 각종 질병에 더욱 취약하다.   
   
쇼핑카트는 소독을 제대로 하지 않는다면 쉽게 질병에 노출되기 싶다. 고객들 또한 쇼핑카트로 인해 다양한 불안감을 느끼고 있었다. 지역 카페 150명 회원을 대상으로 설문조사를 실시했을 때 실제로 많은 사람들이 쇼핑카트를 이용할 때 많은 불안감을 느끼고 있으며, 향균 필름이나 정기소독과 같은 마트의 노력에도 불안감이 해소되지 않는다고 대답하였다.   
   
따라서 현재의 간접적인 방역과 관리로는 고객들이 절대 안심할 수 없다는 것을 확인할 수 있었다. 실제로 현재 마트에서 진행하고 있는 소독들은 코로나 및 각종 질병을 예방하기에 부적합하다. 첫 번째로 다양한 마트들은 카트 손잡이에 향균 필름을 부착하고 있다. 그러나 바이러스를 살균할 수 있다던 향균 필름은 그 효과가 증명되지 않을뿐더러 낡고 헤지기 쉽다. 또한 언제 주기적으로 교체되는지 알 수 없으며 손잡이 외에 부분들은 전혀 고려가 되지 않았다. 두 번째, 방역으로는 일부 직원들이 카트를 정기 소독하고 있지만 그 많은 쇼핑카트를 일일이 소독하기란 어려우며 이용자들이 원할 때마다 소독을 할 수 없다는 점에서 적합하지 않다. 세 번째로 마트 입구에 소독제를 비치하여 고객들이 직접 소독하도록 방치한다. 그러나 카트를 직접 소독하지 않는 이용자들이 34.9% 정도로 꽤 많은 이용자들이 스스로 소독하지 않는 것을 알 수 있다. 이처럼 마트의 간접적이고 소홀한 소독 및 관리는 코로나가 종식된 후에도 고객들을 다양한 질병에 노출시킬 수 있다.   
   
따라서 쇼핑카트를 소독하기 위한 유사 제품들이 출시가 되었지만 각자의 단점으로 인해 상용화되고 있지 않다. 먼저 UV-C 자외선 램프가 장착되어 있는 카트 살균기의 경우 질병관리본부에서 권고하는 닦는 방식이 아니기 때문에 카트를 소독하는 적합한 방법이 아니며 유니레버의 위생손잡이는 손잡이만을 소독한다는 단점이 있다. 뿐만 아니라 다량의 카트를 소독할 수 없기 때문에 편의성을 고려하지 않았다. 또한 농협하나로마트에 카트 소독기를 설치한 적이 있었는데, 이는 설치비용이 2억 7천만원으로 상당히 비쌌으며 월 2회 소독으로 사용자들이 원할 때마다 소독할 수 없다는 단점이 있었다. 이 외에도 유사 특허로 쇼핑카트 핸들장치가 있는데 이 또한 손잡이만을 세척해주며 다양한 크기의 카트가 호환되지 않는다는 단점이 있었다. 이처럼 기존 마트의 소독방식과 유사 제품들의 카트 소독은 많은 한계가 있었다. 이에 우리는 롤러의 위치, 속도를 제어하고, 컴퓨터 비전을 사용함으로 위 단점들을 보완하여 쇼핑카트를 접촉 비접촉으로 소독시키는 로봇을 제안한다.   

## System Architecture   
<img src="/img4README/img_system.jpg" width="720px" height="480px"></img><br/>
MCU는 Cortex-M4로 사용하였다. 카메라로 카트 손잡이의 크기와 기울기를 opencv를 이용해 파악했고, 그 데이터는 miniPC와 MCU간의 SERIAL 통신으로 주고 받았다. 그 값을 토대로 사이드 롤러와 상단 롤러의 속도, 위치를 결정했다. 모터와 모터 드라이버는 IG-32PGM제품과 누리로봇사의 DCMD-50-P를 사용하였다. 전류 제어를 하는데 필요한 전류 센서는 Allegro사의 ACS723 모듈 제품을 사용하였다. 릴레이 스위치로 12V DC팬모터와 220V AC 블로워(헤어드라이기)를 작동시켰고 MOSFET 모듈을 사용하여 펌프 모터와 LED, 후방 사이드 롤러와 브러쉬 롤러의 PWM을 부여하였다. 노즐부에는 퓨어워터텍사의 M-160부스터 펌프모터를 사용하여 분사노즐로 일정량의 세척액을 카트에 분사했다. limited switch 2개를 상단롤러 작업범위의 양끝단에 위치시켰다. 이 스위치들은 상단롤러가 작업범위를 넘어가는 것을 방지하기 위한 안전장치의 역할을 함과 동시에 상단 switch는 상단롤러의 init 값을 결정하는 데에도 사용되었다. 가변저항은 4개를 사용해 각각의 스프링경첩이 눌리는 여부를 판단할 수 있도록 하였고, 이것을 이용해 system의 전체 흐름을 구성했다. Psd 거리센서 2개로 카트의 진입 높이를 파악하여 상단롤러가 알맞게 움직일 수 있도록 하였다. Psd, 가변저항, 전류센서 등 모두 Lowpass filt1er와 moving average filter를 적용해 noise값을 최소화 하였다. 그리고 사용자의 편의를 위해 UI를 제작하고 이를 Touch Screen에서 동작될 수 있도록 하였다.

## Algorithm   
<img src="/img4README/img_argorithm2.jpg" width="720px" height="360px"></img><br/>
<img src="/img4README/img_argorithm.jpg" width="720px" height="480px"></img><br/>
이 로봇의 개별소독 모드(Mode0)의 알고리즘이다.   
개별소독 모드는 마트 이용객이 직접 카트를 넣어서 사용하는 모드이고 다량소독 모드(Mode1)는 여려 개의 카트를 한 번에 소독하는 모드로 직원이 주로 사용할 수 있도록 하였고, 수동 조작이기 때문에 따로 순서가 없다. Mode0에서는 Automatic System이기 때문에 알고리즘을 구성하였다. 먼저 준비상태에 있는 로봇에 카트를 넣게 되면 앞 가변저항 2개의 센서 값 변화로 진행 사항을 알 수 있는데, 하나의 값만 변하면 더 밀어달라는 신호를 보내주고 두 센서 값이 모두 변해야 손잡이를 놓아달라는 신호를 보내준다. 그리고 손잡이르 놓음과 동시에 카메라로 카트 손잡이의 사이즈와 기울기를 확인한다. 카트의 사이즈에 맞게 상단롤러의 위치를 먼저 맞추고 나서 기울기 값으로 앞 사이드 롤러 속도를 부여한다. 동시에 블로워, 팬 모터, LED, 브러쉬 롤러 등 전체 System이 가동된다. 진행이 되면서 브러쉬 롤러에 장착된 Psd 센서에 값이 들어오면 상단 롤러가 위로 올라가도록 하여 카트의 경사진 면을 브러쉬 롤러가 카트에 닿지 않고 닦을 수 있도록 한다. 그 후 앞 사이드 롤러에서 벗어나 뒤 사이드 롤러에만 잡히게 되면 몇 초의 딜레이 후에 브러쉬 롤러의 회전 방향을 역으로 주어 손잡이의 세척을 더 깔끔히 할 수 있도록 하였다. 그 후 뒤 사이드롤러로 배출이 되면 뒤 가변저항 값도 변하면서 System이 처음 init 값으로 초기화가 된다. init일 때의 로봇은 앞 사이드 롤러, 뒤 사이드 롤러, 블로워, 팬 모터, LED, 브러쉬 롤러 등 전체 System이 꺼지고 상단 롤러만 위로 올라가게 작동한다. 상단 롤러가 limited switch를 누르도록 하여 눌리면 처음 위치로 갈 수 있도록 하였다. 이 모든 진행 사항에서의 sensor 값은 miniPC로 전달되어 LCD에서 UI로 알려주고 음성 스피커로 한 번 더 알려준다.

## Hardware   
<img src="/img4README/img_hardware1.JPG" width="480px" height="360px"></img><br/>
<img src="/img4README/img_hardware2.JPG" width="480px" height="360px"></img><br/>
하드웨어는 3D 모델링 툴인 Inventor 프로그램을 사용하여 설계했다. 알루미늄 프로파일로 골조를 제작하였고 알루미늄 상판 위에 아크릴로 케이싱한 디자인이 우측 그림이다. 방수를 고려하여 내부에도 아크릴을 씌웠고, 각각의 모터에도 3D프린팅으로 케이스를 씌웠다.   
카트를 밀어주는 4개의 사이드 롤러와 카트를 닦아주는 브러쉬 롤러 그리고 브러쉬 롤러의 높이 위치를 결정해주는 상단 롤러로 구성돼 있다.

## Software   
### 1. Cart Handle Detection   
<img src="/img4README/img_carthandle1.jpg" width="480px" height="320px"></img><br/>
<img src="/img4README/img_carthandle2.jpg" width="480px" height="120px"></img><br/>
Usb_Cam을 통해 카트의 손잡이를 인식한다. 인식한 손잡이의 윤곽선을 검출해 카트 손잡이의 길이와 기울기 값을 계산한다. 인식한 길이에 맞게 로봇의 상단 롤러가 내려오게 되고 이에 여러 크기의 카트에 적용할 수 있도록 한다. 또한 손잡이의 좌표 값을 계산해서 얻은 기울기로 robot 제어기에 feedback 역할을 하여 입구 쪽 롤러의 속도를 실시간으로 바꿔줘 카트의 기울어짐을 잡아준다.   

### 2. GUI   
<img src="/img4README/img_gui1.jpg" width="420px" height="240px"></img><br/>
<img src="/img4README/img_gui2.jpg" width="420px" height="240px"></img><br/>
PyQt를 이용하여 UI를 Design 했다. Design은 사용자의 편의성에 가장 중점을 두었고 이를 Touch Screen에서 동작될 수 있도록 하였다. 이 때 Button과 로고는 직접 제작하였다. 사용자는 UI를 이용할 수 있고 그 초기 화면은 위와 같다. 초기 화면에는 크게 시작 Button, 설정 Button, 정지 Button이 있고 로봇의 작동이 완료될 때마다 count를 하여 소독된 카트의 수를 알려주는 일일 누적과 주간 누적이 있다. 또한 수위감지센서를 통해 세척액의 잔량이 얼마인지 알 수 있도록 세척액의 수위를 한 눈에 알아볼 수 있도록 하였다.   
<img src="/img4README/img_gui3.JPG" width="600px" height="720px"></img><br/>
시작 Button을 누르면 총 8가지 Screen과 동시에 음성으로 사용 안내를 받을 수 있다. 알고리즘을 따라 Screen도 바뀌며 음성으로 안내를 해준다.   
<img src="/img4README/img_gui4.jpg" width="420px" height="240px"></img><br/>
설정 Button을 누르면 세척액의 수압 세기와 분사 mode를 선택할 수 있다, 분사 mode에서 닦기 전용은 다량의 카트를 소독할 때 사용하는 것으로, 상단 롤러만 작동하여 Brush로 카트의 상단을 닦아주는 것이다. 또한, 상단 롤러의 위치도 조절할 수 있으며 사용자의 안전을 위해 긴급 정지 Button을 넣어주었다. 정지를 누르면 시스템이 멈추고 다시 시작하기 전까지 작동하지 않는다. 또한 화살표 버튼을 클릭하여 수동으로 상단 롤러의 위치를 조정할 수 있다.   

### 3. Serial Port & Protocol   
mini PC(Jetson nano)와 MCU간의 통신은 uart 시리얼 통신을 이용했다. 시리얼 통신 특성상 통신 프로토콜을 따로 설정해두지 않으면 값이 밀리는 현상이 일어나기 때문에 start bit와 checksum bit를 확인하는 등의 규격을 맞춰 노이즈가 생기더라도 지장이 없도록 하였다.

## Experiment   
향균 필름을 통해 디바이스가 얼마나 카트를 잘 닦아줄 수 있는지 확인하였다. 먼저 향균 필름을 카트 손잡이에 바르고 UV 램프로 비추면 [표 3]과 같이 닦인 부분이 확인된다. 이것을 이미지 처리를 이용하여 닦인 부분과 그렇지 않은 부분을 비교하여 구분한 뒤 차이를 극대화 하여 이진화를 하고 픽셀 값으로 계산해서 최종적으로 몇 97% 이상으로 닦인 것을 확인할 수 있었다.

## Conclusion   
접촉·비접촉 쇼핑카트 살균, 소독 및 케어 로봇을 개발하면서 기존에 있었던 디바이스의 한계를 넘는 새로운 방식의 소독 시스템을 구현할 수 있었다. 질병관리본부에서 권고하는 접촉 방식을 이용하여 많은 카트를 닦을 수 있는 방법을 고안하다가 세차장 방식에서 아이디어를 떠올렸고, 사람과 밀접하게 사용하는 디바이스이기 때문에 다양한 상황과 한계까지 고려하여 디바이스를 개발하였다. 그 과정에서 많은 것을 배울 수 있었다. 현재는 카트만을 소독하고 있지만 조금 더 수정한다면 바구니, 공항카트 등에까지 적용시킬 수 있을 것으로 기대한다. 상단 롤러와 사이드 롤러를 제어할 때 다양한 크기의 카트가 호환이 가능하도록 하였고 잘 닦아줄 수 있도록 고려하였다.   
이 디바이스는 다양한 사람들이 사용하기 때문에 초기에 카트를 넣는 기울기가 모두 다를 것으로 예상했다. 따라서 사이드 롤러를 각각 제어하여 카트의 기울기를 잡아주었고 여러 실험 끝에 카트를 일직선으로 배출할 수 있었다. 상단 롤러 또한 PSD센서에 카트의 높이가 잘 잡히지 않아 상단 롤러가 잘 상승하지 않거나 부드럽게 움직이지 않는 등의 오류가 있었지만 여러 시행착오 끝에 위치제어를 할 수 있었다. 각각의 roller를 제어한 후 알고리즘에 맞춰 디바이스가 작동할 수 있도록 했다.   
특히 사람과 밀접하게 사용된다는 것을 관건으로 두어 사용자들의 안전이나 편리성을 중심으로 두었다. 단순히 비상정지 Switch만을 장착한 것이 아니라 User Interface에도 긴급 정지 Button을 넣어 이중으로 안전장치를 설치하였다. 더 나아가 사람이 특정 범위 내에 인식이 되면 일시 정지하는 등의 안전장치를 추가로 고려한다면 충분히 많은 사람들이 안심하게 사용할 수 있는 디바이스가 될 것이다. 또한 실제 사용성을 고려해 사용자가 초기에 로봇을 작동시킬 때 전원 연결 후 아이콘 클릭 하나로 전체 프로세스가 실행되도록 하였다.

## References   
[1] Dong-Hee Paek, Yeong-Dae Kim, Whang Cho, “The Current-Position Cascade PID Control of Delta-type Parallel Robot”, p.278-279, Apr. 30. 2020   
[2] 김정석, 배수민, 최수정, 오창석, “쇼핑 카트 핸들 세척 장치”, Mar. 28. 2014
