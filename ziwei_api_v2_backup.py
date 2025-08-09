# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import json
# # import subprocess
# # import os
# # import re
# # import tempfile
# # from typing import Dict, Optional, Tuple

# # app = Flask(__name__)
# # CORS(app)

# # class ZiweiAPI:
# #     def __init__(self):
# #         self.node_script_content = '''
# # try {
# #     var iztro = require('./node_modules/iztro');
# # } catch (error) {
# #     console.error('错误：无法加载iztro库');
# #     process.exit(1);
# # }

# # const args = process.argv.slice(2);
# # if (args.length < 4) {
# #     console.error('参数不足');
# #     process.exit(1);
# # }

# # const [date, hour, gender, fixLeap] = args;

# # try {
# #     const astrolabe = iztro.astro.bySolar(
# #         date,
# #         parseInt(hour),
# #         gender,
# #         fixLeap === 'true',
# #         'zh-CN'
# #     );
    
# #     console.log(JSON.stringify(astrolabe, null, 2));
# # } catch (error) {
# #     console.error('排盘失败:', error.message);
# #     process.exit(1);
# # }
# # '''

# #     def parse_time_input(self, time_str: str) -> Tuple[Optional[int], Optional[str], str]:
# #         """解析时间输入并返回对应的时辰索引"""
# #         if not time_str:
# #             return None, None, "时间不能为空"
        
# #         time_str = time_str.strip()
# #         patterns = [
# #             r'^(\d{1,2})[:\：\.\-](\d{2})$',  # 14:30, 14：30, 14.30, 14-30
# #             r'^(\d{3,4})$',                    # 1430
# #             r'^(\d{1,2})$'                     # 14
# #         ]
        
# #         hour = None
# #         minute = None
        
# #         for pattern in patterns:
# #             match = re.match(pattern, time_str)
# #             if match:
# #                 if len(match.groups()) == 2:
# #                     hour = int(match.group(1))
# #                     minute = int(match.group(2))
# #                 elif len(match.groups()) == 1:
# #                     if len(match.group(1)) >= 3:
# #                         time_digits = match.group(1)
# #                         if len(time_digits) == 3:
# #                             hour = int(time_digits[0])
# #                             minute = int(time_digits[1:])
# #                         else:
# #                             hour = int(time_digits[:2])
# #                             minute = int(time_digits[2:])
# #                     else:
# #                         hour = int(match.group(1))
# #                         minute = 0
# #                 break
        
# #         if hour is None or not (0 <= hour <= 23):
# #             return None, None, f"无法解析时间格式: {time_str}"
        
# #         if minute is None:
# #             minute = 0
        
# #         if not (0 <= minute <= 59):
# #             return None, None, f"分钟必须在0-59之间: {minute}"
        
# #         time_chen_index, time_chen_name, time_range = self._get_time_chen(hour, minute)
        
# #         return time_chen_index, time_chen_name, f"{hour:02d}:{minute:02d} → {time_chen_name} ({time_range})"

# #     def _get_time_chen(self, hour: int, minute: int) -> Tuple[int, str, str]:
# #         """根据小时和分钟判断时辰"""
# #         total_minutes = hour * 60 + minute
        
# #         if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
# #             return 0, "子时", "23:00-01:00"
        
# #         time_ranges = [
# #             (1 * 60, 3 * 60, 1, "丑时", "01:00-03:00"),
# #             (3 * 60, 5 * 60, 2, "寅时", "03:00-05:00"),
# #             (5 * 60, 7 * 60, 3, "卯时", "05:00-07:00"),
# #             (7 * 60, 9 * 60, 4, "辰时", "07:00-09:00"),
# #             (9 * 60, 11 * 60, 5, "巳时", "09:00-11:00"),
# #             (11 * 60, 13 * 60, 6, "午时", "11:00-13:00"),
# #             (13 * 60, 15 * 60, 7, "未时", "13:00-15:00"),
# #             (15 * 60, 17 * 60, 8, "申时", "15:00-17:00"),
# #             (17 * 60, 19 * 60, 9, "酉时", "17:00-19:00"),
# #             (19 * 60, 21 * 60, 10, "戌时", "19:00-21:00"),
# #             (21 * 60, 23 * 60, 11, "亥时", "21:00-23:00"),
# #         ]
        
