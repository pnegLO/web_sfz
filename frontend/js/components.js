// 组件注册

// 左侧菜单组件
Vue.component('left-sidebar', {
    template: `
        <el-menu
            default-active="1-1"
            class="el-menu-vertical-demo"
            background-color="#ffffff"
            text-color="#2c3e50"
            active-text-color="#3c88fd"
            :collapse-transition="false"
            @select="handleSelect">
            
            <el-submenu index="1">
                <template slot="title">
                    <i class="el-icon-picture"></i>
                    <span>换底色</span>
                </template>
                <el-menu-item-group title="蓝底转换">
                    <el-menu-item index="1-1">蓝底转红底</el-menu-item>
                    <el-menu-item index="1-2">蓝底转白底</el-menu-item>
                    <el-menu-item index="1-3">蓝底转自定义颜色</el-menu-item>
                    <el-menu-item index="1-4">蓝底转自定义图片</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="红底转换">
                    <el-menu-item index="1-5">红底转蓝底</el-menu-item>
                    <el-menu-item index="1-6">红底转白底</el-menu-item>
                    <el-menu-item index="1-7">红底转自定义颜色</el-menu-item>
                    <el-menu-item index="1-8">红底转自定义图片</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="白底转换">
                    <el-menu-item index="1-9">白底转红底</el-menu-item>
                    <el-menu-item index="1-10">白底转蓝底</el-menu-item>
                    <el-menu-item index="1-11">白底转自定义颜色</el-menu-item>
                    <el-menu-item index="1-12">白底转自定义图片</el-menu-item>
                </el-menu-item-group>
            </el-submenu>
            
            <el-submenu index="2">
                <template slot="title">
                    <i class="el-icon-crop"></i>
                    <span>选尺寸</span>
                </template>
                <el-menu-item index="2-1">原尺寸</el-menu-item>
                <el-menu-item index="2-2">1寸照</el-menu-item>
                <el-menu-item index="2-3">2寸照</el-menu-item>
                <el-menu-item index="2-4">大1寸照</el-menu-item>
                <el-menu-item index="2-5">小1寸照</el-menu-item>
                <el-menu-item index="2-6">大2寸照</el-menu-item>
                <el-menu-item index="2-7">小2寸照</el-menu-item>
            </el-submenu>
            
            <el-menu-item index="3">
                <i class="el-icon-scissors"></i>
                <span slot="title">裁剪照片</span>
            </el-menu-item>
        </el-menu>
    `,
    methods: {
        handleSelect(index, indexPath) {
            this.$emit('menu-select', index, indexPath);
        }
    }
});

// 步骤导航组件
Vue.component('step-navigation', {
    props: ['activeStep'],
    template: `
        <el-row :gutter="20">
            <el-col :span="24">
                <el-steps :active="activeStep" finish-status="success" simple>
                    <el-step title="上传照片" icon="el-icon-upload"></el-step>
                    <el-step title="选择参数" icon="el-icon-set-up"></el-step>
                    <el-step title="生成并下载" icon="el-icon-download"></el-step>
                </el-steps>
            </el-col>
        </el-row>
    `
});

// 上传区域组件
Vue.component('upload-section', {
    props: ['fileList'],
    template: `
        <el-row :gutter="20">
            <el-col :span="24">
                <el-upload
                    class="upload-demo"
                    drag
                    action="#"
                    :http-request="handleManualUpload"
                    :on-change="handleFileChange"
                    :on-progress="handleProgress"
                    :on-success="handleSuccess"
                    :on-error="handleError"
                    :before-upload="beforeUpload"
                    :file-list="fileList"
                    :auto-upload="false"
                    ref="upload">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将照片拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">只能上传 JPG/PNG 格式照片，且不超过 10MB</div>
                </el-upload>
            </el-col>
        </el-row>
    `,
    methods: {
        handleManualUpload(options) {
            console.log('准备手动上传文件');
            // 这是一个空方法，阻止自动上传
        },
        handleFileChange(file, fileList) {
            this.$emit('file-uploaded', file, fileList);
        },
        beforeUpload(file) {
            this.$emit('before-upload', file);
        },
        handleProgress(event, file, fileList) {
            this.$emit('upload-progress', event, file, fileList);
        },
        handleSuccess(response, file, fileList) {
            this.$emit('upload-success', response, file, fileList);
        },
        handleError(err, file, fileList) {
            this.$emit('upload-error', err, file, fileList);
        }
    }
});

