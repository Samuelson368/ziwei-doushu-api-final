// 紫微斗数UI组件模块
class AstrolabeUI {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.core = new AstrolabeCore();
    }
    
    // 渲染输入表单
    renderInputForm() {
        const formHTML = `
            <div class="astrolabe-form">
                <h3>请输入出生信息</h3>
                <div class="form-row">
                    <div class="form-group">
                        <label>出生日期：</label>
                        <input type="date" id="birth-date" value="2000-08-16">
                    </div>
                    <div class="form-group">
                        <label>出生时辰：</label>
                        <select id="birth-time">
                            ${this.generateTimeOptions()}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>性别：</label>
                        <select id="gender">
                            <option value="女">女</option>
                            <option value="男">男</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>日期类型：</label>
                        <select id="date-type">
                            <option value="solar">阳历</option>
                            <option value="lunar">农历</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <button onclick="generateAndDisplay()" class="generate-btn">开始排盘</button>
                    </div>
                </div>
            </div>
        `;
        this.container.innerHTML = formHTML;
    }
    
    // 生成时辰选项
    generateTimeOptions() {
        const times = [
            '子时 (23:00-01:00)', '丑时 (01:00-03:00)', '寅时 (03:00-05:00)', '卯时 (05:00-07:00)',
            '辰时 (07:00-09:00)', '巳时 (09:00-11:00)', '午时 (11:00-13:00)', '未时 (13:00-15:00)',
            '申时 (15:00-17:00)', '酉时 (17:00-19:00)', '戌时 (19:00-21:00)', '亥时 (21:00-23:00)'
        ];
        return times.map((time, index) => 
            `<option value="${index}" ${index === 2 ? 'selected' : ''}>${time}</option>`
        ).join('');
    }
    
    // 生成并显示星盘
    generateAndDisplay() {
        try {
            const birthDate = document.getElementById('birth-date').value;
            const birthTime = parseInt(document.getElementById('birth-time').value);
            const gender = document.getElementById('gender').value;
            const dateType = document.getElementById('date-type').value;
            
            const astrolabe = this.core.generateAstrolabe(birthDate, birthTime, gender, dateType);
            this.displayAstrolabe(astrolabe);
        } catch (error) {
            alert('排盘失败：' + error.message);
        }
    }
    
    // 显示星盘
    displayAstrolabe(astrolabe) {
        const resultHTML = `
            <div class="astrolabe-result">
                ${this.renderBasicInfo(astrolabe)}
                ${this.renderPalaceGrid(astrolabe.palaces)}
                ${this.renderAnalysisTools()}
            </div>
        `;
        this.container.innerHTML += resultHTML;
    }
    
    // 渲染基础信息
    renderBasicInfo(astrolabe) {
        return `
            <div class="basic-info">
                <h3>基础信息</h3>
                <div class="info-grid">
                    <span>性别：${astrolabe.gender}</span>
                    <span>阳历：${astrolabe.solarDate}</span>
                    <span>农历：${astrolabe.lunarDate}</span>
                    <span>时辰：${astrolabe.time}</span>
                    <span>星座：${astrolabe.sign}</span>
                    <span>生肖：${astrolabe.zodiac}</span>
                    <span>命宫：${astrolabe.soul}</span>
                    <span>身宫：${astrolabe.body}</span>
                </div>
            </div>
        `;
    }
    
    // 渲染宫位网格
    renderPalaceGrid(palaces) {
        const palaceOrder = [4, 3, 2, 1, 5, -1, -1, 0, 6, 11, 10, 9, 7, -1, -1, 8];
        
        const gridHTML = palaceOrder.map((index, position) => {
            if (index === -1) {
                return position === 5 ? 
                    '<div class="palace-center">紫微斗数<br>星盘</div>' : 
                    '<div class="palace-empty"></div>';
            } else {
                const palace = palaces[index];
                return this.renderPalace(palace);
            }
        }).join('');
        
        return `
            <div class="palace-grid">
                ${gridHTML}
            </div>
        `;
    }
    
    // 渲染单个宫位
    renderPalace(palace) {
        const stars = [
            ...palace.majorStars.map(s => `<span class="star major">${s.name}</span>`),
            ...palace.minorStars.map(s => `<span class="star minor">${s.name}</span>`),
            ...palace.miscStars.slice(0, 5).map(s => `<span class="star misc">${s.name}</span>`)
        ].join('');
        
        return `
            <div class="palace" data-palace="${palace.name}">
                <div class="palace-name">${palace.name}</div>
                <div class="palace-branch">${palace.heavenlyStem}${palace.earthlyBranch}</div>
                <div class="palace-stars">${stars}</div>
            </div>
        `;
    }
    
    // 渲染分析工具
    renderAnalysisTools() {
        return `
            <div class="analysis-tools">
                <h3>分析工具</h3>
                <div class="tool-buttons">
                    <button onclick="findZiwei()" class="tool-btn">查找紫微星</button>
                    <button onclick="findJi()" class="tool-btn">查找化忌</button>
                    <button onclick="analyzePattern()" class="tool-btn">格局分析</button>
                </div>
                <div id="analysis-result" class="analysis-result"></div>
            </div>
        `;
    }
    
    // 分析工具方法
    findZiwei() {
        try {
            const result = this.core.findStar('紫微');
            document.getElementById('analysis-result').innerHTML = 
                `<p>紫微星位于：<strong>${result.palace().name}</strong></p>`;
        } catch (error) {
            console.error(error);
        }
    }
    
    findJi() {
        try {
            const result = this.core.findMutagenPalaces('忌');
            const palaceNames = result.map(p => p.name).join('、');
            document.getElementById('analysis-result').innerHTML = 
                `<p>化忌星位于：<strong>${palaceNames}</strong></p>`;
        } catch (error) {
            console.error(error);
        }
    }
    
    analyzePattern() {
        // 这里可以添加更复杂的格局分析逻辑
        document.getElementById('analysis-result').innerHTML = 
            '<p>格局分析功能开发中...</p>';
    }
}

// 导出模块
window.AstrolabeUI = AstrolabeUI;