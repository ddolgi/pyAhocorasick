#!/usr/bin/env python3
# -*- encoding=utf-8 -*- 
'''
Created on Mar 15, 2014

@author: tonyzhang
'''

__all__ = ['Ahocorasick', ]

class Node(object):
    
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        
class Ahocorasick(object):
    
    def __init__(self):
        self.__root = Node()
        
    def addWord(self, word):
        tmp = self.__root
        for i in range(0, len(word)):
            if word[i] not in tmp.next:
                tmp.next[word[i]] = Node()
            tmp = tmp.next[word[i]]
        tmp.isWord = True
    
    def make(self):
        '''
            build the fail function 
        '''
        tmpQueue = []
        tmpQueue.append(self.__root)
        while(len(tmpQueue) > 0):
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if k in p.next:
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None :
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])
    
    def search(self, content):
        '''
            @return: a list of tuple,the tuple contain the match start and end index
        '''
        p = self.__root
        result = []
        startWordIndex = 0
        endWordIndex = -1
        currentPosition = 0
        
        while currentPosition < len(content):
            word = content[currentPosition]
            while word not in p.next and p != self.__root:
                p = p.fail
            
            if word in p.next:
                if p == self.__root:
                    startWordIndex = currentPosition
                p = p.next[word]
            else:
                p = self.__root
            
            if p.isWord:
                result.append((startWordIndex, currentPosition))
            
            currentPosition += 1
        return result
    
    def mask(self, content):
        replacepos = self.search(content)
        result = content
        for i in replacepos:
            result = result[0:i[0]] + (i[1] - i[0] + 1) * u'*' + content[i[1] + 1:]
        return result


if __name__ == '__main__':
    ah = Ahocorasick()
    ah.addWord('abc')
    ah.addWord('bc')
    ah.addWord('cd')
    ah.make()
    print(ah.search(u'abc123cdef'))
    print(ah.mask(u'abc123cdef'))

