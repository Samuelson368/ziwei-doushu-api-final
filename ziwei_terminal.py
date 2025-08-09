#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数终端排盘工具
直接在VSCode终端中显示排盘结果
"""

import json
import subprocess
import sys
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class ZiweiTerminal:
    """紫微斗数终端排盘器"""
    
    def __init__(self):
        """初始化排盘器"""
        self.node_script = self._create_node_script()
        
        # 时辰对应表：(开始时间, 结束时间, 时辰名, 索引)
        self.time_periods = [
            (23, 0, 1, 0, "子时", 0),   # 23:00-01:00 (跨日)
            (1, 0, 3, 0, "丑时", 1),    # 01:00-03:00
            (3, 0, 5, 0, "寅时", 2),    # 03:00-05:00
            (5, 0, 7, 0, "卯时", 3),    # 05:00-07:00
            (7, 0, 9, 0, "辰时", 4),    # 07:00-09:00
            (9, 0, 11, 0, "巳时", 5),   # 09:00-11:00
            (11, 0, 13, 0, "午时", 6),  # 11:00-13:00
            (13, 0, 15, 0, "未时", 7),  # 13:00-15:00
            (15, 0, 17, 0, "申时", 8),  # 15:00-17:00
            (17, 0, 19, 0, "酉时", 9),  # 17:00-19:00
            (19, 0, 21, 0, "戌时", 10), # 19:00-21:00
            (21, 0, 23, 0, "亥时", 11), # 21:00-23:00
        ]
    
    def parse_time_input(self, time_str: str) -> Tuple[Optional[int], Optional[str], str]:
        """
        解析时间输入并返回对应的时辰索引
        
        Args:
            time_str: 时间字符串，如 "14:30", "14：30", "1430", "14.30" 等
            
        Returns:
            Tuple[时辰索引, 时辰名称, 时间范围字符串]
        """
        if not time_str:
            return None, None, ""
        
        # 清理输入，移除空格
        time_str = time_str.strip()
        
        # 支持多种格式：14:30, 14：30, 1430, 14.30, 14-30
        patterns = [
            r'^(\d{1,2})[:\：\.\-](\d{2})$',  # 14:30, 14：30, 14.30, 14-30
            r'^(\d{3,4})$',                    # 1430
            r'^(\d{1,2})$'                     # 14 (只有小时)
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
                    if len(match.group(1)) >= 3:  # 1430格式
                        time_digits = match.group(1)
                        if len(time_digits) == 3:  # 930
                            hour = int(time_digits[0])
                            minute = int(time_digits[1:])
                        else:  # 1430
                            hour = int(time_digits[:2])
                            minute = int(time_digits[2:])
                    else:  # 只有小时
                        hour = int(match.group(1))
                        minute = 0
                break
        
        if hour is None:
            return None, None, f"无法解析时间格式: {time_str}"
        
        # 验证时间有效性
        if not (0 <= hour <= 23):
            return None, None, f"小时必须在0-23之间: {hour}"
        
        if minute is None:
            minute = 0
        
        if not (0 <= minute <= 59):
            return None, None, f"分钟必须在0-59之间: {minute}"
        
        # 判断时辰
        time_chen_index, time_chen_name, time_range = self._get_time_chen(hour, minute)
        
        return time_chen_index, time_chen_name, f"{hour:02d}:{minute:02d} → {time_chen_name} ({time_range})"
    
    def _get_time_chen(self, hour: int, minute: int) -> Tuple[int, str, str]:
        """
        根据小时和分钟判断时辰
        
        Args:
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            
        Returns:
            Tuple[时辰索引, 时辰名称, 时间范围]
        """
        # 转换为分钟数便于比较
        total_minutes = hour * 60 + minute
        
        # 子时特殊处理（23:00-01:00，跨日）
        if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
            return 0, "子时", "23:00-01:00"
        
        # 其他时辰
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
        
        # 默认返回（理论上不会到达这里）
        return 0, "子时", "23:00-01:00"
        
    def _create_node_script(self) -> str:
        """创建Node.js脚本内容"""
        return '''
// 检查是否有iztro库
try {
    var iztro = require('./node_modules/iztro');
} catch (error) {
    console.error('错误：无法加载iztro库');
    console.error('请先运行：npm install iztro');
    process.exit(1);
}

// 获取命令行参数
const args = process.argv.slice(2);
if (args.length < 4) {
    console.error('参数不足：需要 日期 时辰 性别 是否修正闰年');
    console.error('示例：node script.js "2000-8-16" 2 "女" true');
    process.exit(1);
}

const [date, hour, gender, fixLeap] = args;

console.error(`调试信息: 日期=${date}, 时辰=${hour}, 性别=${gender}, 修正闰年=${fixLeap}`);

try {
    // 生成星盘 - 使用iztro官方API
    const astrolabe = iztro.astro.bySolar(
        date,                    // 阳历日期字符串
        parseInt(hour),          // 时辰索引 0-11
        gender,                  // 性别 "男"/"女"
        fixLeap === 'true',      // 是否修正闰年
        'zh-CN'                  // 语言
    );
    
    console.error('排盘成功，正在输出结果...');
    
    // 输出JSON格式结果到stdout
    console.log(JSON.stringify(astrolabe, null, 2));
    
} catch (error) {
    console.error('排盘失败:', error.message);
    console.error('错误详情:', error);
    process.exit(1);
}
'''

    def _write_node_script(self) -> str:
        """写入Node.js脚本文件"""
        script_path = 'temp_ziwei_script.js'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(self.node_script)
        return script_path
    
    def generate_astrolabe(self, birth_date: str, birth_hour: int, gender: str, fix_leap: bool = True) -> Optional[Dict]:
        """
        生成星盘
        
        Args:
            birth_date: 出生日期，格式如 "2000-8-16"
            birth_hour: 出生时辰 (0-11)
            gender: 性别 "男" 或 "女"
            fix_leap: 是否修正闰年
            
        Returns:
            星盘数据字典，失败返回None
        """
        # 检查node_modules是否存在
        if not os.path.exists('node_modules/iztro'):
            print("❌ 错误：未找到 node_modules/iztro")
            print("请先运行：npm install iztro")
            return None
        
        script_path = self._write_node_script()
        
        try:
            print(f"🔄 正在调用Node.js排盘...")
            print(f"   参数: {birth_date} {birth_hour} {gender} {fix_leap}")
            
            # 调用Node.js脚本
            result = subprocess.run([
                'node', script_path,
                birth_date, str(birth_hour), gender, str(fix_leap).lower()
            ], capture_output=True, text=True, encoding='utf-8')
            
            # 显示调试信息
            if result.stderr:
                print(f"🔧 调试信息: {result.stderr}")
            
            if result.returncode == 0:
                try:
                    # 解析JSON结果
                    astrolabe_data = json.loads(result.stdout)
                    print("✅ 星盘数据获取成功！")
                    return astrolabe_data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"原始输出: {result.stdout[:500]}...")
                    return None
            else:
                print(f"❌ Node.js执行失败（返回码: {result.returncode}）")
                print(f"错误信息: {result.stderr}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 调用Node.js失败：{e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ 解析JSON失败：{e}")
            return None
        except FileNotFoundError:
            print("❌ 未找到Node.js，请确保已安装Node.js")
            return None
        finally:
            # 清理临时文件
            if os.path.exists(script_path):
                os.remove(script_path)
    
    def display_all_palaces_info(self, astrolabe_data: Dict) -> None:
        """显示所有宫位详细信息"""
        if not astrolabe_data:
            print("❌ 无星盘数据")
            return
            
        print("🌟" + "="*60 + "🌟")
        print("               紫微斗数完整星盘")
        print("🌟" + "="*60 + "🌟")
        
        # 基本信息
        print(f"\n📅 基本信息")
        print("-" * 40)
        print(f"性别：{astrolabe_data.get('gender', '未知')}")
        print(f"阳历：{astrolabe_data.get('solarDate', '未知')}")
        print(f"农历：{astrolabe_data.get('lunarDate', '未知')}")
        print(f"时辰：{astrolabe_data.get('time', '未知')} ({astrolabe_data.get('timeRange', '未知')})")
        print(f"星座：{astrolabe_data.get('sign', '未知')}")
        print(f"生肖：{astrolabe_data.get('zodiac', '未知')}")
        print(f"五行局：{astrolabe_data.get('fiveElementsClass', '未知')}")
        print(f"命主：{astrolabe_data.get('soul', '未知')}")
        print(f"身主：{astrolabe_data.get('body', '未知')}")
        
        # 获取命宫和身宫位置
        soul_branch = astrolabe_data.get('earthlyBranchOfSoulPalace', '')
        body_branch = astrolabe_data.get('earthlyBranchOfBodyPalace', '')
        
        print(f"\n🏮 十二宫位星耀分布")
        print("=" * 60)
        
        # 显示所有宫位
        palaces = astrolabe_data.get('palaces', [])
        
        # 按传统顺序显示十二宫
        palace_order = ["命", "兄弟", "夫妻", "子女", "财帛", "疾厄", 
                       "迁移", "交友", "官禄", "田宅", "福德", "父母"]
        
        # 创建宫位名称映射
        palace_map = {}
        for palace in palaces:
            palace_name = palace.get('name', '')
            if palace_name in palace_order:
                palace_map[palace_name] = palace
        
        for palace_name in palace_order:
            if palace_name in palace_map:
                palace = palace_map[palace_name]
                self._display_single_palace(palace, soul_branch, body_branch)
        
        print("\n🌟" + "="*60 + "🌟")
        print("               星盘显示完成")
        print("🌟" + "="*60 + "🌟")
    
    def _get_star_meaning(self, star_name: str) -> str:
        """获取星耀含义"""
        star_meanings = {
            "紫微": "帝王星，主尊贵、权威、领导能力",
            "天机": "智慧星，主聪明、策划、变动",
            "太阳": "光明星，主热情、积极、奉献",
            "武曲": "财星，主务实、理财、执行力",
            "天同": "福星，主温和、知足、人缘好",
            "廉贞": "囚星，主感情丰富、魅力、艺术",
            "天府": "财库星，主稳重、保守、财库",
            "太阴": "母亲星，主温柔、细腻、内敛",
            "贪狼": "桃花星，主多才、社交、欲望",
            "巨门": "暗星，主口才、是非、深沉",
            "天相": "印星，主辅助、协调、服务",
            "天梁": "老人星，主稳重、慈善、化解",
            "七杀": "将军星，主冲动、开创、竞争",
            "破军": "消耗星，主破坏、重建、变化",
            "文昌": "文星，主文才、学习、考试",
            "文曲": "文星，主口才、多艺、应变",
            "左辅": "助星，主贵人、辅助、合作",
            "右弼": "助星，主协调、团队、执行",
            "天魁": "贵人星，主提拔、机会、地位",
            "天钺": "贵人星，主暗助、缘分、运气",
            "化禄": "财星，主财运、享受、缘分",
            "化权": "权星，主权力、能力、主导",
            "化科": "名星，主名声、考试、贵人",
            "化忌": "忌星，主阻碍、执着、专注"
        }
        return star_meanings.get(star_name, "")
    
    def _get_mutagen_meaning(self, mutagen: str) -> str:
        """获取四化含义"""
        mutagen_meanings = {
            "禄": "增加财运和享受，带来缘分和机会",
            "权": "增强权威和能力，提升主导性",
            "科": "带来名声和贵人，利于考试文书",
            "忌": "带来阻碍和困扰，但也代表专注执着"
        }
        return mutagen_meanings.get(mutagen, "")
    
    def _display_single_palace(self, palace: Dict, soul_branch: str, body_branch: str) -> None:
        """显示单个宫位信息"""
        palace_name = palace.get('name', '')
        earthly_branch = palace.get('earthlyBranch', '')
        heavenly_stem = palace.get('heavenlyStem', '')
        
        # 判断是否为命宫或身宫
        is_soul_palace = earthly_branch == soul_branch
        is_body_palace = earthly_branch == body_branch
        
        # 宫位标题
        palace_indicators = []
        if is_soul_palace:
            palace_indicators.append("命")
        if is_body_palace:
            palace_indicators.append("身")
        
        indicator_str = f" [{', '.join(palace_indicators)}]" if palace_indicators else ""
        
        print(f"\n🏮 {palace_name}宫 ({heavenly_stem}{earthly_branch}){indicator_str}")
        print("-" * 50)
        
        # 获取星耀
        major_stars = palace.get('majorStars', [])
        minor_stars = palace.get('minorStars', [])
        adjective_stars = palace.get('adjectiveStars', [])
        
        # 显示主星
        if major_stars:
            print(f"⭐ 主星 ({len(major_stars)}颗):")
            for star in major_stars:
                star_name = star.get('name', '未知')
                brightness = star.get('brightness', '')
                mutagen = star.get('mutagen', '')
                
                star_info = f"  • {star_name}"
                if brightness:
                    star_info += f" ({brightness})"
                if mutagen:
                    star_info += f" [化{mutagen}]"
                
                print(star_info)
        else:
            print("⭐ 主星: 无主星（空宫）")
        
        # 显示辅星
        if minor_stars:
            print(f"🌟 辅星 ({len(minor_stars)}颗):")
            for star in minor_stars:
                star_name = star.get('name', '未知')
                mutagen = star.get('mutagen', '')
                
                star_info = f"  • {star_name}"
                if mutagen:
                    star_info += f" [化{mutagen}]"
                
                print(star_info)
        
        # 显示杂耀（只显示前6颗，避免太多）
        if adjective_stars:
            display_count = min(6, len(adjective_stars))
            remaining = len(adjective_stars) - display_count
            
            print(f"✨ 杂耀 ({len(adjective_stars)}颗，显示前{display_count}颗):")
            for star in adjective_stars[:display_count]:
                star_name = star.get('name', '未知')
                print(f"  • {star_name}")
            
            if remaining > 0:
                print(f"  ... 还有{remaining}颗杂耀")
        
        # 如果所有星耀都没有，标记为完全空宫
        if not major_stars and not minor_stars and not adjective_stars:
            print("📝 此宫完全无星")
        
        # 四化星统计
        all_mutagens = []
        for star_list in [major_stars, minor_stars, adjective_stars]:
            for star in star_list:
                mutagen = star.get('mutagen', '')
                if mutagen:
                    all_mutagens.append(f"{star.get('name', '')}化{mutagen}")
        
        if all_mutagens:
            print(f"🔮 四化: {', '.join(all_mutagens)}")

def main():
    """主函数"""
    print("🌟 紫微斗数终端排盘工具")
    print("="*40)
    
    # 创建排盘器
    ziwei = ZiweiTerminal()
    
    try:
        # 获取用户输入
        print("\n请输入出生信息：")
        birth_date = input("出生日期 (格式: 2000-8-16): ").strip()
        if not birth_date:
            birth_date = "2000-8-16"  # 默认值
            
        print("\n⏰ 出生时间输入说明：")
        print("支持多种格式：")
        print("  • 14:30 或 14：30 (标准格式)")
        print("  • 1430 (连续数字)")
        print("  • 14.30 或 14-30 (其他分隔符)")
        print("  • 14 (只输入小时，分钟默认为00)")
        print("\n📅 时辰对应关系：")
        print("  子时(23:00-01:00) 丑时(01:00-03:00) 寅时(03:00-05:00) 卯时(05:00-07:00)")
        print("  辰时(07:00-09:00) 巳时(09:00-11:00) 午时(11:00-13:00) 未时(13:00-15:00)")
        print("  申时(15:00-17:00) 酉时(17:00-19:00) 戌时(19:00-21:00) 亥时(21:00-23:00)")
        
        while True:
            birth_time = input("\n请输入出生时间 (如: 14:30): ").strip()
            if not birth_time:
                birth_time = "14:30"  # 默认值
            
            # 解析时间
            birth_hour_index, time_chen_name, time_result = ziwei.parse_time_input(birth_time)
            
            if birth_hour_index is not None:
                print(f"✅ 时间解析结果: {time_result}")
                break
            else:
                print(f"❌ {time_result}")
                print("请重新输入正确的时间格式")
        
        gender = input("\n性别 (男/女): ").strip()
        if gender not in ["男", "女"]:
            gender = "女"  # 默认值
            
        print(f"\n正在排盘...")
        print(f"出生日期: {birth_date}")
        print(f"出生时间: {time_result}")
        print(f"性别: {gender}")
        
        # 生成星盘
        astrolabe_data = ziwei.generate_astrolabe(birth_date, birth_hour_index, gender)
        
        if astrolabe_data:
            # 显示所有宫位信息
            ziwei.display_all_palaces_info(astrolabe_data)
        else:
            print("❌ 排盘失败，请检查输入信息和环境配置")
            
    except KeyboardInterrupt:
        print("\n\n👋 已退出程序")
    except Exception as e:
        print(f"❌ 程序错误: {e}")

if __name__ == "__main__":
    main()