# #         for start_min, end_min, index, name, range_str in time_ranges:
# #             if start_min <= total_minutes < end_min:
# #                 return index, name, range_str
        
# #         return 0, "子时", "23:00-01:00"

# #     def generate_astrolabe(self, birth_date: str, birth_time: str, gender: str, fix_leap: bool = True) -> Dict:
# #         """生成星盘API"""
# #         # 解析时间
# #         birth_hour_index, time_chen_name, time_result = self.parse_time_input(birth_time)
        
# #         if birth_hour_index is None:
# #             return {
# #                 "success": False,
# #                 "error": time_result,
# #                 "data": None
# #             }
        
# #         # 检查node_modules
# #         if not os.path.exists('node_modules/iztro'):
# #             return {
# #                 "success": False,
# #                 "error": "未找到 node_modules/iztro，请先运行：npm install iztro",
# #                 "data": None
# #             }
        
# #         # 创建临时脚本文件
# #         with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
# #             f.write(self.node_script_content)
# #             script_path = f.name
        
# #         try:
# #             result = subprocess.run([
# #                 'node', script_path,
# #                 birth_date, str(birth_hour_index), gender, str(fix_leap).lower()
# #             ], capture_output=True, text=True, encoding='utf-8')
            
# #             if result.returncode == 0:
# #                 try:
# #                     astrolabe_data = json.loads(result.stdout)
# #                     return {
# #                         "success": True,
# #                         "error": None,
# #                         "data": {
# #                             "astrolabe": astrolabe_data,
# #                             "time_info": {
# #                                 "original_time": birth_time,
# #                                 "parsed_result": time_result,
# #                                 "time_chen_index": birth_hour_index,
# #                                 "time_chen_name": time_chen_name
# #                             }
# #                         }
# #                     }
# #                 except json.JSONDecodeError as e:
# #                     return {
# #                         "success": False,
# #                         "error": f"JSON解析失败: {str(e)}",
# #                         "data": None
# #                     }
# #             else:
# #                 return {
# #                     "success": False,
# #                     "error": f"Node.js执行失败: {result.stderr}",
# #                     "data": None
# #                 }
                
# #         except Exception as e:
# #             return {
# #                 "success": False,
# #                 "error": f"执行错误: {str(e)}",
# #                 "data": None
# #             }
# #         finally:
# #             # 清理临时文件
# #             if os.path.exists(script_path):
# #                 os.remove(script_path)

# # # 创建API实例
# # ziwei_api = ZiweiAPI()

# # @app.route('/api/ziwei/astrolabe', methods=['POST'])
# # def create_astrolabe():
# #     """紫微斗数排盘API接口"""
# #     try:
# #         data = request.get_json()
        
# #         # 验证必需参数
# #         if not data:
# #             return jsonify({
# #                 "success": False,
# #                 "error": "请求体不能为空",
# #                 "data": None
# #             }), 400
        
# #         required_fields = ['birth_date', 'birth_time', 'gender']
# #         for field in required_fields:
# #             if field not in data:
# #                 return jsonify({
# #                     "success": False,
# #                     "error": f"缺少必需参数: {field}",
# #                     "data": None
# #                 }), 400
        
# #         birth_date = data['birth_date']
# #         birth_time = data['birth_time']
# #         gender = data['gender']
# #         fix_leap = data.get('fix_leap', True)
        
# #         # 验证性别参数
# #         if gender not in ['男', '女']:
# #             return jsonify({
# #                 "success": False,
# #                 "error": "性别参数必须是 '男' 或 '女'",
# #                 "data": None
# #             }), 400
        
# #         # 生成星盘
# #         result = ziwei_api.generate_astrolabe(birth_date, birth_time, gender, fix_leap)
        
