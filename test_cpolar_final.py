import requests
import json

def test_cpolar_api():
    # 使用你的实际cpolar地址
    BASE_URL = "https://487d0592.r19.vip.cpolar.cn"
    
    print(f"🌐 测试cpolar API: {BASE_URL}")
    print("="*50)
    
    # 1. 健康检查
    print("📊 测试1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 健康检查成功: {result['message']}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False
    
    # 2. API信息
    print("\n📋 测试2: API信息")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API名称: {result['name']}")
            print(f"✅ API版本: {result['version']}")
        else:
            print(f"❌ API信息获取失败: {response.status_code}")
    except Exception as e:
        print(f"❌ API信息获取异常: {e}")
    
    # 3. 紫微排盘功能测试
    print("\n🔮 测试3: 紫微排盘功能")
    test_data = {
        "birth_date": "2000-8-16",
        "birth_time": "14:30", 
        "gender": "女",
        "fix_leap": True
    }
    
    print(f"输入数据: {test_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ziwei/astrolabe", 
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ 公网排盘成功!")
                
                time_info = result['data']['time_info']
                astrolabe = result['data']['astrolabe']
                
                print(f"📅 时间解析: {time_info['parsed_result']}")
                print(f"👤 性别: {astrolabe['gender']}")
                print(f"📆 阳历: {astrolabe['solarDate']}")
                print(f"🌙 农历: {astrolabe['lunarDate']}")
                print(f"⭐ 星座: {astrolabe['sign']}")
                print(f"🐾 生肖: {astrolabe['zodiac']}")
                print(f"🏮 五行局: {astrolabe['fiveElementsClass']}")
                
                print("\n🎉 所有测试通过！API可以正常通过公网访问！")
                print("✅ 现在可以在Coze中创建插件了！")
                return True
            else:
                print(f"❌ 排盘失败: {result['error']}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 排盘测试失败: {e}")
        return False

if __name__ == "__main__":
    test_cpolar_api()