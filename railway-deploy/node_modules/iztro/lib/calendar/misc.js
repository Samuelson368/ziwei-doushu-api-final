"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getZodiac = exports.getSign = exports.lunarDateToStr = exports.lunarDayToStr = exports.lunarMonthToStr = exports.lunarYearToStr = exports.getTerm = void 0;
var data_1 = require("../data");
var i18n_1 = require("../i18n");
var convertor_1 = require("./convertor");
var rules_1 = require("./rules");
/**
 * 传入公历年获得该年第termNo个节气的公历节气日
 *
 * @param year 公历年(1900-2100)；n二十四节气中的第几个节气(1~24)；从n=1(小寒)算起
 * @param termNo 节气序号【1～24】
 * @return 节气日期
 * @example
 * termDay = getTerm(1987, 3); // termDay=4; 即1987年2月4日立春
 */
var getTerm = function (year, termNo) {
    if (year < 1900 || year > 2100) {
        throw new Error('Year should be greater or equal then 1900.');
    }
    if (termNo < 1 || termNo > 24) {
        throw new Error('termNo should be between 1 and 24.');
    }
    var _table = rules_1.TERM_INFO[year - 1900];
    var _info = [];
    for (var i = 0; i < 30; i += 5) {
        _info.push(parseInt('0x' + _table.substring(i, i + 5), 16).toString());
    }
    var _calday = [];
    _info.forEach(function (item) {
        _calday.push(item.substring(0, 1));
        _calday.push(item.substring(1, 3));
        _calday.push(item.substring(3, 4));
        _calday.push(item.substring(4, 6));
    });
    return parseInt(_calday[termNo - 1], 10);
};
exports.getTerm = getTerm;
/**
 * 将数字年份转化为中文字符串
 *
 * @param lunarYear 农历年份数字
 * @returns 农历年份字符串
 * @example
 * str = lunarYearToStr(1986); // str = '一九八六'
 */
var lunarYearToStr = function (lunarYear) {
    var y = lunarYear.toString();
    var char = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
    var result = '';
    for (var i = 0; i < y.length; i++) {
        result = result + char[+y.charAt(i)];
    }
    return result;
};
exports.lunarYearToStr = lunarYearToStr;
/**
 * 将数字月份转化为中文字符串
 *
 * @param lunarMonth 农历月份数字
 * @returns 农历月份字符串
 * @example
 * str = lunarMonthToStr(1); // str = '正月'
 */
var lunarMonthToStr = function (lunarMonth) {
    if (lunarMonth > 12 || lunarMonth < 1) {
        throw new Error('lunarMonth should be between 1 and 12.');
    }
    return "".concat(rules_1.LUNAR_MONTH_NAME[lunarMonth], "\u6708");
};
exports.lunarMonthToStr = lunarMonthToStr;
/**
 * 将数字日转化为中文字符串
 *
 * @param lunarDay 农历日数字
 * @returns 农历日字符串
 * @example
 * str = lunarDayToStr(7); // str = '初七'
 */
var lunarDayToStr = function (lunarDay) {
    var result = '';
    switch (lunarDay) {
        case 10:
            result = '初十';
            break;
        case 20:
            result = '二十';
            break;
        case 30:
            result = '三十';
            break;
        default:
            result = "".concat(rules_1.LUNAR_DAY_NAME[Math.floor(lunarDay / 10)]).concat(rules_1.NUM_TO_CHAR[lunarDay % 10]);
    }
    return result;
};
exports.lunarDayToStr = lunarDayToStr;
/**
 * 将 YYYY-MM-DD 格式的农历日期转化为中文字符串
 *
 * @param lunarDateStr 农历日期字符串 YYYY-MM-DD
 * @param isLeap 是否闰月
 * @returns 农历日期的中文字符串
 */
var lunarDateToStr = function (lunarDateStr, isLeap) {
    var _a = lunarDateStr.split('-').map(function (item) { return +item; }), year = _a[0], month = _a[1], day = _a[2];
    return "".concat((0, exports.lunarYearToStr)(year), "\u5E74").concat(isLeap ? '(闰)' : '').concat((0, exports.lunarMonthToStr)(month)).concat((0, exports.lunarDayToStr)(day));
};
exports.lunarDateToStr = lunarDateToStr;
/**
 * 获取星座
 *
 * @param  solarDateStr [description]
 * @return 星座
 */
var getSign = function (solarDateStr) {
    var _a = (0, convertor_1.normalizeSolarDateStr)(solarDateStr), month = _a[1], day = _a[2];
    var s = [
        'capricorn',
        'aquarius',
        'pisces',
        'aries',
        'taurus',
        'gemini',
        'cancer',
        'leo',
        'virgo',
        'libra',
        'scorpio',
        'sagittarius',
        'capricorn',
    ];
    var arr = [20, 19, 21, 21, 21, 22, 23, 23, 23, 23, 22, 22];
    var idx = Math.floor((month * 2 - (day < arr[month - 1] ? 2 : 0)) / 2);
    return (0, i18n_1.t)(s[idx]);
};
exports.getSign = getSign;
/**
 * 通过年支获取生肖
 *
 * @param earthlyBranchOfYear 年支
 * @example
 * const zodiac = calendar.getZodiac("卯") ;// zodiac='兔'
 */
var getZodiac = function (earthlyBranchOfYear) {
    var earthlyBranch = (0, i18n_1.kot)(earthlyBranchOfYear, 'Earthly');
    return (0, i18n_1.t)(data_1.ZODIAC[data_1.EARTHLY_BRANCHES.indexOf(earthlyBranch)]);
};
exports.getZodiac = getZodiac;
