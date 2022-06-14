# 피부 트러블 디텍션

---
## 📋 Introduction
- 아트랩 기업 연계 프로젝트로, 주어진 데이터를 활용해 피부 내 트러블을 탐지하는 모델을 설계합니다.
- Streamlit을 이용해 피부 내 트러블을 찾아주는 서비스를 제공합니다.
<br>

---
## 📑 Dataset
- 데이터는 피부 부위별 사진과 세 개의 피부 트러블 타입으로 라벨링으로 구성 돼 있습니다.


### 전처리
**Copy & Paste**
- annotation이 존재하지 않는 이미지에 대해 전처리를 진행했습니다.
- 다른 사람의 trouble patch를 Copy & Paste 하여 새로운 trouble 이미지를 만들었습니다.
    - flip, rotate, resize augmentation을 patch에 적용
    
![image](src\copypaste.png)

<br>

---
## 📝 평가 Metric
### mAP 50
- 피부 트러블 개수를 적절히 표현해주는 mAP50으로 기준 평가 지표를 설정하였습니다.
### F1 Score
- 피부 트러블을 잘 예측하는 **Precision**과 실제 트러블을 잘 재현한 **Recall**을 모두 고려한 **F1 Score**을 사용해 최종 모델 평가를 진행합니다.
<br>

---
## 🧪 Experiments
### Model
- 학습 시간과 모델의 성능을 종합적으로 판단 해 **TOOD ResNext**를 최종 모델로 선정하였습니다.

|  | mAP50 | mean F1 | Anchor|  Training Time | 
| :---: | :---: | :---: | :---: | :---: |
| TOOD ResNext | 0.493 | 0.4562 | Free | 12h |
| ATSS Swin-L Dyhead | 0.468 | 0.4608 | Base | 15h |
| CenterNet++ | 0.425 | 0.4144 | Free |  38h | 
<br>

### Copy & Paste Dataset
- annotation 없는 이미지에 Copy & Paste하여 이미지 추가 확보한 다음 성능 비교를 진행했습니다.

|  | mAP50 | mean F1 Score |
| --- | --- | --- |
| Copy & Paste 전 | 0.446 | 0.4674 |
| Copy & Paste 후 | 0.480 | 0.4859 |
<br>

### Remove background
- 피부 외 배경요소를 지우면 학습이 더 잘되지 않을까 하는 가설로 학습을 진행했습니다

|  | mAP50 | mean F1 Score |
| --- | --- | --- |
| Remove bg 전 | 0.446 | 0.4674 |
| Remove bg 후 | 0.450 | 0.4679 |
<br>

### Training by part
- 피부 부위별로 학습을 따로 진행해 전체 부위를 학습한 모델과 비교 분석하였습니다.

|  | train by part(mAP) | train by all(mAP) | train by part(F1) | train by all(F1) |
| --- | --- | --- | --- | --- |
| part 0 | 0.462 | 0.475 | 0.4781 | 0.4812 |
| part 1 | 0.402 | 0.409 | 0.4239 | 0.4222 |
| part 2 | 0.384 | 0.380 | 0.3950 | 0.3993 |
| part 3 | 0.410 | 0.427 | 0.4321 | 0.4421 |
| part 4 | 0.423 | 0.416 | 0.4484 | 0.4218 |
<br>

### Loss

**BBox Loss**
- 모델을 TOOD ResNext로 고정 후 BBox loss 실험을 진행했습니다.

|  | mAP50 | mean F1 Score|
| :---: | :---: | :---: |
| GIoU | 0.493 | 0.4841 |
| DIoU | 0.491 | 0.4719 |
| CIoU | 0.488 | 0.4631 |

<br>    

**Classification Loss**
- 모델을 TOOD ResNext로 고정 후 PAFPN으로 Neck을 바꾸고 classification loss 실험을 진행했습니다.

|  | mAP50 | mean F1 Score|
| :---: | :---: | :---: |
| Focal | 0.485 | 0.4880 |
| GHMC | 0.485 | 0.4841 |

<br>

### Inference 결과
- 좌측은 mmdetection으로, 우측은 SAHI를 적용하여 inference한 결과입니다.
<br>

![image](src\inference_img.png)


---
## 🎯 Result
- 우리의 최종 모델은 **mAP50 0.521**, **Mean F1 score 0.4965**의 성능을 보입니다.

|  | mAP50 | mean F1 | type1 F1 | type2 F1 | type3 F1 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| TOOD ResNext | 0.521 | 0.4965 | 0.6189 | 0.4829 | 0.3877 |


---
## Demo
- 
