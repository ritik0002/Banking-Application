<template>
    <div>
        <div>
            <div class="Info">
                <h1 class="lead display-5">Transaction History</h1>
                <p class="lead text-muted">See all your transactions here</p>
            </div>
        </div>
        <div>
            <input class="searchbar" v-model="searchQuery" placeholder="filter transaction type">
        </div>
        <div class="container">
            <table class="table">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Date</th>
                        <th scope="col">Type</th>
                        <th scope="col">Description</th>
                        <th scope="col">Encrypted Amount</th>
                        <th scope="col">Amount(£)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(x, index) in Transactions" :key="index">
                        <!-- Template element doesn't effect the HTML elements (so table contents stay) -->
                        <template v-if="type[x.type].includes(searchQuery.toLowerCase())===true || searchQuery===''">
                        <td>{{ x.id }}</td>
                        <td>{{ x.date }}</td>
                        <td>
                            <div v-if="x.type === 'D'">
                                Deposit
                            </div>
                            <div v-else-if="x.type == 'W'">
                                Withdrawal
                            </div>
                            <div v-else-if="x.type === 'T'">
                                Transfer
                            </div>
                        </td>
                        <td>{{ x.description }}</td>
                        <td>{{ x.amount }}</td>
                        <td ><button ref="buttonT"  @click="fetch_current_transaction(x.id,index)">Get Amount</button></td>
                    </template>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
</template>

<script>
function getCookie(name) {
    let cookieValue = "";
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
export default {

    data() {
        return {
            searchQuery:"",
            Transactions: null,
            Transaction:null,
            id:null,
            type:{
                "D":"deposit",
                "W":"withdrawal",
                "T":"transfer",
            }
        }
    },
    methods: {

        async fetch_Transactions() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id
            let response = await fetch("http://127.0.0.1:8000/api/transaction/"+this.id+"/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            this.Transactions = data.Transaction;
        },

        async fetch_current_transaction(id,index) {
            let response = await fetch("http://127.0.0.1:8000/api/transactions/"+id+"/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            this.Transaction = data.Transaction.amount;
            console.log("yes", this.Transaction);
            // this.Transactions[index]=this.Transaction;
            this.$refs.buttonT[index].innerHTML = this.Transaction
            this.$refs.buttonT[index].style.border = "none";
            this.$refs.buttonT[index].style.background = "none";
            this.$refs.buttonT[index].style.cursor = "default";
            this.$refs.buttonT[index].disabled = true;
            this.$refs.buttonT[index].style.color="black";
            this.$refs.buttonT[index].style.fontWeight="bold";
        },




        //if your not authenicated you get sent back to the login screen
        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
    },
    mounted() {
        this.getSession();
        this.fetch_Transactions();
    }
}
</script>

<style scoped>
.Info {
    color: white;
    height: 15%;
    /* background-color: #02093B; */
    background-image: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    padding: 2%;

    /* /* font: ; */
}

.Info p {
    margin-left: 5%;

}
.searchbar{
    margin:2% 0;
    margin-left:10%;
    width: 80%;
    padding:0.5%;
    border:solid black 2px;

}
</style>