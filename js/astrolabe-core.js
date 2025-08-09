// 紫微斗数核心功能模块
class AstrolabeCore {
    constructor() {
        this.currentAstrolabe = null;
    }
    
    // 生成星盘
    generateAstrolabe(birthDate, birthTime, gender, dateType = 'solar') {
        try {
            if (dateType === 'solar') {
                this.currentAstrolabe = iztro.astro.bySolar(birthDate, birthTime, gender, true, 'zh-CN');
            } else {
                this.currentAstrolabe = iztro.astro.byLunar(birthDate, birthTime, gender, false, true, 'zh-CN');
            }
            return this.currentAstrolabe;
        } catch (error) {
            console.error('生成星盘失败：', error);
            throw error;
        }
    }
    
    // 查找星耀
    findStar(starName) {
        if (!this.currentAstrolabe) {
            throw new Error('请先生成星盘');
        }
        return this.currentAstrolabe.star(starName);
    }
    
    // 获取运限
    getHoroscope(date, hour = 0) {
        if (!this.currentAstrolabe) {
            throw new Error('请先生成星盘');
        }
        return this.currentAstrolabe.horoscope(date, hour);
    }
    
    // 查找化忌宫位
    findMutagenPalaces(mutagenType) {
        if (!this.currentAstrolabe) {
            throw new Error('请先生成星盘');
        }
        return this.currentAstrolabe.haveMutagen(mutagenType);
    }
    
    // 复杂查询：某星的三方四正是否有特定四化
    checkStarSurroundingMutagen(starName, mutagenType) {
        if (!this.currentAstrolabe) {
            throw new Error('请先生成星盘');
        }
        return this.currentAstrolabe.star(starName).surroundedPalaces().haveMutagen(mutagenType);
    }
}

// 导出模块
window.AstrolabeCore = AstrolabeCore;