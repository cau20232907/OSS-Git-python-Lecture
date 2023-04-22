import random
def gradetype(): #학점 종류 확인 및 변환표 만들기
    #공통부분 미리 생성
    gradelist={'A': 4.0, 'A0': 4.0, 'B': 3.0, 'B0': 3.0,
               'C': 2.0, 'C0': 2.0, 'D': 1.0, 'D0': 1.0,
               'P': 'Pass', 'F': 0.0, 'FA': 0.0}
    print("학점 계산 방식을 입력하세요.")
    while True:
        print("A+가 4.5이고 A-가 없는 학점이면 2분할, A+가 4.3이고 A-가 존재하는 학점이면 3분할 학점입니다.")
        print("2분할 학점이면 2를, 3분할 학점이면 3을 입력해 주세요")
        match int(input()): #input 받아서 바로 match문 돌리기
            case 2:
                gradelist.update({'A+': 4.5, 'B+': 3.5,
                                  'C+': 2.5, 'D+': 1.5})
                return gradelist
            case 3:
                gradelist.update({'A+': 4.3, 'A-': 3.7, 'B+': 3.3,
                                  'B-': 2.7, 'C+': 2.3, 'C-': 1.7,
                                  'D+': 1.3, 'D-': 0.7})
                return gradelist
            case _:
                print("잘못된 입력입니다")
                print("학점 계산 방식을 다시 입력해 주세요")

def lectcodemaker(name, codeset): #과목코드생성기
    #중복 확인
    for num in codeset.keys():
        if codeset[num]==name:
            return num

    #무작위 생성
    code=random.randrange(1, 1000000)
    while code in codeset: #중복 방지
        code = random.randrange(1, 1000000)
    codeset[code]=name
    return code

def gradein(gradeinfo, gradelist, leccode=dict()): #input
    #leccode에 default값으로 dict() 넣은 것처럼 gradelist에도 gradetype() default값으로 넣으려 했는데 이러면 main보다 gradetype()가 먼저 실행되어서 포기했습니다.
    if len(gradelist) == 0:
        gradelist = gradetype()
    print(gradelist)
    print("학점에 음수를 입력하면 프로그램이 종료됩니다.")
    while True:
        code=input("과목명을 입력하세요: ")
        period = int(input("학점을 입력하세요: "))
        if period < 0:
            break
        grade = input("평점을 입력하세요: ")
        if grade not in gradelist:
            print("올바른 평점이 아닙니다. 다시 입력해 주세요.")
            continue
        code=lectcodemaker(code,leccode) # 프로그램 종료나 올바른 평점 미입력으로 학점이 저장이 되지 않았어도 과목코드가 생성되는 것을 막기 위해 코드 변환은 맨 마지막에
        gradeinfo.append((code, period, grade))
        print("입력되었습니다.")
    return gradelist

def checkbest(target, gradeinfo, gradeexch, retrycheck): #재수강한 과목의 경우 이 시도가 최선의 시도인지(이걸 평점에 더하면 되는지) 확인하는 함수
    # retrycheck 리스트는 static으로 선언해서 이 함수 안에서만 쓰는 게 좋았을 것 같은데 여기도 static이 있는지 모르겠네요...
    if target[0] in retrycheck: #이미 이전에 수강한 성적을 반영했다면 False 반환
        return False

    for i in gradeinfo:
        if gradeexch[target[2]]<gradeexch[i[2]]:
            return False
    retrycheck.add(target[0]) #성적 반영한 재수강 목록에 더함(재수강했는데 성적이 같은 경우 성적을 두 번 더하지 않기 위한 조치)
    return True

