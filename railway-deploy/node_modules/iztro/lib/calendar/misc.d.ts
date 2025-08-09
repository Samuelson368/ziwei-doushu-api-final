import { EarthlyBranchName } from '../i18n';
/**
 * 传入公历年获得该年第termNo个节气的公历节气日
 *
 * @param year 公历年(1900-2100)；n二十四节气中的第几个节气(1~24)；从n=1(小寒)算起
 * @param termNo 节气序号【1～24】
 * @return 节气日期
 * @example
 * termDay = getTerm(1987, 3); // termDay=4; 即1987年2月4日立春
 */
export declare const getTerm: (year: number, termNo: number) => number;
/**
 * 将数字年份转化为中文字符串
 *
 * @param lunarYear 农历年份数字
 * @returns 农历年份字符串
 * @example
 * str = lunarYearToStr(1986); // str = '一九八六'
 */
export declare const lunarYearToStr: (lunarYear: number) => string;
/**
 * 将数字月份转化为中文字符串
 *
 * @param lunarMonth 农历月份数字
 * @returns 农历月份字符串
 * @example
 * str = lunarMonthToStr(1); // str = '正月'
 */
export declare const lunarMonthToStr: (lunarMonth: number) => string;
/**
 * 将数字日转化为中文字符串
 *
 * @param lunarDay 农历日数字
 * @returns 农历日字符串
 * @example
 * str = lunarDayToStr(7); // str = '初七'
 */
export declare const lunarDayToStr: (lunarDay: number) => string;
/**
 * 将 YYYY-MM-DD 格式的农历日期转化为中文字符串
 *
 * @param lunarDateStr 农历日期字符串 YYYY-MM-DD
 * @param isLeap 是否闰月
 * @returns 农历日期的中文字符串
 */
export declare const lunarDateToStr: (lunarDateStr: string, isLeap: boolean) => string;
/**
 * 获取星座
 *
 * @param  solarDateStr [description]
 * @return 星座
 */
export declare const getSign: (solarDateStr: string) => string;
/**
 * 通过年支获取生肖
 *
 * @param earthlyBranchOfYear 年支
 * @example
 * const zodiac = calendar.getZodiac("卯") ;// zodiac='兔'
 */
export declare const getZodiac: (earthlyBranchOfYear: EarthlyBranchName) => string;
