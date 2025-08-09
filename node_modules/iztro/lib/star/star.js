"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getHoroscopeStar = exports.getYearly12 = exports.getJiangqian12StartIndex = exports.getBoShi12 = exports.getchangsheng12 = exports.getChangesheng12StartIndex = exports.getAdjectiveStar = exports.getMinorStar = exports.getMajorStar = exports.initStars = void 0;
var astro_1 = require("../astro");
var calendar_1 = require("../calendar");
var data_1 = require("../data");
var i18n_1 = require("../i18n");
var utils_1 = require("../utils");
var location_1 = require("./location");
var initStars = function () { return [[], [], [], [], [], [], [], [], [], [], [], []]; };
exports.initStars = initStars;
/**
 * 安主星，寅宫下标为0，若下标对应的数组为空数组则表示没有星耀
 *
 * 安紫微诸星诀
 * - 紫微逆去天机星，隔一太阳武曲辰，
 * - 连接天同空二宫，廉贞居处方是真。
 *
 * 安天府诸星诀
 * - 天府顺行有太阴，贪狼而后巨门临，
 * - 随来天相天梁继，七杀空三是破军。
 *
 * @param solarDateStr 公历日期 YYYY-MM-DD
 * @param timeIndex 时辰索引【0～12】
 * @param fixLeap 是否调整农历闰月（若该月不是闰月则不会生效）
 * @returns {Array<Star[]>} 从寅宫开始每一个宫的星耀
 */
var getMajorStar = function (solarDateStr, timeIndex, fixLeap) {
    var _a = (0, location_1.getStartIndex)(solarDateStr, timeIndex, fixLeap), ziweiIndex = _a.ziweiIndex, tianfuIndex = _a.tianfuIndex;
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, timeIndex).yearly;
    var stars = (0, exports.initStars)();
    var ziweiGroup = [
        'ziweiMaj',
        'tianjiMaj',
        '',
        'taiyangMaj',
        'wuquMaj',
        'tiantongMaj',
        '',
        '',
        'lianzhenMaj',
    ];
    var tianfuGroup = [
        'tianfuMaj',
        'taiyinMaj',
        'tanlangMaj',
        'jumenMaj',
        'tianxiangMaj',
        'tianliangMaj',
        'qishaMaj',
        '',
        '',
        '',
        'pojunMaj',
    ];
    ziweiGroup.forEach(function (s, i) {
        // 安紫微星系，起始宫逆时针安
        if (s !== '') {
            stars[(0, utils_1.fixIndex)(ziweiIndex - i)].push({
                name: (0, i18n_1.t)(s),
                type: 'major',
                scope: 'origin',
                brightness: (0, utils_1.getBrightness)((0, i18n_1.t)(s), (0, utils_1.fixIndex)(ziweiIndex - i)),
                mutagen: (0, utils_1.getMutagen)((0, i18n_1.t)(s), yearly[0]),
            });
        }
    });
    tianfuGroup.forEach(function (s, i) {
        if (s !== '') {
            stars[(0, utils_1.fixIndex)(tianfuIndex + i)].push({
                name: (0, i18n_1.t)(s),
                type: 'major',
                scope: 'origin',
                brightness: (0, utils_1.getBrightness)((0, i18n_1.t)(s), (0, utils_1.fixIndex)(tianfuIndex + i)),
                mutagen: (0, utils_1.getMutagen)((0, i18n_1.t)(s), yearly[0]),
            });
        }
    });
    return stars;
};
exports.getMajorStar = getMajorStar;
/**
 * 安14辅星，寅宫下标为0，若下标对应的数组为空数组则表示没有星耀
 *
 * @param solarDateStr 阳历日期字符串
 * @param timeIndex 时辰索引【0～12】
 * @param fixLeap 是否修复闰月，假如当月不是闰月则不生效
 * @returns 14辅星
 */
