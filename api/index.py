from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess
import os
import re
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZiweiAPI:
    def __init__(self):
        """初始化ZiweiAPI，支持多种部署环境"""
        # 检测运行环境
        self.is_vercel = os.environ.get('VERCEL') == '1'
        self.is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        self.is_render = os.environ.get('RENDER') is not None
        
        # 根据环境设置路径 - 针对api/目录结构优化
        if self.is_vercel:
            # Vercel环境：脚本在根目录，Python在api/目录
            self.script_path = '/var/task/api/ziwei_node_script.js'
            self.node_path = 'node'
        elif self.is_railway or self.is_render:
            # Railway/Render环境：从api目录访问根目录
            self.script_path = os.path.join('..', 'ziwei_node_script.js')
            self.node_path = 'node'
        else:
            # 本地开发环境：从api目录访问根目录
            self.script_path = os.path.join('..', 'ziwei_node_script.js')
            self.node_path = 'node'
        
        logger.info(f"🌍 环境检测: Vercel={self.is_vercel}, Railway={self.is_railway}, Render={self.is_render}")
        logger.info(f"📁 脚本路径: {self.script_path}")
        logger.info(f"📂 当前工作目录: {os.getcwd()}")

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

    def check_environment(self) -> Dict[str, bool]:
        """检查运行环境和依赖"""
        checks = {
            "node_available": False,
            "script_exists": False,
            "node_modules_exists": False,
            "iztro_available": False
        }
        
        # 检查Node.js
        try:
            result = subprocess.run([self.node_path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                checks["node_available"] = True
                logger.info(f"✅ Node.js版本: {result.stdout.strip()}")
        except Exception as e:
            logger.error(f"❌ Node.js检查失败: {e}")
        
        # 检查脚本文件
        if os.path.exists(self.script_path):
            checks["script_exists"] = True
            logger.info(f"✅ 脚本文件存在: {self.script_path}")
        else:
            logger.error(f"❌ 脚本文件不存在: {self.script_path}")
            # 调试信息
            logger.error(f"📂 当前目录: {os.getcwd()}")
            try:
                logger.error(f"📁 当前目录文件: {os.listdir('.')}")
                if not self.is_vercel:
                    logger.error(f"📁 父目录文件: {os.listdir('..')}")
            except Exception as e:
                logger.error(f"📁 无法列出目录: {e}")
        
        # 检查node_modules - 针对不同环境的路径
        node_modules_paths = []
        
        if self.is_vercel:
            node_modules_paths = [
                '/var/task/node_modules',  # Vercel主路径
                '/opt/node_modules',       # Vercel备用路径
            ]
        else:
            node_modules_paths = [
                os.path.join('..', 'node_modules'),              # 相对于api目录
                os.path.join(os.getcwd(), '..', 'node_modules'), # 绝对路径
                'node_modules',                                   # 当前目录（备用）
            ]
        
        for path in node_modules_paths:
            if os.path.exists(path):
                checks["node_modules_exists"] = True
                logger.info(f"✅ node_modules存在: {path}")
                
                # 检查iztro
                iztro_path = os.path.join(path, 'iztro')
                if os.path.exists(iztro_path):
                    checks["iztro_available"] = True
                    logger.info(f"✅ iztro库可用: {iztro_path}")
                break
        
        if not checks["node_modules_exists"]:
            logger.error(f"❌ 在以下路径均未找到node_modules: {node_modules_paths}")
        
        return checks

    def generate_astrolabe(self, birth_date: str, birth_time: str, gender: str, fix_leap: bool = True) -> Dict:
        """生成星盘API - Vercel api/目录优化版"""
        # 解析时间
        birth_hour_index, time_chen_name, time_result = self.parse_time_input(birth_time)
        
        if birth_hour_index is None:
            return {
                "success": False,
                "error": time_result,
                "data": None
            }
        
        # 环境检查
        env_checks = self.check_environment()
        if not env_checks["node_available"]:
            return {
                "success": False,
                "error": "Node.js环境不可用",
                "data": None,
                "environment": env_checks
            }
        
        if not env_checks["script_exists"]:
            return {
                "success": False,
                "error": f"脚本文件不存在: {self.script_path}",
                "data": None,
                "environment": env_checks
            }
        
        if not env_checks["iztro_available"]:
            return {
                "success": False,
                "error": "iztro库不可用，请检查node_modules",
                "data": None,
                "environment": env_checks
            }
        
        try:
            # 构建执行命令
            cmd = [
                self.node_path,
                self.script_path,
                birth_date,
                str(birth_hour_index),
                gender,
                str(fix_leap).lower()
            ]
            
            logger.info(f"🚀 执行命令: {' '.join(cmd)}")
            
            # 设置环境变量和工作目录
            env = os.environ.copy()
            
            if self.is_vercel:
                # Vercel环境设置
                cwd = '/var/task'
                env['NODE_PATH'] = '/var/task/node_modules'
            else:
                # 其他环境：切换到父目录（项目根目录）
                cwd = os.path.abspath(os.path.join(os.getcwd(), '..'))
                env['NODE_PATH'] = os.path.join(cwd, 'node_modules')
            
            logger.info(f"📁 工作目录: {cwd}")
            logger.info(f"🔧 NODE_PATH: {env.get('NODE_PATH')}")
            
            # 执行Node.js脚本
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30,  # 30秒超时
                env=env,
                cwd=cwd
            )
            
            logger.info(f"📤 返回码: {result.returncode}")
            if result.stderr:
                logger.warning(f"⚠️ stderr: {result.stderr}")
            if result.stdout:
                logger.info(f"📝 stdout长度: {len(result.stdout)}")
            
            if result.returncode == 0:
                try:
                    astrolabe_data = json.loads(result.stdout)
                    logger.info("✅ 排盘成功！")
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
                            },
                            "environment": {
                                "platform": "vercel" if self.is_vercel else "railway" if self.is_railway else "render" if self.is_render else "local",
                                "timestamp": datetime.now().isoformat(),
                                "cwd": cwd,
                                "script_path": self.script_path
                            }
                        }
                    }
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON解析失败: {e}")
                    logger.error(f"📝 原始输出: {result.stdout[:200]}...")
                    return {
                        "success": False,
                        "error": f"JSON解析失败: {str(e)}",
                        "data": {
                            "raw_output": result.stdout[:500],  # 限制输出长度
                            "stderr": result.stderr
                        }
                    }
            else:
                logger.error(f"❌ Node.js执行失败: {result.stderr}")
                return {
                    "success": False,
                    "error": f"Node.js执行失败",
                    "data": {
                        "stderr": result.stderr,
                        "stdout": result.stdout,
                        "returncode": result.returncode,
                        "cmd": ' '.join(cmd),
                        "cwd": cwd
                    }
                }
                
        except subprocess.TimeoutExpired:
            logger.error("⏰ 请求超时")
            return {
                "success": False,
                "error": "请求超时（30秒），请稍后重试",
                "data": None
            }
        except Exception as e:
            logger.error(f"💥 执行错误: {e}")
            return {
                "success": False,
                "error": f"系统错误: {str(e)}",
                "data": {
                    "exception_type": type(e).__name__,
                    "cwd": os.getcwd()
                }
            }