// 处理选项组件
Vue.component('processing-options', {
    props: [
        'selectedColor', 'customColor', 'showCustomColorPicker', 
        'showCustomImagePicker', 'bgImageFileList', 'selectedSize',
        'presetColors', 'photoSizes'
    ],
    template: `
        <div>
            <!-- 背景色选择 -->
            <el-row :gutter="20" class="color-picker-container">
                <el-col :span="24">
                    <el-card shadow="hover">
                        <div slot="header">
                            <span>背景选择</span>
                        </div>
                        
                        <!-- 快速背景色选择 -->
                        <div>
                            <h4>预设颜色</h4>
                            <div 
                                v-for="(color, index) in presetColors" 
                                :key="index"
                                :style="{ backgroundColor: color.value }" 
                                :class="['color-swatch', selectedColor === color.key ? 'active' : '']"
                                @click="selectColor(color.key)">
                            </div>
                        </div>
                        
                        <!-- 自定义背景色 -->
                        <div v-if="showCustomColorPicker" class="custom-bg-container">
                            <h4>自定义颜色</h4>
                            <el-color-picker v-model="localCustomColor" show-alpha @change="updateCustomColor"></el-color-picker>
                            <span style="margin-left: 10px;">已选颜色: {{localCustomColor}}</span>
                        </div>
                        
                        <!-- 自定义背景图片 -->
                        <div v-if="showCustomImagePicker" class="custom-bg-container">
                            <h4>自定义背景图片</h4>
                            <el-upload
                                action="#"
                                :auto-upload="false"
                                :on-change="handleBgImageChange"
                                :file-list="bgImageFileList"
                                list-type="picture-card">
                                <i class="el-icon-plus"></i>
                            </el-upload>
                            <div class="mosaic-option" v-if="showCustomImagePicker">
                                <el-checkbox v-model="useMosaic" @change="selectMosaic">使用马赛克背景</el-checkbox>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
            
            <!-- 尺寸选择 -->
            <el-row :gutter="20" class="size-picker-container">
                <el-col :span="24">
                    <el-card shadow="hover">
                        <div slot="header">
                            <span>尺寸规格</span>
                        </div>
                        <el-row :gutter="12">
                            <el-col :xs="12" :sm="8" :md="6" :lg="4" v-for="(size, index) in photoSizes" :key="index">
                                <el-card 
                                    :body-style="{ padding: '10px' }" 
                                    shadow="hover"
                                    :class="['size-card', selectedSize === size.key ? 'active' : '']"
                                    @click.native="selectSize(size.key)">
                                    <div style="text-align: center;">
                                        <h4 style="margin: 5px 0;">{{size.name}}</h4>
                                        <p style="margin: 5px 0; color: #666;">{{size.dimensions}}</p>
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    `,
    data() {
        return {
            localCustomColor: this.customColor,
            useMosaic: false
        };
    },
    methods: {
        selectColor(colorKey) {
            this.$emit('color-selected', colorKey);
        },
        updateCustomColor(value) {
            this.$emit('custom-color-change', value);
        },
        handleBgImageChange(file) {
            this.$emit('bg-image-change', file);
        },
        selectSize(sizeKey) {
            this.$emit('size-selected', sizeKey);
        },
        selectMosaic(value) {
            if (value) {
                this.$emit('color-selected', 'mosaic');
            } else {
                this.$emit('color-selected', 'custom_image');
            }
        }
    },
    watch: {
        customColor(newVal) {
            this.localCustomColor = newVal;
        }
    }
});

