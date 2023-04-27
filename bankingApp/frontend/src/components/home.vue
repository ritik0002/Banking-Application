<template>
     <div class="Info">
            <h1 class="lead display-5">Account Information</h1>
            <p class="lead text-muted">Withdraw and deposit and view your balance<br>See your total transactions </p>
        </div>
    <div class="container">
        <div class="row">
           
            <h1 class="Title"></h1>

            <div class="col-6">

                <div class="col mb-2">
                    
                    <div class="padding col border rounded border-secondary p-75 bg-light">
                        <h2>Deposit Money</h2>
                        <form @submit.prevent="saveDeposit">
                            <div class="input-group">
                                <input type="Number" step="0.01" v-model="inputData"
                                    class="form-control border border-dark" />
                                <button class="btn-color" type="submit">Submit</button>
                            </div>
                        </form>
                    </div>
                    <div class="padding col border rounded border-secondary p-75 bg-light">
                        <h2>Withdraw Money</h2>
                        <form @submit.prevent="saveWithdraw">
                            <div class="input-group">
                                <input type="Number" step="0.01" v-model="inputData2"
                                    class="form-control border border-dark" />
                                <button class="btn-color" type="submit">Submit</button>
                                <p id="errorMessage"></p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="c2 col">
                    <h2 class="balance d-inline">Current Balance: £{{balancedp }}</h2>
                    <!-- id:{{ id }} -->
                </div>
                <div class="col w-75 mx-auto">
                    <CChart type="pie" ref="chart" :data="chartValues"/>
                </div>
            </div>
        </div>
    </div>

    <!-- <div>
       <h1>Display Transactions</h1>
        <h2>Fetch Transactions:</h2>
        {{this.Transactions}}
        <h3>Post Transaction</h3>
        <button @click="saveDeposit">Click me to POST</button>
    </div>
    </div> -->
</template>


<script>
import { CChart } from '@coreui/vue-chartjs'

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
    components: {
        CChart
    },
    computed:{
        balancedp(){
            let temp=Number(this.balance)
            return temp.toFixed(2);
        },
        chartValues(){
            return {options: {
                            responsive: true,
                            maintainAspectRatio: false, // This will prevent the chart from scaling proportionally
                        },
                        labels: ['Deposit','Withdraw','Transfer'],
                        datasets: [
                            {
                                backgroundColor: ['#41B883', '#00D8FF','#FF0000'],
                                data:[this.Transactions.deposits.toFixed(2),this.Transactions.withdrawals.toFixed(2),this.Transactions.transfer.toFixed(2)],
                            },                        
                        ],
                        hoverOffset: 4,
        }
    },
},
    data() {
        return {
            d_val:null,
            w_val:null,
            encryptedData: '',
            inputData: null,
            inputData2: null,
            amount: null,
            Transactions:{"withdrawals":0,"deposits":0,"transfer":0},
            balance: null,
            id: null,

        }
    },

    methods: {

        async fetch_Balance() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id
            let response = await fetch("http://127.0.0.1:8000/api/user/"+this.id);
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            //retrieve balance
            this.balance = data.user.balance;
            console.log(`This is balance:${this.balance}`)
        },
        async fetch_Transactions() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id
            //ajax request to perform list recipes
            let response = await fetch("http://localhost:8000/api/transaction/filter/"+this.id+"/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            console.log(data.Transaction)
            //retrieve list of Transactions objects
            this.Transactions = data.Transaction;
            console.log(this.Transactions.withdrawals)
            console.log(this.Transactions["deposits"])
            // this.chart.chartData.datasets[0].data = [this.Transactions.withdrawals,this.Transactions.deposits];
            // this.chart.update();
        },
        async saveWithdraw() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id
            if (parseFloat(this.balance) < (parseFloat(parseFloat(this.inputData2).toFixed(2)))) {
                document.getElementById("errorMessage").innerHTML = "Error withdrawal amount is larger than balance!"
            } else {
                let current_day =new Date().toISOString().slice(0, 19).replace('T', ' ');

                const Transaction = JSON.stringify({
                    amount: parseFloat(this.inputData2).toFixed(2),
                    type: "W",
                    date: current_day,
                })

                let response = await fetch("http://127.0.0.1:8000/api/transaction/"+this.id+"/", {
                    method: 'POST',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                    },
                    body: Transaction,
                })
                this.fetch_Transactions();
                this.fetch_Balance();
                this.inputData2=""

            }



        },
        async saveDeposit() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id

            let current_day =new Date().toISOString().slice(0, 19).replace('T', ' ');


            const Transaction = JSON.stringify({
                amount: parseFloat(this.inputData).toFixed(2),
                type: "D",
                date: current_day,
            })

            let response = await fetch("http://127.0.0.1:8000/api/transaction/"+this.id+"/", {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: Transaction,
            })
            this.inputData=""
            this.fetch_Transactions();
            this.fetch_Balance();


        },

        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            this.id=data.User.id
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
    },
    mounted() {
        this.fetch_Balance();
        this.getSession();
        // this.fetch_user();
        this.fetch_Transactions();
        // this.$nextTick(() => {
        //     this.$refs.chart.chartObject.update();
        // }, 0);
        this.$nextTick(() => {
            if (this.$refs.chart.chartObject) {
                this.$refs.chart.chartObject.update();
            }
        }, 0);
    },
    created(){
        this.Transactions={"withdrawals":0,"deposits":0,'transfer':0};
        this.fetch_Transactions();  
    },

}
</script>

<style scoped>
.padding {
    padding: 1%;
    margin: 10% 0;
}

.btn-color {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
    border: solid rgb(255, 255, 255) 2px;
    padding: 2% 8% 2% 8%;

}

.btn-color:hover {
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    border: solid rgb(0, 0, 0) 2px;


}
.col-6{
    align-self: center;
}

.form-control:focus {
    border-color: #000000 !important;
    box-shadow: 1px 1px 5px rgb(17, 4, 78) !important;
}

.balance {
    text-align: center;
}

.c2 {
    text-align: center;
}
.Title{
    margin-top:2%;
}


.Info{
    color:white;
    height:15%;
    /* background-color: #02093B; */
    background-image: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    padding:2%;

    /* /* font: ; */
}
.Info p{
    margin-left:5%;

}


</style>