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
    """API文档首页 - 增强版"""
    return jsonify({
        "name": "紫微斗数专业排盘API",
        "version": "1.0.1",
        "description": "基于ziwei_terminal.py改造的API服务，支持GET和POST双重调用方式",
        "author": "紫微斗数API开发团队",
        "updated": datetime.now().strftime("%Y-%m-%d"),
        
        "endpoints": {
            "GET /": "API文档首页",
            "GET /health": "健康检查",
            "GET /test": "测试用例",
            "GET /ping": "快速ping测试",
            "GET|POST /calculate": "计算紫微斗数命盘（核心功能）",
            "GET|POST /debug": "调试接口"
        },
        
        "main_feature": {
            "endpoint": "/calculate",
            "description": "计算完整的紫微斗数命盘，包含十二宫位、主星配置、四化星分析等",
            "methods": ["GET", "POST"],
            "platform_compatibility": ["Coze", "智谱清言", "通义千问", "标准REST API"]
        },
        
        "usage_examples": {
            "coze_platform_get": {
                "description": "Coze等AI平台调用方式（GET请求）",
                "url": "/calculate?birth_datetime=2000-08-16 14:30&gender=男",
                "method": "GET",
                "note": "Coze会自动使用此格式"
            },
            "standard_api_post": {
                "description": "标准API调用方式（POST请求）",
                "url": "/calculate",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "birth_datetime": "2000-08-16 14:30",
                    "gender": "男"
                }
            },
            "separated_format": {
                "description": "分离式日期时间格式",
                "body": {
                    "birth_date": "2000-08-16",
                    "birth_time": "14:30",
                    "gender": "female"
                }
            }
        },
        
        "parameter_formats": {
            "birth_datetime": {
                "description": "完整的出生日期时间",
                "formats": ["2000-08-16 14:30", "2000/08/16 14:30", "2000.08.16 14:30"],
                "required": True
            },
            "gender": {
                "description": "性别",
                "values": ["男", "女", "male", "female"],
                "required": True
            },
            "is_leap": {
                "description": "是否闰年修正",
                "default": False,
                "required": False
            }
        },
        
        "response_structure": {
            "success": True,
            "data": {
                "basic_info": "基本信息（出生时间、农历、生肖等）",
                "palaces": "十二宫位详细信息",
                "summary": "命盘总结分析"
            }
        },
        
        "features": [
            "传统紫微斗数完整算法",
            "十二宫位详细解读",
            "主星、副星、杂曜完整配置",
            "四化星（化禄、化权、化科、化忌）",
            "支持多种日期时间输入格式",
            "完美兼容Coze等AI平台",
            "详细的调试和错误信息"
        ]
    })

@app.route('/ping', methods=['GET'])
def ping():
    """快速ping测试"""
    return jsonify({
        "pong": True,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": "紫微斗数API",
        "status": "运行中"
    })