// 预览区域组件
Vue.component('preview-section', {
    props: ['originalImageUrl', 'processedImageUrl', 'previewBackgroundStyle'],
    template: `
        <div class="preview-container">
            <div class="preview-box">
                <h4 class="preview-title">原始照片</h4>
                <img v-if="originalImageUrl" :src="originalImageUrl" class="preview-image" alt="原始照片">
                <div v-else class="no-image-placeholder">
                    <i class="el-icon-picture-outline" style="font-size: 48px; color: #dcdfe6;"></i>
                    <p>上传照片后在此处预览</p>
                </div>
            </div>
            
            <div class="preview-box" :style="previewBackgroundStyle">
                <h4 class="preview-title">效果预览</h4>
                <img v-if="processedImageUrl" :src="processedImageUrl" class="preview-image" alt="处理后照片">
                <div v-else-if="originalImageUrl" class="preview-image-overlay">
                    <img :src="originalImageUrl" class="preview-image preview-image-original" alt="效果预览">
                </div>
                <div v-else class="no-image-placeholder">
                    <i class="el-icon-picture-outline" style="font-size: 48px; color: #dcdfe6;"></i>
                    <p>处理后的效果将显示在这里</p>
                </div>
            </div>
        </div>
    `
});

// 操作按钮组件
Vue.component('action-buttons', {
    props: ['canSubmit', 'uploading', 'processedImageUrl'],
    template: `
        <el-row class="action-buttons">
            <el-col :span="24" style="text-align: center;">
                <el-button type="primary" size="medium" icon="el-icon-s-operation" @click="submit" :loading="uploading" :disabled="!canSubmit">
                    {{ uploading ? '处理中...' : '开始处理' }}
                </el-button>
                <el-button type="success" size="medium" icon="el-icon-download" @click="download" :disabled="!processedImageUrl">
                    下载图片
                </el-button>
            </el-col>
        </el-row>
    `,
    methods: {
        submit() {
            this.$emit('submit');
        },
        download() {
            this.$emit('download');
        }
    }
});

// 消息显示组件
Vue.component('message-display', {
    props: ['message', 'messageType'],
    template: `
        <transition name="fade">
            <el-alert
                v-if="message"
                :title="message"
                :type="messageType"
                :closable="false"
                show-icon>
            </el-alert>
        </transition>
    `
});

// 工具栏组件
Vue.component('tool-bar', {
    props: ['active-tool'],
    template: `
        <div class="tool-panel">
            <div class="tool-item" :class="{ active: activeTool === 'color' }" @click="$emit('tool-select', 'color')">
                <i class="el-icon-picture-outline tool-icon"></i>
                <span class="tool-text">换底色</span>
            </div>
            <div class="tool-item" :class="{ active: activeTool === 'size' }" @click="$emit('tool-select', 'size')">
                <i class="el-icon-crop tool-icon"></i>
                <span class="tool-text">尺寸</span>
            </div>
            <div class="tool-item" :class="{ active: activeTool === 'upload' }" @click="$emit('tool-select', 'upload')">
                <i class="el-icon-upload tool-icon"></i>
                <span class="tool-text">上传</span>
            </div>
        </div>
    `
});

// 预览区域组件
Vue.component('photo-preview', {
    props: ['original-image-url', 'processed-image-url', 'selected-size'],
    template: `
        <div class="preview-container">
            <div class="preview-tabs">
                <div class="preview-tab active">证件照预览</div>
            </div>

            <div class="preview-content">
                <div class="preview-wrapper" v-if="processedImageUrl || originalImageUrl">
                    <div class="size-indicators">
                        <div class="horizontal-ruler">{{ getSizeWidth() }}mm</div>
                        <div class="vertical-ruler">{{ getSizeHeight() }}mm</div>
                    </div>
                    <img 
                        v-if="processedImageUrl" 
                        :src="processedImageUrl" 
                        class="preview-image" 
                        alt="处理后照片">
                    <img 
                        v-else 
                        :src="originalImageUrl" 
                        class="preview-image" 
                        alt="原始照片">
                </div>
                <div v-else class="upload-prompt">
                    <i class="el-icon-picture-outline" style="font-size: 48px; color: #dcdfe6;"></i>
                    <p>请上传证件照进行处理</p>
                </div>
            </div>
        </div>
    `,
    methods: {
        getSizeWidth() {
            const sizeMap = {
                'one_inch': 25,
                'two_inch': 35,
                'large_one_inch': 33,
                'small_one_inch': 22,
                'large_two_inch': 35,
                'small_two_inch': 27,
                'original': 35 // 默认值
            };
            return sizeMap[this.selectedSize] || 35;
        },
        getSizeHeight() {
            const sizeMap = {
                'one_inch': 35,
                'two_inch': 49,
                'large_one_inch': 48,
                'small_one_inch': 32,
                'large_two_inch': 53,
                'small_two_inch': 40,
                'original': 49 // 默认值
            };
            return sizeMap[this.selectedSize] || 49;
        }
    }
});

