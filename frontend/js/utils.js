// 工具函数

/**
 * 读取文件并转换为 Data URL
 * @param {File} file - 要读取的文件
 * @returns {Promise<string>} - 返回数据 URL
 */
function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(file);
    });
}

/**
 * 显示通知消息
 * @param {Object} vm - Vue 实例
 * @param {Object} options - 通知选项
 */
function showNotification(vm, options) {
    const defaults = {
        duration: 3000,
        showClose: true,
        type: 'info'
    };
    
    vm.$message(Object.assign({}, defaults, options));
}

/**
 * 格式化日期时间
 * @param {Date} date - 日期对象
 * @param {string} format - 格式模板
 * @returns {string} - 格式化后的日期字符串
 */
function formatDateTime(date, format = 'YYYY-MM-DD_HHmmss') {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 生成文件名
 * @param {string} prefix - 文件名前缀
 * @param {string} extension - 文件扩展名
 * @returns {string} - 生成的文件名
 */
function generateFileName(prefix = 'processed_photo', extension = 'jpg') {
    const timestamp = formatDateTime(new Date());
    return `${prefix}_${timestamp}.${extension}`;
}

/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} - 防抖处理后的函数
 */
function debounce(func, wait = 300) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
} 