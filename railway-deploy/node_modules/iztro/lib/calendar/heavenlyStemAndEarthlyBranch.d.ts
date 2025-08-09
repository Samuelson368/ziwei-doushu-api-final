import { HeavenlyStemAndEarthlyBranch, HeavenlyStemAndEarthlyBranchDate } from '../data/types';
import { HeavenlyStemName } from '../i18n';
/**
 * 农历年份计算年干支
 *
 * @param  year 农历年的年份数
 * @return [干, 支]
 */
export declare const heavenlyStemAndEarthlyBranchOfYear: (year: number) => HeavenlyStemAndEarthlyBranch;
/**
 * 通过公历日期计算月干支
 *
 * @param date 公历日期
 * @returns [干, 支]
 */
export declare const heavenlyStemAndEarthlyBranchOfMonth: (date: Date) => HeavenlyStemAndEarthlyBranch;
/**
 * 获取公历日期计算日干支
 *
 * @param date 公历日期
 * @param timeIndex 时辰索引，主要是为了修复晚子时需要加一天的问题
 * @returns [干, 支]
 */
export declare const heavenlyStemAndEarthlyBranchOfDay: (date: Date, timeIndex: number) => HeavenlyStemAndEarthlyBranch;
/**
 * 通过当天的日天干获取第 `t` （0~11）个时辰的干支，需要通过五鼠遁来定时辰天干
 *
 * @param timeIndex 时辰序号（0~11），子时为0，亥时为11
 * @param heavenlyStemNameOfDay 当日天干
 * @returns [干, 支]
 */
export declare const heavenlyStemAndEarthlyBranchOfTime: (timeIndex: number, heavenlyStemNameOfDay: HeavenlyStemName) => HeavenlyStemAndEarthlyBranch;
/**
 * 通过农历获取生辰干支
 *
 * @param dateStr 农历日期 YYYY-MM-DD
 * @param timeIndex 时辰索引【0～12】
 * @param isLeap 是否为闰月
 * @returns HeavenlyStemAndEarthlyBranchResult
 */
export declare const getHeavenlyStemAndEarthlyBranchByLunarDate: (dateStr: string, timeIndex: number, isLeap?: boolean) => HeavenlyStemAndEarthlyBranchDate;
/**
 * 将阳历转化为干支纪年
 *
 * @param dateStr 公历日期 YYYY-MM-DD
 * @param timeIndex 时辰索引【0～12】
 * @returns HeavenlyStemAndEarthlyBranchResult
 */
export declare const getHeavenlyStemAndEarthlyBranchBySolarDate: (dateStr: string | Date, timeIndex: number) => HeavenlyStemAndEarthlyBranchDate;
