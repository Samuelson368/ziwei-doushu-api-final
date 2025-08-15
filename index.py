from flask import Flask, request, jsonify
import json
import subprocess
import os
import sys
import tempfile
from datetime import datetime
import traceback
import re

app = Flask(__name__)

def parse_input_time(input_str):
    """解析用户输入的时间格式"""
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M", 
        "%Y.%m.%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(input_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")
        except ValueError:
            continue
    
    raise ValueError("无法解析时间格式")

def get_time_chen_index(hour, minute):
    """
    根据小时和分钟获取时辰索引（0-11）
    复制自ziwei_terminal.py的逻辑
    """
    # 转换为分钟数便于比较
    total_minutes = hour * 60 + minute
    
    # 子时特殊处理（23:00-01:00，跨日）
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return 0  # 子时
    
    # 其他时辰的分钟边界
    time_ranges = [
        (1 * 60, 3 * 60, 1),    # 丑时 01:00-03:00
        (3 * 60, 5 * 60, 2),    # 寅时 03:00-05:00
        (5 * 60, 7 * 60, 3),    # 卯时 05:00-07:00
        (7 * 60, 9 * 60, 4),    # 辰时 07:00-09:00
        (9 * 60, 11 * 60, 5),   # 巳时 09:00-11:00
        (11 * 60, 13 * 60, 6),  # 午时 11:00-13:00
        (13 * 60, 15 * 60, 7),  # 未时 13:00-15:00
        (15 * 60, 17 * 60, 8),  # 申时 15:00-17:00
        (17 * 60, 19 * 60, 9),  # 酉时 17:00-19:00
        (19 * 60, 21 * 60, 10), # 戌时 19:00-21:00
        (21 * 60, 23 * 60, 11), # 亥时 21:00-23:00
    ]
    
    for start_min, end_min, index in time_ranges:
        if start_min <= total_minutes < end_min:
            return index
    
    # 默认返回子时
    return 0

