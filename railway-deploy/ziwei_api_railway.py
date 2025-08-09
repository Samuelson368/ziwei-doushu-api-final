from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess
import os
import re
from typing import Dict, Optional, Tuple

app = Flask(__name__)
CORS(app)

class ZiweiAPI:
    def __init__(self):
        # 使用固定的脚本文件路径
        self.script_path = os.path.join(os.getcwd(), 'ziwei_node_script.js')

    def parse_time_input(self, time_str: str) -> Tuple[Optional[int], Optional[str], str]:
        """解析时间输入并返回对应的时辰索引"""
        if not time_str:
            return None, None, "时间不能为空"
        
        time_str = time_str.strip()
        patterns = [
            r'^(\d{1,2})[:\：\.\-](\d{2})$',  # 14:30, 14：30, 14.30, 14-30
            r'^(\d{3,4})$',                    # 1430
            r'^(\d{1,2})$'                     # 14
        ]
        
        hour = None
        minute = None
        
        for pattern in patterns:
            match = re.match(pattern, time_str)
            if match:
                if len(match.groups()) == 2:
                    hour = int(match.group(1))
                    minute = int(match.group(2))
                elif len(match.groups()) == 1:
                    if len(match.group(1)) >= 3:
                        time_digits = match.group(1)
                        if len(time_digits) == 3:
                            hour = int(time_digits[0])
                            minute = int(time_digits[1:])
                        else:
                            hour = int(time_digits[:2])
                            minute = int(time_digits[2:])
                    else:
                        hour = int(match.group(1))
                        minute = 0
                break
        
        if hour is None or not (0 <= hour <= 23):
            return None, None, f"无法解析时间格式: {time_str}"
        
        if minute is None:
            minute = 0
        
        if not (0 <= minute <= 59):
            return None, None, f"分钟必须在0-59之间: {minute}"
        
        time_chen_index, time_chen_name, time_range = self._get_time_chen(hour, minute)
        
        return time_chen_index, time_chen_name, f"{hour:02d}:{minute:02d} → {time_chen_name} ({time_range})"

    def _get_time_chen(self, hour: int, minute: int) -> Tuple[int, str, str]:
        """根据小时和分钟判断时辰"""
        total_minutes = hour * 60 + minute
        
        if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
            return 0, "子时", "23:00-01:00"
        
        time_ranges = [
            (1 * 60, 3 * 60, 1, "丑时", "01:00-03:00"),
            (3 * 60, 5 * 60, 2, "寅时", "03:00-05:00"),
            (5 * 60, 7 * 60, 3, "卯时", "05:00-07:00"),
            (7 * 60, 9 * 60, 4, "辰时", "07:00-09:00"),
            (9 * 60, 11 * 60, 5, "巳时", "09:00-11:00"),
            (11 * 60, 13 * 60, 6, "午时", "11:00-13:00"),
            (13 * 60, 15 * 60, 7, "未时", "13:00-15:00"),
            (15 * 60, 17 * 60, 8, "申时", "15:00-17:00"),
            (17 * 60, 19 * 60, 9, "酉时", "17:00-19:00"),
            (19 * 60, 21 * 60, 10, "戌时", "19:00-21:00"),
            (21 * 60, 23 * 60, 11, "亥时", "21:00-23:00"),
        ]
        
        for start_min, end_min, index, name, range_str in time_ranges:
            if start_min <= total_minutes < end_min:
                return index, name, range_str
        
        return 0, "子时", "23:00-01:00"

    def generate_astrolabe(self, birth_date: str, birth_time: str, gender: str, fix_leap: bool = True) -> Dict:
        """生成星盘API"""
        # 解析时间
        birth_hour_index, time_chen_name, time_result = self.parse_time_input(birth_time)
        
        if birth_hour_index is None:
            return {
                "success": False,
                "error": time_result,
                "data": None
            }
        
        # 检查node_modules
        if not os.path.exists('node_modules/iztro'):
            return {
                "success": False,
                "error": "未找到 node_modules/iztro，请先运行：npm install iztro",
                "data": None
            }
        
        # 检查脚本文件
        if not os.path.exists(self.script_path):
            return {
                "success": False,
                "error": f"未找到脚本文件: {self.script_path}",
                "data": None
            }
        
        try:
            # 在项目根目录执行Node.js脚本
            current_dir = os.getcwd()
            
            # 检查是否在生产环境
            is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')
            
            # 生产环境减少调试输出
            if not is_production:
                print(f"🔧 Debug: 当前工作目录: {current_dir}")
                print(f"🔧 Debug: 脚本文件路径: {self.script_path}")
                print(f"🔧 Debug: 执行参数: {birth_date} {birth_hour_index} {gender} {fix_leap}")
            
            result = subprocess.run([
                'node', self.script_path,
                birth_date, str(birth_hour_index), gender, str(fix_leap).lower()
            ], capture_output=True, text=True, encoding='utf-8', cwd=current_dir, timeout=30)
            
            if not is_production:
                print(f"🔧 Debug: 返回码: {result.returncode}")
                if result.stderr:
                    print(f"🔧 Debug: stderr: {result.stderr}")
            
            if result.returncode == 0:
                try:
                    astrolabe_data = json.loads(result.stdout)
                    if not is_production:
                        print("✅ 排盘成功！")
                    return {
                        "success": True,
                        "error": None,
                        "data": {
                            "astrolabe": astrolabe_data,
                            "time_info": {
                                "original_time": birth_time,
                                "parsed_result": time_result,
                                "time_chen_index": birth_hour_index,
                                "time_chen_name": time_chen_name
                            }
                        }
                    }
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "error": f"JSON解析失败: {str(e)}",
                        "data": None
                    }
            else:
                return {
                    "success": False,
                    "error": f"Node.js执行失败: {result.stderr}",
                    "data": None
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "排盘超时，请稍后重试",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"执行错误: {str(e)}",
                "data": None
            }