# #         if result['success']:
# #             return jsonify(result), 200
# #         else:
# #             return jsonify(result), 400
            
# #     except Exception as e:
# #         return jsonify({
# #             "success": False,
# #             "error": f"服务器错误: {str(e)}",
# #             "data": None
# #         }), 500

# # @app.route('/api/health', methods=['GET'])
# # def health_check():
# #     """健康检查接口"""
# #     return jsonify({
# #         "status": "healthy",
# #         "message": "紫微斗数API服务正常运行"
# #     })

# # @app.route('/', methods=['GET'])
# # def index():
# #     """首页"""
# #     return jsonify({
# #         "name": "紫微斗数排盘API",
# #         "version": "1.0.0",
# #         "description": "基于iztro库的紫微斗数排盘服务",
# #         "endpoints": {
# #             "/api/ziwei/astrolabe": "POST - 生成紫微斗数星盘",
# #             "/api/health": "GET - 健康检查"
# #         }
# #     })

# # if __name__ == '__main__':
# #     print("🌟 紫微斗数API服务启动中...")
# #     print("📡 服务地址: http://localhost:5000")
# #     print("🔍 健康检查: http://localhost:5000/api/health")
# #     print("📚 API文档: http://localhost:5000")
# #     app.run(host='0.0.0.0', port=5000, debug=True)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# import subprocess
# import os
# import re
# import tempfile
# from typing import Dict, Optional, Tuple

# app = Flask(__name__)
# CORS(app)

# class ZiweiAPI:
#     def __init__(self):
#         self.node_script_content = '''
# try {
#     var iztro = require('./node_modules/iztro');
# } catch (error) {
#     console.error('错误：无法加载iztro库');
#     console.error('当前工作目录:', process.cwd());
#     console.error('尝试加载的路径:', './node_modules/iztro');
#     process.exit(1);
# }

# const args = process.argv.slice(2);
# if (args.length < 4) {
#     console.error('参数不足');
#     process.exit(1);
# }

# const [date, hour, gender, fixLeap] = args;

# try {
#     const astrolabe = iztro.astro.bySolar(
#         date,
#         parseInt(hour),
#         gender,
#         fixLeap === 'true',
#         'zh-CN'
#     );
    
#     console.log(JSON.stringify(astrolabe, null, 2));
# } catch (error) {
#     console.error('排盘失败:', error.message);
#     process.exit(1);
# }
# '''

#     def parse_time_input(self, time_str: str) -> Tuple[Optional[int], Optional[str], str]:
#         """解析时间输入并返回对应的时辰索引"""
#         if not time_str:
#             return None, None, "时间不能为空"
        
#         time_str = time_str.strip()
#         patterns = [
#             r'^(\d{1,2})[:\：\.\-](\d{2})$',  # 14:30, 14：30, 14.30, 14-30
#             r'^(\d{3,4})$',                    # 1430
#             r'^(\d{1,2})$'                     # 14
#         ]
        
#         hour = None
#         minute = None
        
#         for pattern in patterns:
#             match = re.match(pattern, time_str)
#             if match:
#                 if len(match.groups()) == 2:
#                     hour = int(match.group(1))
#                     minute = int(match.group(2))
#                 elif len(match.groups()) == 1:
#                     if len(match.group(1)) >= 3:
#                         time_digits = match.group(1)
#                         if len(time_digits) == 3:
#                             hour = int(time_digits[0])
#                             minute = int(time_digits[1:])
#                         else:
#                             hour = int(time_digits[:2])
#                             minute = int(time_digits[2:])
#                     else:
#                         hour = int(match.group(1))
#                         minute = 0
#                 break
        
#         if hour is None or not (0 <= hour <= 23):
#             return None, None, f"无法解析时间格式: {time_str}"
        
#         if minute is None:
#             minute = 0
        
#         if not (0 <= minute <= 59):
#             return None, None, f"分钟必须在0-59之间: {minute}"
        
