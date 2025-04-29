<template>
  <div>
    <div class="search">
      <el-input placeholder="食物名称" style="width: 200px" v-model="name"></el-input>
      <el-select placeholder="食物种类" style="width: 120px; margin-left: 10px" v-model="category">
        <el-option label="全部" value=""></el-option>
            <el-option label="家常菜" value="家常菜"></el-option>
            <el-option label="零食、点心、冷饮" value="零食、点心、冷饮"></el-option>
            <el-option label="甘肃菜" value="甘肃菜"></el-option>
            <el-option label="广东菜" value="广东菜"></el-option>
			<el-option label="私家菜" value="私家菜"></el-option>
			<el-option label="饮料" value="饮料"></el-option>
			<el-option label="湖北菜" value="湖北菜"></el-option>
			<el-option label="蛋类、肉类及制品" value="蛋类、肉类及制品"></el-option>
			<el-option label="上海菜" value="上海菜"></el-option>
			<el-option label="蔬果和菌藻" value="蔬果和菌藻"></el-option>
			<el-option label="台湾菜" value="台湾菜"></el-option>
			<el-option label="四川菜" value="四川菜"></el-option>
			<el-option label="食用油、油脂及制品" value="食用油、油脂及制品"></el-option>
			<el-option label="调味品" value="调味品"></el-option>
			<el-option label="河南菜" value="河南菜"></el-option>
			<el-option label="山西菜" value="山西菜"></el-option>
			<el-option label="素斋菜" value="素斋菜"></el-option>
			<el-option label="广西菜" value="广西菜"></el-option>
			<el-option label="其它" value="其它"></el-option>
			<el-option label="安徽菜" value="安徽菜"></el-option>
			<el-option label="江苏菜" value="江苏菜"></el-option>
			<el-option label="山东菜" value="山东菜"></el-option>
			<el-option label="日本料理" value="日本料理"></el-option>
			<el-option label="谷薯芋、杂豆、主食" value="谷薯芋、杂豆、主食"></el-option>
			<el-option label="滇黔菜" value="滇黔菜"></el-option>
			<el-option label="福建菜" value="福建菜"></el-option>
			<el-option label="其他西餐" value="其他西餐"></el-option>
			<el-option label="广州菜" value="广州菜"></el-option>
			<el-option label="法国菜" value="法国菜"></el-option>
			<el-option label="浙江菜" value="浙江菜"></el-option>
			<el-option label="湖南菜" value="湖南菜"></el-option>
			<el-option label="其他菜肴" value="其他菜肴"></el-option>
			<el-option label="北京菜" value="北京菜"></el-option>
			<el-option label="奶类及制品" value="奶类及制品"></el-option>
			<el-option label="陕西菜" value="陕西菜"></el-option>
			<el-option label="坚果、大豆及制品" value="坚果、大豆及制品"></el-option>
			<el-option label="青海菜" value="青海菜"></el-option>
			<el-option label="砂锅、煮" value="砂锅、煮"></el-option>
			<el-option label="海南菜" value="海南菜"></el-option>
			<el-option label="少数民族菜" value="少数民族菜"></el-option>
			<el-option label="东北菜" value="东北菜"></el-option>
			<el-option label="意大利菜" value="意大利菜"></el-option>
			<el-option label="韩国料理" value="韩国料理"></el-option>
			<el-option label="清真菜" value="清真菜"></el-option>
			<el-option label="江西菜" value="江西菜"></el-option>
			<el-option label="固体饮料类" value="固体饮料类"></el-option>
			<el-option label="东南亚风味" value="东南亚风味"></el-option>
			<el-option label="天津菜" value="天津菜"></el-option>
      </el-select>
      <el-button type="info" plain style="margin-left: 10px" @click="load(1)">搜索</el-button>
      <el-button type="warning" plain @click="reset">重置</el-button>
    </div>

    <div class="operation">
      <el-button type="primary" plain @click="handleAdd">新增食物</el-button>
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <div class="table">
      <el-table :data="tableData" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="ID" width="80" align="center" sortable></el-table-column>
        <el-table-column prop="name" label="食物名称" width="150"></el-table-column>
        <el-table-column prop="category" label="种类" width="100"></el-table-column>
        <el-table-column label="营养值/100g" align="center">
          <el-table-column prop="calories" label="卡路里" width="100"></el-table-column>
          <el-table-column prop="carbohydrates" label="碳水(g)" width="100"></el-table-column>
          <el-table-column prop="fat" label="脂肪(g)" width="100"></el-table-column>
          <el-table-column prop="protein" label="蛋白(g)" width="100"></el-table-column>
          <el-table-column prop="fiber" label="纤维(g)" width="100"></el-table-column>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="80"></el-table-column>

        <el-table-column label="操作" width="150" align="center">
          <template v-slot="scope">
            <el-button type="primary" plain size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" plain size="mini" @click="del(scope.row.id)">删除</el-button>
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

    <el-dialog :title="form.id ? '编辑食物' : '新增食物'" :visible.sync="formVisible" width="30%" 
               :close-on-click-modal="false" destroy-on-close>
      <el-form label-width="100px" style="padding-right: 30px" :model="form" :rules="rules" ref="formRef">
        <el-form-item label="食物名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入食物名称"></el-input>
        </el-form-item>
        <el-form-item label="食物种类">
          <el-select v-model="form.category" placeholder="请选择种类" style="width: 100%">
            <el-option label="家常菜" value="家常菜"></el-option>
            <el-option label="零食、点心、冷饮" value="零食、点心、冷饮"></el-option>
            <el-option label="甘肃菜" value="甘肃菜"></el-option>
            <el-option label="广东菜" value="广东菜"></el-option>
			<el-option label="私家菜" value="私家菜"></el-option>
			<el-option label="饮料" value="饮料"></el-option>
			<el-option label="湖北菜" value="湖北菜"></el-option>
			<el-option label="蛋类、肉类及制品" value="蛋类、肉类及制品"></el-option>
			<el-option label="上海菜" value="上海菜"></el-option>
			<el-option label="蔬果和菌藻" value="蔬果和菌藻"></el-option>
			<el-option label="台湾菜" value="台湾菜"></el-option>
			<el-option label="四川菜" value="四川菜"></el-option>
			<el-option label="食用油、油脂及制品" value="食用油、油脂及制品"></el-option>
			<el-option label="调味品" value="调味品"></el-option>
			<el-option label="河南菜" value="河南菜"></el-option>
			<el-option label="山西菜" value="山西菜"></el-option>
			<el-option label="素斋菜" value="素斋菜"></el-option>
			<el-option label="广西菜" value="广西菜"></el-option>
			<el-option label="其它" value="其它"></el-option>
			<el-option label="安徽菜" value="安徽菜"></el-option>
			<el-option label="江苏菜" value="江苏菜"></el-option>
			<el-option label="山东菜" value="山东菜"></el-option>
			<el-option label="日本料理" value="日本料理"></el-option>
			<el-option label="谷薯芋、杂豆、主食" value="谷薯芋、杂豆、主食"></el-option>
			<el-option label="滇黔菜" value="滇黔菜"></el-option>
			<el-option label="福建菜" value="福建菜"></el-option>
			<el-option label="其他西餐" value="其他西餐"></el-option>
			<el-option label="广州菜" value="广州菜"></el-option>
			<el-option label="法国菜" value="法国菜"></el-option>
			<el-option label="浙江菜" value="浙江菜"></el-option>
			<el-option label="湖南菜" value="湖南菜"></el-option>
			<el-option label="其他菜肴" value="其他菜肴"></el-option>
			<el-option label="北京菜" value="北京菜"></el-option>
			<el-option label="奶类及制品" value="奶类及制品"></el-option>
			<el-option label="陕西菜" value="陕西菜"></el-option>
			<el-option label="坚果、大豆及制品" value="坚果、大豆及制品"></el-option>
			<el-option label="青海菜" value="青海菜"></el-option>
			<el-option label="砂锅、煮" value="砂锅、煮"></el-option>
			<el-option label="海南菜" value="海南菜"></el-option>
			<el-option label="少数民族菜" value="少数民族菜"></el-option>
			<el-option label="东北菜" value="东北菜"></el-option>
			<el-option label="意大利菜" value="意大利菜"></el-option>
			<el-option label="韩国料理" value="韩国料理"></el-option>
			<el-option label="清真菜" value="清真菜"></el-option>
			<el-option label="江西菜" value="江西菜"></el-option>
			<el-option label="固体饮料类" value="固体饮料类"></el-option>
			<el-option label="东南亚风味" value="东南亚风味"></el-option>
			<el-option label="天津菜" value="天津菜"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="卡路里" prop="calories">
          <el-input-number v-model="form.calories" :min="0" :precision="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="碳水化合物">
          <el-input-number v-model="form.carbohydrates" :min="0" :precision="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="脂肪含量">
          <el-input-number v-model="form.fat" :min="0" :precision="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="蛋白质">
          <el-input-number v-model="form.protein" :min="0" :precision="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="纤维素">
          <el-input-number v-model="form.fiber" :min="0" :precision="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="form.unit" :min="0" :precision="1" style="width: 100%"></el-input>
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
  name: "Food",
  data() {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      name: '',
      category: '',
      formVisible: false,
      form: {},
      rules: {
        name: [{ required: true, message: '请输入食物名称', trigger: 'blur' }],
        calories: [{ type: 'number', message: '必须为数字值', trigger: 'blur' }]
      },
      ids: []
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    handleAdd() {
      this.form = { unit: '' }
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
            url: this.form.id ? '/food/update' : '/food/add',
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
    del(id) {
      this.$confirm('确认删除该食物记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete(`/food/delete/${id}`).then(res => {
          res.code === '200' && this.load(1)
          this.$message[res.code === '200' ? 'success' : 'error'](res.msg || '操作成功')
        })
      })
    },
    handleSelectionChange(rows) {
      this.ids = rows.map(v => v.id)
    },
    delBatch() {
      if (!this.ids.length) return this.$message.warning('请选择数据')
      this.$confirm('确认批量删除选中记录？', '警告', { type: 'warning' }).then(() => {
        this.$request.delete('/food/delete/batch', { data: this.ids }).then(res => {
          res.code === '200' && this.load(1)
          this.$message[res.code === '200' ? 'success' : 'error'](res.msg || '操作成功')
        })
      })
    },
    load(pageNum) {
      if (pageNum) this.pageNum = pageNum
      this.$request.get('/food/selectPage', {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          name: this.name,
          category: this.category
        }
      }).then(res => {
        this.tableData = res.data?.list || []
        this.total = res.data?.total || 0
      })
    },
    reset() {
      this.name = ''
      this.category = ''
      this.load(1)
    },
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum
      this.load()
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
.el-input-number {
  width: 100%;
}
</style>