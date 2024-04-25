# -*- coding: utf-8 -*-

"""
@ function: |CalculateAccuracy:       计算 MAE 和 MSE
            |calculate_MAE:           计算 MAE
            |calculate_MSE：          计算 MSE
            |calculate_harmonic:      计算调和平均准确率
            |calculate_huabei:        计算华北短期准确率
            |calculate_huazhong_wind: 计算华中风电短期准确率
            |calculate_huazhong_solar:计算华中光伏短期准确率
            |calculate_sichuan_wind:  计算四川风电短期准确率
            |calculate_sichuan_solar: 计算四川光伏短期准确率
            |calculate_nanfang_wind_2022: 计算南网2022版风电短期准确率 乔锋 2023年5月31日
            |calculate_nanfang_solar_2022: 计算南网2022版光伏短期准确率 乔锋 2023年5月31日
            |calculate_nanfang_wind:  计算南方风电短期准确率
            |calculate_nanfang_solar: 计算南方光伏短期准确率
            |calculate_shanxi_wind:   计算山西风电短期准确率
            |calculate_shanxi_solar:  计算山西光伏短期准确率
            |calculate_shandong_wind: 计算山东风电短期准确率
            |calculate_shandong_solar:计算山东光伏短期准确率
            |calculate_fujian_wind:   计算福建风电短期准确率
            |calculate_anhui_wind:    计算安徽风电短期准确率
            |calculate_anhui_solar:   计算安徽光伏短期准确率
            |calculate_zhejiang_wind: 计算浙江风电短期准确率  2022年3月18日
            |calculate_zhejiang_solar:计算浙江光伏短期准确率  2022年3月18日
            |calculate_dongbei_wind:  计算东北风电短期准确率
            |calculate_dongbei_solar: 计算东北光伏短期准确率
            |calculate_shanxi_2021_wind: 计算山西2021版风电短期准确率
            |calculate_shanxi_2021_solar: 计算山西2021版光伏短期准确率
            |calculate_xibei_wind_2022: 计算陕西2022版风电短期准确率
            |calculate_xibei_solar_2022: 计算陕西2022版光伏短期准确率
            |calculate_xinjiang_wind_2022: 计算新疆2022版风电短期准确率
            |calculate_xinjiang_solar_2022: 计算新疆2022版风电短期准确率
            |calculate_xibei_wind_2023: 计算陕西2023版风电短期准确率
            |calculate_xibei_solar_2023: 计算陕西2023版光伏短期准确率
            |calculate_xinjiang_wind_2023: 计算新疆2023版风电短期准确率
            |calculate_xinjiang_solar_2023: 计算新疆2023版风电短期准确率
            |calculate_harmonic_2023:      计算2023版调和平均准确率


            --------------------------------------
@ author:   sun-shu-bei song-mei-yang
@ date:     2020-07-22
@ update:   2023-05-31
@ vision：  v1.11.0
@ update:
            1. 时间格式处兼容性      sun-shu-bei  2017-11-13
            2. 日mse时间格式排序     sun-shu-bei  2017-11-13
            3. pandas列名显示问题   sun-shu-bei  2017-11-15
            4. 简化时间格式         sun-shu-bei  2018-01-04
            5. 添加调和平均准确率    sun-shu-bei  2018-01-31
            6. 添加合格率计算        zhang-qi     2018-03-29
            7. 增加Python3版本的支持 sun-shu-bei  2020-07-22
            8. 修改调和平均数        song-mei-yang 2020-12-11
            9. 增加华北、华中、南方、东北、山西、山东、福建、安徽、浙江、四川
            等各省两个细则函数       song-mei-yang 2020-12-11
            10 增加山西2021版双细则考核函数 song-mei-yang 2021-12-09
            11 根据均方根误差计算不达标天数时将原标准20% 改为 15% song-mei-yang 2022-01-17
            12 新增西北区域柔性考核  song-mei-yang 2022-03-10
            13 浙江两个细则 数据预处理 bug修复 song-mei-yang 2022-03-18
            14 新增南方电网2022版风光两个细则计算规则 qiaofeng 2023-05-31
            15 新增西北电网2023版风光两个细则计算规则 song-mei-yang 2023-12-01

 """
import numpy
import datetime
import pandas
import calendar



def check(date_time=None,power_real=None,power_forecast=None):
    if len(str(date_time))==19:
        return str(date_time)
    else:
        print(date_time)
    if str(power_real).isdigit():
        return float(power_real)
    else:
        print(power_real)
    if str(power_forecast).isdigit:
        return float(power_forecast)
    else:
        print(power_forecast)