#         time_chen_index, time_chen_name, time_range = self._get_time_chen(hour, minute)
        
#         return time_chen_index, time_chen_name, f"{hour:02d}:{minute:02d} → {time_chen_name} ({time_range})"

#     def _get_time_chen(self, hour: int, minute: int) -> Tuple[int, str, str]:
#         """根据小时和分钟判断时辰"""
#         total_minutes = hour * 60 + minute
        
#         if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
#             return 0, "子时", "23:00-01:00"
        
#         time_ranges = [
#             (1 * 60, 3 * 60, 1, "丑时", "01:00-03:00"),
#             (3 * 60, 5 * 60, 2, "寅时", "03:00-05:00"),
#             (5 * 60, 7 * 60, 3, "卯时", "05:00-07:00"),
#             (7 * 60, 9 * 60, 4, "辰时", "07:00-09:00"),
#             (9 * 60, 11 * 60, 5, "巳时", "09:00-11:00"),
#             (11 * 60, 13 * 60, 6, "午时", "11:00-13:00"),
#             (13 * 60, 15 * 60, 7, "未时", "13:00-15:00"),
#             (15 * 60, 17 * 60, 8, "申时", "15:00-17:00"),
#             (17 * 60, 19 * 60, 9, "酉时", "17:00-19:00"),
#             (19 * 60, 21 * 60, 10, "戌时", "19:00-21:00"),
#             (21 * 60, 23 * 60, 11, "亥时", "21:00-23:00"),
#         ]
        
#         for start_min, end_min, index, name, range_str in time_ranges:
#             if start_min <= total_minutes < end_min:
#                 return index, name, range_str
        
#         return 0, "子时", "23:00-01:00"

#     def generate_astrolabe(self, birth_date: str, birth_time: str, gender: str, fix_leap: bool = True) -> Dict:
#         """生成星盘API"""
#         # 解析时间
#         birth_hour_index, time_chen_name, time_result = self.parse_time_input(birth_time)
        
#         if birth_hour_index is None:
#             return {
#                 "success": False,
#                 "error": time_result,
#                 "data": None
#             }
        
#         # 检查node_modules
#         if not os.path.exists('node_modules/iztro'):
#             return {
#                 "success": False,
#                 "error": "未找到 node_modules/iztro，请先运行：npm install iztro",
#                 "data": None
#             }
        
#         # 创建临时脚本文件
#         with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
#             f.write(self.node_script_content)
#             script_path = f.name
        
#         try:
#             # 关键修复：指定工作目录为当前目录
#             current_dir = os.getcwd()
#             print(f"Debug: 当前工作目录: {current_dir}")
#             print(f"Debug: 临时脚本路径: {script_path}")
            
#             result = subprocess.run([
#                 'node', script_path,
#                 birth_date, str(birth_hour_index), gender, str(fix_leap).lower()
#             ], capture_output=True, text=True, encoding='utf-8', cwd=current_dir)
            
#             print(f"Debug: Node.js 返回码: {result.returncode}")
#             print(f"Debug: Node.js stdout: {result.stdout[:200]}...")
#             print(f"Debug: Node.js stderr: {result.stderr}")
            
#             if result.returncode == 0:
#                 try:
#                     astrolabe_data = json.loads(result.stdout)
#                     return {
#                         "success": True,
#                         "error": None,
#                         "data": {
#                             "astrolabe": astrolabe_data,
#                             "time_info": {
#                                 "original_time": birth_time,
#                                 "parsed_result": time_result,
#                                 "time_chen_index": birth_hour_index,
#                                 "time_chen_name": time_chen_name
#                             }
#                         }
#                     }
#                 except json.JSONDecodeError as e:
#                     return {
#                         "success": False,
#                         "error": f"JSON解析失败: {str(e)}",
#                         "data": None
#                     }
#             else:
#                 return {
#                     "success": False,
#                     "error": f"Node.js执行失败: {result.stderr}",
#                     "data": None
#                 }
                
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": f"执行错误: {str(e)}",
#                 "data": None
#             }
#         finally:
#             # 清理临时文件
#             if os.path.exists(script_path):
#                 os.remove(script_path)

