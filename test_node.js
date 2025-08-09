// test_node.js
try {
    console.log('测试开始...');
    console.log('当前工作目录:', process.cwd());
    console.log('检查node_modules/iztro...');
    
    var iztro = require('./node_modules/iztro');
    console.log('✅ iztro库加载成功!');
    console.log('iztro版本:', require('./node_modules/iztro/package.json').version);
    
    // 测试基本功能
    console.log('测试排盘功能...');
    const astrolabe = iztro.astro.bySolar('2000-8-16', 7, '女', true, 'zh-CN');
    console.log('✅ 排盘成功!');
    console.log('性别:', astrolabe.gender);
    console.log('阳历:', astrolabe.solarDate);
    
} catch (error) {
    console.error('❌ 错误:', error.message);
    console.error('详细信息:', error);
}