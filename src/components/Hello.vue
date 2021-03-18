<template>
  <div>
    <el-upload class="upload" drag action="/test" multiple ref="upload"
               list-type="file"
               :show-file-list="false"
               :http-request="httpRequest">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">推荐以上传文件形式上传题目，将.json格式的文档拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">也可直接在下方填入相关信息</div>
    </el-upload>
  <elform :articleContent="article"
          :optionsContent="options"
          :answersContent="answers"></elform>
  </div>


</template>

<script >
  import elform from './elform'
  import axios from 'axios';
  export default {
    name: 'Hello',
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1',
        //url:"http://192.168.71.214:5000/uploadFile",
        url:"http://192.168.71.214:5000/uploadFile",
        article:'',
        options:'',
        answers:'',
      };
    },
    methods: {
      httpRequest(param) {
        console.log(param);
        let fileObj = param.file; // 相当于input里取得的files
        let data = new FormData(); // FormData 对象
        let extension = fileObj.name.substring(fileObj.name.lastIndexOf('.') + 1)
        let size = fileObj.size / 1024 / 1024
        if (extension !== 'json') {
          this.$notify.warning({
            title: '警告',
            message: `只能上传后缀是.json的文件`
          });
        } else if(size > 10) {
          this.$notify.warning({
            title: '警告',
            message: `文件大小不得超过10M`
          });
        } else {
          data.append("file", fileObj); // 文件对象
          //data.append("name", this.regeditForm.name);
          //data.append("description", this.regeditForm.description);
          axios({
            method: 'POST',
            url: this.url,
            data: data,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(res => {
              this.$message.success("文件上传成功");
              this.article=res.data.article;
              this.options=JSON.stringify(res.data.options);
              this.answers=JSON.stringify(res.data.answers);
              console.log(res);
            }).catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
        }
      },
    },
    components:{
      elform
    }
  }

</script>
<style scoped>
  .upload{
    margin-bottom:20px;
  }
  .el-row {
    margin-bottom: 20px;
  &:last-child {
     margin-bottom: 0;
   }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    margin: 0 auto;
    width: 90%;
  }
</style>