// 控制面板组件
Vue.component('control-panel', {
    props: [
        'active-tool', 
        'selected-color', 
        'custom-color',
        'selected-size',
        'preset-colors',
        'photo-sizes'
    ],
    template: `
        <div class="control-panel">
            <!-- 侧栏标题 -->
            <div class="panel-header">照片设置</div>

            <!-- 底色选择 -->
            <div class="panel-section" v-show="activeTool === 'color'">
                <div class="panel-title">
                    照片底色
                </div>
                <div class="color-grid">
                    <div class="color-swatch checkerboard" :class="{ active: selectedColor === 'transparent' }" @click="$emit('color-select', 'transparent')"></div>
                    <div class="color-swatch white-bg" :class="{ active: selectedColor === 'white' }" @click="$emit('color-select', 'white')"></div>
                    <div class="color-swatch light-blue-bg" :class="{ active: selectedColor === 'light-blue' }" @click="$emit('color-select', 'light-blue')"></div>
                    
                    <div class="color-swatch blue-bg" :class="{ active: selectedColor === 'blue' }" @click="$emit('color-select', 'blue')"></div>
                    <div class="color-swatch red-bg" :class="{ active: selectedColor === 'red' }" @click="$emit('color-select', 'red')"></div>
                    <div class="color-swatch gray-bg" :class="{ active: selectedColor === 'gray' }" @click="$emit('color-select', 'gray')"></div>
                    
                    <div class="color-swatch gradient1" :class="{ active: selectedColor === 'gradient1' }" @click="$emit('color-select', 'gradient1')"></div>
                    <div class="color-swatch gradient2" :class="{ active: selectedColor === 'gradient2' }" @click="$emit('color-select', 'gradient2')"></div>
                    <div class="color-swatch gradient3" :class="{ active: selectedColor === 'gradient3' }" @click="$emit('color-select', 'gradient3')"></div>
                    
                    <div class="color-swatch custom-color" :class="{ active: selectedColor === 'custom' }" @click="$emit('color-select', 'custom')"></div>
                </div>
                
                <div v-if="selectedColor === 'custom'" class="custom-color-section">
                    <el-color-picker 
                        v-model="localCustomColor" 
                        show-alpha 
                        @change="updateCustomColor">
                    </el-color-picker>
                </div>
            </div>
            
            <!-- 尺寸选择 -->
            <div class="panel-section" v-show="activeTool === 'size'">
                <div class="panel-title">照片尺寸</div>
                
                <div class="size-row">
                    <div class="size-item" :class="{ active: selectedSize === 'one_inch' }" @click="$emit('size-select', 'one_inch')">
                        <div class="size-name">1寸</div>
                        <div class="size-dimensions">25×35mm（295×413px）</div>
                    </div>
                </div>
                
                <div class="size-row">
                    <div class="size-item" :class="{ active: selectedSize === 'two_inch' }" @click="$emit('size-select', 'two_inch')">
                        <div class="size-name">2寸</div>
                        <div class="size-dimensions">35×49mm（413×579px）</div>
                    </div>
                </div>
                
                <div class="size-row">
                    <div class="size-item" :class="{ active: selectedSize === 'small_two_inch' }" @click="$emit('size-select', 'small_two_inch')">
                        <div class="size-name">小2寸</div>
                        <div class="size-dimensions">27×40mm（320×472px）</div>
                    </div>
                </div>
            </div>
            
            <!-- 上传图片 -->
            <div class="panel-section" v-show="activeTool === 'upload'">
                <div class="panel-title">上传照片</div>
                <el-upload
                    class="upload-area"
                    drag
                    action="#"
                    :http-request="handleManualUpload"
                    :on-change="handleFileChange"
                    :auto-upload="false">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">拖拽文件或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">支持JPG/PNG格式，不超过10MB</div>
                </el-upload>
            </div>
        </div>
    `,
    data() {
        return {
            localCustomColor: this.customColor
        };
    },
    methods: {
        updateCustomColor(val) {
            this.$emit('custom-color-change', val);
        },
        handleFileChange(file) {
            this.$emit('file-change', file);
        },
        handleManualUpload() {
            // 阻止自动上传
        }
    },
    watch: {
        customColor(val) {
            this.localCustomColor = val;
        }
    }
});