class CalculateAccuracy:

    def __init__(self, date_time, power_real, power_forecast, capacity):

        self.date_time = date_time
        self.power_real = power_real
        self.power_forecast = power_forecast
        self.capacity = capacity

    def calculate_MAE(self,para=0.03):

        index_more = numpy.where(self.power_real > self.capacity * para)
        dt = self.date_time[index_more[0]]
        pr = self.power_real[index_more[0]]
        pf = self.power_forecast[index_more[0]]
        len_loop = len(dt)
        time_list = []

        if self.date_time[0][10] == '_':
            for loop in range(len_loop):
                t = datetime.datetime.strptime(dt[loop], '%Y-%m-%d_%H:%M:%S')
                y_m = t.strftime('%Y-%m')
                time_list.append(y_m)
        else:
            for loop in range(len_loop):
                t = datetime.datetime.strptime(dt[loop], '%Y-%m-%d %H:%M:%S')
                y_m = t.strftime('%Y-%m')
                time_list.append(y_m)

        bias_abs = abs(pr - pf)

        # 创建 DataFrame
        df = pandas.DataFrame({'date': time_list, 'bias': bias_abs})
        error_mean = df['bias'].groupby(df['date']).mean()
        MAE = error_mean/float(self.capacity) * 100.0

        return MAE

    def calculate_MSE(self):

        len_loop = len(self.date_time)
        ymd_list = []

        if self.date_time[0][10] == '_':

            for a_loop in range(len_loop):
                t = datetime.datetime.strptime(self.date_time[a_loop], '%Y-%m-%d_%H:%M:%S')
                y_m_d = t.strftime('%Y-%m-%d')
                ymd_list.append(y_m_d)
        else:
            for a_loop in range(len_loop):
                t = datetime.datetime.strptime(self.date_time[a_loop], '%Y-%m-%d %H:%M:%S')
                y_m_d = t.strftime('%Y-%m-%d')
                ymd_list.append(y_m_d)

        bias = self.power_real - self.power_forecast
        bias_square = numpy.square(bias)

        # 创建 DataFrame
        df_day = pandas.DataFrame({'date': ymd_list, 'bias_square': bias_square})
        error_day_mean = df_day['bias_square'].groupby(df_day['date']).mean()
        day_mse = numpy.sqrt(error_day_mean)/float(self.capacity)
        error_day = day_mse.index
        error_value = day_mse.values * 100.0
        ym_list = []
        error_list = []
        count_day = []

        for b_loop in range(len(error_day)):
            bd = datetime.datetime.strptime(error_day[b_loop], '%Y-%m-%d')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
            error_list.append(error_value[b_loop])

            if error_value[b_loop] > 15:
                count_day.append(1)
            else:
                count_day.append(0)

        df_month = pandas.DataFrame({'date': ym_list, 'MSE': error_list, 'day_mark': count_day})
        MSE = df_month['MSE'].groupby(df_month['date']).mean()
        off_grade = df_month['day_mark'].groupby(df_month['date']).sum()

        return day_mse, MSE, off_grade

    def calculate_harmonic(self):
        '''
        西北两个细则中超短期第二小时点的调和平均数准确率
        输入为实际功率 及 超短期预测功率 输入numpy.array格式
        输出为DataFrame格式的超短期准确率、超短期准确率考核分
        
        FBI WARNING : 
            确保输入超短期第二小时预测数据
            返回的超短期第二小时准确率
    
        '''

        # 创建DataFrame
        # df_score = pandas.DataFrame([], columns=['date','harmonic', 'harmonic_score'])
        df_data = pandas.DataFrame([],columns=['time', 'power_real', 'power_forecast'])
        df_data['time'] = self.date_time
        df_data['power_real'] = self.power_real
        df_data['power_forecast'] = self.power_forecast
        # 计算调和平均准确率考核分数
        dfs_time = df_data['time']
        power_real = df_data['power_real']
        power_forecast = df_data['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        bias_item = abs((power_real / (power_real + power_forecast)) - 0.5)  # 偏差项计算
        abs_error = abs(power_real - power_forecast)  # 实际功率与预测功率之差
        multi_item = bias_item * abs_error
        sum_item = multi_item.groupby(ymd).sum()
        sum_error = abs_error.groupby(ymd).sum()  # 96个点的差值求和计算
        harmonic = 1 - 2 * sum_item / sum_error
        harmonic_score = numpy.where(harmonic < 0.75, 100 * (0.75 - harmonic) * self.capacity * 0.015 * 0.1, 0)
        date_ymd = harmonic.index
        # 输出成DataFrame格式
        df_score = pandas.DataFrame({'date': date_ymd, 'day_harmonic': numpy.array(harmonic), 'day_pen_score': numpy.array(harmonic_score)})

        return df_score

    def calculate_harmonic_2023(self):
        '''
        输入为实际功率及第*小时超短期预测功率 输入numpy.array格式
        输出为DataFrame格式的第*小时重点时刻调和平均数准确率 + 其它时刻调和平均数准确率
        由于输入第*小时不确定 故暂不输出对应的考核分数

        2023年11月08日西北能监局关于印发西北区域两个细则 附件1并网运行管理实施细则 
        超短期预测曲线第1、2、3、4小时调和平均数准确率
        风电第1小时80% 第2小时75% 第3小时70% 第4小时65%
        光伏第1小时85% 第2小时80% 第3小时75% 第4小时70%
        
        重点时段为：用电高峰时段 + 新能源大发时段  
        重点时段每减少1%按照全场装机容量*0.0015分/万千瓦
        其它时段每减少1%按照全场装机容量*0.0003分/万千瓦
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为: 11:00-17:00
        新疆用  电高峰时段为: 07:00-10:00  18:00-23:00
        FBI WARNING : 
            pr和pf均在装机容量的3%以为时 该点不计入误差计算
            确保输入超短期第*小时预测数据
            返回的超短期第*小时准确率
    
        '''
        # 创建DataFrame
        # df_score = pandas.DataFrame([], columns=['date','harmonic', 'harmonic_score'])
        df_data = pandas.DataFrame([],columns=['time', 'power_real', 'power_forecast'])
        df_data['time'] = self.date_time
        df_data['power_real'] = self.power_real
        df_data['power_forecast'] = self.power_forecast
        # 计算调和平均准确率
        dfs_time = df_data['time']
        power_real = df_data['power_real']
        power_forecast = df_data['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        df_hour = dfs_time.str[11:16] # 选取 hh-mm
        # 实际和预测均在装机容量的3%以内时 不计入误差计算
        n_index = numpy.where(numpy.logical_or(power_real >= self.capacity * 0.03, power_forecast >= self.capacity * 0.03))
        power_real = power_real[n_index[0]]
        power_forecast = power_forecast[n_index[0]]
        ymd = ymd[n_index[0]]
        df_hour = df_hour[n_index[0]]

        df_clean = pandas.DataFrame([],columns=['ymd','hour', 'power_real', 'power_forecast'])
        df_clean['ymd'] = ymd
        df_clean['hour'] = df_hour
        df_clean['power_real'] = power_real
        df_clean['power_forecast'] = power_forecast

        # 高峰时段计算调和平均数准确率


        bias_item = abs((power_real / (power_real + power_forecast)) - 0.5)  # 偏差项计算
        abs_error = abs(power_real - power_forecast)  # 实际功率与预测功率之差
        multi_item = bias_item * abs_error
        sum_item = multi_item.groupby(ymd).sum()
        sum_error = abs_error.groupby(ymd).sum()  # 96个点的差值求和计算
        harmonic = 1 - 2 * sum_item / sum_error
        harmonic_score = numpy.where(harmonic < 0.75, 100 * (0.75 - harmonic) * self.capacity * 0.015 * 0.1, 0)
        date_ymd = harmonic.index
        # 输出成DataFrame格式
        df_score = pandas.DataFrame({'date': date_ymd, 'day_harmonic': numpy.array(harmonic), 'day_pen_score': numpy.array(harmonic_score)})

        return df_score




    def calculate_huabei(self):
        '''
            北京、天津、河北、冀北、内蒙古两个细则考核 输入numpy.array格式
            返回每日短期准确率
            返回每日短期考核电量
            FBI WARING :   
                准确率公式多适用于冀北 冀南风光项目
        '''
        df_hebei = pandas.DataFrame([],columns=['time','power_real','power_forecast'])
        df_hebei['time'] = self.date_time
        df_hebei['power_real'] = self.power_real
        df_hebei['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_hebei['time']
        pr = df_hebei['power_real']
        pf = df_hebei['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        ymd_new = []
        acc_new = []
        pen_new = []

        grouped = pr.groupby(ymd)
        for key, group in grouped:
            ymd_new.append(key)
            pr_temp = pr.iloc[group.index].values
            pf_temp = pf.iloc[group.index].values
            pr_clean = pr_temp[numpy.where(pr_temp > -99)]  # 实际功率为-99的剔除后进行计算
            pr_clean = numpy.where(pr_clean < 0, 0, pr_clean)
            pf_clean = pf_temp[numpy.where(pr_temp > -99)]
            bias = abs(pr_clean - pf_clean)
            temp_0 = sum(bias ** 3)
            temp_1 = sum(bias)
            if len(pr_clean) == 0:
                temp = -0.99
                acc_new.append(temp)
            elif temp_1 == 0:
                temp = 1
                acc_new.append(temp)
            else:
                temp = 1 - numpy.sqrt(temp_0 / temp_1) / float(self.capacity)
                acc_new.append(temp)

            if temp == -0.99:
                temp_pen = -99
            elif temp < 0.85:  # 河北要求短期准确率高于0.85
                temp_pen = (0.85 - temp) * cap * 0.4
            else:
                temp_pen = 0
            pen_new.append(temp_pen)

        df_penalty = pandas.DataFrame({'date': ymd_new, 'day_acc': acc_new, 'day_pen_mwh': pen_new})

        return df_penalty

    def calculate_jiangsu(self):
        '''
        江苏两个细则考核 输入numpy.array格式
        风光都适用
        计算每个点 合格率 
        FBI WARNING : 
            江苏只能返回超过月度 及 月考核金额(万元)
        '''
        df_jiangsu = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_jiangsu['time'] = self.date_time
        df_jiangsu['power_real'] = self.power_real
        df_jiangsu['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_jiangsu['time']
        pr = df_jiangsu['power_real']
        pf = df_jiangsu['power_forecast']
        # ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        ym = dfs_time.str[0:7]

        ym_new = []
        pen_new = []
        grouped = pr.groupby(ym)
        for key, group in grouped:
            ym_new.append(key)
            pr_temp = pr.iloc[group.index].values
            pf_temp = pf.iloc[group.index].values
            percent_pass = 1- abs(pr_temp-pf_temp)/float(cap)
            count_not_pass = len(percent_pass[percent_pass<0.9])
            y = int(key[0:4])
            m = int(key[5:])
            month_count_sum = calendar.monthrange(y,m)[1]*96
            pen_month = (count_not_pass - month_count_sum*0.02)*cap*0.00015
            pen_new.append(pen_month)
        month_pen = pandas.DataFrame({'date': ym_new,'month_pen_rmb': pen_new})

        return month_pen

    def calculate_huazhong_wind(self):
        '''
        华中两个细则考核 输入numpy.array格式
        适用于风电项目（河南、湖北、湖南、江西、重庆 六省市）
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        FBI WARING:
            四川满足有相关系数规则 因此四川单独列出
        '''
        df_huazhong = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_huazhong['time'] = self.date_time
        df_huazhong['power_real'] = self.power_real
        df_huazhong['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_huazhong['time']
        pr = df_huazhong['power_real']
        pf = df_huazhong['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # # 计算相关系数
        # corr = df_huazhong.groupby(ymd).apply(lambda x: numpy.corrcoef(x.power_real,x.power_forecast)[0, 1])


        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        date_ymd = rmse.index
        rmse = numpy.array(rmse)   # 转为数组
        # corr = numpy.array(corr)   # 转为数组
        penalty_mwh = numpy.where(rmse > 0.2, (rmse - 0.2) * cap * 1,  0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame({'date': date_ymd,'day_acc': 1-rmse, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_huazhong_solar(self):
        '''
        
        华中光伏两个细则考核 输入numpy.array格式
        适用于光伏项目（河南、湖北、湖南、江西、重庆 六省市）
        返回每日短期准确率 (1-mae)
        返回每日短期考核电量（MWH)
        
        '''
        df_huazhong = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_huazhong['time'] = self.date_time
        df_huazhong['power_real'] = self.power_real
        df_huazhong['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_huazhong['time']
        pr = df_huazhong['power_real']
        pf = df_huazhong['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算每日平均绝对误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = abs(pr - pf) # （实际功率-预测功率）
        mae = error.groupby(ymd).mean()  # 平均绝对误差
        mae = mae/float(cap)

        date_ymd = mae.index
        mae = numpy.array(mae)    # 转为数组

        penalty_mwh = numpy.where(mae > 0.15, (mae - 0.15) * cap * 1.5,  0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame({'date': date_ymd,'day_acc': 1-mae, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_sichuan_wind(self):
        '''
        四川两个细则考核 输入numpy.array格式
        适用于风电项目四川
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        返回每日相关系数 （与当月电量相关，暂不计算每日相关系数考核电量）

        '''
        df_sichuan = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_sichuan['time'] = self.date_time
        df_sichuan['power_real'] = self.power_real
        df_sichuan['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_sichuan['time']
        pr = df_sichuan['power_real']
        pf = df_sichuan['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算相关系数
        corr = df_sichuan.groupby(ymd).apply(lambda x: numpy.corrcoef(x.power_real,x.power_forecast)[0, 1])


        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        date_ymd = rmse.index
        rmse = numpy.array(rmse)   # 转为数组
        corr = numpy.array(corr)   # 转为数组
        penalty_mwh = numpy.where(rmse > 0.2, (rmse - 0.2) * cap * 1,  0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame({'date': date_ymd,'day_acc': 1-rmse, 'day_corr': corr,'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_sichuan_solar(self):
        '''
        
        四川光伏两个细则考核 输入numpy.array格式
        适用于光伏项目四川
        返回每日短期准确率 (1-mae)
        返回每日短期考核电量（MWH)

        '''
        df_sichuan = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_sichuan['time'] = self.date_time
        df_sichuan['power_real'] = self.power_real
        df_sichuan['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_sichuan['time']
        pr = df_sichuan['power_real']
        pf = df_sichuan['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd


        # 计算每日平均绝对误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = abs(pr - pf) # （实际功率-预测功率）
        mae = error.groupby(ymd).mean()  # 平均绝对误差
        mae = mae/float(cap)

        date_ymd = mae.index
        mae = numpy.array(mae)    # 转为数组

        penalty_mwh = numpy.where(mae > 0.15, (mae - 0.15) * cap * 1.5,  0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame({'date': date_ymd,'day_acc': 1-mae, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_nanfang_wind_2022(self):
        '''
        按照国家能源局南方监管局 南方能监市场2022第91号文 （适用对象广东、广西、云南、贵州、海南、深圳）
        南网考核1+7系统计算规则要求：当预测功率、可用功率、实际功率均小于装机10%，不纳入准确率计算；
        注：1+7考核系统不纳入计算后导致准确率比纳入计算的准确率更低
        rmse/pmi        pmi ≥ 0.2Cap
        rmse/cap*0.2    pmi < 0.2Cap

        input：
            日期、实际功率、预测准确率、装机容量
        return：
            日期、准确率、考核电量
        准确率计算及考核要求：
            同一时刻，实际功率、预测功率都低于装机容量的10%的数据会被剔除，不参与准确率计算
            当准确率计算结果小于0时，准确率按0执行
            短期考核电量==（60%-准确率）* cap * 0.2
            实际执行规则为 不使用(不足一个百分点的按一个百分点计)此规则,准确率直接相减计算
        '''
        df_nanfang_wind = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_nanfang_wind['time'] = self.date_time
        df_nanfang_wind['power_real'] = self.power_real
        df_nanfang_wind['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_nanfang_wind['time']
        pr = df_nanfang_wind['power_real']
        pf = df_nanfang_wind['power_forecast']
        ymd = dfs_time.astype(str).str[0:10]

        popstand = 0.1 * cap
        # 预测功率小于0.1倍装机阈值时 等于0.1倍装机 ；此行不在用于指标计算中
        # df_nanfang_wind['power_forecast'] = numpy.where(df_nanfang_wind['power_forecast'] < popstand, popstand,
        #                                               df_nanfang_wind['power_forecast'])
        df_nanfang_wind['popdata'] = numpy.where(
            (df_nanfang_wind['power_real'] < popstand) & (df_nanfang_wind['power_forecast'] < popstand), 0, 1)
        df_nanfang_wind = df_nanfang_wind[df_nanfang_wind['popdata'] == 1]
        df_nanfang_wind['fm'] = df_nanfang_wind['power_real'].apply(lambda x: x if x > 0.2 * cap else 0.2 * cap)
        fm = df_nanfang_wind['fm']

        dfs_time = df_nanfang_wind['time']
        pr = df_nanfang_wind['power_real']
        pf = df_nanfang_wind['power_forecast']

        error = abs(pr - pf)
        offset = (error / fm) ** 2
        acc = 1 - numpy.sqrt(offset.groupby(ymd).mean())
        date_ymd=acc.index
        acc = numpy.array(numpy.where(acc < 0, 0, acc))
        penalty_mwh = numpy.array(numpy.where(acc < 0.6, (0.6 - acc) * cap * 0.2, 0))
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_nanfang_solar_2022(self):
        '''
        按照国家能源局南方监管局 南方能监市场2022第91号文 （适用对象广东、广西、云南、贵州、海南、深圳）
        南网考核1+7系统计算规则要求：当预测功率、可用功率、实际功率均小于装机10%，不纳入准确率计算；
        注：1+7考核系统不纳入计算后导致准确率比纳入计算的准确率更低
        rmse/pmi        pmi ≥ 0.2Cap
        rmse/cap*0.2    pmi < 0.2Cap
        
        input：
            日期、实际功率、预测准确率、装机容量
        return：
            日期、准确率、考核电量
        准确率计算及考核要求：
            同一时刻，实际功率、预测功率都低于装机容量的10%的数据会被剔除，不参与准确率计算
            当准确率计算结果小于0时，准确率按0执行
            短期考核电量==（65%-准确率）* cap
            实际执行规则为 不使用(不足一个百分点的按一个百分点计)此规则,准确率直接相减计算
        '''
        df_nanfang_solar = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_nanfang_solar['time'] = self.date_time
        df_nanfang_solar['power_real'] = self.power_real
        df_nanfang_solar['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_nanfang_solar['time']
        pr = df_nanfang_solar['power_real']
        pf = df_nanfang_solar['power_forecast']
        ymd = dfs_time.astype(str).str[0:10]  # 选取 yyyy-mm-dd

        popstand = 0.1 * cap
        df_nanfang_solar['popdata'] = numpy.where((df_nanfang_solar['power_real'] < popstand) & (df_nanfang_solar['power_forecast'] < popstand), 0, 1)
        df_nanfang_solar = df_nanfang_solar[df_nanfang_solar['popdata'] == 1]
        df_nanfang_solar['fm'] = df_nanfang_solar['power_real'].apply(lambda x: x if x > 0.2 * cap else 0.2 * cap)
        fm = df_nanfang_solar['fm']


        error = abs(pr - pf)
        offset = (error / fm) ** 2
        acc = 1 - numpy.sqrt(offset.groupby(ymd).mean())
        date_ymd = acc.index
        acc = numpy.array(numpy.where(acc < 0, 0, acc))
        penalty_mwh = numpy.array(numpy.where(acc < 0.65, (0.65 - acc) * cap, 0))
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_nanfang_wind(self):
        '''
        南方两个细则考核 输入numpy.array格式
        适用于装机30MW以上风电项目（云南、贵州、广东、广西、海南、深圳）
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        '''

        df_nanfang_wind = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_nanfang_wind['time'] = self.date_time
        df_nanfang_wind['power_real'] = self.power_real
        df_nanfang_wind['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_nanfang_wind['time']
        pr = df_nanfang_wind['power_real']
        pf = df_nanfang_wind['power_forecast']
        ymd = dfs_time.astype(str).str[0:10]


        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算
        date_ymd = rmse.index


        rmse = numpy.array(rmse)  # 转为数组
        penalty_mwh = numpy.where(rmse > 0.2, (rmse - 0.2) * cap * 1, 0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pen_mwh': penalty_mwh})


        return df_penalty

    def calculate_nanfang_solar(self):
        '''
        南方两个细则考核 输入numpy.array格式
        适用于装机30MW以上风电项目（云南、贵州、广东、广西、海南、深圳）
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        '''
        df_nanfang_solar = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_nanfang_solar['time'] = self.date_time
        df_nanfang_solar['power_real'] = self.power_real
        df_nanfang_solar['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_nanfang_solar['time']
        pr = df_nanfang_solar['power_real']
        pf = df_nanfang_solar['power_forecast']
        ymd = dfs_time.astype(str).str[0:10]  # 选取 yyyy-mm-dd

        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        date_ymd = rmse.index
        rmse = numpy.array(rmse)  # 转为数组

        penalty_mwh = numpy.where(rmse > 0.15, (rmse - 0.15) * cap * 1, 0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_shanxi_wind(self):
        '''
        山西两个细则考核 输入numpy.array格式
        适用于山西风电项目
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        '''
        df_shanxi_wind = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_shanxi_wind['time'] = self.date_time
        df_shanxi_wind['power_real'] = self.power_real
        df_shanxi_wind['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_shanxi_wind['time']
        pr = df_shanxi_wind['power_real']
        pf = df_shanxi_wind['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        date_ymd = rmse.index
        rmse = numpy.array(rmse)  # 转为数组

        penalty_mwh = numpy.where(rmse > 0.2, (rmse - 0.2) * cap * 1, 0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_shanxi_solar(self):
        '''

        山西光伏两个细则考核 输入numpy.array格式
        适用于山西光伏项目
        返回每日短期准确率 (1-mae)、每日短期合格率(day_pass)
        返回每日考核总电量（MWH) 即返回每日(短期准确率考核电量 + 短期合格率考核电量)之和

        '''
        df_shanxi = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_shanxi ['time'] = self.date_time
        df_shanxi ['power_real'] = self.power_real
        df_shanxi ['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_shanxi ['time']
        pr = df_shanxi ['power_real']
        pf = df_shanxi ['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零

        # 计算每日平均绝对误差

        error = abs(pr - pf)  # 实际功率-预测功率
        mae = error.groupby(ymd).mean()  # 平均绝对误差
        mae = mae / float(cap)

        # 计算合格率
        percent_of_pass = 1 - error/float(cap)
        array_percent_of_pass = numpy.array(percent_of_pass)
        array_percent_of_pass = numpy.where(array_percent_of_pass > 0.8, 1, 0)
        percent_of_pass = pandas.Series(array_percent_of_pass)
        percent_of_pass_day = percent_of_pass.groupby(ymd).mean()  # 日合格率
        #  DataFrame 转 array
        date_ymd = mae.index
        mae = numpy.array(mae)  # 转为数组
        array_percent_of_pass_day = numpy.array(percent_of_pass_day)  # 转为数组

        mae_penalty_mwh = numpy.where(mae > 0.15, (mae - 0.15) * cap * 1.5, 0)  # 均方根误差考核分数计算
        percent_of_pass_penalty_mwh = numpy.where(array_percent_of_pass_day < 0.8, (0.8-array_percent_of_pass_day) * cap * 1, 0)
        penalty_mwh = mae_penalty_mwh + percent_of_pass_penalty_mwh

        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - mae, 'day_pass': array_percent_of_pass_day, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_shandong_wind(self):
        '''
        山东两个细则考核 输入numpy.array格式
        适用于山东风电项目
        山东直接看修模程序中 月均准确率即可
        '''
        pass

    def calculate_shandong_solar(self):
        '''
        山东两个细则考核 输入numpy.array格式
        适用于山东光伏项目
        返回每日短期准确率 即 (1-rmse) 
        返回每日短期考核电量（MWH)
        '''
        df_shandong_solar = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_shandong_solar['time'] = self.date_time
        df_shandong_solar['power_real'] = self.power_real
        df_shandong_solar['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_shandong_solar['time']
        pr = df_shandong_solar['power_real']
        pf = df_shandong_solar['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        date_ymd = rmse.index
        rmse = numpy.array(rmse)  # 转为数组

        penalty_mwh = numpy.where(rmse > 0.15, (rmse - 0.15) * cap * 1, 0)  # 均方根误差考核分数计算
        penalty_mwh = numpy.array(penalty_mwh)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_fujian_wind(self):
        '''

        福建风电两个细则考核 输入numpy.array格式
        适用于山西光伏项目
        返回每日短期准确率 (1-rmse)、每日短期合格率(day_pass)
    
        '''
        df_fujian = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_fujian ['time'] = self.date_time
        df_fujian ['power_real'] = self.power_real
        df_fujian ['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_fujian ['time']
        pr = df_fujian ['power_real']
        pf = df_fujian ['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零

        # 计算均方根误差

        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算

        # 计算合格率
        point_percent_of_pass = 1 - abs(pr-pf)/float(cap)
        array_percent_of_pass = numpy.array(point_percent_of_pass)
        array_percent_of_pass = numpy.where(array_percent_of_pass > 0.8, 1, 0)
        percent_of_pass = pandas.Series(array_percent_of_pass)
        percent_of_pass_day = percent_of_pass.groupby(ymd).mean()  # 日合格率
        #  DataFrame 转 array
        date_ymd = rmse.index
        rmse = numpy.array(rmse)  # 转为数组
        array_percent_of_pass_day = numpy.array(percent_of_pass_day)  # 转为数组

        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pass': array_percent_of_pass_day})

        return df_penalty

    def calculate_anhui_wind(self):
        '''

        安徽风电两个细则考核 输入numpy.array格式
        适用于安徽风电项目
        由于准确率公式分母为实际功率（需考虑分母为零的异常情况）；
            需对实际功率数据预处理
            当天实际功率数据都小于10MW 则不计算这天的准确率和考核电量
            准确率小于零是归为零
        返回每日短期准确率 (1-rmse)、每日短期考核电量

        '''
        df_anhui = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_anhui['time'] = self.date_time
        df_anhui['power_real'] = self.power_real
        df_anhui['power_forecast'] = self.power_forecast
        cap = self.capacity
        # ymd_all = df_anhui['time'].str[0:10]  # 选取 yyyy-mm-dd
        # #  获取每日
        # ymd_new = []
        # for key, group in df_anhui['time'].groupby(ymd_all):
        #     ymd_new.append(key)
        #  数据预处理 当实际功率小于10MW 则不纳入准确率计算
        df_anhui_clean = df_anhui.drop(df_anhui[df_anhui['power_real']<10].index)
        ymd_clean = df_anhui_clean['time'].str[0:10]
        pr = df_anhui_clean['power_real']
        pf = df_anhui_clean['power_forecast']

        # 计算均方根误差

        error = ((pr - pf) / pr) * ((pr - pf) / pr)  # （实际功率-预测功率）
        mse = error.groupby(ymd_clean).mean()  # 标准差计算
        rmse = numpy.sqrt(mse)  # 均方根误差计算
        acc = 1 - rmse
        acc = acc.where(acc > 0,0)  # 准确率小于零 归为零；DataFrame.where cond is True, keep the original value

        #  DataFrame 转 array
        date_ymd = acc.index    # 每天准确率
        acc = numpy.array(acc)  # 转为数组
        penalty_mwh = numpy.where(acc < 0.8, (0.8-acc) * cap * 0.2, 0)   # 均方根误差考核分数计算
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_anhui_solar(self):
        '''

        安徽光伏两个细则考核 输入numpy.array格式
        适用于安徽光伏项目
        由于准确率公式分母为实际功率（需考虑分母为零的异常情况）；
            需对实际功率数据预处理
            实际功率数据上午和晚上小于10MW、实际功率中午等于0MW时 不参与准确率计算
            准确率小于零 归为零
        返回每日短期准确率 (1-rmse)、每日短期考核电量

        '''
        df_anhui = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_anhui['time'] = self.date_time
        df_anhui['power_real'] = self.power_real
        df_anhui['power_forecast'] = self.power_forecast
        cap = self.capacity

        df_anhui['hms'] = df_anhui['time'].str[11:]
        #  数据预处理 当00:00至10:45、14:15至23：45期间实际功率小于10MW 则不纳入准确率计算
        #  数据预处理 当11:00至14:00 期间实际功率小于10MW 则不纳入准确率计算
        df_anhui_morning = df_anhui[df_anhui['hms'] <= '10:45:00']
        df_anhui_clean = df_anhui.drop(df_anhui_morning[df_anhui_morning['power_real'] < 10].index)
        df_anhui_night = df_anhui.loc[(df_anhui['hms'] >= '14:25:00') & (df_anhui['hms'] <= '23:45:00')]
        df_anhui_clean_2 = df_anhui_clean.drop(df_anhui_night[df_anhui_night['power_real'] < 10].index)
        df_anhui_noon = df_anhui.loc[(df_anhui['hms'] >= '11:00:00') & (df_anhui['hms'] <= '14:00:00')]
        df_anhui_clean_3 = df_anhui_clean_2.drop(df_anhui_noon[df_anhui_noon['power_real'] <= 0].index)

        ymd_clean = df_anhui_clean_3['time'].str[0:10]
        pr = df_anhui_clean_3['power_real']
        pf = df_anhui_clean_3['power_forecast']

        # 计算均方根误差

        error = ((pr - pf) / pr) * ((pr - pf) / pr)  # （实际功率-预测功率）
        mse = error.groupby(ymd_clean).mean()  # 标准差计算
        rmse = numpy.sqrt(mse)  # 均方根误差计算
        acc = 1 - rmse
        acc = acc.where(acc > 0,0)  # 准确率小于零 归为零；DataFrame.where cond is True, keep the original value

        #  DataFrame 转 array
        date_ymd = acc.index    # 每天准确率
        acc = numpy.array(acc)  # 转为数组
        penalty_mwh = numpy.where(acc < 0.8, (0.8-acc) * cap * 0.1, 0)   # 均方根误差考核分数计算
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_zhejiang_wind(self):
        '''
        浙江风电两个细则考核 输入numpy.array格式
        适用于浙江风电项目
        由于准确率公式分母为实际功率（需考虑分母为零的异常情况）；
            需对实际功率数据预处理
            实际功率为零 预测功率为零 偏差率为0
            实际功率为零 预测功率不为零 偏差率为100%
                2022年3月18日
                实际功率不为零，预测功率不为零，偏差率大于100% 该时间点的偏差率为100%
            准确率小于零 归为零
        返回每日短期准确率 (1-rmse)、每日短期考核电量
        '''
        df_zhejiang = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_zhejiang['time'] = self.date_time
        df_zhejiang['power_real'] = self.power_real
        df_zhejiang['power_forecast'] = self.power_forecast
        cap = self.capacity

        #  数据预处理 实际功率为零 预测功率为零 偏差率为0; 实际功率为零 预测功率不为零 偏差率为100%

        ymd = df_zhejiang['time'].str[0:10]
        pr = df_zhejiang['power_real']
        pf = df_zhejiang['power_forecast']
        df_zhejiang['deviation'] = abs(pr-pf)
        df_zhejiang.loc[
            (df_zhejiang['power_real'] == 0.0) & (df_zhejiang['power_forecast'] != 0.0), ['deviation']] = -99.0
        df_zhejiang['error'] = -99
        df_zhejiang.loc[(df_zhejiang['deviation'] == -99.0), ['error']] = 1.0  # 实际为零 预测非零时 偏差率为1
        df_zhejiang.loc[(df_zhejiang['deviation'] == 0.0), ['error']] = 0.0    # 实际为零 预测为零时 偏差率为0
        pr_pf_nonzero = df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'deviation']
        pr_nonzero = df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'power_real']
        df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'error'] = (pr_pf_nonzero/pr_nonzero) * (pr_pf_nonzero/pr_nonzero)
        # 实际功率不为零 预测功率不为零 如果此时偏差率大于100%时 则偏差率为100%
        df_zhejiang.loc[(df_zhejiang['error'] > 1), 'error'] = 1
        # 计算标准差
        mse = df_zhejiang.error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse)  # 均方根误差计算
        acc = 1 - rmse
        acc = acc.where(acc > 0,0)  # 准确率小于零 归为零；DataFrame.where cond is True, keep the original value

        #  DataFrame 转 array
        date_ymd = acc.index    # 每天准确率
        acc = numpy.array(acc)  # 转为数组
        penalty_mwh = numpy.where(acc < 0.8, (0.8-acc) * cap * 0.2, 0)   # 均方根误差考核分数计算--风电乘以0.2
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_zhejiang_solar(self):
        '''

        浙江光伏两个细则考核 输入numpy.array格式
        适用于浙江光伏项目
        由于准确率公式分母为实际功率（需考虑分母为零的异常情况）；
            需对实际功率数据预处理
            实际功率为零 预测功率为零 偏差率为0
            实际功率为零 预测功率不为零 偏差率为100%
            2022年3月18日
                实际功率不为零，预测功率不为零，偏差率大于100% 该时间点的偏差率为100%
            准确率小于零 归为零
        返回每日短期准确率 (1-rmse)、每日短期考核电量

        '''
        df_zhejiang = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_zhejiang['time'] = self.date_time
        df_zhejiang['power_real'] = self.power_real
        df_zhejiang['power_forecast'] = self.power_forecast
        cap = self.capacity

        #  数据预处理 实际功率为零 预测功率为零 偏差率为0; 实际功率为零 预测功率不为零 偏差率为100%

        ymd = df_zhejiang['time'].str[0:10]
        pr = df_zhejiang['power_real']
        pf = df_zhejiang['power_forecast']
        df_zhejiang['deviation'] = abs(pr-pf)
        df_zhejiang.loc[
            (df_zhejiang['power_real'] == 0.0) & (df_zhejiang['power_forecast'] != 0.0), ['deviation']] = -99.0
        df_zhejiang['error'] = -99
        df_zhejiang.loc[(df_zhejiang['deviation'] == -99.0), ['error']] = 1.0  # 实际为零 预测非零时 偏差率为1
        df_zhejiang.loc[(df_zhejiang['deviation'] == 0.0), ['error']] = 0.0    # 实际为零 预测非零时 偏差率为0
        pr_pf_nonzero = df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'deviation']
        pr_nonzero = df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'power_real']
        df_zhejiang.loc[(df_zhejiang['deviation'] > 0.0), 'error'] = (pr_pf_nonzero/pr_nonzero) * (pr_pf_nonzero/pr_nonzero)
        # 实际功率不为零 预测功率不为零 如果此时偏差率大于100%时 则偏差率为100%
        df_zhejiang.loc[(df_zhejiang['error'] > 1), 'error'] = 1
        mse = df_zhejiang.error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse)  # 均方根误差计算
        acc = 1 - rmse
        acc = acc.where(acc > 0,0)  # 准确率小于零 归为零；DataFrame.where cond is True, keep the original value

        #  DataFrame 转 array
        date_ymd = acc.index    # 每天准确率
        acc = numpy.array(acc)  # 转为数组
        penalty_mwh = numpy.where(acc < 0.8, (0.8-acc) * cap * 0.2, 0)   # 均方根误差考核分数计算--风电乘以0.2
        # 转DataFrame格式
        df_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': acc, 'day_pen_mwh': penalty_mwh})

        return df_penalty

    def calculate_dongbei_wind(self):
        '''
        东北两个细则考核 输入numpy.array格式
        适用于风电项目（蒙东、黑龙江、吉林、辽宁）
        返回每月短期准确率（调度要求月均大于75%）、每月合格率（调度要求月均大于80%）
        返回每月短期考核分、每月合格率考核分
        FBI WARING:
            
        '''
        df_dongbei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_dongbei['time'] = self.date_time
        df_dongbei['power_real'] = self.power_real
        df_dongbei['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_dongbei['time']
        pr = df_dongbei['power_real']
        pf = df_dongbei['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算
        # 计算合格率
        point_percent_of_pass = 1 - (pr-pf)/float(cap)  # 计算点合格率
        array_percent_of_pass = numpy.array(point_percent_of_pass)
        array_percent_of_pass = numpy.where(array_percent_of_pass >= 0.75, 1, 0)  # 风电场(1-偏差)>=0.75 记为1
        percent_of_pass = pandas.Series(array_percent_of_pass)
        percent_of_pass_day = percent_of_pass.groupby(ymd).mean()  # 计算日合格率

        date_ymd = rmse.index
        rmse = numpy.array(rmse)   # 转为数组
        array_percent_of_pass_day = numpy.array(percent_of_pass_day)

        # 日考核DataFrame格式
        df_day_penalty = pandas.DataFrame({'date': date_ymd,'day_acc': 1-rmse,'day_pass':array_percent_of_pass_day})
        df_day_penalty['month'] = df_day_penalty['date'].str[0:7]
        ym_acc = df_day_penalty['day_acc'].groupby(df_day_penalty['month']).mean()    # 计算月均准确率
        ym_pass = df_day_penalty['day_pass'].groupby(df_day_penalty['month']).mean()  # 计算月均合格率

        # 月考核DataFrame格式
        date_ym = ym_acc.index
        ym_acc = numpy.array(ym_acc)   # 转为数组
        ym_pass = numpy.array(ym_pass)  # 转为数组
        # 计算月考核分
        penalty_acc_score = numpy.where(ym_acc < 0.75, (0.75 - ym_acc) * cap , 0)  # 每降低一个百分点，每10万千瓦扣1分
        penalty_pass_score = numpy.where(ym_pass < 0.8, (0.8 - ym_pass) * cap, 0)  # 每降低一个百分点，每10万千瓦扣1分
        df_month_penalty = pandas.DataFrame({'date': date_ym,'month_acc': ym_acc,'month_pass':ym_pass,
                                             'month_pen_acc':penalty_acc_score,'month_pen_pass':penalty_pass_score})

        return df_day_penalty,df_month_penalty

    def calculate_dongbei_solar(self):
        '''
        东北两个细则考核 输入numpy.array格式
        适用于光伏项目（蒙东、黑龙江、吉林、辽宁）
        返回每月短期准确率（调度要求月均大于85%）、每月合格率（调度要求月均大于80%）
        返回每月短期考核分、每月合格率考核分
        FBI WARING:

        '''
        df_dongbei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_dongbei['time'] = self.date_time
        df_dongbei['power_real'] = self.power_real
        df_dongbei['power_forecast'] = self.power_forecast
        cap = self.capacity

        dfs_time = df_dongbei['time']
        pr = df_dongbei['power_real']
        pf = df_dongbei['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd

        # 计算均方根误差
        pr = numpy.where(pr < 0, 0, pr)  # 实际功率小于零时归零
        error = (pr - pf) * (pr - pf)  # （实际功率-预测功率）
        mse = error.groupby(ymd).mean()  # 标准差计算
        rmse = numpy.sqrt(mse) / float(cap)  # 均方根误差计算
        # 计算合格率
        point_percent_of_pass = 1 - (pr - pf) / float(cap)  # 计算点合格率
        array_percent_of_pass = numpy.array(point_percent_of_pass)
        array_percent_of_pass = numpy.where(array_percent_of_pass >= 0.75, 1, 0)  # 风电场(1-偏差)>=0.75 记为1
        percent_of_pass = pandas.Series(array_percent_of_pass)
        percent_of_pass_day = percent_of_pass.groupby(ymd).mean()  # 计算日合格率

        date_ymd = rmse.index
        rmse = numpy.array(rmse)  # 转为数组
        array_percent_of_pass_day = numpy.array(percent_of_pass_day)

        # 日考核DataFrame格式
        df_day_penalty = pandas.DataFrame(
            {'date': date_ymd, 'day_acc': 1 - rmse, 'day_pass': array_percent_of_pass_day})
        df_day_penalty['month'] = df_day_penalty['date'].str[0:7]
        ym_acc = df_day_penalty['day_acc'].groupby(df_day_penalty['month']).mean()  # 计算月均准确率
        ym_pass = df_day_penalty['day_pass'].groupby(df_day_penalty['month']).mean()  # 计算月均合格率

        # 月考核DataFrame格式
        date_ym = ym_acc.index
        ym_acc = numpy.array(ym_acc)  # 转为数组
        ym_pass = numpy.array(ym_pass)  # 转为数组
        # 计算月考核分
        penalty_acc_score = numpy.where(ym_acc < 0.85, (0.85 - ym_acc) * cap, 0)  # 每降低一个百分点，每10万千瓦扣1分
        penalty_pass_score = numpy.where(ym_pass < 0.8, (0.8 - ym_pass) * cap, 0)  # 每降低一个百分点，每10万千瓦扣1分
        df_month_penalty = pandas.DataFrame({'date': date_ym, 'month_acc': ym_acc, 'month_pass': ym_pass,
                                             'month_pen_acc': penalty_acc_score, 'month_pen_pass': penalty_pass_score})

        return df_day_penalty, df_month_penalty
    
    def calculate_qualification(self):
        '''
        计算合格率
        '''
        len_loop = len(self.date_time)
        ymd_list = []
        ym_list=[]

        for a_loop in range(len_loop):
            t = datetime.datetime.strptime(self.date_time[a_loop], '%Y-%m-%d_%H:%M:%S')
            y_m_d = t.strftime('%Y-%m-%d')
            yy_mm = t.strftime('%Y-%m')
            ym_list.append(yy_mm)
            ymd_list.append(y_m_d)

        qualification = 1-numpy.abs(self.power_real - self.power_forecast)/self.capacity
        signs=numpy.logical_not(qualification<0.8)

        # 创建 DataFrame
        df_day = pandas.DataFrame({'date': ymd_list, 'qualification': qualification,'signs':signs})
        qualification_day = df_day['signs'].groupby(df_day['date']).mean()

        df_month = pandas.DataFrame({'date': ym_list, 'qualification': qualification, 'signs':signs})
        qualification_month = df_month['signs'].groupby(df_month['date']).mean()
       
        return  qualification_day, qualification_month

    def calculate_shanxi_2021_wind(self):
        '''
            山西2021年7月1日执行新两个细则考核 输入numpy.array格式
            计算风电项目 峰谷时段为00:00-06:00；11:00-15:00,17:00-21:00；22:00-23:45
            返回每日短期准确率
            返回每日最大绝对值误差率
            返回每日短期考核电量
            返回每日最大绝对值误差率考核电量
            FBI WARING :
                短期准确率公式同冀北、冀南风光
        '''
        df_shanxi = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_shanxi['time'] = self.date_time
        df_shanxi['power_real'] = self.power_real
        df_shanxi['power_forecast'] = self.power_forecast

        dfs_time = df_shanxi['time']
        pr = df_shanxi['power_real']
        pf = df_shanxi['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        df_hour = dfs_time.str[11:16]  # pandas series
        ymd_new = []
        acc_new = []
        pen_new = []
        ae_new = []
        ae_pen_new = []

        grouped = pr.groupby(ymd)
        for key, group in grouped:
            ymd_new.append(key)
            pr_temp = pr.iloc[group.index].values
            pf_temp = pf.iloc[group.index].values
            hour_temp = df_hour.iloc[group.index].values  # 返回字符
            pr_clean = pr_temp[numpy.where(pr_temp > -99)]  # 实际功率为-99的剔除后进行计算
            pr_clean = numpy.where(pr_clean < 0, 0, pr_clean)
            pf_clean = pf_temp[numpy.where(pr_temp > -99)]
            hour_temp_clean = hour_temp[numpy.where(pr_temp > -99)]
            # 提取每天峰谷时段
            mask = (hour_temp_clean >= '00:00') & (hour_temp_clean <= '06:00') | (hour_temp_clean >= '11:00') & (
                        hour_temp_clean <= '15:00') | (hour_temp_clean >= '17:00') & (hour_temp_clean <= '21:00') | (
                               hour_temp_clean >= '22:00') & (hour_temp_clean <= '23:45')
            pr_peak_valley = pr_clean[mask]
            pf_peak_valley = pf_clean[mask]
            # 仅debug使用此行 hour_peak_valley = hour_temp_clean[mask]
            # 小于0.1倍装机的实际功率不参与考核，需要剔除
            pr_peak_valley_clean = pr_peak_valley[numpy.where(pr_peak_valley >= self.capacity * 0.1)]
            pf_peak_valley_clean = pf_peak_valley[numpy.where(pr_peak_valley >= self.capacity * 0.1)]
            # 仅debug使用此行 hour_peak_valley_clean = hour_peak_valley[numpy.where(pr_peak_valley >= self.capacity*0.1)]
            # 计算最大绝对值误差率
            if len(pr_peak_valley_clean) == 0:
                ae = 0
                ae_new.append(ae)
                ae_penalty = 0
                ae_pen_new.append(ae_penalty)
            elif len(pr_peak_valley_clean) > 0:
                ae = numpy.max((abs(pr_peak_valley_clean - pf_peak_valley_clean) / pr_peak_valley_clean))
                ae_new.append(ae)
                # 计算最大绝对值误差率考核电量
                if ae <= 0.15:
                    ae_penalty = 0.0
                    ae_pen_new.append(ae_penalty)
                elif ae > 0.15:
                    ae_penalty = (ae - 0.15) * self.capacity
                    ae_pen_new.append(ae_penalty)

            bias = abs(pr_clean - pf_clean)
            temp_0 = sum(bias ** 3)
            temp_1 = sum(bias)
            if len(pr_clean) == 0:
                temp = -0.99
                acc_new.append(temp)
            elif temp_1 == 0:
                temp = 1
                acc_new.append(temp)
            else:
                temp = 1 - numpy.sqrt(temp_0 / temp_1) / float(self.capacity)
                acc_new.append(temp)

            if temp == -0.99:
                temp_pen = -99
            elif temp < 0.85:  # 河北要求短期准确率高于0.85
                temp_pen = (0.85 - temp) * self.capacity * 0.4
            else:
                temp_pen = 0
            pen_new.append(temp_pen)

        df_penalty = pandas.DataFrame({'date': ymd_new, 'day_acc': acc_new, 'day_pen_mwh': pen_new, 'max_ae': ae_new,
                                       'max_ae_pen_mwh': ae_pen_new})

        return df_penalty

    def calculate_shanxi_2021_solar(self):
        '''
            山西2021年7月1日执行新两个细则考核 输入numpy.array格式
            计算光伏项目 峰谷时段为11:00-15:00
            返回每日短期准确率
            返回每日最大绝对值误差率
            返回每日短期考核电量
            返回每日最大绝对值误差率考核电量
            FBI WARING :
                短期准确率公式同冀北 冀南风光项目
        '''
        df_shanxi = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_shanxi['time'] = self.date_time
        df_shanxi['power_real'] = self.power_real
        df_shanxi['power_forecast'] = self.power_forecast

        dfs_time = df_shanxi['time']
        pr = df_shanxi['power_real']
        pf = df_shanxi['power_forecast']
        ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
        df_hour = dfs_time.str[11:16]  # pandas series
        ymd_new = []
        acc_new = []
        pen_new = []
        ae_new = []
        ae_pen_new = []

        grouped = pr.groupby(ymd)
        for key, group in grouped:
            ymd_new.append(key)
            pr_temp = pr.iloc[group.index].values
            pf_temp = pf.iloc[group.index].values
            hour_temp = df_hour.iloc[group.index].values  # 返回字符
            pr_clean = pr_temp[numpy.where(pr_temp > -99)]  # 实际功率为-99的剔除后进行计算
            pr_clean = numpy.where(pr_clean < 0, 0, pr_clean)
            pf_clean = pf_temp[numpy.where(pr_temp > -99)]
            hour_temp_clean = hour_temp[numpy.where(pr_temp > -99)]
            # 提取每天峰谷时段
            mask = (hour_temp_clean >= '11:00') & (hour_temp_clean <= '15:00')
            pr_peak_valley = pr_clean[mask]
            pf_peak_valley = pf_clean[mask]
            # 仅debug使用此行 hour_peak_valley = hour_temp_clean[mask]
            # 小于0.1倍装机的实际功率不参与考核，需要剔除
            pr_peak_valley_clean = pr_peak_valley[numpy.where(pr_peak_valley >= self.capacity*0.1)]
            pf_peak_valley_clean = pf_peak_valley[numpy.where(pr_peak_valley >= self.capacity*0.1)]
            # 仅debug使用此行 hour_peak_valley_clean = hour_peak_valley[numpy.where(pr_peak_valley >= self.capacity*0.1)]
            # 计算最大绝对值误差率
            if len(pr_peak_valley_clean) == 0:
                ae = 0
                ae_new.append(ae)
                ae_penalty = 0
                ae_pen_new.append(ae_penalty)
            elif len(pr_peak_valley_clean) > 0:
                ae = numpy.max((abs(pr_peak_valley_clean - pf_peak_valley_clean)/pr_peak_valley_clean))
                ae_new.append(ae)
                # 计算最大绝对值误差率考核电量
                if ae <= 0.15:
                    ae_penalty = 0.0
                    ae_pen_new.append(ae_penalty)
                elif ae > 0.15:
                    ae_penalty = (ae - 0.15) * self.capacity
                    ae_pen_new.append(ae_penalty)
            bias = abs(pr_clean - pf_clean)
            temp_0 = sum(bias ** 3)
            temp_1 = sum(bias)
            if len(pr_clean) == 0:
                temp = -0.99
                acc_new.append(temp)
            elif temp_1 == 0:
                temp = 1
                acc_new.append(temp)
            else:
                temp = 1 - numpy.sqrt(temp_0 / temp_1) / float(self.capacity)
                acc_new.append(temp)

            if temp == -0.99:
                temp_pen = -99
            elif temp < 0.85:  # 河北要求短期准确率高于0.85
                temp_pen = (0.85 - temp) * self.capacity * 0.4
            else:
                temp_pen = 0
            pen_new.append(temp_pen)

        df_penalty = pandas.DataFrame({'date': ymd_new, 'day_acc': acc_new, 'day_pen_mwh': pen_new, 'max_ae': ae_new, 'max_ae_pen_mwh': ae_pen_new})

        return df_penalty

    def calculate_xibei_wind_2022(self):
        '''

        2021年12月22日西北能监局发布修订完善西北区域两个细则
        适用风 风电预测曲线最大误差不超过25%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为：11:00-17:00
        新疆用  电高峰时段为：07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        df_xibei = df_xibei[df_xibei['power_real'] >= 0]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.25  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 特殊条件下
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real > cap * 0.03))
            n_index2 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real <= cap * 0.03))
            n_index3 = numpy.where(
                numpy.logical_and(power_forecast > cap * 0.03, power_real == 0))
            n_index4 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real == 0))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 满足特殊条件
            error_deviation = numpy.where(power_forecast > 0, (power_real - power_forecast) / power_forecast, 0)
            error_deviation[n_index1[0]] = 1
            error_deviation[n_index2[0]] = 0
            error_deviation[n_index3[0]] = 1
            error_deviation[n_index4[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pf| ==> |pr-pf| = TSD*pf
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_forecast / 40 * TSD,
                0)
            # 2022西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '10:00' <= row.hour <= '16:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 新能源用电高峰时段
                elif '06:00' <= row.hour <= '09:00' or '17:00' <= row.hour <= '22:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xibei_wind_2023(self):
        '''

        2023年11月08日西北能监局关于印发西北区域两个细则 附件1并网运行管理实施细则 

        适用风 风电预测曲线最大误差不超过25%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为: 11:00-17:00
        新疆用  电高峰时段为: 07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        # 实际功率在[-5,cap] 都纳入计算
        df_xibei = df_xibei[df_xibei['power_real'] >= -5]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.25  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 当实际功率和预测功率均在装机容量的3%以内 不予考核
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real <= cap * 0.03))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 分母必须是abs(pr) 由于power_real存在[-3MW,0]的情况，故此时的E偏差为负值
            error_deviation = numpy.where(power_real > -5, (power_real - power_forecast) / abs(power_real), 0)
            error_deviation[n_index1[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pr| ==> |pr-pf| = TSD*pr
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_real / 40 * TSD,
                0)
            # 2023西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '10:00' <= row.hour <= '16:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.1
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 用电高峰时段
                elif '06:00' <= row.hour <= '09:00' or '17:00' <= row.hour <= '22:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.15
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xinjiang_wind_2023(self):
        '''

        2023年11月08日西北能监局关于印发西北区域两个细则 附件1并网运行管理实施细则 

        适用风 风电预测曲线最大误差不超过25%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为: 11:00-17:00
        新疆用  电高峰时段为: 07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        # 实际功率在[-5,cap] 都纳入计算
        df_xibei = df_xibei[df_xibei['power_real'] >= -5]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.25  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 当实际功率和预测功率均在装机容量的3%以内 不予考核
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real <= cap * 0.03))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 分母必须是abs(pr) 由于power_real存在[-3MW,0]的情况，故此时的E偏差为负值
            error_deviation = numpy.where(power_real > -5, (power_real - power_forecast) / abs(power_real), 0)
            error_deviation[n_index1[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pr| ==> |pr-pf| = TSD*pr
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_real / 40 * TSD,
                0)
            # 2023西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '11:00' <= row.hour <= '17:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.1
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 用电高峰时段
                elif '07:00' <= row.hour <= '10:00' or '18:00' <= row.hour <= '23:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.15
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xibei_solar_2023(self):
        '''

        2023年11月08日西北能监局关于印发西北区域两个细则 附件1并网运行管理实施细则 
        适用光伏预测曲线最大误差不超过20%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为:11:00-17:00
        新疆用  电高峰时段为:07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        # 实际功率在[-5,cap] 都纳入计算
        df_xibei = df_xibei[df_xibei['power_real'] >= -5]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.2  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 当实际功率和预测功率均在装机容量的3%以内 不予考核
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real <= cap * 0.03))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 分母必须是abs(pr) 由于power_real存在[-3MW,0]的情况，故此时的E偏差为负值
            error_deviation = numpy.where(power_real > -5, (power_real - power_forecast) / abs(power_real), 0)
            error_deviation[n_index1[0]] = 0
            numpy.seterr(divide='ignore', invalid='ignore')
            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pr| ==> |pr-pf| = TSD*pr
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_real / 40 * TSD,
                0)
            # 2023西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '10:00' <= row.hour <= '16:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.1
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 用电高峰时段
                elif '06:00' <= row.hour <= '09:00' or '17:00' <= row.hour <= '22:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.15
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0    
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xinjiang_solar_2023(self):
        '''

        2023年11月08日西北能监局关于印发西北区域两个细则 附件1并网运行管理实施细则 
        适用光伏预测曲线最大误差不超过20%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为:11:00-17:00
        新疆用  电高峰时段为:07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        # 实际功率在[-5,cap] 都纳入计算
        df_xibei = df_xibei[df_xibei['power_real'] >= -5]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.2  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 当实际功率和预测功率均在装机容量的3%以内 不予考核
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real <= cap * 0.03))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 分母必须是abs(pr) 由于power_real存在[-3MW,0]的情况，故此时的E偏差为负值
            error_deviation = numpy.where(power_real > -5, (power_real - power_forecast) / abs(power_real), 0)
            error_deviation[n_index1[0]] = 0
            numpy.seterr(divide='ignore', invalid='ignore')
            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pr| ==> |pr-pf| = TSD*pr
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_real / 40 * TSD,
                0)
            # 2023西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '11:00' <= row.hour <= '17:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.1
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 用电高峰时段
                elif '07:00' <= row.hour <= '10:00' or '18:00' <= row.hour <= '23:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.15
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0    
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.05
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xibei_solar_2022(self):
        '''

        2021年12月22日西北能监局发布修订完善西北区域两个细则
        适用光伏预测曲线最大误差不超过20%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为：11:00-17:00
        新疆用  电高峰时段为：07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        df_xibei = df_xibei[df_xibei['power_real'] >= 0]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.2  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 特殊条件下
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real > cap * 0.03))
            n_index2 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real <= cap * 0.03))
            n_index3 = numpy.where(
                numpy.logical_and(power_forecast > cap * 0.03, power_real == 0))
            n_index4 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real == 0))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 满足特殊条件
            error_deviation = numpy.where(power_forecast > 0, (power_real - power_forecast) / power_forecast, 0)
            error_deviation[n_index1[0]] = 1
            error_deviation[n_index2[0]] = 0
            error_deviation[n_index3[0]] = 1
            error_deviation[n_index4[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pf| ==> |pr-pf| = TSD*pf
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_forecast / 40 * TSD,
                0)
            # 2022西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '10:00' <= row.hour <= '16:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 新能源用电高峰时段
                elif '06:00' <= row.hour <= '09:00' or '17:00' <= row.hour <= '22:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xinjiang_wind_2022(self):
        '''

        2021年12月22日西北能监局发布修订完善西北区域两个细则
        适用风 风电预测曲线最大误差不超过25%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为：11:00-17:00
        新疆用  电高峰时段为：07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        df_xibei = df_xibei[df_xibei['power_real'] >= 0]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.25  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 特殊条件下
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real > cap * 0.03))
            n_index2 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real <= cap * 0.03))
            n_index3 = numpy.where(
                numpy.logical_and(power_forecast > cap * 0.03, power_real == 0))
            n_index4 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real == 0))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 满足特殊条件
            error_deviation = numpy.where(power_forecast > 0, (power_real - power_forecast) / power_forecast, 0)
            error_deviation[n_index1[0]] = 1
            error_deviation[n_index2[0]] = 0
            error_deviation[n_index3[0]] = 1
            error_deviation[n_index4[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pf| ==> |pr-pf| = TSD*pf
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_forecast / 40 * TSD,
                0)
            # 2022西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '11:00' <= row.hour <= '17:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 新能源用电高峰时段
                elif '07:00' <= row.hour <= '10:00' or '18:00' <= row.hour <= '23:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties


    def calculate_xinjiang_solar_2022(self):
        '''

        2021年12月22日西北能监局发布修订完善西北区域两个细则
        适用光伏预测曲线最大误差不超过20%
        西北（除新疆外）新能源大发时段为 10:00-16:00
        西北（除新疆外）用  电高峰时段为 06:00-09:00  17:00-22:00

        新疆新能源大发时段为: 11:00-17:00
        新疆用  电高峰时段为: 07:00-10:00  18:00-23:00

        返回每日短期偏差积分电量
        FBI WARING
        '''
        df_xibei = pandas.DataFrame([], columns=['time', 'power_real', 'power_forecast'])
        df_xibei['time'] = self.date_time
        df_xibei['power_real'] = self.power_real
        df_xibei['power_forecast'] = self.power_forecast
        df_xibei = df_xibei[df_xibei['power_real'] >= 0]
        df_xibei = df_xibei[df_xibei['power_forecast'] >= 0]
        series_time = df_xibei['time']
        df_xibei['hour'] = series_time.str[11:16]
        if len(df_xibei) > 0:
            # 取列
            dfs_time = df_xibei['time']
            power_real = df_xibei['power_real']
            power_forecast = df_xibei['power_forecast']
            ymd = dfs_time.str[0:10]  # 选取 yyyy-mm-dd
            df_hour = dfs_time.str[11:16]  # pandas series
            cap = self.capacity
            TSD = 0.2  # 风电日预测曲线最大误差0.25 ; 光伏日预测曲线最大误差0.2
            # 特殊条件下
            n_index1 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real > cap * 0.03))
            n_index2 = numpy.where(
                numpy.logical_and(power_forecast == 0, power_real <= cap * 0.03))
            n_index3 = numpy.where(
                numpy.logical_and(power_forecast > cap * 0.03, power_real == 0))
            n_index4 = numpy.where(
                numpy.logical_and(power_forecast <= cap * 0.03, power_real == 0))
            numpy.seterr(divide='ignore', invalid='ignore')
            # 满足特殊条件
            error_deviation = numpy.where(power_forecast > 0, (power_real - power_forecast) / power_forecast, 0)
            error_deviation[n_index1[0]] = 1
            error_deviation[n_index2[0]] = 0
            error_deviation[n_index3[0]] = 1
            error_deviation[n_index4[0]] = 0

            # 偏差积分电量 计算时考虑了允许偏差25%，偏差变成26%就考核1% ；参考 TSD = |(pr-pf)/pf| ==> |pr-pf| = TSD*pf
            power_deviation = numpy.where(
                abs(error_deviation) > TSD,
                abs(power_real - power_forecast) / 40 - power_forecast / 40 * TSD,
                0)
            # 2022西北新细则要求，新能源大发时段风电的偏差大于25%时 or 用电高峰时段的偏差时
            df_xibei['error_deviation'] = error_deviation
            df_xibei['power_deviation'] = power_deviation
            df_xibei['score_deviation'] = power_deviation
            for index, row in df_xibei.iterrows():
                # 新能源大发时段
                if '11:00' <= row.hour <= '17:00':
                    if row.error_deviation > TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                    elif row.error_deviation < -TSD :
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0
                # 新能源用电高峰时段
                elif '07:00' <= row.hour <= '10:00' or '18:00' <= row.hour <= '23:00' :
                    if row.error_deviation > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    elif row.error_deviation < -TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation*0.4
                else:
                    if abs(row.error_deviation) > TSD:
                        df_xibei.at[index, 'score_deviation'] = row.power_deviation * 0.2
                    else:
                        df_xibei.at[index, 'score_deviation'] = 0

        score_deviation = df_xibei['score_deviation']
        power_deviation = df_xibei['power_deviation']
        # date_month = pandas.Series(list(map(time2split_month, date_time)))
        # date_day = pandas.Series(list(map(time2split_day, date_time)))
        date_month = df_xibei['time'].str[0:7]
        date_day = df_xibei['time'].str[0:10]
        deviation_score = score_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_day).sum()  # 偏差考核分数计算
        ym_list = []
        ymd_list = []
        for name, group in score_deviation.groupby(date_day):
            bd = datetime.datetime.strptime(name, '%Y-%m-%d')
            yy_mm_dd = bd.strftime('%Y-%m-%d')
            ymd_list.append(yy_mm_dd)
        day_penalties = pandas.DataFrame(
            numpy.c_[ymd_list, deviation_power, deviation_score],
            columns=['date', 'Deviation_energy', 'Deviation_score'])
        deviation_score = score_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        deviation_power = power_deviation.groupby(date_month).sum()  # 偏差考核分数计算
        ym_list = []
        for name, group in score_deviation.groupby(date_month):
            bd = datetime.datetime.strptime(name, '%Y-%m')
            yy_mm = bd.strftime('%Y-%m')
            ym_list.append(yy_mm)
        month_penalties = pandas.DataFrame(
            numpy.c_[ym_list, deviation_power, deviation_score],
            columns=['month', 'Deviation_energy', 'Deviation_score'])

        return day_penalties, month_penalties
