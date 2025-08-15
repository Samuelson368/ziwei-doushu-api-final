console.log('=== 紫微斗数计算开始 ===');

// 环境检查
console.log('Node.js版本:', process.version);
console.log('当前工作目录:', process.cwd());

try {
    // 加载iztro库 - 尝试多种加载方式
    let iztro;
    try {
        iztro = require('iztro');
        console.log('✅ 直接加载iztro成功');
    } catch (e1) {
        try {
            iztro = require('./node_modules/iztro');
            console.log('✅ 相对路径加载iztro成功');
        } catch (e2) {
            console.error('❌ 所有加载方式都失败了');
            console.error('直接加载错误:', e1.message);
            console.error('相对路径错误:', e2.message);
            process.exit(1);
        }
    }
    
    // 检查astro对象
    if (!iztro.astro) {
        console.error('❌ iztro.astro 不存在');
        console.error('iztro对象属性:', Object.keys(iztro));
        process.exit(1);
    }
    console.log('✅ iztro.astro 对象存在');
    
    // 设置计算参数
    const date = "1990-1-1";
    const hour = 6;
    const gender = "女";
    const fixLeap = false;
    
    console.log('计算参数:');
    console.log('- 日期:', date);
    console.log('- 时辰索引:', hour, '(0-11)');
    console.log('- 性别:', gender);
    console.log('- 修正闰年:', fixLeap);
    
    // 调用iztro进行计算 - 与ziwei_terminal.py完全一致
    console.log('开始调用iztro.astro.bySolar...');
    const astrolabe = iztro.astro.bySolar(
        date,                    // 阳历日期字符串
        hour,                    // 时辰索引 0-11
        gender,                  // 性别 "男"/"女"
        fixLeap,                 // 是否修正闰年
        'zh-CN'                  // 语言
    );
    
    console.log('✅ 紫微斗数计算成功！');
    
    // 格式化输出结果 - 包含完整信息
    const result = {
        success: true,
        data: {
            basic_info: {
                birth_date: "1990-01-01",
                birth_time: "12:00",
                gender: "female",
                solar_date: astrolabe.solarDate || '未知',
                lunar_date: astrolabe.lunarDate || '未知',
                time_chen: astrolabe.time || '未知',
                time_range: astrolabe.timeRange || '未知',
                sign: astrolabe.sign || '未知',
                zodiac: astrolabe.zodiac || '未知',
                five_elements_class: astrolabe.fiveElementsClass || '未知',
                soul: astrolabe.soul || '未知',
                body: astrolabe.body || '未知'
            },
            palaces: astrolabe.palaces ? astrolabe.palaces.map(palace => ({
                name: palace.name || '未知',
                earthly_branch: palace.earthlyBranch || '未知',
                heavenly_stem: palace.heavenlyStem || '未知',
                major_stars: palace.majorStars ? palace.majorStars.map(star => ({
                    name: star.name || '未知',
                    brightness: star.brightness || '',
                    mutagen: star.mutagen || ''
                })) : [],
                minor_stars: palace.minorStars ? palace.minorStars.map(star => ({
                    name: star.name || '未知',
                    mutagen: star.mutagen || ''
                })) : [],
                adjective_stars_count: palace.adjectiveStars ? palace.adjectiveStars.length : 0
            })) : [],
            summary: {
                description: `${astrolabe.solarDate || date}出生，农历${astrolabe.lunarDate || '未知'}`,
                time_info: `${astrolabe.time || '未知'} (${astrolabe.timeRange || '未知'})`,
                soul_palace: astrolabe.earthlyBranchOfSoulPalace || '未知',
                body_palace: astrolabe.earthlyBranchOfBodyPalace || '未知',
                calculation_time: new Date().toISOString()
            }
        }
    };
    
    console.log('CALCULATION_SUCCESS');
    console.log(JSON.stringify(result, null, 2));
    console.log('CALCULATION_END');
    
} catch (error) {
    console.error('❌ 计算过程发生错误:');
    console.error('错误消息:', error.message);
    console.error('错误堆栈:', error.stack);
    
    const errorResult = {
        success: false,
        error: error.message,
        error_type: error.constructor.name,
        stack: error.stack
    };
    
    console.log('CALCULATION_ERROR');
    console.log(JSON.stringify(errorResult, null, 2));
    console.log('CALCULATION_END');
}

console.log('=== 紫微斗数计算结束 ===');