# 创建API实例
ziwei_api = ZiweiAPI()

@app.route('/api/ziwei/astrolabe', methods=['POST'])
def create_astrolabe():
    """紫微斗数排盘API接口"""
    try:
        data = request.get_json()
        
        # 验证请求体
        if not data:
            return jsonify({
                "success": False,
                "error": "请求体不能为空",
                "data": None
            }), 400
        
        # 验证必需参数
        required_fields = ['birth_date', 'birth_time', 'gender']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"缺少必需参数: {', '.join(missing_fields)}",
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
        
        # 验证日期格式（基本检查）
        try:
            # 尝试解析日期格式 YYYY-M-D
            date_parts = birth_date.split('-')
            if len(date_parts) != 3:
                raise ValueError("日期格式错误")
            year, month, day = map(int, date_parts)
            if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("日期范围错误")
        except ValueError:
            return jsonify({
                "success": False,
                "error": "日期格式错误，请使用 YYYY-M-D 格式（例如：2024-8-18）",
                "data": None
            }), 400
        
        logger.info(f"📥 收到排盘请求: {birth_date} {birth_time} {gender}")
        
        # 生成星盘
        result = ziwei_api.generate_astrolabe(birth_date, birth_time, gender, fix_leap)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"💥 API错误: {e}")
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}",
            "data": None
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    env_checks = ziwei_api.check_environment()
    
    return jsonify({
        "status": "healthy" if all(env_checks.values()) else "degraded",
        "message": "紫微斗数API服务运行中",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "platform": "vercel" if ziwei_api.is_vercel else "railway" if ziwei_api.is_railway else "render" if ziwei_api.is_render else "local",
            "checks": env_checks,
            "cwd": os.getcwd(),
            "script_path": ziwei_api.script_path
        }
    })

