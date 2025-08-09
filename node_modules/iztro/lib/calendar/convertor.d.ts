import { LunarDate, SolarDate } from '../data/types';
/**
 * 将农历日期字符串拆分成年，月，日
 *
 * @param dateStr 农历日期字符串 YYYY-MM-DD
 * @returns [年, 月, 日]
 * @example
 * normalizeLunarDateStr('2023-07-31'); // [2023, 7, 31]
 */
export declare const normalizeLunarDateStr: (dateStr: string) => number[];
/**
 * 将公历日期字符串拆分成年，月，日
 *
 * @param dateStr 公历日期
 * @returns [年, 月, 日]
 * @example
 * normalizeSolarDateStr('2023-07-31'); // [2023, 7, 31]
 */
export declare const normalizeSolarDateStr: (dateStr: string | Date) => number[];
/**
 * 公历转农历，年份需要在【1900~2100】之间，并且日期必须在1900-1-31之后
 *
 * @param dateStr 公历日期 YYYY-MM-DD格式的字符串或者Date对象
 * @returns LunarDate
 */
export declare const solar2lunar: (dateStr: string | Date) => LunarDate;
/**
 *
 * @param dateStr 农历日期 YYYY-MM-DD
 * @param isLeapMonth 是否闰月，若该月不是闰月，会忽略该参数
 * @returns SolarDate
 */
export declare const lunar2solar: (dateStr: string, isLeapMonth?: boolean) => SolarDate;