def gradeout(gradeinfo, gradeexch, leccode): #계산
    #예외처리
    if len(gradeexch) == 0: #학점 정보 없음
        print("학점 변환 정보가 없습니다.")
        return
    elif len(gradeinfo) == 0: #과목 없음
        print("입력된 과목 정보가 없습니다.")
        return
    codeset=list()
    for i in gradeinfo: # 튜플은 슬라이싱이 불가능해 슬라이싱한 리스트를 직접 만들기
        codeset.append(i[0])
    if set(codeset) != set(leccode.keys()): #과목코드 리스트 불일치(프로그램 잘못 만든 거 아니면 실행될 일은 없음, 프로그램시 실수 방지용)
        print("과목코드 생성 과정에서 문제가 발생하였습니다.")
        print(codeset)
        return

    #계산
    gradecal = [0, 0.0, 0, 0]
    retrycheck=set() #재수강으로 인해 같은 과목 코드가 여러 개 있는 경우 그 과목을 더했는지 확인하기 위한 배열
    #[전체학점, 변환점수합, 등급이 'P'인 과목 학점 합(평균계산시 제외하고 계산 필요), 등급이 'F'인 과목 학점 합(제출용 계산시 제외하고 계산 필요)]
    for i in gradeinfo:
        if codeset.count(i[0])>1: #재수강 확인
        #입력받을 때 재수강 시 재수강 전 성적과 후 성적을 리스트에 같이 보관하려다 보니 이 작업을 할 필요가 있음
            targets=list()
            for j in gradeinfo: #일단 과목코드 같은 과목 별도 리스트로 묶기
                if i[0]==j[0]:
                    targets.append(j)
            if checkbest(i, targets, gradeexch, retrycheck) == False:
                continue
        gradecal[0] += i[1]
        if i[2] == 'P':#Pass 과목은 변환점수 계산 불가로 별도로 카운트
            gradecal[2] += i[1]
        else:
            gradecal[1] += i[1] * gradeexch[i[2]]
            if i[2] == 'F': #등급이 'F'인 과목 별도로 카운트(제출용 학점 계산시 제외 필요)(등급이 'FA'인 경우 제출용에도 합산하므로 제외)
                gradecal[3] += i[1]
    print()
    print("제출용 %d학점" % (gradecal[0] - gradecal[3]), end='')
    #(제출용 학점)-(등급이 'P'인 학점)이 0학점이어서 0으로 나누게 되는 경우 방지를 위한 코드
    todiv=gradecal[0] - gradecal[2] - gradecal[3]
    if todiv!=0:
        print("(GPA: %.2f)" %(gradecal[1] / todiv))
    else:
        print() #(제출용 학점)-(등급이 'P'인 학점)이 0학점인 경우 단순 줄바꿈만 진행
    print("열람용 %d학점" %gradecal[0], end='')
    #위 제출용과 같음, 등급이 'P'인 학점만 존재하는 경우 0으로 나누기 오류를 막기 위한 조치
    todiv=gradecal[0] - gradecal[2]
    if todiv!=0:
        print("(GPA: %.2f)" %(gradecal[1] / todiv))
    else:
        print()

def gradeprint(gradeinfo, leccode): #output
    for i in gradeinfo:
        print('[%s]' %leccode[i[0]],'%d학점:' %i[1],i[2])


gradeinfo = list()
gradeexch=dict()
lecturecode=dict()
work = 1
while work:
    print(gradeinfo)
    print(gradeexch)
    print(lecturecode)
    print("작업을 선택하세요.")
    print("0. 프로그램 종료")
    print("1. 입력")
    print("2. 출력")
    print("3. 계산")
    work = int(input())
    match work:
        case 1:
            gradeexch=gradein(gradeinfo,gradelist=gradeexch, leccode=lecturecode)
            # gradeexch의 함수 내 변경사항이 main에 전달되지 않아(lecturecode는 정상적으로 전달됨) 임시조치로 gradeexch를 return값으로 받음
        case 2:
            gradeprint(gradeinfo, lecturecode)
        case 3:
            gradeout(gradeinfo,gradeexch,lecturecode)
        case 0:
            break
        case _:
            print("잘못된 입력입니다.")