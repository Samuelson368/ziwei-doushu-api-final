"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getHeavenlyStemAndEarthlyBranchBySolarDate = exports.getHeavenlyStemAndEarthlyBranchByLunarDate = exports.heavenlyStemAndEarthlyBranchOfTime = exports.heavenlyStemAndEarthlyBranchOfDay = exports.heavenlyStemAndEarthlyBranchOfMonth = exports.heavenlyStemAndEarthlyBranchOfYear = void 0;
var dayjs_1 = __importDefault(require("dayjs"));
var data_1 = require("../data");
var i18n_1 = require("../i18n");
var utils_1 = require("../utils");
var convertor_1 = require("./convertor");
var misc_1 = require("./misc");
/**
 * 传入offset偏移量返回干支
 *
 * @param offset 相对甲子的偏移量，单位为天
 * @return [干, 支]
 */
var heavenlyStemAndEarthlyBranchFromOffset = function (offset) {
    return [(0, i18n_1.t)(data_1.HEAVENLY_STEMS[offset % 10]), (0, i18n_1.t)(data_1.EARTHLY_BRANCHES[offset % 12])];
};
/**
 * 农历年份计算年干支
 *
 * @param  year 农历年的年份数
 * @return [干, 支]
 */
var heavenlyStemAndEarthlyBranchOfYear = function (year) {
    var heavenStemKey = (year - 3) % 10;
    var earthlyBranchKey = (year - 3) % 12;
    if (heavenStemKey === 0)
        heavenStemKey = 10; // 如果余数为0则为最后一个天干
    if (earthlyBranchKey === 0)
        earthlyBranchKey = 12; // 如果余数为0则为最后一个地支
    return [(0, i18n_1.t)(data_1.HEAVENLY_STEMS[heavenStemKey - 1]), (0, i18n_1.t)(data_1.EARTHLY_BRANCHES[earthlyBranchKey - 1])];
};
exports.heavenlyStemAndEarthlyBranchOfYear = heavenlyStemAndEarthlyBranchOfYear;
/**
 * 通过公历日期计算月干支
 *
 * @param date 公历日期
 * @returns [干, 支]
 */
var heavenlyStemAndEarthlyBranchOfMonth = function (date) {
    var _a = (0, convertor_1.normalizeSolarDateStr)(date), year = _a[0], month = _a[1], day = _a[2];
    // 当月的第一个节气
    // 返回当月「节」为几日开始
    var firstNode = (0, misc_1.getTerm)(year, month * 2 - 1);
    var offset = (year - 1900) * 12 + month + 11;
    if (day >= firstNode) {
        return heavenlyStemAndEarthlyBranchFromOffset(offset + 1);
    }
    return heavenlyStemAndEarthlyBranchFromOffset(offset);
};
exports.heavenlyStemAndEarthlyBranchOfMonth = heavenlyStemAndEarthlyBranchOfMonth;
/**
 * 获取公历日期计算日干支
 *
 * @param date 公历日期
 * @param timeIndex 时辰索引，主要是为了修复晚子时需要加一天的问题
 * @returns [干, 支]
 */
var heavenlyStemAndEarthlyBranchOfDay = function (date, timeIndex) {
    var _a = (0, convertor_1.normalizeSolarDateStr)(date), year = _a[0], month = _a[1], day = _a[2];
    var dayFix = timeIndex === 12 ? 1 : 0; // 若时辰索引为12表示是晚子时，需要加一天
    var dayCyclical = Date.UTC(year, month - 1, 1, 0, 0, 0, 0) / 86400000 + 25567 + 10;
    return heavenlyStemAndEarthlyBranchFromOffset(dayCyclical + day + dayFix - 1);
};
exports.heavenlyStemAndEarthlyBranchOfDay = heavenlyStemAndEarthlyBranchOfDay;
/**
 * 通过当天的日天干获取第 `t` （0~11）个时辰的干支，需要通过五鼠遁来定时辰天干
 *
 * @param timeIndex 时辰序号（0~11），子时为0，亥时为11
 * @param heavenlyStemNameOfDay 当日天干
 * @returns [干, 支]
 */
var heavenlyStemAndEarthlyBranchOfTime = function (timeIndex, heavenlyStemNameOfDay) {
    var heavenlyStemOfDay = (0, i18n_1.kot)(heavenlyStemNameOfDay, 'Heavenly');
    var startHeavenlyStem = data_1.RAT_RULE[heavenlyStemOfDay];
    var heavenlyStem = data_1.HEAVENLY_STEMS[(0, utils_1.fixIndex)(data_1.HEAVENLY_STEMS.indexOf(startHeavenlyStem) + (0, utils_1.fixIndex)(timeIndex), 10)];
    var earthlyBranch = data_1.EARTHLY_BRANCHES[(0, utils_1.fixIndex)(timeIndex)];
    return [(0, i18n_1.t)(heavenlyStem), (0, i18n_1.t)(earthlyBranch)];
};
exports.heavenlyStemAndEarthlyBranchOfTime = heavenlyStemAndEarthlyBranchOfTime;
/**
 * 通过农历获取生辰干支
 *
 * @param dateStr 农历日期 YYYY-MM-DD
 * @param timeIndex 时辰索引【0～12】
 * @param isLeap 是否为闰月
 * @returns HeavenlyStemAndEarthlyBranchResult
 */
var getHeavenlyStemAndEarthlyBranchByLunarDate = function (dateStr, timeIndex, isLeap) {
    var lunarYear = (0, convertor_1.normalizeLunarDateStr)(dateStr)[0];
    var solar = (0, convertor_1.lunar2solar)(dateStr, isLeap);
    var solarDate = new Date((0, dayjs_1.default)(solar.toString()).format());
    var yearly = (0, exports.heavenlyStemAndEarthlyBranchOfYear)(lunarYear);
    var monthly = (0, exports.heavenlyStemAndEarthlyBranchOfMonth)(solarDate);
    var daily = (0, exports.heavenlyStemAndEarthlyBranchOfDay)(solarDate, timeIndex);
    var hourly = (0, exports.heavenlyStemAndEarthlyBranchOfTime)(timeIndex, daily[0]);
    return {
        yearly: yearly,
        monthly: monthly,
        daily: daily,
        hourly: hourly,
        toString: function () {
            if (yearly[0].length > 1) {
                return "".concat(yearly.join(' '), " - ").concat(monthly.join(' '), " - ").concat(daily.join(' '), " - ").concat(hourly.join(' '));
            }
            else {
                return "".concat(yearly.join(''), " ").concat(monthly.join(''), " ").concat(daily.join(''), " ").concat(hourly.join(''));
            }
        },
    };
};
exports.getHeavenlyStemAndEarthlyBranchByLunarDate = getHeavenlyStemAndEarthlyBranchByLunarDate;
/**
 * 将阳历转化为干支纪年
 *
 * @param dateStr 公历日期 YYYY-MM-DD
 * @param timeIndex 时辰索引【0～12】
 * @returns HeavenlyStemAndEarthlyBranchResult
 */
var getHeavenlyStemAndEarthlyBranchBySolarDate = function (dateStr, timeIndex) {
    var lunarDate = (0, convertor_1.solar2lunar)(dateStr);
    return (0, exports.getHeavenlyStemAndEarthlyBranchByLunarDate)(lunarDate.toString(), timeIndex, lunarDate.isLeap);
};
exports.getHeavenlyStemAndEarthlyBranchBySolarDate = getHeavenlyStemAndEarthlyBranchBySolarDate;