# 创建API实例
ziwei_api = ZiweiAPI()

@app.route('/api/ziwei/astrolabe', methods=['POST'])
def create_astrolabe():
    """紫微斗数排盘API接口"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        if not data:
            return jsonify({
                "success": False,
                "error": "请求体不能为空",
                "data": None
            }), 400
        
        required_fields = ['birth_date', 'birth_time', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必需参数: {field}",
                    "data": None
                }), 400
        
        birth_date = data['birth_date']
        birth_time = data['birth_time']
        gender = data['gender']
        fix_leap = data.get('fix_leap', True)
        
        # 验证性别参数
        if gender not in ['男', '女']:
            return jsonify({
                "success": False,
                "error": "性别参数必须是 '男' 或 '女'",
                "data": None
            }), 400
        
        # 生成星盘
        result = ziwei_api.generate_astrolabe(birth_date, birth_time, gender, fix_leap)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}",
            "data": None
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "message": "紫微斗数API服务正常运行 (Railway部署版)",
        "environment": "production" if os.environ.get('RAILWAY_ENVIRONMENT') else "development"
    })

@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "name": "紫微斗数排盘API (Railway版)",
        "version": "1.0.0",
        "description": "基于iztro库的紫微斗数排盘服务，部署在Railway云平台",
        "endpoints": {
            "/api/ziwei/astrolabe": "POST - 生成紫微斗数星盘",
            "/api/health": "GET - 健康检查"
        },
        "features": [
            "智能时间解析 (支持14:30、1430、14.30等格式)",
            "完整星盘数据 (宫位、星耀、四化信息)",
            "高可用云部署"
        ]
    })

if __name__ == '__main__':
    import os
    
    # 获取端口号
    port = int(os.environ.get('PORT', 5002))
    
    # 检查是否在生产环境
    is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')
    
    if is_production:
        print("🚀 Railway生产环境启动...")
        print(f"📡 服务端口: {port}")
        
        # 生产环境使用Waitress
        try:
            from waitress import serve
            print("🌟 使用Waitress生产服务器启动...")
            serve(app, host='0.0.0.0', port=port, threads=4)
        except ImportError:
            print("⚠️  Waitress未安装，使用Flask开发服务器...")
            app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print("🔧 本地开发环境启动...")
        print(f"📡 服务地址: http://0.0.0.0:{port}")
        print("🔍 健康检查: /api/health")
        print("📚 API文档: /")
        app.run(host='0.0.0.0', port=port, debug=True)