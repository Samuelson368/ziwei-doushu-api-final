// ziwei_node_script.js
try {
    console.error('=== 调试信息 ===');
    console.error('当前工作目录:', process.cwd());
    console.error('脚本文件位置:', __filename);
    console.error('脚本目录:', __dirname);
    console.error('尝试加载 iztro...');
    
    var iztro = require('./node_modules/iztro');
    console.error('✅ iztro库加载成功');
} catch (error) {
    console.error('❌ 无法加载iztro库');
    console.error('错误详情:', error.message);
    console.error('错误堆栈:', error.stack);
    process.exit(1);
}

const args = process.argv.slice(2);
if (args.length < 4) {
    console.error('参数不足：需要 日期 时辰 性别 是否修正闰年');
    process.exit(1);
}

const [date, hour, gender, fixLeap] = args;

console.error(`参数: 日期=${date}, 时辰=${hour}, 性别=${gender}, 修正闰年=${fixLeap}`);

try {
    const astrolabe = iztro.astro.bySolar(
        date,
        parseInt(hour),
        gender,
        fixLeap === 'true',
        'zh-CN'
    );
    
    console.error('✅ 排盘成功');
    console.log(JSON.stringify(astrolabe, null, 2));
} catch (error) {
    console.error('❌ 排盘失败:', error.message);
    console.error('错误详情:', error.stack);
    process.exit(1);
}