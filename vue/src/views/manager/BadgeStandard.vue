<template>
  <div>
    <!-- 搜索区域 -->
    <div class="search">
      <el-input placeholder="勋章名称" style="width: 200px" v-model="badgeName"></el-input>
      <el-select placeholder="勋章类型" style="width: 120px; margin-left: 10px" v-model="badgeType">
        <el-option label="全部" value=""></el-option>
        <el-option label="饮食" value="饮食"></el-option>
        <el-option label="运动" value="运动"></el-option>
      </el-select>
      <el-button type="info" plain style="margin-left: 10px" @click="load(1)">搜索</el-button>
      <el-button type="warning" plain @click="reset">重置</el-button>
    </div>

    <!-- 操作按钮 -->
    <div class="operation">
      <el-button type="primary" plain @click="handleAdd">新增勋章标准</el-button>
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <!-- 表格列表 -->
    <div class="table">
      <el-table :data="tableData" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="ID" width="80" align="center" sortable></el-table-column>
        <el-table-column prop="type" label="勋章类型" width="100" align="center"></el-table-column>
        <el-table-column prop="name" label="勋章名称" width="150"></el-table-column>
        <el-table-column prop="days" label="达标数据" width="100" align="center"></el-table-column>
        <el-table-column prop="description" label="描述说明" width="200"></el-table-column>
        <el-table-column label="图片" width="200">
			<template slot-scope="scope">
				<img :src="scope.row.url" alt="图片" style="max-width: 100%; max-height: 80px;" />
			</template>
		</el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template v-slot="scope">
            <el-button type="primary" plain size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" plain size="mini" @click="del(scope.row.id)">删除</el-button>
            <!-- 保留行操作按钮：AI生成图片 
            <el-button type="info" plain size="mini" @click="handleAIGenerate(scope.row)">AI生成图片</el-button>-->
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-size="pageSize"
          layout="total, prev, pager, next"
          :total="total">
        </el-pagination>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="form.id ? '编辑勋章标准' : '新增勋章标准'" :visible.sync="formVisible" width="40%"
               :close-on-click-modal="false" destroy-on-close>
      <el-form label-width="120px" style="padding-right: 30px" :model="form" :rules="rules" ref="formRef">
        <el-form-item label="勋章类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型" style="width: 100%">
            <el-option label="饮食打卡天数" value="饮食打卡天数"></el-option>
            <el-option label="运动打卡天数" value="运动打卡天数"></el-option>
			<el-option label="饮食连续打卡天数" value="饮食连续打卡天数"></el-option>
			<el-option label="运动连续打卡天数" value="运动连续打卡天数"></el-option>
			<el-option label="饮食记录摄入" value="饮食记录摄入"></el-option>
			<el-option label="运动记录消耗" value="运动记录消耗"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="勋章名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入勋章名称"></el-input>
        </el-form-item>
        <el-form-item label="达标数据" prop="days">
          <el-input-number 
            v-model="form.days" 
            :min="0" 
            :precision="0"
            controls-position="right" 
            style="width: 100%"
            placeholder="请输入达标数据"></el-input-number>
        </el-form-item>
        <el-form-item label="描述说明" prop="description">
          <el-input v-model="form.description" placeholder="请输入描述说明"></el-input>
        </el-form-item>
        <!-- 使用头像上传方式来更改图片 -->
        <el-form-item label="图片" prop="url">
          <el-upload
              class="avatar-uploader"
              :action="$baseUrl + '/files/upload'"  
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
		      :before-upload="beforeAvatarUpload">
            <img v-if="form.url" :src="form.url" class="avatar" />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="formVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "BadgeStandard",
  data() {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      badgeName: null,
      badgeType: null,
      formVisible: false,
      form: {},
      rules: {
        type: [
          { required: true, message: '请选择勋章类型', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入勋章名称', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        days: [
          { required: true, message: '请输入达标天数', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ]
      },
      ids: [],
      // 当前需要更改图片的记录（用于表格行的手动更改图片）
      currentRow: null
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    // 新增记录
    handleAdd() {
      this.form = { type: '饮食打卡天数', days: 0 }
      this.formVisible = true
    },
    // 编辑记录
    handleEdit(row) {
      this.form = JSON.parse(JSON.stringify(row))
      this.formVisible = true
    },
    // 保存记录（新增或更新）
    save() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$request({
            url: this.form.id ? '/badgeStandard/update' : '/badgeStandard/add',
            method: this.form.id ? 'PUT' : 'POST',
            data: this.form
          }).then(res => {
            if (res.code === '200') {
              this.$message.success('保存成功')
              this.load(1)
              this.formVisible = false
            } else {
              this.$message.error(res.msg)
            }
          })
        }
      })
    },
    // 删除单个记录
    del(id) {
      this.$confirm('确认删除该记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete(`/badgeStandard/delete/${id}`).then(res => {
          if (res.code === '200') {
            this.load(1)
            this.$message.success('操作成功')
          } else {
            this.$message.error(res.msg)
          }
        })
      })
    },
    // 多选框变化
    handleSelectionChange(rows) {
      this.ids = rows.map(item => item.id)
    },
    // 批量删除
    delBatch() {
      if (!this.ids.length) return this.$message.warning('请选择数据')
      this.$confirm('确认批量删除选中记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete('/badgeStandard/delete/batch', { data: this.ids }).then(res => {
          if (res.code === '200') {
            this.load(1)
            this.$message.success('操作成功')
          } else {
            this.$message.error(res.msg)
          }
        })
      })
    },
    // 分页加载
    load(pageNum) {
      if (pageNum) this.pageNum = pageNum
      this.$request.get('/badgeStandard/selectPage', {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          badgeName: this.badgeName,
          badgeType: this.badgeType
        }
      }).then(res => {
        this.tableData = res.data?.list
        this.total = res.data?.total
      })
    },
    // 重置搜索条件
    reset() {
      this.badgeName = null
      this.badgeType = null
      this.load(1)
    },
    // 分页切换
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum
      this.load(pageNum)
    },
	//handleAvatarSuccess(response, file, fileList) {
	  // 把user的头像属性换成上传的图片的链接
	  //this.$set(this.form, 'avatar', response.data)
	//},
	// 对话框中上传图片成功回调（借鉴头像上传方式）
	handleAvatarSuccess(response, file) {
	  // response.data 包含图片地址
	  this.$set(this.form, 'url', response.data)
	  //this.$message.success('图片上传成功')
	},
    // 表格行“AI生成图片”调用后端生成接口
    handleAIGenerate(row) {
      this.$request.post('/py/create', { id: row.id }).then(res => {
        if (res.code === '200') {
          row.url = res.data.url
          this.$message.success('AI生成图片成功')
        } else {
          this.$message.error(res.msg)
        }
      })
    },
    // 对话框中上传图片成功回调（借鉴头像上传方式）
    //handleAvatarSuccess(response, file) {
      // response.data 包含图片地址
      //this.$set(this.form, 'url', response.data)
      //this.$message.success('图片上传成功')
      // 如果当前为编辑状态，则自动调用 update 更新记录
      //if (this.form.id) {
        //this.save()
      //}
    //},
    // 上传前校验（可选）
    beforeAvatarUpload(file) {
      const isImage = file.type.indexOf('image/') === 0
      if (!isImage) {
        this.$message.error('上传文件必须为图片格式')
      }
      return isImage
    }
  }
}
</script>

<style scoped>
.search {
  margin-bottom: 15px;
}
.operation {
  margin: 10px 0;
}
.el-table .cell {
  white-space: nowrap;
}
/* 头像上传样式 */
.avatar-uploader {
  display: block;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
}
.avatar {
  width: 120px;
  height: 120px;
  display: block;
  border-radius: 50%;
}
</style>


