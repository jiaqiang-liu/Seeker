# -*- coding: utf-8 -*-
import numpy
import logging

logging.basicConfig(level=logging.INFO)

#计算网页pagerank
def GetMatrixA(urls_obj_list):
    n = len(urls_obj_list)
    A = [[0.0000000001] * n for i in range(n)]
    logging.debug('matrix_DBG', n)
    for url in urls_obj_list:
        for link_id in url.links_id:
            try:
                A[url.id][link_id] += 1
            except:
                logging.debug('log-error', url.id, link_id)
                pass
    return A


class RankPageAlgorithm(object):

    def __init__(self, A): #传入一个二维矩阵，和一个一维矩阵
        self.A = numpy.array(A)
        self.B = []
        n = len(A)
        for i in range(n):
            self.B.append([1 / n])

    def calcu(self):
        for i in range(10):
            self.B = self.A.dot(self.B)
        res = [x[0] for x in self.B]
        return res

    def deepcalcu(self):
        pass
