import requests
import json
import time

def test_ziwei_complete():
    """完整测试紫微斗数API"""
    
    print("🚀 开始完整测试紫微斗数API...")
    print("="*50)
    
    # 测试1：健康检查
    print("📊 测试1: 健康检查")
    try:
        response = requests.get("http://localhost:5002/api/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 健康检查成功: {result['message']}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False
    
    # 测试2：API信息
    print("\n📋 测试2: API信息")
    try:
        response = requests.get("http://localhost:5002/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API名称: {result['name']}")
            print(f"✅ API版本: {result['version']}")
        else:
            print(f"❌ API信息获取失败: {response.status_code}")
    except Exception as e:
        print(f"❌ API信息获取异常: {e}")
    
    # 测试3：紫微排盘功能
    print("\n🔮 测试3: 紫微排盘功能")
    
    test_cases = [
        {
            "name": "标准格式测试",
            "data": {
                "birth_date": "2000-8-16",
                "birth_time": "14:30",
                "gender": "女",
                "fix_leap": True
            }
        },
        {
            "name": "数字格式测试", 
            "data": {
                "birth_date": "1995-12-3",
                "birth_time": "0830",
                "gender": "男",
                "fix_leap": True
            }
        },
        {
            "name": "点号格式测试",
            "data": {
                "birth_date": "1988-5-20",
                "birth_time": "23.45",
                "gender": "女",
                "fix_leap": False
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  测试3.{i}: {test_case['name']}")
        print(f"  输入数据: {test_case['data']}")
        
        try:
            response = requests.post(
                "http://localhost:5002/api/ziwei/astrolabe", 
                json=test_case['data'],
                timeout=30  # 30秒超时
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("  ✅ 排盘成功!")
                    
                    # 显示关键信息
                    time_info = result['data']['time_info']
                    astrolabe = result['data']['astrolabe']
                    
                    print(f"  📅 时间解析: {time_info['parsed_result']}")
                    print(f"  👤 性别: {astrolabe['gender']}")
                    print(f"  📆 阳历: {astrolabe['solarDate']}")
                    print(f"  🌙 农历: {astrolabe['lunarDate']}")
                    print(f"  ⭐ 星座: {astrolabe['sign']}")
                    print(f"  🐾 生肖: {astrolabe['zodiac']}")
                    print(f"  🏮 五行局: {astrolabe['fiveElementsClass']}")
                    print(f"  💫 命主: {astrolabe['soul']}")
                    print(f"  🎭 身主: {astrolabe['body']}")
                    
                    # 显示命宫信息
                    palaces = astrolabe['palaces']
                    ming_palace = next((p for p in palaces if p['name'] == '命'), None)
                    if ming_palace:
                        print(f"  🏮 命宫: {ming_palace['heavenlyStem']}{ming_palace['earthlyBranch']}")
                        if ming_palace['majorStars']:
                            stars = [star['name'] for star in ming_palace['majorStars']]
                            print(f"      主星: {', '.join(stars)}")
                    
                else:
                    print(f"  ❌ 排盘失败: {result['error']}")
                    return False
            else:
                print(f"  ❌ HTTP错误: {response.status_code}")
                print(f"  错误内容: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("  ❌ 请求超时，可能Node.js依赖未安装或iztro库有问题")
            return False
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
            return False
        
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "="*50)
    print("🎉 所有测试完成！API功能正常！")
    print("✅ 可以进行下一步：部署到云端或配置Coze插件")
    return True

if __name__ == "__main__":
    test_ziwei_complete()