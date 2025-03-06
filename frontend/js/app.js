// Vue 应用主逻辑
new Vue({
    el: '#app',
    data() {
        return {
            activeStep: 0,
            fileList: [],
            bgImageFileList: [],
            message: '',
            messageType: 'info',
            uploading: false,
            selectedColor: 'red',
            customColor: '#FF0000',
            selectedSize: 'original',
            showCustomColorPicker: false,
            showCustomImagePicker: false,
            showMosaicOption: false,
            originalImageUrl: '',
            processedImageUrl: '',
            processedFilePath: '',
            bgImageUrl: '',
            currentSourceColor: 'blue', // 默认源颜色
            presetColors: [
                { key: 'red', value: '#FF0000' },
                { key: 'blue', value: '#0000FF' },
                { key: 'white', value: '#FFFFFF' },
                { key: 'custom', value: '#FF00FF' },
            ],
            photoSizes: [
                { key: 'original', name: '原尺寸', dimensions: '原始尺寸' },
                { key: 'one_inch', name: '1寸照', dimensions: '25x35mm' },
                { key: 'two_inch', name: '2寸照', dimensions: '35x49mm' },
                { key: 'large_one_inch', name: '大1寸照', dimensions: '33x48mm' },
                { key: 'small_one_inch', name: '小1寸照', dimensions: '22x32mm' },
                { key: 'large_two_inch', name: '大2寸照', dimensions: '35x53mm' },
                { key: 'small_two_inch', name: '小2寸照', dimensions: '27x40mm' },
            ],
            activeTool: 'upload', // 默认显示上传工具
        };
    },
    computed: {
        canSubmit() {
            return this.fileList.length > 0;
        },
        previewBackgroundStyle() {
            if (this.selectedColor === 'mosaic') {
                return { backgroundImage: 'url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAA0SURBVHjaYvz//z8DJYCJgUIw8AawUMPQ/0S4kBTnsuBSRKkBo4E4GojUi0ZKDWAAEGAA9SsQWtS7QkwAAAAASUVORK5CYII=")' };
            } else if (this.selectedColor === 'custom') {
                return { backgroundColor: this.customColor };
            } else if (this.selectedColor === 'custom_image' && this.bgImageUrl) {
                return { backgroundImage: `url(${this.bgImageUrl})`, backgroundSize: 'cover' };
            } else {
                const colorMap = {
                    'red': '#FF0000',
                    'blue': '#0000FF',
                    'white': '#FFFFFF'
                };
                return { backgroundColor: colorMap[this.selectedColor] || '#FF0000' };
            }
        }
    },
    methods: {
        handleMenuSelect(index, indexPath) {
            console.log('菜单选择:', index, indexPath);
            
            // 重置显示选项
            this.showCustomColorPicker = false;
            this.showCustomImagePicker = false;
            this.showMosaicOption = false;
            
            // 处理换底色菜单
            if (index.startsWith('1-')) {
                // 确定源颜色
                if (index >= '1-1' && index <= '1-4') {
                    this.currentSourceColor = 'blue';
                } else if (index >= '1-5' && index <= '1-8') {
                    this.currentSourceColor = 'red';
                } else if (index >= '1-9' && index <= '1-12') {
                    this.currentSourceColor = 'white';
                }
                
                // 确定目标颜色和显示选项
                const targetIndex = parseInt(index.split('-')[1]) % 4;
                if (targetIndex === 1) { // 转红底或转蓝底
                    this.selectedColor = (this.currentSourceColor === 'blue') ? 'red' : 'blue';
                } else if (targetIndex === 2) { // 转白底
                    this.selectedColor = 'white';
                } else if (targetIndex === 3) { // 转自定义颜色
                    this.selectedColor = 'custom';
                    this.showCustomColorPicker = true;
                } else if (targetIndex === 0) { // 转自定义图片
                    this.selectedColor = 'custom_image';
                    this.showCustomImagePicker = true;
                    this.showMosaicOption = true;
                }
            }
            
            // 处理尺寸选择菜单
            if (index.startsWith('2-')) {
                const sizeIndex = parseInt(index.split('-')[1]) - 1;
                this.selectedSize = this.photoSizes[sizeIndex].key;
            }
        },
        selectPresetColor(colorKey) {
            this.selectedColor = colorKey;
            this.showCustomColorPicker = (colorKey === 'custom');
            this.showCustomImagePicker = (colorKey === 'custom_image');
        },
        selectSize(sizeKey) {
            this.selectedSize = sizeKey;
        },
        beforeUpload(file) {
            const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png';
            const isLt10M = file.size / 1024 / 1024 < 10;

            if (!isJPGOrPNG) {
                this.$message.error('上传图片只能是 JPG/PNG 格式!');
                return false;
            }
            if (!isLt10M) {
                this.$message.error('上传图片大小不能超过 10MB!');
                return false;
            }

            // 预览原始图片
            const reader = new FileReader();
            reader.onload = (e) => {
                this.originalImageUrl = e.target.result;
                console.log("图片已加载到预览区域");
            };
            reader.readAsDataURL(file);
            
            this.activeStep = 1;
            return true;
        },
        handleBgImageChange(file) {
            this.bgImageFileList = [file];
            
            if (file && file.raw) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.bgImageUrl = e.target.result;
                };
                reader.readAsDataURL(file.raw);
            }
        },
        handleProgress(event, file, fileList) {
            this.uploading = true;
        },
        handleSuccess(response, file, fileList) {
            this.uploading = false;
            this.message = response.message;
            this.messageType = 'success';
            this.activeStep = 2;
            
            // 使用后端返回的实际路径
            const processedUrl = '/processed/' + response.filename;
            console.log('处理后的图片URL:', processedUrl);
            this.processedImageUrl = processedUrl;
            this.processedFilePath = response.processed_path;
            
            this.$message({
                message: '照片处理成功！',
                type: 'success',
                duration: 3000,
                showClose: true,
                center: true
            });
        },
        handleError(err, file, fileList) {
            this.uploading = false;
            this.message = err.response ? err.response.data.error : '上传失败，请重试';
            this.messageType = 'error';
            this.$message({
                message: this.message,
                type: 'error',
                duration: 5000,
                showClose: true
            });
        },
        handleManualUpload(options) {
            console.log('准备手动上传文件');
            // 这是一个空方法，阻止自动上传
        },
        handleFileChange(file) {
            this.fileList = [file];
            console.log('文件已更新:', file);
            
            // 确保预览图片显示
            if (file && file.raw) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.originalImageUrl = e.target.result;
                    console.log("图片已加载到预览区域");
                    // 自动切换到颜色工具
                    this.activeTool = 'color';
                };
                reader.readAsDataURL(file.raw);
            }
        },
        submitUpload() {
            if (this.fileList.length === 0) {
                this.$message({
                    message: '请先选择要上传的照片',
                    type: 'warning',
                    duration: 3000,
                    showClose: true
                });
                return;
            }
            
            this.uploading = true;
            
            const formData = new FormData();
            formData.append('file', this.fileList[0].raw);
            formData.append('color', this.selectedColor);
            formData.append('size', this.selectedSize);
            
            // 显示处理中提示
            this.$message({
                message: '正在处理您的照片...',
                type: 'info',
                duration: 0,
                showClose: false
            });
            
            axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                this.uploading = false;
                this.processedImageUrl = '/processed/' + response.data.filename;
                
                // 关闭之前的消息
                this.$message.closeAll();
                
                // 显示成功消息
                this.$message({
                    message: '照片处理成功！',
                    type: 'success',
                    duration: 3000,
                    showClose: true
                });
            }).catch(error => {
                this.uploading = false;
                
                // 关闭之前的消息
                this.$message.closeAll();
                
                // 显示错误消息
                this.$message({
                    message: error.response ? error.response.data.error : '处理失败，请重试',
                    type: 'error',
                    duration: 5000,
                    showClose: true
                });
            });
        },
        downloadImage() {
            if (!this.processedImageUrl) {
                this.$message({
                    message: '没有可下载的图片',
                    type: 'warning',
                    duration: 3000,
                    showClose: true
                });
                return;
            }
            
            // 显示下载进度提示
            this.$message({
                message: '正在准备下载...',
                type: 'info',
                duration: 2000
            });
            
            // 创建下载链接
            const link = document.createElement('a');
            link.href = this.processedImageUrl;
            link.setAttribute('download', generateFileName('processed_photo'));
            document.body.appendChild(link);
            
            // 添加动画效果
            setTimeout(() => {
                link.click();
                document.body.removeChild(link);
                
                this.$message({
                    message: '图片下载中，请选择保存位置',
                    type: 'success',
                    duration: 3000,
                    showClose: true
                });
            }, 500);
        },
        handleToolSelect(tool) {
            this.activeTool = tool;
        },
        handleReset() {
            this.$confirm('确定要重置所有编辑吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.originalImageUrl = '';
                this.processedImageUrl = '';
                this.fileList = [];
                this.selectedColor = 'red';
                this.selectedSize = 'original';
                this.activeTool = 'upload';
                this.$message({
                    type: 'success',
                    message: '已重置'
                });
            }).catch(() => {});
        },
        handleColorChange(colorConfig) {
            console.log('颜色变更:', colorConfig);
            this.currentSourceColor = colorConfig.source;
            this.selectedColor = colorConfig.target;
            
            // 如果选择了自定义颜色，显示颜色选择器
            if (colorConfig.target === 'custom') {
                this.$prompt('请输入自定义颜色值 (HEX格式, 如: #FF5500)', '自定义颜色', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    inputPattern: /^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$/,
                    inputValue: this.customColor,
                    inputErrorMessage: '请输入正确的颜色值'
                }).then(({ value }) => {
                    this.customColor = value.startsWith('#') ? value : '#' + value;
                    this.$message({
                        type: 'success',
                        message: '已选择颜色: ' + this.customColor
                    });
                }).catch(() => {
                    // 用户取消输入，回到默认值
                    this.selectedColor = 'red';
                });
            }
            
            // 如果选择了自定义图片，显示图片上传
            if (colorConfig.target === 'image') {
                this.$message({
                    message: '请上传自定义背景图片',
                    type: 'info',
                    duration: 3000
                });
                
                // 这里可以添加触发图片上传的代码
            }
        },
        handleQuickColorSelect(color) {
            if (color === 'custom') {
                this.selectedColor = 'custom';
                // 弹出颜色选择器
                this.$prompt('请输入自定义颜色值', '自定义颜色', {
                    inputValue: this.customColor,
                    showCancelButton: true
                }).then(({ value }) => {
                    this.customColor = value;
                });
            } else if (color === 'mosaic') {
                this.selectedColor = 'mosaic';
            } else if (color === 'image') {
                this.selectedColor = 'image';
            } else {
                this.selectedColor = color;
            }
        },
        handleBgImageUpload() {
            // 阻止自动上传
        },
        onCustomColorChange(value) {
            this.customColor = value;
        },
        requestImageUpload() {
            this.selectedColor = 'image';
            this.$message({
                message: '请在右侧上传背景图片',
                type: 'info',
                duration: 3000
            });
        },
        handleCustomColorSelect(color) {
            this.selectedColor = 'custom';
            this.customColor = color;
            this.$message({
                message: '已选择自定义颜色: ' + color,
                type: 'success',
                duration: 2000
            });
        }
    },
    mounted() {
        // 创建需要的文件夹
        if (!document.querySelector('link[href="css/variables.css"]')) {
            console.warn('CSS 文件未正确加载，请确保 css 文件夹已创建');
        }
        
        // 页面加载完成后显示欢迎信息
        this.$notify({
            title: '欢迎使用证件照处理平台',
            message: '请上传您的证件照，选择合适的底色和尺寸，一键生成专业效果',
            type: 'info',
            duration: 5000,
            position: 'top-right'
        });
    }
}); 