def call_iztro_api(birth_date, birth_time, gender, is_leap=False):
    """调用iztro库计算紫微斗数 - 完全基于ziwei_terminal.py的逻辑"""
    try:
        # 转换性别格式 - 保持中文，与ziwei_terminal.py一致
        gender_map = {"男": "男", "女": "女", "male": "男", "female": "女"}
        iztro_gender = gender_map.get(gender, "男")
        
        app.logger.info(f"原始性别: {repr(gender)}, 转换后: {iztro_gender}")
        
        # 解析时间并获取时辰索引
        hour, minute = map(int, birth_time.split(':'))
        time_chen_index = get_time_chen_index(hour, minute)
        
        app.logger.info(f"时间解析: {birth_time} -> 时辰索引: {time_chen_index}")
        
        # 格式化日期为iztro需要的格式（去掉前导0）
        year, month, day = birth_date.split('-')
        formatted_date = f"{year}-{int(month)}-{int(day)}"
        
        app.logger.info(f"格式化日期: {birth_date} -> {formatted_date}")
        
        # 创建一个固定名称的JS文件，便于调试
        js_file_path = 'ziwei_calculation.js'
        
        # 创建Node.js脚本 - 完全复制ziwei_terminal.py的逻辑
        js_code = f'''console.log('=== 紫微斗数计算开始 ===');

// 环境检查
console.log('Node.js版本:', process.version);
console.log('当前工作目录:', process.cwd());

try {{
    // 加载iztro库 - 尝试多种加载方式
    let iztro;
    try {{
        iztro = require('iztro');
        console.log('✅ 直接加载iztro成功');
    }} catch (e1) {{
        try {{
            iztro = require('./node_modules/iztro');
            console.log('✅ 相对路径加载iztro成功');
        }} catch (e2) {{
            console.error('❌ 所有加载方式都失败了');
            console.error('直接加载错误:', e1.message);
            console.error('相对路径错误:', e2.message);
            process.exit(1);
        }}
    }}
    
    // 检查astro对象
    if (!iztro.astro) {{
        console.error('❌ iztro.astro 不存在');
        console.error('iztro对象属性:', Object.keys(iztro));
        process.exit(1);
    }}
    console.log('✅ iztro.astro 对象存在');
    
    // 设置计算参数
    const date = "{formatted_date}";
    const hour = {time_chen_index};
    const gender = "{iztro_gender}";
    const fixLeap = {str(is_leap).lower()};
    
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
    const result = {{
        success: true,
        data: {{
            basic_info: {{
                birth_date: "{birth_date}",
                birth_time: "{birth_time}",
                gender: "{gender}",
                solar_date: astrolabe.solarDate || '未知',
                lunar_date: astrolabe.lunarDate || '未知',
                time_chen: astrolabe.time || '未知',
                time_range: astrolabe.timeRange || '未知',
                sign: astrolabe.sign || '未知',
                zodiac: astrolabe.zodiac || '未知',
                five_elements_class: astrolabe.fiveElementsClass || '未知',
                soul: astrolabe.soul || '未知',
                body: astrolabe.body || '未知'
            }},
            palaces: astrolabe.palaces ? astrolabe.palaces.map(palace => ({{
                name: palace.name || '未知',
                earthly_branch: palace.earthlyBranch || '未知',
                heavenly_stem: palace.heavenlyStem || '未知',
                major_stars: palace.majorStars ? palace.majorStars.map(star => ({{
                    name: star.name || '未知',
                    brightness: star.brightness || '',
                    mutagen: star.mutagen || ''
                }})) : [],
                minor_stars: palace.minorStars ? palace.minorStars.map(star => ({{
                    name: star.name || '未知',
                    mutagen: star.mutagen || ''
                }})) : [],
                adjective_stars_count: palace.adjectiveStars ? palace.adjectiveStars.length : 0
            }})) : [],
            summary: {{
                description: `${{astrolabe.solarDate || date}}出生，农历${{astrolabe.lunarDate || '未知'}}`,
                time_info: `${{astrolabe.time || '未知'}} (${{astrolabe.timeRange || '未知'}})`,
                soul_palace: astrolabe.earthlyBranchOfSoulPalace || '未知',
                body_palace: astrolabe.earthlyBranchOfBodyPalace || '未知',
                calculation_time: new Date().toISOString()
            }}
        }}
    }};
    
    console.log('CALCULATION_SUCCESS');
    console.log(JSON.stringify(result, null, 2));
    console.log('CALCULATION_END');
    
}} catch (error) {{
    console.error('❌ 计算过程发生错误:');
    console.error('错误消息:', error.message);
    console.error('错误堆栈:', error.stack);
    
    const errorResult = {{
        success: false,
        error: error.message,
        error_type: error.constructor.name,
        stack: error.stack
    }};
    
    console.log('CALCULATION_ERROR');
    console.log(JSON.stringify(errorResult, null, 2));
    console.log('CALCULATION_END');
}}

console.log('=== 紫微斗数计算结束 ===');'''
        
        # 写入JS文件
        with open(js_file_path, 'w', encoding='utf-8') as f:
            f.write(js_code)
        
        app.logger.info(f"JS计算文件已创建: {js_file_path}")
        
        try:
            # 执行Node.js脚本
            result = subprocess.run([
                'node', js_file_path
            ], capture_output=True, text=True, timeout=30, encoding='utf-8')
            
            app.logger.info(f"Node.js执行完成 - 返回码: {result.returncode}")
            
            if result.stderr:
                app.logger.info(f"Node.js调试信息: {result.stderr}")
            
            if result.returncode == 0:
                # 解析成功结果
                if 'CALCULATION_SUCCESS' in result.stdout and 'CALCULATION_END' in result.stdout:
                    start_marker = 'CALCULATION_SUCCESS'
                    end_marker = 'CALCULATION_END'
                    
                    start_pos = result.stdout.find(start_marker) + len(start_marker)
                    end_pos = result.stdout.find(end_marker, start_pos)
                    
                    if end_pos != -1:
                        json_str = result.stdout[start_pos:end_pos].strip()
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            app.logger.error(f"JSON解析错误: {e}")
                            return {"success": False, "error": f"JSON解析失败: {e}"}
                
                # 解析错误结果
                if 'CALCULATION_ERROR' in result.stdout and 'CALCULATION_END' in result.stdout:
                    start_marker = 'CALCULATION_ERROR'
                    end_marker = 'CALCULATION_END'
                    
                    start_pos = result.stdout.find(start_marker) + len(start_marker)
                    end_pos = result.stdout.find(end_marker, start_pos)
                    
                    if end_pos != -1:
                        json_str = result.stdout[start_pos:end_pos].strip()
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            pass
                
                return {"success": False, "error": "无法解析计算结果", "raw_output": result.stdout[:500]}
            else:
                return {"success": False, "error": f"Node.js执行失败: {result.stderr}"}
        
        finally:
            # 保留JS文件便于调试（生产环境中可以删除）
            # if os.path.exists(js_file_path):
            #     os.remove(js_file_path)
            pass
                
    except Exception as e:
        app.logger.error(f"计算异常: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False, 
            "error": f"Python执行错误: {str(e)}"
        }

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "紫微斗数API服务",
        "version": "1.0.0",
        "description": "基于ziwei_terminal.py改造的API服务",
        "endpoints": {
            "POST /calculate": "计算紫微斗数命盘",
            "GET /test": "测试用例",
            "GET /health": "健康检查",
            "POST /debug": "调试接口"
        },
        "usage": {
            "url": "/calculate",
            "method": "POST",
            "body": {
                "birth_datetime": "2000-08-16 14:30",
                "gender": "male"
            }
        },
        "examples": {
            "english": {
                "birth_datetime": "2000-08-16 14:30",
                "gender": "male"
            },
            "chinese": {
                "birth_datetime": "2000-08-16 14:30", 
                "gender": "男"
            },
            "separated": {
                "birth_date": "2000-08-16",
                "birth_time": "14:30",
                "gender": "female"
            }
        }
    })