# # 创建API实例
# ziwei_api = ZiweiAPI()

# @app.route('/api/ziwei/astrolabe', methods=['POST'])
# def create_astrolabe():
#     """紫微斗数排盘API接口"""
#     try:
#         data = request.get_json()
        
#         # 验证必需参数
#         if not data:
#             return jsonify({
#                 "success": False,
#                 "error": "请求体不能为空",
#                 "data": None
#             }), 400
        
#         required_fields = ['birth_date', 'birth_time', 'gender']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({
#                     "success": False,
#                     "error": f"缺少必需参数: {field}",
#                     "data": None
#                 }), 400
        
#         birth_date = data['birth_date']
#         birth_time = data['birth_time']
#         gender = data['gender']
#         fix_leap = data.get('fix_leap', True)
        
#         # 验证性别参数
#         if gender not in ['男', '女']:
#             return jsonify({
#                 "success": False,
#                 "error": "性别参数必须是 '男' 或 '女'",
#                 "data": None
#             }), 400
        
#         # 生成星盘
#         result = ziwei_api.generate_astrolabe(birth_date, birth_time, gender, fix_leap)
        
#         if result['success']:
#             return jsonify(result), 200
#         else:
#             return jsonify(result), 400
            
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": f"服务器错误: {str(e)}",
#             "data": None
#         }), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """健康检查接口"""
#     return jsonify({
#         "status": "healthy",
#         "message": "紫微斗数API服务正常运行"
#     })

# @app.route('/', methods=['GET'])
# def index():
#     """首页"""
#     return jsonify({
#         "name": "紫微斗数排盘API",
#         "version": "1.0.0",
#         "description": "基于iztro库的紫微斗数排盘服务（已修复）",
#         "endpoints": {
#             "/api/ziwei/astrolabe": "POST - 生成紫微斗数星盘",
#             "/api/health": "GET - 健康检查"
#         }
#     })

# if __name__ == '__main__':
#     print("🌟 紫微斗数API服务启动中（修复版）...")
#     print("📡 服务地址: http://localhost:5000")
#     print("🔍 健康检查: http://localhost:5000/api/health")
#     print("📚 API文档: http://localhost:5000")
#     app.run(host='0.0.0.0', port=5000, debug=True)
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
            print(f"🔧 Debug: 当前工作目录: {current_dir}")
            print(f"🔧 Debug: 脚本文件路径: {self.script_path}")
            print(f"🔧 Debug: 执行参数: {birth_date} {birth_hour_index} {gender} {fix_leap}")
            
            result = subprocess.run([
                'node', self.script_path,
                birth_date, str(birth_hour_index), gender, str(fix_leap).lower()
            ], capture_output=True, text=True, encoding='utf-8', cwd=current_dir)
            
            print(f"🔧 Debug: 返回码: {result.returncode}")
            if result.stderr:
                print(f"🔧 Debug: stderr: {result.stderr}")
            
            if result.returncode == 0:
                try:
                    astrolabe_data = json.loads(result.stdout)
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
        "message": "紫微斗数API服务正常运行 v2"
    })

@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "name": "紫微斗数排盘API v2",
        "version": "1.0.0",
        "description": "基于iztro库的紫微斗数排盘服务（使用固定脚本）",
        "endpoints": {
            "/api/ziwei/astrolabe": "POST - 生成紫微斗数星盘",
            "/api/health": "GET - 健康检查"
        }
    })

if __name__ == '__main__':
    import os
    # 支持云平台的PORT环境变量
    port = int(os.environ.get('PORT', 5002))
    print("🌟 紫微斗数API服务启动中 v2...")
    print(f"📡 服务地址: http://0.0.0.0:{port}")
    print("🔍 健康检查: /api/health")
    print("📚 API文档: /")
    app.run(host='0.0.0.0', port=port, debug=False)  # 生产模式