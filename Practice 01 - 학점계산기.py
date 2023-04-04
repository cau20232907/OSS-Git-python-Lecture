gradeexch2 = {'A+': 4.5, 'A': 4.0, 'A0': 4.0, 'B+': 3.5, 'B': 3.0, 'B0': 3.0, 'C+': 2.5, 'C': 2.0, 'C0': 2.0,
              'D+': 1.5, 'D': 1.0, 'D0': 1.0, 'P': 'Pass', 'F': 0.0, 'FA': 0.0}
gradeexch3 = {'A+': 4.3, 'A': 4.0, 'A0': 4.0, 'A-': 3.7, 'B+': 3.4, 'B': 3.0, 'B0': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0,
              'C0': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D0': 1.0, 'D-': 0.7, 'P': 'Pass', 'F': 0.0, 'FA': 0.0}
gradeinfo = list()
gradegap = 0
work = 1
while True:
    print("작업을 선택하세요.")
    print("1. 입력")
    print("2. 출력")
    work = int(input())
    if work != 1 and work != 2:
        print("잘못된 입력입니다.")
        continue
    if work == 1:
        while gradegap != 2 and gradegap != 3:
            print("학점 계산 방식을 입력하세요.")
            print("A+가 4.5이고 A-가 없는 학점이면 2분할, A+가 4.3이고 A-가 존재하는 학점이면 3분할 학점입니다.")
            print("2분할 학점이면 2를, 3분할 학점이면 3을 입력해 주세요")
            gradegap = int(input())
            if gradegap == 2 or gradegap == 3:
                break
            print("잘못된 입력입니다")
        print("학점에 음수를 입력하면 프로그램이 종료됩니다.")
        while True:
            print("학점을 입력하세요:")
            period = int(input())
            if period < 0:
                break
            print("평점을 입력하세요:")
            grade = input()
            if grade not in gradeexch3 or (grade == 2 and grade not in gradeexch2):
                print("올바른 평점이 아닙니다. 다시 입력해 주세요.")
                continue
            gradeinfo.append([period, grade])
            print("입력되었습니다.")
    else:
        gradecal = [[0, 0.0, 0], [0, 0.0, 0]]
        if gradegap == 2:
            for i in gradeinfo:
                gradecal[0][0] += i[0]
                if i[1] != 'P':
                    gradecal[0][1] += i[0] * gradeexch2[i[1]]
                    if i[1] != 'F':
                        gradecal[1][0] += i[0]
                        gradecal[1][1] += i[0] * gradeexch2[i[1]]
                else:
                    gradecal[0][2] += i[0]
                    gradecal[1][0] += i[0]
                    gradecal[1][2] += i[0]
        else:
            for i in gradeinfo:
                gradecal[0][0] += i[0]
                if i[1] != 'P':
                    gradecal[0][1] += i[0] * gradeexch3[i[1]]
                    if i[1] != 'F':
                        gradecal[1][0] += i[0]
                        gradecal[1][1] += i[0] * gradeexch3[i[1]]
                else:
                    gradecal[0][2] += i[0]
                    gradecal[1][0] += i[0]
                    gradecal[1][2] += i[0]
        print()
        print("제출용 %d학점(GPA: %.2f)" % (gradecal[1][0], gradecal[1][1] / (gradecal[1][0] - gradecal[1][2])))
        print("열람용 %d학점(GPA: %.2f)" % (gradecal[0][0], gradecal[0][1] / (gradecal[0][0] - gradecal[0][2])))
        print("\n프로그램을 종료합니다.")
        break
