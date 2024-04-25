# -*- coding: utf-8 -*-

"""

@ function: |OutliersProcessing: 异常值（极大值、极小值、重复值）剔除，返回正常数值的下标.
            |outliers:           用于一维数据
            |outliers_pv：       主要针对光伏的二维数据
            |outliers_wd：       主要针对风电的二维数据
            --------------------------------------------------------------------
            |QuartileProcessing：异常值四分位处理，返回正常数值的下标
            |quartile_process：四分位数据清洗
@ author:   sun-shu-bei
@ date:     2020-07-22
@ vision：  v1.5.0
@ modify:
            1. 索引修改 sun-shu-bei 2018-01-04
            2. 四分位修改 sun-shu-bei 2018-01-23
            3. 增加支持Python3版本 sun-shu-bei 2020-07-22
"""
import numpy


class OutliersProcessing:

    def __init__(self, repeat_frequency, min_value, max_value):
        self.repeat_frequency = repeat_frequency
        self.min_value = min_value
        self.max_value = max_value

    def outliers(self, data):

        # 标记重复值
        len_data = len(data)
        temp_label = numpy.zeros_like(data)
        repeat_label = numpy.ones_like(data)
        for num_a in range(1, len_data):
            if data[num_a] == data[num_a - 1] and data[num_a] != 0 :
                repeat_label[num_a] = repeat_label[num_a - 1] + 1

        # 标记待删除重复值，极大值、极小值、nan、-99
        for num_b in range(0, len_data):
            if repeat_label[num_b] >= self.repeat_frequency:
                temp_label[num_b + 1 - self.repeat_frequency: num_b + 1] = 1
            if data[num_b] < self.min_value or data[num_b] > \
                    self.max_value or numpy.isnan(data[num_b]) or data[num_b] == -99:
                temp_label[num_b] = 1
        index_data = numpy.where(temp_label == 0)
        return index_data

    def outliers_pv(self, pw, rd):

        # 标记重复值
        len_data = len(pw)
        temp_label = numpy.zeros_like(pw)
        repeat_label = numpy.ones_like(pw)
        for num_a in range(1, len_data):
            if pw[num_a] == pw[num_a - 1] and rd[num_a] != 0:
                repeat_label[num_a] = repeat_label[num_a - 1] + 1

        # 标记待删除重复值，极大值、极小值、nan、-99
        for num_b in range(0, len_data):
            if repeat_label[num_b] >= self.repeat_frequency:
                temp_label[num_b + 1 - self.repeat_frequency: num_b + 1] = 1
            if pw[num_b] < self.min_value or pw[num_b] > self.max_value or numpy.isnan(pw[num_b]) or pw[num_b] == -99:
                temp_label[num_b] = 1
        index_data = numpy.where(temp_label == 0)

        return index_data

    def outliers_wd(self, pw, wd):

        # 标记重复值
        len_data = len(pw)
        temp_label = numpy.zeros_like(pw)
        repeat_label = numpy.ones_like(pw)
        for num_a in range(1, len_data):
            if pw[num_a] == pw[num_a - 1] and wd[num_a] >= 3:
                repeat_label[num_a] = repeat_label[num_a - 1] + 1

        # 标记待删除重复值，极大值、极小值、nan、-99
        for num_b in range(0, len_data):
            if repeat_label[num_b] >= self.repeat_frequency:
                temp_label[num_b + 1 - self.repeat_frequency: num_b + 1] = 1
            if pw[num_b] < self.min_value or pw[num_b] > self.max_value or numpy.isnan(pw[num_b]) or pw[num_b] == -99:
                temp_label[num_b] = 1
        index_data = numpy.where(temp_label == 0)

        return index_data


class QuartileProcessing:

    def __init__(self, power, speed, array_index, capacity):

        self.power = power
        self.speed = speed
        self.array_index = array_index
        self.capacity = capacity

    def quartile_process(self, x=1.5, y=1.5):

        # 横向四分位数据清洗
        vmax = 30
        loop_stp = 0.5                 # 步长
        loop_speed = vmax + loop_stp   # 循环最大值
        temp_label_sp = numpy.zeros_like(self.speed)

        for a_loop in numpy.arange(0, loop_speed, loop_stp):
            index_sp = numpy.where(numpy.logical_and(self.speed >= a_loop, self.speed < a_loop + loop_stp))

            if len(index_sp[0]) > 0:
                temp_pw = self.power[index_sp]
                temp_lb_sp = temp_label_sp[index_sp]
                p1 = numpy.percentile(temp_pw, 25)
                p3 = numpy.percentile(temp_pw, 75)
                dp = p3 - p1
                re_p1 = p1 - x * dp
                re_p3 = p3 + y * dp
                index_limit_pw = numpy.where(numpy.logical_or(temp_pw > re_p3, temp_pw < re_p1))
                temp_lb_sp[index_limit_pw] = 1
                temp_label_sp[index_sp] = temp_lb_sp
            else:
                continue
        label_normal_sp = numpy.where(temp_label_sp == 0)
        power_hon = self.power[label_normal_sp]
        speed_hon = self.speed[label_normal_sp]
        array_index_hon = self.array_index[label_normal_sp]

        # 纵向四分位数据清洗
        temp_label_pw = numpy.zeros_like(speed_hon)
        loop_stp = self.capacity/29.0          # 步长
        loop_power = self.capacity             # 循环最大值
        for a_loop in numpy.arange(0, loop_power, loop_stp):
            index_pw = numpy.where(numpy.logical_and(power_hon >= a_loop, power_hon < a_loop + loop_stp))

            if len(index_pw[0]) > 0:
                temp_sp = speed_hon[index_pw]
                temp_lb_pw = temp_label_pw[index_pw]
                p1 = numpy.percentile(temp_sp, 25)
                p3 = numpy.percentile(temp_sp, 75)
                dp = p3 - p1
                re_p1 = p1 - x * dp
                re_p3 = p3 + y * dp
                index_limit_sp = numpy.where(numpy.logical_or(temp_sp > re_p3, temp_sp < re_p1))
                temp_lb_pw[index_limit_sp] = 1
                temp_label_pw[index_pw] = temp_lb_pw
            else:
                continue
        label_normal_pw = numpy.where(temp_label_pw == 0)
        array_index_hon_lon = array_index_hon[label_normal_pw]
        label_normal = array_index_hon_lon
        list_index = list(self.array_index)
        label_limit = list(set(list_index).difference(set(list(label_normal))))

        return label_normal, label_limit
