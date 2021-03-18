<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="使用模型">
      <el-switch
        style="display: block;position:absolute;left:0%;top:25%"
        v-model="useLarge"
        active-color="#13ce66"
        inactive-color="#409EFF"
        active-text="BERT-LARGE"
        inactive-text="BERT-BASE">
      </el-switch>
    </el-form-item>
    <el-form-item label="文档内容" >
      <el-input type="textarea" v-model="form.article" :autosize="{ minRows: 1, maxRows: 8}" placeholder="直接输入文本即可，例：There is one _ thing i like to mention here . Before we begin our _ , my family and i do not eat ."></el-input>
    </el-form-item>
    <el-form-item label="MASK标记">
      <el-input v-model="form.mask" placeholder="与文档内容中的填空标记对应，例：_"></el-input>
    </el-form-item>
    <el-form-item label="是否包含正确答案" id="ell">
      <el-radio-group style="position:absolute;left:0%;top:0%;" v-model="form.includeAnswer" @change="agreeChange">
        <el-row>
        <el-radio class="el-radio" label='1' style="width:80%;">是</el-radio>
        </el-row>
        <el-row>
        <el-radio label="2" style="float: top;width:80%;">否</el-radio>
        </el-row>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="答案选项">
      <el-input  type="textarea" v-model="form.options" :autosize="{ minRows: 1, maxRows: 4}" placeholder='若手动输入，请使用英文标点符号、双引号，且逗号后无需加空格，例：[["common","exciting","special","embarrassing"],["show","journey","vacation","meal"]]'></el-input>
    </el-form-item>
    <el-form-item label="正确答案">
      <el-input type="textarea" :disabled="inputAnswer" v-model="form.answers" :autosize="{ minRows: 1, maxRows: 2}" placeholder='规则同上，例：["C","B"]'></el-input>
    </el-form-item>
    <div v-if="showAns">{{temp1}}{{ans}}{{temp2}}{{acc}}</div>
    <el-form-item>
      <el-button type="primary" @click="onSubmit"> 提交</el-button>
      <el-button @click="onClear">清空</el-button>
    </el-form-item>

  </el-form>
</template>

<script>
  import axios from 'axios';
    export default {
      name: "eleform",
      props: [
        'articleContent',
        'optionsContent',
        'answersContent'
      ],
      data() {
        return {
          showAns: false,
          inputAnswer: false,
          temp1:'',
          ans:'',
          temp2:'',
          acc:'',
          url:"http://192.168.71.214:5000/clozeTest",
          useLarge: false,
          form: {
            model: 'bert-base-uncased',
            type: 'A',
            article: '',
            mask: '_',
            includeAnswer: '1',
            options: '',
            answers: ''
          }
        }
      },
      methods: {
        agreeChange:function(val){
          this.inputAnswer=(val=='1')?false:true;
        },
        onSubmit() {
          if(this.form.article==null||this.form.article==''||this.form.article==undefined){
            console.log(this.article)
            this.$notify.warning({
              title: '警告',
              message: '文档内容为空'
            });
          }else if(this.form.mask==null||this.form.mask==''||this.form.mask==undefined){
            this.$notify.warning({
              title: '警告',
              message: 'MASK为空'
            });
          }else if(this.form.options==null||this.form.options==''||this.form.options==undefined){
            this.$notify.warning({
              title: '警告',
              message: '答案选项为空'
            });
          }else if(this.form.answers==null||this.form.answers==''||this.form.answers==undefined){
            this.$notify.warning({
              title: '警告',
              message: '正确答案为空'
            });
          }else{
            this.$message.success("提交成功,请耐心等待输出结果,一般等待时间不超过20秒");
            if(this.useLarge == false){
              this.form.model = 'bert-base-uncased';
            }else{
              this.form.model = 'bert-large-uncased'
            }
            if(this.form.model == "bert-base-uncased"){
              this.temp1 = "BERT-BASE运算中,请等待答案输出。";
            }else{
              this.temp1 = "BERT-LARGE运算中,请等待答案输出。";
            }
            this.ans = '';
            this.temp2 = '';
            this.acc = '';
            this.showAns = true;
            let data = new FormData(); // FormData 对象
            data.append("model", this.form.model);
            data.append("article", this.form.article);
            data.append("mask", this.form.mask);
            data.append("options", this.form.options);
            data.append("includeAnswer", this.form.includeAnswer);

            if(this.form.includeAnswer == "1"){
              data.append("answers", this.form.answers);
            }

            axios({
              method: 'post',
              url: this.url,
              data: data,
              headers: {'Content-Type': 'multipart/form-data'}
            }).then(res => {
              if(this.form.model == "bert-base-uncased"){
                this.temp1 = "BERT-BASE输出答案: ";
              }else{
                this.temp1 = "BERT-LARGE输出答案: ";
              }
              this.ans = res.data.ans;
              if(this.form.includeAnswer == "1"){
                this.temp2 = " 准确率: "
                this.acc = res.data.acc;
              }
              this.showAns = true;
              console.log(res);
            }).catch((error) => {
              // eslint-disable-next-line
              this.temp1 = "输出异常，可能是输入格式错误，请仔细核对格式说明并点击清空或刷新页面重试。"
              this.ans = '';
              this.temp2 = '';
              this.acc = '';
              this.showAns = true;
              console.error(error);
            });
          }
        },
        onClear() {
          this.form.article='';
          this.form.mask='';
          this.form.options='';
          this.form.answers='';
          this.showAns=false;
        }
      },
      watch:{     //监听value的变化，进行相应的操作即可
        "articleContent": function (newv, oldv) {
          this.form.article=newv;
        },
        "optionsContent": {
          immediate: true,
          handler:function(newValue, oldValue) {
            let tempStr = newValue;
            this.form.options = tempStr;
            //console.log(typeof newValue)
          },
        },
        answersContent: {
          immediate: true,
          handler(newValue, oldValue) {
            this.form.answers = newValue;
          },
        }
      }
    }
</script>

<style >
  .el-row {
    margin-top:18px;
    margin-bottom: 20px;
  &:last-child {
     margin-bottom: 0;
   }
  }
</style>
