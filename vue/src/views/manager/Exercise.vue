<template>
  <div>
    <div class="search">
      <el-input placeholder="运动名称" style="width: 200px" v-model="exerciseName"></el-input>
      <el-select placeholder="运动类型" style="width: 120px; margin-left: 10px" v-model="exerciseCategory">
        <el-option label="全部" value=""></el-option>
        <el-option label="有氧运动" value="有氧运动"></el-option>
        <el-option label="力量训练" value="力量训练"></el-option>
        <el-option label="球类运动" value="球类运动"></el-option>
        <el-option label="游泳" value="游泳"></el-option>
		<el-option label="冬季运动" value="冬季运动"></el-option>
		<el-option label="武术格斗" value="武术格斗"></el-option>
		<el-option label="休闲运动" value="休闲运动"></el-option>
		<el-option label="极限运动" value="极限运动"></el-option>
      </el-select>
      <el-button type="info" plain style="margin-left: 10px" @click="load(1)">搜索</el-button>
      <el-button type="warning" plain @click="reset">重置</el-button>
    </div>

    <div class="operation">
      <el-button type="primary" plain @click="handleAdd">新增运动</el-button>
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <div class="table">
      <el-table :data="tableData" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="exerciseId" label="ID" width="80" align="center" sortable></el-table-column>
        <el-table-column prop="exerciseName" label="运动名称" width="150"></el-table-column>
        <el-table-column prop="exerciseCategory" label="运动类型" width="120"></el-table-column>
        <el-table-column prop="caloriesBurnRate" label="消耗卡路里/10分钟" width="150" align="center"></el-table-column>
        
        <el-table-column label="操作" width="150" align="center">
          <template v-slot="scope">
            <el-button type="primary" plain size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" plain size="mini" @click="del(scope.row.exercise_id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

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

    <el-dialog :title="form.exercise_id ? '编辑运动' : '新增运动'" :visible.sync="formVisible" width="30%" 
               :close-on-click-modal="false" destroy-on-close>
      <el-form label-width="120px" style="padding-right: 30px" :model="form" :rules="rules" ref="formRef">
        <el-form-item label="运动名称" prop="exerciseName">
          <el-input v-model="form.exerciseName" placeholder="请输入运动名称"></el-input>
        </el-form-item>
        <el-form-item label="运动类型" prop="exerciseCategory">
          <el-select v-model="form.exerciseCategory" placeholder="请选择类型" style="width: 100%">
            <el-option label="有氧运动" value="有氧运动"></el-option>
            <el-option label="力量训练" value="力量训练"></el-option>
            <el-option label="球类运动" value="球类运动"></el-option>
            <el-option label="游泳" value="游泳"></el-option>
		    <el-option label="冬季运动" value="冬季运动"></el-option>
		    <el-option label="武术格斗" value="武术格斗"></el-option>
		    <el-option label="休闲运动" value="休闲运动"></el-option>
		    <el-option label="极限运动" value="极限运动"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="消耗卡路里" prop="caloriesBurnRate">
          <el-input-number 
            v-model="form.caloriesBurnRate" 
            :min="1" 
            :precision="0"
            controls-position="right" 
            style="width: 100%"
            placeholder="每10分钟消耗量"></el-input-number>
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
  name: "Exercise",
  data() {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      exerciseName: null,
      exerciseCategory: null,
      formVisible: false,
      form: {},
      rules: {
        exerciseName: [
          { required: true, message: '请输入运动名称', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        exerciseCategory: [
          { required: true, message: '请选择运动类型', trigger: 'change' }
        ],
        caloriesBurnRate: [
          { required: true, message: '请输入消耗量', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ]
      },
      ids: []
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    handleAdd() {
      this.form = { caloriesBurnRate: 10 } // 设置默认值
      this.formVisible = true
    },
    handleEdit(row) {
      this.form = JSON.parse(JSON.stringify(row))
      this.formVisible = true
    },
    save() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$request({
            url: this.form.exerciseId ? '/exercise/update' : '/exercise/add',
            method: this.form.exerciseId ? 'PUT' : 'POST',
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
    del(id) {
      this.$confirm('确认删除该运动记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete(`/exercise/delete/${id}`).then(res => {
          res.code === '200' && this.load(1)
          this.$message[res.code === '200' ? 'success' : 'error'](res.msg || '操作成功')
        })
      })
    },
    handleSelectionChange(rows) {
      this.ids = rows.map(v => v.exerciseId)
    },
    delBatch() {
      if (!this.ids.length) return this.$message.warning('请选择数据')
      this.$confirm('确认批量删除选中记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete('/exercise/delete/batch', { data: this.ids }).then(res => {
          res.code === '200' && this.load(1)
          this.$message[res.code === '200' ? 'success' : 'error'](res.msg || '操作成功')
        })
      })
    },
    load(pageNum) {
      if (pageNum) this.pageNum = pageNum
      this.$request.get('/exercise/selectPage', { 
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          exerciseName: this.exerciseName,
          exerciseCategory: this.exerciseCategory
        }
      }).then(res => {
        this.tableData = res.data?.list 
        this.total = res.data?.total 
      })
    },
    reset() {
      this.exerciseName = null
      this.exerciseCategory = null
      this.load(1)
    },
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum
      this.load(pageNum)
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
</style>