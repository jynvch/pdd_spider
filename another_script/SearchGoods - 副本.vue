<template>
    <div class="search-view">
        <el-form inline>
            <el-form-item label="搜索词">
                <el-input v-model.number="filterData.q" placeholder="搜索词"></el-input>
            </el-form-item>
            <el-form-item label="商品id">
                <el-input v-model.number="goodsId" placeholder="商品id"></el-input>
            </el-form-item>
            <el-form-item label="cookie">
                <el-input v-model="cookie" placeholder="请填写cookie"></el-input>
            </el-form-item>
            <el-form-item label="accessToken">
                <el-input v-model="accessToken" placeholder="请填写accessToken"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getFirstList">搜索</el-button>
                <el-button type="primary" @click="getA">测试</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" v-loading="loading" ref="table" border size="mini">
            <el-table-column label="序号" type="index"></el-table-column>
            <el-table-column prop="goodsID" label="商品ID" show-overflow-tooltip></el-table-column>
            <el-table-column prop="goodsName" label="商品名称" width="300" show-overflow-tooltip></el-table-column>
            <el-table-column prop="price" label="售价"></el-table-column>
            <el-table-column prop="salesTip" label="销量"></el-table-column>
            <el-table-column prop="mallName" label="店铺名称"></el-table-column>
        </el-table>
    </div>
</template>

<script>
import { ipcApiHandle } from '@/api/ipc';
import { getContent } from '@/api/util';
export default {
    name: "SearchGoods",
    components: {},
    data() {
        return {
            loading: false,
            filterData: {
                page: 1,
                size: 50,
                q:'',
                sort:'default',
                filter:'',
                list_id:'',
                flip:'',
                anti_content:'',
                pdduid:'',
                source:'',
                search_met: 'manual'

            },
            goodsId: '',
            goodsIdRank:'',
            cookie: "",
            accessToken: "",
            isOver: false,
            tableData: []
        };
    },
    mounted() {
    },
    methods: {
        getA(){
            //let r=getContent('蚊帐',[])
            //console.log(r)
        },
        getFirstList(){
            if (this.filterData.q == '') {
                this.$message.warning('请输入搜索词')
                return false
            }
            if (this.goodsId == '') {
                this.$message.warning('请输入商品ID')
                return false
            }
            if (this.cookie == ''||this.accessToken) {
                this.$message.warning('请填写cookie和accessToken')
                //return false
            }
            //请求参数
            let url = 'http://mobile.yangkeduo.com/search_result.html'
            let params ={
                search_key:this.filterData.q,
                search_src:'new',
                search_met:'btn_sort'
            }
            let header = {
                "Cookie": this.cookie,
                "Referer": 'http://mobile.yangkeduo.com/classification.html',
                "Accept-Language": "zh-CN,zh;q=0.9",
                "AccessToken": this.accessToken,
                //"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404"
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36;"
            }
            this.loading = true;
            //发送主进程
            let ipcRes = this.$electron.ipcRenderer.sendSync('request-searchgoods', url, params, header)
            ipcApiHandle(ipcRes).then((res) => {
                this.filterData.flip=res.flip
                this.filterData.list_id=res.listID
                this.filterData.page+=1
                this.tableData=this.tableData.concat(res.list);
                setTimeout(()=>{
                    this.getList()
                },2000)
            }).catch((err, code) => {
                this.loading = false;
            })
        },
        getList() {
            if (this.isOver) {
                this.$message.warning('搜索结束,重新搜索请点击重置')
                return false
            }
            this.loading = true;
            //请求参数
            let url = 'http://mobile.yangkeduo.com/proxy/api/search'
            this.filterData.anti_content=getContent(this.filterData.q,this.cookie.split(';'))
            console.log('request_params',this.filterData)
            let params = this.filterData
            let header = {
                "Cookie": this.cookie,
                "Referer": `http://mobile.yangkeduo.com/search_result.html?search_key=${encodeURI(this.filterData.q)}`,
                "Accept-Language": "zh-CN,zh;q=0.9",
                //"AccessToken": this.accessToken,
                //"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404"
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36;"   
           }
            //发送主进程
            let ipcRes = this.$electron.ipcRenderer.sendSync('request-api', url, params, header)
            ipcApiHandle(ipcRes).then((res) => {
                this.filterData.flip=res.flip
                let listRaw = res.items;
                this.tableData = this.tableData.concat(listRaw);
                this.filterData.page = this.filterData.page + 1;
                    if (this.tableData.length>=res.total) {
                        this.loading = false;
                        this.isOver = true;
                    }else{
                        setTimeout(()=>{
                            this.getList()
                        },2000)
                    }
            }).catch((err, code) => {
                this.$message.error('搜索发生异常,请稍后重试')
                this.loading = false;
            })
        },
    }
};
</script>
<style scoped>
.search-view .el-form {
    margin-top: 50px;
}
</style>

