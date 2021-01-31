"""
제작: CuriHuS
https://curihus.tistory.com
본 코드는 2020년 1학기 웹/파이썬 프로그래밍 이성원 교수님 수업에서
기말고사 시험의 예시 답안입니다.
100% 정답은 아니며 오류가 발견되거나 관련 질문은 블로그 댓글로 남겨주시면
수정 작업 및 답변을 드리겠습니다.

"""

import csv
import copy
class RemoteControl():
    def __init__(self):
        self.nowChannel_index = 0
        self.__enabledChannelList = [] #문제에서 요구한 private 데이터
        self.enabledNumberList= []
        self.nowChannel = []
        self.blockChannelList = []
        self.favorlist = {}
        
    def powerOnRemoteControl(self, channel_list):
        self.__enabledChannelList = channel_list
        self.nowChannel = channel_list[0]
        for i in range(len(channel_list)):
            self.enabledNumberList.append(channel_list[i][0])
        return len(channel_list)

    def gotoChannel(self, asked_number):
        if asked_number in self.enabledNumberList:
            self.nowChannel_index = self.enabledNumberList.index(asked_number)
            self.nowChannel = self.__enabledChannelList[self.nowChannel_index]
            return self.nowChannel[1]
        else:
            return self.nowChannel[1]

    def nextChannel(self):
        self.nowChannel_index += 1
        if len(self.__enabledChannelList) == self.nowChannel_index: #현재 채널 index가 마지막이면 0번째 index로 이동하기 위한 if문
            self.nowChannel_index = 0
            self.nowChannel = self.__enabledChannelList[0]
        else:
            self.nowChannel = self.__enabledChannelList[self.nowChannel_index]
        
        return self.nowChannel[1]

    def previousChannel(self):
        self.nowChannel_index -= 1
        if self.nowChannel_index == -1: # 현재 채널 index가 처음이라면 가장 뒤 index로 이동하기 위한 if문
            self.nowChannel_index = (len(self.__enabledChannelList)-1)
            self.nowChannel = self.__enabledChannelList[self.nowChannel_index]
        else: # 평범한 상황
            self.nowChannel = self.__enabledChannelList[self.nowChannel_index]

        return self.nowChannel[1]

    def blockChannel(self):
        self.blockChannelList.append(self.nowChannel)
        self.__enabledChannelList.remove(self.nowChannel)
        self.enabledNumberList.remove(self.nowChannel[0])
        if self.nowChannel_index == len(self.__enabledChannelList): #index 마지막
            self.nowChannel_index = 0
            self.nowChannel = self.__enabledChannelList[0]

        else: # index 마지막 아닌 경우 큰 변화 없음.
            self.nowChannel = self.__enabledChannelList[self.nowChannel_index]

        return self.nowChannel[1]


    def unblockChannel(self, unblock_number):
        for i in range(len(self.blockChannelList)):
            if unblock_number == self.blockChannelList[i][0]: # 찾았다
                self.unblock = self.blockChannelList[i]
                self.blockChannelList.remove(self.unblock)
                self.__enabledChannelList.append(self.unblock)
                self.__enabledChannelList.sort()
                self.enabledNumberList.append(self.unblock[0])
                self.enabledNumberList.sort()
                self.nowChannel_index = self.__enabledChannelList.index(self.nowChannel)
                return 1
            else:
                continue
        return -1

    def powerOffRemoteControl(self):
        with open('output.csv', 'w', newline='') as fileWrite: #Windows에서는 newline 구문이 없으면 두 줄씩 띄워짐
            myWriter = csv.writer(fileWrite)
            for i in range(len(self.__enabledChannelList)):
                myWriter.writerow(self.__enabledChannelList[i])

    def favorChannel(self):
        if self.nowChannel[0] not in self.favorlist: # favorlist에 채널이 없는 경우
            self.favor = 1
            self.favorlist.update({self.nowChannel[0]:self.favor})
            return 1
        else:
            self.favor = self.favorlist[self.nowChannel[0]]+1
            self.favorlist.update({self.nowChannel[0]:self.favor})
            return 1
        return -1

    def aiNextChannel(self):
        self.favor_noblock = copy.deepcopy(self.favorlist)
        for i in range(len(self.blockChannelList)):
            self.favor_noblock.__delitem__(self.blockChannelList[i][0])
        # noblock= dict / block된 채널을 거른 dict
        # favorlist는 block+unblock 채널이 모두 있어서 추가적인 dict 필요
        # dict의 경우 copy 모듈의 deepcopy를 활용해야 복사가 가능함(list의 경우 .copy()로 가능)

        self.favor = self.favor_noblock[self.nowChannel[0]] # 선호도(value)
        self.favor_list = list(self.favor_noblock.values()) #favorlist = dict 타입, favor_list: list타입(선호도 순위를 알기 위한 list)
        self.favor_list_sort = sorted(self.favor_list).copy() # favor_list_sort : 선호도를 오름차순으로 정렬
        self.favor_list_reverse = sorted(self.favor_list, reverse=True).copy() #favor_list_reverse : 선호도를 내림차순으로 정렬
        self.favor_list_name = self.favor_noblock.keys() #채널 번호 목록(noblock 기준)
        self.favor_noblock_list = list(self.favor_noblock) # noblock상태인 채널번호 리스트

        # aiNextChannel 메소드는 선호도가 한 단계 낮은 채널로 이동.
        
        if self.favor == self.favor_list_sort[0]: #현재 채널 선호도가 제일 작은 값이라면 선호도가 제일 큰 채널로.
            for i in range(len(self.__enabledChannelList)):
                if self.__enabledChannelList[i][0] == self.favor_noblock_list[self.favor_list.index(self.favor_list_reverse[0])]: # 채널번호.
                    self.nowChannel_index = i
                    self.nowChannel = self.__enabledChannelList[i]
                    return self.nowChannel[0]
                else:
                    continue
        else: #현재 채널 선호도보다 작은 채널이 최소 1개는 존재.
            for i in range(self.favor_list_reverse.index(self.favor)+1, len(self.favor_list_reverse)):
                if self.favor_list_reverse[i] == self.favor: #선호도 등급이 같은 경우
                    continue
                else: #선호도 등급이 한단계 낮은 채널 찾았다.
                    self.favor = self.favor_list_reverse[i]
                    self.number = self.favor_noblock_list[self.favor_list.index(self.favor)] #바꿀 채널 번호
                    
                    for j in range(len(self.__enabledChannelList)):
                        if self.number == self.__enabledChannelList[j][0]: #이제 현재 활성화된 채널의 바꿀 채널 번호 index를 찾음
                            self.nowChannel_index = j
                            self.nowChannel = self.__enabledChannelList[j]
                            return self.nowChannel[0]
                        else:
                            continue

    def aiPreviousChannel(self):
        self.favor_noblock = copy.deepcopy(self.favorlist)
        for i in range(len(self.blockChannelList)):
            self.favor_noblock.__delitem__(self.blockChannelList[i][0])
        # noblock= dict / block된 채널 거름.

        self.favor = self.favor_noblock[self.nowChannel[0]] # 선호도(value)
        self.favor_list = list(self.favor_noblock.values()) #favorlist = dict 타입, favor_list: list타입
        self.favor_list_sort = sorted(self.favor_list).copy()
        self.favor_list_reverse = sorted(self.favor_list, reverse=True).copy()
        self.favor_list_items = self.favor_noblock.items()
        self.favor_noblock_list = list(self.favor_noblock) # noblock상태인 채널번호 리스트
        


        if self.favor == self.favor_list_reverse[0]: #현재 채널 선호도가 제일 큰 값이라면
            for i in range(len(self.__enabledChannelList)):
                if self.__enabledChannelList[i][0] == self.favor_noblock_list[self.favor_list.index(self.favor_list_sort[0])]: # 채널번호.
                    self.nowChannel_index = i
                    self.nowChannel = self.__enabledChannelList[i]
                    return self.nowChannel[0]
                else:
                    continue
        else: #현재 채널 선호도보다 큰 채널이 최소 1개 존재
            for i in range(self.favor_list_sort.index(self.favor), len(self.favor_list_sort)):
                if self.favor_list_sort[i] == self.favor: #선호도 등급이 같은 경우
                    continue
                else: #선호도 등급이 한단계 높은 채널 찾았다.
                    self.favor = self.favor_list_sort[i]
                    self.number = self.favor_noblock_list[self.favor_list.index(self.favor)] #바꿀 채널 번호
                    
                    for j in range(len(self.__enabledChannelList)):
                        if self.number == self.__enabledChannelList[j][0]: #찾았다.
                            self.nowChannel_index = j
                            self.nowChannel = self.__enabledChannelList[j]
                            return self.nowChannel[0]
                        else: #못찾은경우 다시.
                            continue
