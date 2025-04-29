<template>
	<view class="container">
		<view class="page-body">
			<view class="wrapper">
				<view class="toolbar" @tap="format" style="height: 120px;overflow-y: auto;">
					<view
						:class="formats.bold ? 'ql-active' : ''"
						class="iconfont icon-zitijiacu"
						data-name="bold"
					></view>
					<view
						:class="formats.italic ? 'ql-active' : ''"
						class="iconfont icon-zitixieti"
						data-name="italic"
					></view>
					<view
						:class="formats.underline ? 'ql-active' : ''"
						class="iconfont icon-zitixiahuaxian"
						data-name="underline"
					></view>
					<view
						:class="formats.strike ? 'ql-active' : ''"
						class="iconfont icon-zitishanchuxian"
						data-name="strike"
					></view>
					<view
						:class="formats.align === 'left' ? 'ql-active' : ''"
						class="iconfont icon-zuoduiqi"
						data-name="align"
						data-value="left"
					></view>
					<view
						:class="formats.align === 'center' ? 'ql-active' : ''"
						class="iconfont icon-juzhongduiqi"
						data-name="align"
						data-value="center"
					></view>
					<view
						:class="formats.align === 'right' ? 'ql-active' : ''"
						class="iconfont icon-youduiqi"
						data-name="align"
						data-value="right"
					></view>
					<view
						:class="formats.align === 'justify' ? 'ql-active' : ''"
						class="iconfont icon-zuoyouduiqi"
						data-name="align"
						data-value="justify"
					></view>
					<view
						:class="formats.lineHeight ? 'ql-active' : ''"
						class="iconfont icon-line-height"
						data-name="lineHeight"
						data-value="2"
					></view>
					<view
						:class="formats.letterSpacing ? 'ql-active' : ''"
						class="iconfont icon-Character-Spacing"
						data-name="letterSpacing"
						data-value="2em"
					></view>
					<view
						:class="formats.marginTop ? 'ql-active' : ''"
						class="iconfont icon-722bianjiqi_duanqianju"
						data-name="marginTop"
						data-value="20px"
					></view>
					<view
						:class="formats.previewarginBottom ? 'ql-active' : ''"
						class="iconfont icon-723bianjiqi_duanhouju"
						data-name="marginBottom"
						data-value="20px"
					></view>
					<view class="iconfont icon-clearedformat" @tap="removeFormat"></view>
					<view
						:class="formats.fontFamily ? 'ql-active' : ''"
						class="iconfont icon-font"
						data-name="fontFamily"
						data-value="Pacifico"
					></view>
					<view
						:class="formats.fontSize === '24px' ? 'ql-active' : ''"
						class="iconfont icon-fontsize"
						data-name="fontSize"
						data-value="24px"
					></view>
 
					<view
						:class="formats.color === '#0000ff' ? 'ql-active' : ''"
						class="iconfont icon-text_color"
						data-name="color"
						data-value="#0000ff"
					></view>
					<view
						:class="formats.backgroundColor === '#00ff00' ? 'ql-active' : ''"
						class="iconfont icon-fontbgcolor"
						data-name="backgroundColor"
						data-value="#00ff00"
					></view>
 
					<view class="iconfont icon-date" @tap="insertDate"></view>
					<view
						class="iconfont icon--checklist"
						data-name="list"
						data-value="check"
					></view>
					<view
						:class="formats.list === 'ordered' ? 'ql-active' : ''"
						class="iconfont icon-youxupailie"
						data-name="list"
						data-value="ordered"
					></view>
					<view
						:class="formats.list === 'bullet' ? 'ql-active' : ''"
						class="iconfont icon-wuxupailie"
						data-name="list"
						data-value="bullet"
					></view>
					<view class="iconfont icon-undo" @tap="undo"></view>
					<view class="iconfont icon-redo" @tap="redo"></view>
 
					<view class="iconfont icon-outdent" data-name="indent" data-value="-1"></view>
					<view class="iconfont icon-indent" data-name="indent" data-value="+1"></view>
					<view class="iconfont icon-fengexian" @tap="insertDivider"></view>
					<view class="iconfont icon-charutupian" @tap="insertImage"></view>
					<view
						:class="formats.header === 1 ? 'ql-active' : ''"
						class="iconfont icon-format-header-1"
						data-name="header"
						:data-value="1"
					></view>
					<view
						:class="formats.script === 'sub' ? 'ql-active' : ''"
						class="iconfont icon-zitixiabiao"
						data-name="script"
						data-value="sub"
					></view>
					<view
						:class="formats.script === 'super' ? 'ql-active' : ''"
						class="iconfont icon-zitishangbiao"
						data-name="script"
						data-value="super"
					></view>
					<view class="iconfont icon-shanchu" @tap="clear"></view>
					<view
						:class="formats.direction === 'rtl' ? 'ql-active' : ''"
						class="iconfont icon-direction-rtl"
						data-name="direction"
						data-value="rtl"
					></view>
				</view>
				<view class="editor-wrapper">
					<!-- <editor id="editor" class="ql-container" placeholder="开始输入..." showImgSize showImgToolbar showImgResize >
					</editor> -->
					<editor
						id="editor"
						class="ql-container"
						:placeholder="placeholder"
						@statuschange="onStatusChange"
						:show-img-resize="true"
						@ready="onEditorReady"
						@input="getCtx"
					></editor>
				</view>
			</view>
		</view>
	</view>