// 左侧垂直菜单组件
Vue.component('side-menu', {
    template: `
        <div>
            <el-menu
                default-active="blue-to-red"
                class="el-menu-vertical-demo"
                background-color="#ffffff"
                text-color="#333333"
                active-text-color="#3c88fd">
                
                <el-submenu index="color-change">
                    <template slot="title">
                        <i class="el-icon-picture-outline"></i>
                        <span>换底色</span>
                    </template>
                    
                    <el-menu-item-group title="蓝底转换">
                        <el-menu-item index="blue-to-red" @click="emitColorChange('blue', 'red')">蓝底转红底</el-menu-item>
                        <el-menu-item index="blue-to-white" @click="emitColorChange('blue', 'white')">蓝底转白底</el-menu-item>
                        <el-menu-item index="blue-to-custom" @click="emitColorChange('blue', 'custom')">蓝底转自定义颜色</el-menu-item>
                        <el-menu-item index="blue-to-image" @click="emitColorChange('blue', 'image')">蓝底转自定义图片</el-menu-item>
                    </el-menu-item-group>
                    
                    <el-menu-item-group title="红底转换">
                        <el-menu-item index="red-to-blue" @click="emitColorChange('red', 'blue')">红底转蓝底</el-menu-item>
                        <el-menu-item index="red-to-white" @click="emitColorChange('red', 'white')">红底转白底</el-menu-item>
                        <el-menu-item index="red-to-custom" @click="emitColorChange('red', 'custom')">红底转自定义颜色</el-menu-item>
                        <el-menu-item index="red-to-image" @click="emitColorChange('red', 'image')">红底转自定义图片</el-menu-item>
                    </el-menu-item-group>
                    
                    <el-menu-item-group title="白底转换">
                        <el-menu-item index="white-to-blue" @click="emitColorChange('white', 'blue')">白底转蓝底</el-menu-item>
                        <el-menu-item index="white-to-red" @click="emitColorChange('white', 'red')">白底转红底</el-menu-item>
                        <el-menu-item index="white-to-custom" @click="emitColorChange('white', 'custom')">白底转自定义颜色</el-menu-item>
                        <el-menu-item index="white-to-image" @click="emitColorChange('white', 'image')">白底转自定义图片</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                
                <el-menu-item index="quick-color" @click="openQuickColorSelect">
                    <i class="el-icon-magic-stick"></i>
                    <span>背景色快速选择</span>
                </el-menu-item>
                
                <el-menu-item index="show-sizes" @click="openSizeSelector">
                    <i class="el-icon-crop"></i>
                    <span>选择照片尺寸</span>
                </el-menu-item>
            </el-menu>

            <!-- 尺寸选择对话框 -->
            <el-dialog
                title="选择证件照尺寸"
                :visible.sync="sizeSelectorVisible"
                width="600px"
                center>
                <div class="size-card-container">
                    <div 
                        v-for="size in photoSizes" 
                        :key="size.key"
                        class="size-card"
                        :class="{ 'active': selectedSize === size.key }"
                        @click="selectPhotoSize(size.key)">
                        <div class="size-card-inner">
                            <div class="size-name">{{ size.name }}</div>
                            <div class="size-dimensions">{{ size.dimensions }}</div>
                            <div class="size-pixels">{{ size.pixels }}</div>
                        </div>
                    </div>
                </div>
            </el-dialog>

            <!-- 背景色快速选择对话框 -->
            <el-dialog
                title="背景色快速选择"
                :visible.sync="colorSelectorVisible"
                width="400px"
                center>
                <div class="color-section">
                    <div class="section-title">预设背景色</div>
                    <div class="color-grid">
                        <div class="color-item red-bg" @click="selectColor('red')"></div>
                        <div class="color-item blue-bg" @click="selectColor('blue')"></div>
                        <div class="color-item white-bg" @click="selectColor('white')"></div>
                        <div class="color-item gray-bg" @click="selectColor('gray')"></div>
                    </div>
                </div>
                
                <div class="color-section">
                    <div class="section-title">特殊背景</div>
                    <div class="color-grid">
                        <div class="color-item checkerboard" @click="selectColor('mosaic')">
                            <span class="color-label">马赛克</span>
                        </div>
                        <div class="color-item custom-color" @click="selectColor('custom')">
                            <span class="color-label">自定义</span>
                        </div>
                        <div class="color-item custom-image" @click="selectColor('image')">
                            <span class="color-label">图片</span>
                        </div>
                    </div>
                </div>
                
                <!-- 颜色选择器预览 -->
                <div v-if="tempColorPickerVisible" class="color-section">
                    <div class="section-title">自定义颜色预览</div>
                    <div class="custom-color-picker">
                        <el-color-picker v-model="tempCustomColor" show-alpha></el-color-picker>
                        <div class="color-preview" :style="{ backgroundColor: tempCustomColor }"></div>
                    </div>
                    <div class="dialog-footer" style="margin-top: 15px; text-align: right;">
                        <el-button size="small" @click="tempColorPickerVisible = false">取消</el-button>
                        <el-button size="small" type="primary" @click="confirmCustomColor">确认</el-button>
                    </div>
                </div>
            </el-dialog>
        </div>
    `,
    data() {
        return {
            sizeSelectorVisible: false,
            colorSelectorVisible: false,
            tempColorPickerVisible: false,
            tempCustomColor: '#FF0000',
            selectedSize: 'one_inch',
            photoSizes: [
                { key: 'original', name: '原尺寸', dimensions: '保持原比例', pixels: '原始尺寸' },
                { key: 'one_inch', name: '一寸照', dimensions: '25×35毫米', pixels: '295×413像素' },
                { key: 'two_inch', name: '二寸照片', dimensions: '35×49毫米', pixels: '413×579像素' },
                { key: 'large_one_inch', name: '大一寸照', dimensions: '33×48毫米', pixels: '390×567像素' },
                { key: 'small_one_inch', name: '小一寸照片', dimensions: '22×32毫米', pixels: '260×378像素' },
                { key: 'large_two_inch', name: '大二寸照片', dimensions: '35×53毫米', pixels: '413×626像素' },
                { key: 'small_two_inch', name: '小二寸照片', dimensions: '27×40毫米', pixels: '320×472像素' },
            ]
        };
    },
    methods: {
        emitColorChange(source, target) {
            this.$emit('color-change', { source, target });
        },
        openSizeSelector() {
            this.sizeSelectorVisible = true;
        },
        openQuickColorSelect() {
            this.colorSelectorVisible = true;
        },
        selectPhotoSize(sizeKey) {
            this.selectedSize = sizeKey;
            this.$emit('size-change', sizeKey);
            this.sizeSelectorVisible = false;
        },
        selectColor(color) {
            if (color === 'custom') {
                this.tempColorPickerVisible = true;
                return;
            }
            
            this.$emit('quick-color-select', color);
            this.colorSelectorVisible = false;
        },
        confirmCustomColor() {
            this.$emit('custom-color-select', this.tempCustomColor);
            this.tempColorPickerVisible = false;
            this.colorSelectorVisible = false;
        }
    }
}); 