@app.route('/debug', methods=['POST'])
def debug():
    """调试接口 - 查看接收到的数据"""
    try:
        data = request.get_json()
        return jsonify({
            "received_data": data,
            "data_type": str(type(data)),
            "gender_info": {
                "repr": repr(data.get('gender')) if data else None,
                "bytes": [ord(c) for c in data.get('gender', '')] if data and data.get('gender') else None
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """测试接口 - 使用固定参数"""
    try:
        app.logger.info("开始API测试...")
        
        # 使用测试数据
        test_birth_date = "2000-08-16"
        test_birth_time = "14:30"
        test_gender = "male"
        
        result = call_iztro_api(test_birth_date, test_birth_time, test_gender)
        
        return jsonify({
            "status": "success",
            "message": "API服务测试完成",
            "test_data": {
                "birth_date": test_birth_date,
                "birth_time": test_birth_time,
                "gender": test_gender
            },
            "result": result
        })
    except Exception as e:
        app.logger.error(f"测试失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"测试失败: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    """紫微斗数计算接口"""
    try:
        data = request.get_json()
        app.logger.info(f"收到计算请求: {data}")
        
        # 参数验证
        if not data:
            return jsonify({"error": "请提供JSON数据"}), 400
        
        # 支持两种参数格式
        birth_datetime = data.get('birth_datetime')
        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        gender = data.get('gender', 'male')
        
        # 如果有birth_datetime，解析它
        if birth_datetime:
            try:
                parsed_date, parsed_time = parse_input_time(birth_datetime)
                birth_date = parsed_date
                birth_time = parsed_time
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        
        # 检查必需参数
        if not birth_date or not birth_time:
            return jsonify({
                "error": "缺少必需参数",
                "required": ["birth_date", "birth_time", "gender"],
                "examples": {
                    "format1": {
                        "birth_datetime": "2000-08-16 14:30",
                        "gender": "male"
                    },
                    "format2": {
                        "birth_date": "2000-08-16",
                        "birth_time": "14:30", 
                        "gender": "female"
                    }
                }
            }), 400
        
        # 可选参数
        is_leap = data.get('is_leap', False)
        
        # 性别标准化
        gender_str = str(gender).strip()
        if gender_str in ['男', 'male', 'M', 'm', '1']:
            gender = 'male'
        elif gender_str in ['女', 'female', 'F', 'f', '0']:
            gender = 'female'
        else:
            return jsonify({
                "error": "性别参数错误，请使用：male/female/男/女",
                "received": repr(gender_str)
            }), 400
        
        app.logger.info(f"开始计算 - 日期: {birth_date}, 时间: {birth_time}, 性别: {gender}")
        
        # 调用计算
        result = call_iztro_api(birth_date, birth_time, gender, is_leap)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify({
                "error": result.get('error', '计算失败'),
                "error_type": result.get('error_type', '未知错误'),
                "debug_info": "如需调试，请查看生成的ziwei_calculation.js文件"
            }), 500
            
    except Exception as e:
        app.logger.error(f"计算接口错误: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "服务器内部错误",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    try:
        # 检查iztro是否可用
        result = subprocess.run([
            'node', '-e', 'console.log(JSON.stringify({version: require("iztro/package.json").version, astro: typeof require("iztro").astro}))'
        ], capture_output=True, text=True, timeout=10)
        
        iztro_status = "已安装" if result.returncode == 0 else "未安装"
        iztro_info = {}
        
        if result.returncode == 0:
            try:
                iztro_info = json.loads(result.stdout.strip())
            except:
                iztro_info = {"version": "解析失败"}
        
        return jsonify({
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "dependencies": {
                "iztro": iztro_status,
                "version": iztro_info.get('version', '未知'),
                "astro_available": iztro_info.get('astro', '未知')
            },
            "python_version": sys.version,
            "working_directory": os.getcwd()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# 添加CORS支持
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("🌟 紫微斗数API服务启动中...")
    print("📍 服务地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000/")
    print("🔧 健康检查: http://localhost:5000/health")
    print("🧪 测试接口: http://localhost:5000/test")
    
    app.run(debug=True, host='0.0.0.0', port=5000)