</template>
 
<script>
export default {
	props: {
		value: {
			type: String,
			default: ''
		}
	},
	data() {
		return {
			readOnly: false,
			placeholder: '开始输入...',
			richText: '',
			formats: {},
			serverUrl: 'http://localhost:9090/files/upload' // 图片上传 - 接口
		};
	},
	watch: {
		// 监听value属性变化，当父组件传入新值时更新编辑器内容
		value: {
			handler(newVal) {
				// 确保编辑器已初始化
				if (this.editorCtx && newVal !== this.richText) {
					console.log('编辑器内容更新:', newVal);
					this.editorCtx.setContents({
						html: newVal || ''
					});
				}
			},
			immediate: false // 不立即触发，等待编辑器初始化完成
		}
	},
 
	methods: {
		readOnlyChange() {
			this.readOnly = !this.readOnly;
		},
		onEditorReady() {
			// 富文本节点渲染完成
			const query = uni.createSelectorQuery().in(this);
			query
				.select('#editor')
				.context(res => {
					this.editorCtx = res.context;
					// 确保编辑器初始化后立即设置内容
					console.log('编辑器初始化完成，设置内容:', this.value);
					if (this.value) {
						this.editorCtx.setContents({
							html: this.value
						});
						// 同步富文本内容
						this.richText = this.value;
					}
				})
				.exec(this);
			// 标记编辑器已准备好
			this.$emit('ready');
		},
		// 失去焦点时，获取富文本的内容
		getCtx(e) {
			this.richText = e.detail.html;
			this.$emit('input', e.detail.html);
		},
		undo() {
			this.editorCtx.undo();
		},
		redo() {
			this.editorCtx.redo();
		},
		format(e) {
			let { name, value } = e.target.dataset;
			if (!name) return;
			// console.log('format', name, value)
			this.editorCtx.format(name, value);
		},
		onStatusChange(e) {
			const formats = e.detail;
			this.formats = formats;
		},
		insertDivider() {
			this.editorCtx.insertDivider({
				success: function() {
					console.log('insert divider success');
				}
			});
		},
		clear() {
			this.editorCtx.clear({
				success: function(res) {
					console.log('clear success');
				}
			});
		},
		removeFormat() {
			this.editorCtx.removeFormat();
		},
		insertDate() {
			const date = new Date();
			const formatDate = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
			this.editorCtx.insertText({
				text: formatDate
			});
		},
		
		insertImage() {
		    uni.chooseImage({
		      count: 1,
		      success: (res) => {
		        uni.uploadFile({
		          url: this.serverUrl,
		          filePath: res.tempFilePaths[0],
		          name: 'file', // 必须与@RequestParam("file")一致
		          header: {token: uni.getStorageSync('xm-user')?.token},
		          success: (uploadRes) => {
		            const data = JSON.parse(uploadRes.data);
					console.log(data.data)
		            if (data.code === '200') {
		              this.editorCtx.insertImage({
		                src: data.data, // 示例: "/uploads/123.jpg"
		                width: '100%'
		              });
		            }
		          }
		        });
		      }
		    });
		  },
	},
	onLoad() {
		uni.loadFontFace({
			family: 'Pacifico'
			// source: url('./iconfont.ttf')
		});
	}
};
</script>
 
<style>
@import './editor-icon.css';
 
.page-body {
	height: calc(100vh - var(--window-top) - var(--status-bar-height));
}
 
.wrapper {
	height: 100%;
}
 
.editor-wrapper {
	height: calc(100vh - var(--window-top) - var(--status-bar-height) - 140px);
	background: #eee;
}
 
.iconfont {
	display: inline-block;
	padding: 8px 8px;
	width: 24px;
	height: 24px;
	cursor: pointer;
	font-size: 20px;
}
 
.toolbar {
	box-sizing: border-box;
	border-bottom: 0;
	font-family: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
}
 
.ql-container {
	box-sizing: border-box;
	padding: 12px 15px;
	width: 100%;
	min-height: 30vh;
	height: 100%;
	margin-top: 20px;
	font-size: 16px;
	line-height: 1.5;
}
 
.ql-active {
	color: #06c;
}
</style>