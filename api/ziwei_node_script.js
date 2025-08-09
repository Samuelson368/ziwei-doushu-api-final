// // ziwei_node_script.js
// try {
//     console.error('=== 调试信息 ===');
//     console.error('当前工作目录:', process.cwd());
//     console.error('脚本文件位置:', __filename);
//     console.error('脚本目录:', __dirname);
//     console.error('尝试加载 iztro...');
    
//     var iztro = require('./node_modules/iztro');
//     console.error('✅ iztro库加载成功');
// } catch (error) {
//     console.error('❌ 无法加载iztro库');
//     console.error('错误详情:', error.message);
//     console.error('错误堆栈:', error.stack);
//     process.exit(1);
// }

// const args = process.argv.slice(2);
// if (args.length < 4) {
//     console.error('参数不足：需要 日期 时辰 性别 是否修正闰年');
//     process.exit(1);
// }

// const [date, hour, gender, fixLeap] = args;

// console.error(`参数: 日期=${date}, 时辰=${hour}, 性别=${gender}, 修正闰年=${fixLeap}`);

// try {
//     const astrolabe = iztro.astro.bySolar(
//         date,
//         parseInt(hour),
//         gender,
//         fixLeap === 'true',
//         'zh-CN'
//     );
    
//     console.error('✅ 排盘成功');
//     console.log(JSON.stringify(astrolabe, null, 2));
// } catch (error) {
//     console.error('❌ 排盘失败:', error.message);
//     console.error('错误详情:', error.stack);
//     process.exit(1);
// }
// ziwei_node_script.js - Vercel优化版
const path = require('path');

// 尝试多种方式加载iztro
let iztro;
try {
    // 方式1：相对路径加载
    iztro = require('./node_modules/iztro');
    console.error('✅ iztro库加载成功（相对路径）');
} catch (error1) {
    try {
        // 方式2：直接require
        iztro = require('iztro');
        console.error('✅ iztro库加载成功（直接require）');
    } catch (error2) {
        try {
            // 方式3：从根目录加载
            const rootPath = path.join(__dirname, 'node_modules', 'iztro');
            iztro = require(rootPath);
            console.error('✅ iztro库加载成功（根目录路径）');
        } catch (error3) {
            console.error('❌ 无法加载iztro库');
            console.error('错误1:', error1.message);
            console.error('错误2:', error2.message);
            console.error('错误3:', error3.message);
            console.error('当前工作目录:', process.cwd());
            console.error('脚本目录:', __dirname);
            process.exit(1);
        }
    }
}

// 参数验证
const args = process.argv.slice(2);
if (args.length < 4) {
    console.error('❌ 参数不足：需要 日期 时辰 性别 是否修正闰年');
    console.error('当前参数:', args);
    process.exit(1);
}

const [date, hour, gender, fixLeap] = args;

console.error(`📥 参数: 日期=${date}, 时辰=${hour}, 性别=${gender}, 修正闰年=${fixLeap}`);

try {
    const astrolabe = iztro.astro.bySolar(
        date,
        parseInt(hour),
        gender,
        fixLeap === 'true',
        'zh-CN'
    );
    
    console.error('✅ 排盘成功');
    // 输出JSON结果到stdout
    console.log(JSON.stringify(astrolabe, null, 2));
} catch (error) {
    console.error('❌ 排盘失败:', error.message);
    console.error('错误详情:', error.stack);
    process.exit(1);
}