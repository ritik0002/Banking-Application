<template>
    <div class="container">

        <div class="row">
            <h1 class="Title">Account Information</h1>

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
                    <h2 class="balance d-inline">Current Balance: £{{ balance }}</h2>
                    <!-- id:{{ id }} -->
                </div>
                <div class="col w-75 mx-auto">
                    <CChart type="pie" :data="{
                        options: {
                            responsive: true,
                            maintainAspectRatio: false, // This will prevent the chart from scaling proportionally
                        },
                        labels: ['Deposit','Withdraw'],
                        datasets: [
                            {
                                backgroundColor: ['#41B883', '#00D8FF'],
                                data:[this.Transactions.deposits.toFixed(2),this.Transactions.withdrawals.toFixed(2)],
                            },                        
                        ],
                        hoverOffset: 4,
                    }" />
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
    data() {
        return {
            d_val:null,
            w_val:null,
            encryptedData: '',
            inputData: null,
            inputData2: null,
            amount: null,
            Transactions:null,
            balance: null,
            id: null,

        }
    },

    methods: {

        async fetch_Balance() {
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            this.id = data1.User.id   //gets current user id
            let response = await fetch("http://localhost:8000/api/users/" + this.id + "/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            //retrieve balance
            this.balance = data.user.balance;
            console.log(`This is balance:${this.balance}`)
        },
        async fetch_Transactions() {
            //ajax request to perform list recipes
            let response = await fetch("http://localhost:8000/api/transaction/filter/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            console.log(data.Transaction)
            //retrieve list of Transactions objects
            this.Transactions = data.Transaction;
            console.log(this.Transactions.withdrawals)
            console.log(this.Transactions["deposits"])
        },
        async saveWithdraw() {
            if (parseFloat(this.balance) < (parseFloat(parseFloat(this.inputData2).toFixed(2)))) {
                document.getElementById("errorMessage").innerHTML = "Error withdrawal amount is larger than balance!"
            } else {
                let current_day = new Date().toISOString().slice(0, 10)
                const Transaction = JSON.stringify({
                    amount: parseFloat(this.inputData2).toFixed(2),
                    type: "W",
                    date: current_day,
                })

                let response = await fetch("http://127.0.0.1:8000/api/transaction/", {
                    method: 'POST',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                    },
                    body: Transaction,
                })
                this.$data._chart.update()
                this.fetch_Balance();

            }



        },
        async saveDeposit() {
            let current_day = new Date().toISOString().slice(0, 10)

            const Transaction = JSON.stringify({
                amount: parseFloat(this.inputData).toFixed(2),
                type: "D",
                date: current_day,
            })

            let response = await fetch("http://127.0.0.1:8000/api/transaction/", {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: Transaction,
            })
            this.$data._chart.update()
            this.fetch_Balance();


        },

        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
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
    },
    created(){
        this.fetch_Transactions();  
    }
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


</style>