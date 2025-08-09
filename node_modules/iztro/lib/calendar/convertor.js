"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.lunar2solar = exports.solar2lunar = exports.normalizeSolarDateStr = exports.normalizeLunarDateStr = void 0;
var dayjs_1 = __importDefault(require("dayjs"));
var days_1 = require("./days");
var leap_1 = require("./leap");
var misc_1 = require("./misc");
/**
 * 将农历日期字符串拆分成年，月，日
 *
 * @param dateStr 农历日期字符串 YYYY-MM-DD
 * @returns [年, 月, 日]
 * @example
 * normalizeLunarDateStr('2023-07-31'); // [2023, 7, 31]
 */
var normalizeLunarDateStr = function (dateStr) { return dateStr.split('-').map(function (item) { return +item.trim(); }); };
exports.normalizeLunarDateStr = normalizeLunarDateStr;
/**
 * 将公历日期字符串拆分成年，月，日
 *
 * @param dateStr 公历日期
 * @returns [年, 月, 日]
 * @example
 * normalizeSolarDateStr('2023-07-31'); // [2023, 7, 31]
 */
var normalizeSolarDateStr = function (dateStr) {
    var date = (0, dayjs_1.default)(dateStr);
    if (!date.isValid()) {
        throw new Error('invalid date.');
    }
    return [date.year(), date.month() + 1, date.date()];
};
exports.normalizeSolarDateStr = normalizeSolarDateStr;
/**
 * 公历转农历，年份需要在【1900~2100】之间，并且日期必须在1900-1-31之后
 *
 * @param dateStr 公历日期 YYYY-MM-DD格式的字符串或者Date对象
 * @returns LunarDate
 */
var solar2lunar = function (dateStr) {
    var _a = (0, exports.normalizeSolarDateStr)(dateStr), year = _a[0], month = _a[1], day = _a[2];
    // 参数区间1900.1.31~2100.12.31
    // 年份限定、上限
    if (year < 1900 || year > 2100) {
        throw new Error('year should be between 1900 and 2100.');
    }
    // 公历传参最下限 1900-01-31
    if (year === 1900 && month === 1 && day < 31) {
        throw new Error('date must be after 1900-1-31.');
    }
    var utcDate = Date.UTC(year, month - 1, day); // 获取当前日期UTC值
    var utcFloor = Date.UTC(1900, 0, 31); // 获取1900-1-31日的UTC值
    var lunarYear; // 农历年份
    var totalDayOfYear = 0;
    var offset = (utcDate - utcFloor) / 86400000; // 将差值转化为天
    for (lunarYear = 1900; lunarYear < 2101 && offset > 0; lunarYear++) {
        // 从1900年往2100年循环，将offset减去每一年的天数，当offset小于等于0的时候
        // 结束循环，当前的索引即是农历年份
        totalDayOfYear = (0, days_1.getTotalDaysOfLunarYear)(lunarYear);
        offset -= totalDayOfYear;
    }
    if (offset < 0) {
        // 当offset小于0了，需要将农历年份减去1
        offset += totalDayOfYear;
        lunarYear--;
    }
    var leapMonth = (0, leap_1.getLeapMonth)(lunarYear); // 获取农历年闰月，如果该年没有闰月返回0
    var totalDayOfMonth = 0;
    var lunarMonth; // 农历月份
    var leapFixed = false;
    for (lunarMonth = 1; lunarMonth < 13 && offset > 0; lunarMonth++) {
        if (leapMonth > 0 && lunarMonth === leapMonth + 1 && leapFixed === false) {
            // 闰月
            --lunarMonth;
            leapFixed = true;
            totalDayOfMonth = (0, leap_1.getLeapDays)(lunarYear); // 计算农历闰月天数
        }
        else {
            // 非闰月
            totalDayOfMonth = (0, days_1.getTotalDaysOfLunarMonth)(lunarYear, lunarMonth); // 计算农历普通月天数
        }
        // 解除闰月;
        if (leapFixed && lunarMonth === leapMonth + 1) {
            leapFixed = false;
        }
        offset -= totalDayOfMonth;
    }
    // 修复闰月导致数组下标重叠
    if (offset === 0 && leapMonth > 0 && lunarMonth === leapMonth + 1) {
        if (leapFixed) {
            leapFixed = false;
        }
        else {
            leapFixed = true;
            --lunarMonth;
        }
    }
    if (offset < 0) {
        offset += totalDayOfMonth;
        --lunarMonth;
    }
    var lunarDay = offset + 1;
    return {
        lunarYear: lunarYear,
        lunarMonth: lunarMonth,
        lunarDay: lunarDay,
        isLeap: leapFixed,
        toString: function (toCnStr) {
            if (toCnStr) {
                return (0, misc_1.lunarDateToStr)("".concat(lunarYear, "-").concat(lunarMonth, "-").concat(lunarDay), leapFixed);
            }
            return "".concat(lunarYear, "-").concat(lunarMonth, "-").concat(lunarDay);
        },
    };
};
exports.solar2lunar = solar2lunar;
/**
 *
 * @param dateStr 农历日期 YYYY-MM-DD
 * @param isLeapMonth 是否闰月，若该月不是闰月，会忽略该参数
 * @returns SolarDate
 */
var lunar2solar = function (dateStr, isLeapMonth) {
    var _a = (0, exports.normalizeLunarDateStr)(dateStr), year = _a[0], month = _a[1], day = _a[2];
    var leapMonth = (0, leap_1.getLeapMonth)(year);
    if (isLeapMonth && leapMonth !== month) {
        // 该月不是闰月但传入了闰月标志，则讲标志设为false
        isLeapMonth = false;
    }
    var totalLeapDays = (0, leap_1.getLeapDays)(year);
    var totalDaysOfTheMonth = (0, days_1.getTotalDaysOfLunarMonth)(year, month);
    // 获取当月总天数
    var totalDays = isLeapMonth ? totalLeapDays : totalDaysOfTheMonth;
    if (year < 1900 || year > 2100 || day > totalDays) {
        // 日期不合法
        throw new Error('invalid date.');
    }
    // 农历日期时间偏移量
    var offset = 0;
    // 将今年以前的年份时间偏移量加入offset
    for (var i = 1900; i < year; i++) {
        offset += (0, days_1.getTotalDaysOfLunarYear)(i);
    }
    if (leapMonth < month && leapMonth > 0) {
        // 若该月前面有闰月，则需要将闰月天数加入偏移量
        offset += totalLeapDays;
    }
    // 将今年的当月以前的时间偏移量加入offset
    for (var i = 1; i < month; i++) {
        offset += (0, days_1.getTotalDaysOfLunarMonth)(year, i);
    }
    // 转换闰月农历 需补充该年闰月的前一个月的时差
    if (isLeapMonth) {
        offset += totalDaysOfTheMonth;
    }
    // 1900年农历正月一日的公历时间为1900年1月30日0时0分0秒(该时间也是本农历的最开始起始点)
    var stmap = Date.UTC(1900, 1, 30, 0, 0, 0);
    var solarDate = new Date((offset + day - 31) * 86400000 + stmap);
    var solarYear = solarDate.getUTCFullYear();
    var solarMonth = solarDate.getUTCMonth() + 1;
    var solarDay = solarDate.getUTCDate();
    return {
        solarYear: solarYear,
        solarMonth: solarMonth,
        solarDay: solarDay,
        toString: function () {
            return "".concat(solarYear, "-").concat(solarMonth, "-").concat(solarDay);
        },
    };
};
exports.lunar2solar = lunar2solar;