var getMinorStar = function (solarDateStr, timeIndex, fixLeap) {
    var stars = (0, exports.initStars)();
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, timeIndex).yearly;
    var monthIndex = (0, utils_1.fixLunarMonthIndex)(solarDateStr, timeIndex, fixLeap);
    // 此处获取到的是索引，下标是从0开始的，所以需要加1
    var _a = (0, location_1.getZuoYouIndex)(monthIndex + 1), zuoIndex = _a.zuoIndex, youIndex = _a.youIndex;
    var _b = (0, location_1.getChangQuIndex)(timeIndex), changIndex = _b.changIndex, quIndex = _b.quIndex;
    var _c = (0, location_1.getKuiYueIndex)(yearly[0]), kuiIndex = _c.kuiIndex, yueIndex = _c.yueIndex;
    var _d = (0, location_1.getHuoLingIndex)(yearly[1], timeIndex), huoIndex = _d.huoIndex, lingIndex = _d.lingIndex;
    var _e = (0, location_1.getKongJieIndex)(timeIndex), kongIndex = _e.kongIndex, jieIndex = _e.jieIndex;
    var _f = (0, location_1.getLuYangTuoMaIndex)(yearly[0], yearly[1]), luIndex = _f.luIndex, yangIndex = _f.yangIndex, tuoIndex = _f.tuoIndex, maIndex = _f.maIndex;
    stars[zuoIndex].push({
        name: (0, i18n_1.t)('zuofuMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('左辅', zuoIndex),
        mutagen: (0, utils_1.getMutagen)('左辅', yearly[0]),
    });
    stars[youIndex].push({
        name: (0, i18n_1.t)('youbiMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('右弼', youIndex),
        mutagen: (0, utils_1.getMutagen)('右弼', yearly[0]),
    });
    stars[changIndex].push({
        name: (0, i18n_1.t)('wenchangMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('文昌', changIndex),
        mutagen: (0, utils_1.getMutagen)('文昌', yearly[0]),
    });
    stars[quIndex].push({
        name: (0, i18n_1.t)('wenquMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('文曲', quIndex),
        mutagen: (0, utils_1.getMutagen)('文曲', yearly[0]),
    });
    stars[kuiIndex].push({
        name: (0, i18n_1.t)('tiankuiMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('天魁', kuiIndex),
    });
    stars[yueIndex].push({
        name: (0, i18n_1.t)('tianyueMin'),
        type: 'soft',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('天钺', yueIndex),
    });
    stars[luIndex].push({
        name: (0, i18n_1.t)('lucunMin'),
        type: 'lucun',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('禄存', luIndex),
    });
    stars[maIndex].push({
        name: (0, i18n_1.t)('tianmaMin'),
        type: 'tianma',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('天马', maIndex),
    });
    stars[kongIndex].push({
        name: (0, i18n_1.t)('dikongMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('地空', kongIndex),
    });
    stars[jieIndex].push({
        name: (0, i18n_1.t)('dijieMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('地劫', jieIndex),
    });
    stars[huoIndex].push({
        name: (0, i18n_1.t)('huoxingMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('火星', huoIndex),
    });
    stars[lingIndex].push({
        name: (0, i18n_1.t)('lingxingMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('铃星', lingIndex),
    });
    stars[yangIndex].push({
        name: (0, i18n_1.t)('qingyangMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('擎羊', yangIndex),
    });
    stars[tuoIndex].push({
        name: (0, i18n_1.t)('tuoluoMin'),
        type: 'tough',
        scope: 'origin',
        brightness: (0, utils_1.getBrightness)('陀罗', tuoIndex),
    });
    return stars;
};
exports.getMinorStar = getMinorStar;
/**
 * 安杂耀
 *
 * @param solarDateStr 阳历日期字符串
 * @param timeIndex 时辰索引【0～12】
 * @param fixLeap 是否修复闰月，假如当月不是闰月则不生效
 * @returns 38杂耀
 */
var getAdjectiveStar = function (solarDateStr, timeIndex, fixLeap) {
    var stars = (0, exports.initStars)();
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, timeIndex).yearly;
    var _a = (0, location_1.getYearlyStarIndex)(solarDateStr, timeIndex, fixLeap), xianchiIndex = _a.xianchiIndex, huagaiIndex = _a.huagaiIndex, guchenIndex = _a.guchenIndex, guasuIndex = _a.guasuIndex, tiancaiIndex = _a.tiancaiIndex, tianshouIndex = _a.tianshouIndex, tianchuIndex = _a.tianchuIndex, posuiIndex = _a.posuiIndex, feilianIndex = _a.feilianIndex, longchiIndex = _a.longchiIndex, fenggeIndex = _a.fenggeIndex, tiankuIndex = _a.tiankuIndex, tianxuIndex = _a.tianxuIndex, tianguanIndex = _a.tianguanIndex, tianfuIndex = _a.tianfuIndex, tiandeIndex = _a.tiandeIndex, yuedeIndex = _a.yuedeIndex, tiankongIndex = _a.tiankongIndex, jieluIndex = _a.jieluIndex, kongwangIndex = _a.kongwangIndex, xunkongIndex = _a.xunkongIndex, tianshangIndex = _a.tianshangIndex, tianshiIndex = _a.tianshiIndex;
    var _b = (0, location_1.getMonthlyStarIndex)(solarDateStr, timeIndex, fixLeap), yuejieIndex = _b.yuejieIndex, tianyaoIndex = _b.tianyaoIndex, tianxingIndex = _b.tianxingIndex, yinshaIndex = _b.yinshaIndex, tianyueIndex = _b.tianyueIndex, tianwuIndex = _b.tianwuIndex;
    var _c = (0, location_1.getDailyStarIndex)(solarDateStr, timeIndex), santaiIndex = _c.santaiIndex, bazuoIndex = _c.bazuoIndex, enguangIndex = _c.enguangIndex, tianguiIndex = _c.tianguiIndex;
    var _d = (0, location_1.getTimelyStarIndex)(timeIndex), taifuIndex = _d.taifuIndex, fenggaoIndex = _d.fenggaoIndex;
    var _e = (0, location_1.getLuanXiIndex)(yearly[1]), hongluanIndex = _e.hongluanIndex, tianxiIndex = _e.tianxiIndex;
    stars[hongluanIndex].push({ name: (0, i18n_1.t)('hongluan'), type: 'flower', scope: 'origin' });
    stars[tianxiIndex].push({ name: (0, i18n_1.t)('tianxi'), type: 'flower', scope: 'origin' });
    stars[tianyaoIndex].push({ name: (0, i18n_1.t)('tianyao'), type: 'flower', scope: 'origin' });
    stars[xianchiIndex].push({ name: (0, i18n_1.t)('xianchi'), type: 'flower', scope: 'origin' });
    stars[yuejieIndex].push({ name: (0, i18n_1.t)('jieshen'), type: 'helper', scope: 'origin' });
    stars[santaiIndex].push({ name: (0, i18n_1.t)('santai'), type: 'adjective', scope: 'origin' });
    stars[bazuoIndex].push({ name: (0, i18n_1.t)('bazuo'), type: 'adjective', scope: 'origin' });
    stars[enguangIndex].push({ name: (0, i18n_1.t)('engguang'), type: 'adjective', scope: 'origin' });
    stars[tianguiIndex].push({ name: (0, i18n_1.t)('tiangui'), type: 'adjective', scope: 'origin' });
    stars[longchiIndex].push({ name: (0, i18n_1.t)('longchi'), type: 'adjective', scope: 'origin' });
    stars[fenggeIndex].push({ name: (0, i18n_1.t)('fengge'), type: 'adjective', scope: 'origin' });
    stars[tiancaiIndex].push({ name: (0, i18n_1.t)('tiancai'), type: 'adjective', scope: 'origin' });
    stars[tianshouIndex].push({ name: (0, i18n_1.t)('tianshou'), type: 'adjective', scope: 'origin' });
    stars[taifuIndex].push({ name: (0, i18n_1.t)('taifu'), type: 'adjective', scope: 'origin' });
    stars[fenggaoIndex].push({ name: (0, i18n_1.t)('fenggao'), type: 'adjective', scope: 'origin' });
    stars[tianwuIndex].push({ name: (0, i18n_1.t)('tianwu'), type: 'adjective', scope: 'origin' });
    stars[huagaiIndex].push({ name: (0, i18n_1.t)('huagai'), type: 'adjective', scope: 'origin' });
    stars[tianguanIndex].push({ name: (0, i18n_1.t)('tianguan'), type: 'adjective', scope: 'origin' });
    stars[tianfuIndex].push({ name: (0, i18n_1.t)('tianfu'), type: 'adjective', scope: 'origin' });
    stars[tianchuIndex].push({ name: (0, i18n_1.t)('tianchu'), type: 'adjective', scope: 'origin' });
    stars[tianyueIndex].push({ name: (0, i18n_1.t)('tianyue'), type: 'adjective', scope: 'origin' });
    stars[tiandeIndex].push({ name: (0, i18n_1.t)('tiande'), type: 'adjective', scope: 'origin' });
    stars[yuedeIndex].push({ name: (0, i18n_1.t)('yuede'), type: 'adjective', scope: 'origin' });
    stars[tiankongIndex].push({ name: (0, i18n_1.t)('tiankong'), type: 'adjective', scope: 'origin' });
    stars[xunkongIndex].push({ name: (0, i18n_1.t)('xunkong'), type: 'adjective', scope: 'origin' });
    stars[jieluIndex].push({ name: (0, i18n_1.t)('jielu'), type: 'adjective', scope: 'origin' });
    stars[kongwangIndex].push({ name: (0, i18n_1.t)('kongwang'), type: 'adjective', scope: 'origin' });
    stars[guchenIndex].push({ name: (0, i18n_1.t)('guchen'), type: 'adjective', scope: 'origin' });
    stars[guasuIndex].push({ name: (0, i18n_1.t)('guasu'), type: 'adjective', scope: 'origin' });
    stars[feilianIndex].push({ name: (0, i18n_1.t)('feilian'), type: 'adjective', scope: 'origin' });
    stars[posuiIndex].push({ name: (0, i18n_1.t)('posui'), type: 'adjective', scope: 'origin' });
    stars[tianxingIndex].push({ name: (0, i18n_1.t)('tianxing'), type: 'adjective', scope: 'origin' });
    stars[yinshaIndex].push({ name: (0, i18n_1.t)('yinsha'), type: 'adjective', scope: 'origin' });
    stars[tiankuIndex].push({ name: (0, i18n_1.t)('tianku'), type: 'adjective', scope: 'origin' });
    stars[tianxuIndex].push({ name: (0, i18n_1.t)('tianxu'), type: 'adjective', scope: 'origin' });
    stars[tianshiIndex].push({ name: (0, i18n_1.t)('tianshi'), type: 'adjective', scope: 'origin' });
    stars[tianshangIndex].push({ name: (0, i18n_1.t)('tianshang'), type: 'adjective', scope: 'origin' });
    return stars;
};
exports.getAdjectiveStar = getAdjectiveStar;
/**
 * 获取长生12神开始的宫位索引
 *
 * - 水二局长生在申
 * - 木三局长生在亥
 * - 金四局长生在巳
 * - 土五局长生在申
 * - 火六局长生在寅，
 * @param fiveElementClassName 五行局
 * @returns 长生12神开始的索引
 */
var getChangesheng12StartIndex = function (fiveElementClassName) {
    var fiveElementClass = (0, i18n_1.kot)(fiveElementClassName);
    var startIdx = 0;
    switch (data_1.FiveElementsClass[fiveElementClass]) {
        case 2: {
            startIdx = (0, utils_1.fixEarthlyBranchIndex)('shen');
            break;
        }
        case 3: {
            startIdx = (0, utils_1.fixEarthlyBranchIndex)('hai');
            break;
        }
        case 4: {
            startIdx = (0, utils_1.fixEarthlyBranchIndex)('si');
            break;
        }
        case 5: {
            startIdx = (0, utils_1.fixEarthlyBranchIndex)('shen');
            break;
        }
        case 6: {
            startIdx = (0, utils_1.fixEarthlyBranchIndex)('yin');
            break;
        }
    }
    return startIdx;
};
exports.getChangesheng12StartIndex = getChangesheng12StartIndex;
/**
 * 长生12神。
 *
 * 阳男阴女顺行，阴男阳女逆行，安长生、沐浴、冠带、临官、帝旺、衰、病、死、墓、绝 、胎、养。
 *
 * @param solarDateStr 阳历日期字符串
 * @param timeIndex 时辰索引【0～12】
 * @param gender 性别【男｜女】
 * @param fixLeap 是否修复闰月，假如当月不是闰月则不生效
 * @returns 长生12神从寅宫开始的顺序
 */
var getchangsheng12 = function (solarDateStr, timeIndex, gender, fixLeap) {
    var changsheng12 = [];
    var genderKey = (0, i18n_1.kot)(gender);
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, 0).yearly;
    var earthlyBranchNameOfYear = yearly[1];
    var earthlyBranchOfYear = (0, i18n_1.kot)(earthlyBranchNameOfYear);
    // 获取命宫干支，需要通过命宫干支计算五行局
    var _a = (0, astro_1.getSoulAndBody)(solarDateStr, timeIndex, fixLeap), heavenlyStemOfSoul = _a.heavenlyStemOfSoul, earthlyBranchOfSoul = _a.earthlyBranchOfSoul;
    // 获取五行局，通过五行局获取起运年龄
    var fiveElementClass = (0, astro_1.getFiveElementsClass)(heavenlyStemOfSoul, earthlyBranchOfSoul);
    // 长生12神顺序
    var stars = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'];
    var startIdx = (0, exports.getChangesheng12StartIndex)(fiveElementClass);
    for (var i = 0; i < stars.length; i++) {
        var idx = 0;
        if (data_1.GENDER[genderKey] === data_1.earthlyBranches[earthlyBranchOfYear].yinYang) {
            idx = (0, utils_1.fixIndex)(i + startIdx);
        }
        else {
            idx = (0, utils_1.fixIndex)(startIdx - i);
        }
        changsheng12[idx] = (0, i18n_1.t)(stars[i]);
    }
    return changsheng12;
};
exports.getchangsheng12 = getchangsheng12;
/**
 * 博士12神。
 *
 * 从禄存起，阳男阴女顺行，阴男阳女逆行。安博士、力士、青龙、小耗、将军、奏书、飞廉、喜神、病符、大耗、伏兵、官府。
 *
 * @param solarDateStr 阳历日期字符串
 * @param gender 性别【男｜女】
 * @returns 博士12神从寅宫开始的顺序
 */
var getBoShi12 = function (solarDateStr, gender) {
    var genderKey = (0, i18n_1.kot)(gender);
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, 0).yearly;
    var heavenlyStemNameOfYear = yearly[0], earthlyBranchNameOfYear = yearly[1];
    var earthlyBranchOfYear = (0, i18n_1.kot)(earthlyBranchNameOfYear);
    // 博士12神的顺序
    var stars = [
        '博士',
        '力士',
        '青龙',
        '小耗',
        '将军',
        '奏书',
        '飞廉',
        '喜神',
        '病符',
        '大耗',
        '伏兵',
        '官府',
    ];
    var luIndex = (0, location_1.getLuYangTuoMaIndex)(heavenlyStemNameOfYear, earthlyBranchNameOfYear).luIndex;
    var boshi12 = [];
    for (var i = 0; i < stars.length; i++) {
        // 阳男阴女顺行，阴男阳女逆部
        var idx = (0, utils_1.fixIndex)(data_1.GENDER[genderKey] === data_1.earthlyBranches[earthlyBranchOfYear].yinYang ? luIndex + i : luIndex - i);
        boshi12[idx] = (0, i18n_1.t)(stars[i]);
    }
    return boshi12;
};
exports.getBoShi12 = getBoShi12;
/**
 * 安流年将前诸星（按流年地支起将星）
 * - 寅午戍年将星午，申子辰年子将星，
 * - 巳酉丑将酉上驻，亥卯未将卯上停。
 * - 攀鞍岁驿并息神，华盖劫煞灾煞轻，
 * - 天煞指背咸池续，月煞亡神次第行。
 *
 * @param earthlyBranchName 地支
 * @returns 将前诸星起始索引
 */
var getJiangqian12StartIndex = function (earthlyBranchName) {
    var jqStartIdx = -1;
    var earthlyBranchOfYear = (0, i18n_1.kot)(earthlyBranchName);
    if (['yinEarthly', 'wuEarthly', 'xuEarthly'].includes(earthlyBranchOfYear)) {
        jqStartIdx = (0, utils_1.fixEarthlyBranchIndex)('woo');
    }
    else if (['shenEarthly', 'ziEarthly', 'chenEarthly'].includes(earthlyBranchOfYear)) {
        jqStartIdx = (0, utils_1.fixEarthlyBranchIndex)('zi');
    }
    else if (['siEarthly', 'youEarthly', 'chouEarthly'].includes(earthlyBranchOfYear)) {
        jqStartIdx = (0, utils_1.fixEarthlyBranchIndex)('you');
    }
    else if (['haiEarthly', 'maoEarthly', 'weiEarthly'].includes(earthlyBranchOfYear)) {
        jqStartIdx = (0, utils_1.fixEarthlyBranchIndex)('mao');
    }
    return (0, utils_1.fixIndex)(jqStartIdx);
};
exports.getJiangqian12StartIndex = getJiangqian12StartIndex;
/**
 * 流年诸星。
 *
 * - 流年岁前诸星
 *   - 流年地支起岁建，岁前首先是晦气，
 *   - 丧门贯索及官符，小耗大耗龙德继，
 *   - 白虎天德连吊客，病符居后须当记。
 *
 * - 安流年将前诸星（按流年地支起将星）
 *   - 寅午戍年将星午，申子辰年子将星，
 *   - 巳酉丑将酉上驻，亥卯未将卯上停。
 *   - 攀鞍岁驿并息神，华盖劫煞灾煞轻，
 *   - 天煞指背咸池续，月煞亡神次第行。
 *
 * @param solarDateStr 阳历日期字符串
 * @returns 流年诸星从寅宫开始的顺序
 */
var getYearly12 = function (solarDateStr) {
    var jiangqian12 = [];
    var suiqian12 = [];
    var yearly = (0, calendar_1.getHeavenlyStemAndEarthlyBranchBySolarDate)(solarDateStr, 0).yearly;
    var ts12shen = [
        '岁建',
        '晦气',
        '丧门',
        '贯索',
        '官符',
        '小耗',
        '大耗',
        '龙德',
        '白虎',
        '天德',
        '吊客',
        '病符',
    ];
    for (var i = 0; i < ts12shen.length; i++) {
        var idx = (0, utils_1.fixIndex)((0, utils_1.fixEarthlyBranchIndex)(yearly[1]) + i);
        suiqian12[idx] = (0, i18n_1.t)(ts12shen[i]);
    }
    var jq12shen = [
        '将星',
        '攀鞍',
        '岁驿',
        '息神',
        '华盖',
        '劫煞',
        '灾煞',
        '天煞',
        '指背',
        '咸池',
        '月煞',
        '亡神',
    ];
    var jiangqian12StartIndex = (0, exports.getJiangqian12StartIndex)(yearly[1]);
    for (var i = 0; i < jq12shen.length; i++) {
        var idx = (0, utils_1.fixIndex)(jiangqian12StartIndex + i);
        jiangqian12[idx] = (0, i18n_1.t)(jq12shen[i]);
    }
    return { suiqian12: suiqian12, jiangqian12: jiangqian12 };
};
exports.getYearly12 = getYearly12;
/**
 * 获取流耀
 *
 * 魁钺昌曲禄羊陀马鸾喜
 *
 * @param heavenlyStem 天干
 * @param earthlyBranch 地支
 */
var getHoroscopeStar = function (heavenlyStem, earthlyBranch, scope) {
    var _a = (0, location_1.getKuiYueIndex)(heavenlyStem), kuiIndex = _a.kuiIndex, yueIndex = _a.yueIndex;
    var _b = (0, location_1.getChangQuIndexByHeavenlyStem)(heavenlyStem), changIndex = _b.changIndex, quIndex = _b.quIndex;
    var _c = (0, location_1.getLuYangTuoMaIndex)(heavenlyStem, earthlyBranch), luIndex = _c.luIndex, yangIndex = _c.yangIndex, tuoIndex = _c.tuoIndex, maIndex = _c.maIndex;
    var _d = (0, location_1.getLuanXiIndex)(earthlyBranch), hongluanIndex = _d.hongluanIndex, tianxiIndex = _d.tianxiIndex;
    var stars = (0, exports.initStars)();
    stars[kuiIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunkui') : (0, i18n_1.t)('liukui'), type: 'soft', scope: scope });
    stars[yueIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunyue') : (0, i18n_1.t)('liuyue'), type: 'soft', scope: scope });
    stars[changIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunchang') : (0, i18n_1.t)('liuchang'), type: 'soft', scope: scope });
    stars[quIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunqu') : (0, i18n_1.t)('liuqu'), type: 'soft', scope: scope });
    stars[luIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunlu') : (0, i18n_1.t)('liulu'), type: 'lucun', scope: scope });
    stars[yangIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunyang') : (0, i18n_1.t)('liuyang'), type: 'tough', scope: scope });
    stars[tuoIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yuntuo') : (0, i18n_1.t)('liutuo'), type: 'tough', scope: scope });
    stars[maIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunma') : (0, i18n_1.t)('liuma'), type: 'tianma', scope: scope });
    stars[hongluanIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunluan') : (0, i18n_1.t)('liuluan'), type: 'flower', scope: scope });
    stars[tianxiIndex].push({ name: scope === 'decadal' ? (0, i18n_1.t)('yunxi') : (0, i18n_1.t)('liuxi'), type: 'flower', scope: scope });
    if (scope === 'yearly') {
        var nianjieIndex = (0, location_1.getNianjieIndex)(earthlyBranch);
        stars[nianjieIndex].push({ name: (0, i18n_1.t)('nianjie'), type: 'helper', scope: 'yearly' });
    }
    return stars;
};
exports.getHoroscopeStar = getHoroscopeStar;