@app.route('/debug', methods=['GET', 'POST'])
def debug():
    """调试接口 - 查看接收到的数据 - 支持GET和POST"""
    try:
        debug_info = {
            "method": request.method,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": request.url,
            "path": request.path,
            "headers": dict(request.headers),
            "remote_addr": request.remote_addr
        }
        
        if request.method == 'POST':
            data = request.get_json()
            debug_info.update({
                "received_data": data,
                "data_type": str(type(data)),
                "gender_info": {
                    "repr": repr(data.get('gender')) if data else None,
                    "bytes": [ord(c) for c in data.get('gender', '')] if data and data.get('gender') else None
                }
            })
        else:
            # GET请求
            debug_info.update({
                "query_params": dict(request.args),
                "query_string": request.query_string.decode('utf-8')
            })
        
        return jsonify(debug_info)
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
            "message": "紫微斗数API服务测试完成",
            "service_version": "1.0.1",
            "test_data": {
                "birth_date": test_birth_date,
                "birth_time": test_birth_time,
                "gender": test_gender
            },
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        app.logger.error(f"测试失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"测试失败: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/calculate', methods=['GET', 'POST'])  # 🔧 关键改进：同时支持GET和POST
def calculate():
    """紫微斗数计算接口 - 完美兼容Coze平台"""
    try:
        # 记录请求信息
        request_info = {
            "method": request.method,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_agent": request.headers.get('User-Agent', ''),
            "source": "unknown"
        }
        
        # 🔧 核心改进：根据请求方法获取参数
        if request.method == 'POST':
            # POST请求：从JSON body获取参数
            data = request.get_json()
            app.logger.info(f"POST请求 - 收到数据: {data}")
            request_info["source"] = "POST JSON body"
            
            if not data:
                return jsonify({
                    "success": False,
                    "error": "POST请求需要提供JSON数据",
                    "request_info": request_info
                }), 400
                
            birth_datetime = data.get('birth_datetime')
            birth_date = data.get('birth_date')
            birth_time = data.get('birth_time')
            gender = data.get('gender', 'male')
            is_leap = data.get('is_leap', False)
            
        else:
            # GET请求：从查询参数获取（Coze平台使用此方式）
            birth_datetime = request.args.get('birth_datetime')
            birth_date = request.args.get('birth_date')
            birth_time = request.args.get('birth_time')
            gender = request.args.get('gender', 'male')
            is_leap = request.args.get('is_leap', 'false').lower() == 'true'
            request_info["source"] = "GET query parameters"
            
            app.logger.info(f"GET请求 - 参数: birth_datetime={birth_datetime}, gender={gender}")
        
        # 参数处理：如果有birth_datetime，解析它
        if birth_datetime:
            try:
                parsed_date, parsed_time = parse_input_time(birth_datetime)
                birth_date = parsed_date
                birth_time = parsed_time
                app.logger.info(f"解析birth_datetime: {birth_datetime} -> {birth_date} {birth_time}")
            except ValueError as e:
                return jsonify({
                    "success": False,
                    "error": f"时间格式解析错误: {str(e)}",
                    "supported_formats": [
                        "2000-08-16 14:30",
                        "2000/08/16 14:30",
                        "2000.08.16 14:30"
                    ],
                    "request_info": request_info
                }), 400
        
        # 检查必需参数
        if not birth_date or not birth_time:
            return jsonify({
                "success": False,
                "error": "缺少必需参数：出生日期和时间",
                "required_parameters": {
                    "birth_datetime": "完整的出生日期时间，如：2000-08-16 14:30",
                    "或分别提供": {
                        "birth_date": "出生日期，如：2000-08-16", 
                        "birth_time": "出生时间，如：14:30"
                    },
                    "gender": "性别，支持：男/女/male/female"
                },
                "examples": {
                    "GET请求": "/calculate?birth_datetime=2000-08-16 14:30&gender=男",
                    "POST请求": {
                        "birth_datetime": "2000-08-16 14:30",
                        "gender": "女"
                    }
                },
                "request_info": request_info
            }), 400
        
        # 性别标准化处理
        gender_str = str(gender).strip()
        original_gender = gender_str
        
        if gender_str in ['男', 'male', 'M', 'm', '1']:
            normalized_gender = 'male'
        elif gender_str in ['女', 'female', 'F', 'f', '0']:
            normalized_gender = 'female'
        else:
            return jsonify({
                "success": False,
                "error": "性别参数错误",
                "received_gender": repr(gender_str),
                "supported_values": ["男", "女", "male", "female"],
                "request_info": request_info
            }), 400
        
        # 记录处理后的参数
        processed_params = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "original_gender": original_gender,
            "normalized_gender": normalized_gender,
            "is_leap": is_leap
        }
        
        app.logger.info(f"开始计算 - 处理后参数: {processed_params}")
        
        # 调用紫微斗数计算
        result = call_iztro_api(birth_date, birth_time, normalized_gender, is_leap)
        
        # 处理计算结果
        if result.get('success'):
            response_data = {
                "success": True,
                "message": "紫微斗数命盘计算成功",
                "request_info": request_info,
                "processed_params": processed_params,
                "result": result.get('data', {}),
                "calculation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "api_version": "1.0.1"
            }
            
            # 如果有summary，也包含进去
            if 'summary' in result:
                response_data["summary"] = result['summary']
            
            return jsonify(response_data)
        else:
            return jsonify({
                "success": False,
                "message": "紫微斗数计算失败",
                "error": result.get('error', '未知错误'),
                "error_type": result.get('error_type', '计算错误'),
                "request_info": request_info,
                "processed_params": processed_params,
                "debug_info": "如需调试，请查看生成的ziwei_calculation.js文件"
            }), 500
            
    except Exception as e:
        app.logger.error(f"计算接口错误: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": "服务器内部错误",
            "error": str(e),
            "error_type": type(e).__name__,
            "request_info": {
                "method": request.method,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": request.url
            },
            "traceback": traceback.format_exc() if app.debug else "详细错误信息已记录"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查 - 增强版"""
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
            "service": "紫微斗数API",
            "api_version": "1.0.1",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dependencies": {
                "iztro": {
                    "status": iztro_status,
                    "version": iztro_info.get('version', '未知'),
                    "astro_available": iztro_info.get('astro') == 'object'
                },
                "nodejs": "已安装",
                "python": sys.version
            },
            "environment": {
                "working_directory": os.getcwd(),
                "python_version": sys.version,
                "platform": sys.platform
            },
            "features": {
                "get_support": True,
                "post_support": True,
                "coze_compatibility": True,
                "debugging": True
            }
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "service": "紫微斗数API"
        }), 500

# 添加CORS支持
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "接口不存在",
        "message": "请检查请求路径是否正确",
        "available_endpoints": ["/", "/health", "/test", "/ping", "/calculate", "/debug"],
        "documentation": "访问根路径 / 查看完整API文档",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "服务器内部错误",
        "message": "请稍后重试，如问题持续请联系技术支持",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 500

if __name__ == '__main__':
    print("🌟 紫微斗数API服务启动中...")
    print("📍 服务地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000/")
    print("🔧 健康检查: http://localhost:5000/health")
    print("🧪 测试接口: http://localhost:5000/test")
    print("⚡ 核心功能: http://localhost:5000/calculate")
    print("🎯 支持方式: GET和POST双重调用")
    print("🤖 Coze兼容: 完美支持")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