@app.route('/api/environment', methods=['GET'])
def environment_info():
    """环境信息接口（调试用）"""
    return jsonify({
        "environment": {
            "vercel": ziwei_api.is_vercel,
            "railway": ziwei_api.is_railway,
            "render": ziwei_api.is_render,
            "script_path": ziwei_api.script_path,
            "node_path": ziwei_api.node_path,
            "cwd": os.getcwd(),
            "env_vars": {
                "VERCEL": os.environ.get('VERCEL'),
                "RAILWAY_ENVIRONMENT": os.environ.get('RAILWAY_ENVIRONMENT'),
                "RENDER": os.environ.get('RENDER'),
                "PORT": os.environ.get('PORT'),
                "NODE_PATH": os.environ.get('NODE_PATH')
            }
        },
        "checks": ziwei_api.check_environment(),
        "debug_info": {
            "current_files": os.listdir('.') if os.path.exists('.') else [],
            "parent_files": os.listdir('..') if os.path.exists('..') else [],
        }
    })

@app.route('/', methods=['GET'])
def index():
    """API首页和文档"""
    return jsonify({
        "name": "紫微斗数排盘API",
        "version": "2.0.0",
        "description": "基于iztro库的紫微斗数排盘服务，支持云端部署",
        "endpoints": {
            "/": "GET - API文档",
            "/api/ziwei/astrolabe": "POST - 生成紫微斗数星盘",
            "/api/health": "GET - 健康检查",
            "/api/environment": "GET - 环境信息（调试）"
        },
        "usage": {
            "method": "POST",
            "url": "/api/ziwei/astrolabe",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "birth_date": "2004-8-18",
                "birth_time": "09:30",
                "gender": "男",
                "fix_leap": True
            }
        },
        "examples": {
            "curl": "curl -X POST https://your-app.vercel.app/api/ziwei/astrolabe -H 'Content-Type: application/json' -d '{\"birth_date\":\"2004-8-18\",\"birth_time\":\"09:30\",\"gender\":\"男\",\"fix_leap\":true}'",
            "response": {
                "success": True,
                "error": None,
                "data": {
                    "astrolabe": "...",
                    "time_info": "..."
                }
            }
        },
        "author": "紫微斗数开发团队",
        "timestamp": datetime.now().isoformat()
    })

# Vercel无服务器函数入口点 - 关键！
def handler(request):
    """Vercel WSGI入口函数"""
    return app(request.environ, lambda *args: None)

# 导出app给Vercel使用
app_handler = app

if __name__ == '__main__':
    # 本地开发模式
    port = int(os.environ.get('PORT', 5002))
    
    print("🌟 紫微斗数API服务启动中...")
    print(f"📡 服务地址: http://0.0.0.0:{port}")
    print(f"🔍 健康检查: /api/health")
    print(f"📚 API文档: /")
    print(f"🌍 环境信息: /api/environment")
    print(f"📁 当前目录: {os.getcwd()}")
    
    # 启动Flask开发服务器
    app.run(host='0.0.0.0', port=port, debug=False)