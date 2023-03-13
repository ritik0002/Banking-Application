<template>

    <div>
        Balance: {{ balance }}
        id:{{id}}
    </div>
    <div>
    <h1>Deposit</h1>
    <form @submit.prevent="saveNewObject">
      <input type="Number" step="0.01" v-model="inputData"/>
      <button type="submit">Send to Backend</button>
    </form>
    <p>Encrypted Data: {{ encryptedData }}</p>


    <div>
       <h1>Display Transactions</h1>
        <h2>Fetch Transactions:</h2>
        {{this.Transactions}}
        <h3>Post Transaction</h3>
        <button @click="saveNewObject">Click me to POST</button>
    </div>
    </div>


    <div>
        <h1>Account Information</h1>
        <h2>Withdraw Money</h2>
        <form @submit.prevent="saveWithdraw">
            <input type="text" v-model="amount"/>
            <div><button type="submit">Submit</button></div>
        </form>

    </div>
</template>


<script>
function getCookie(name){
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
            return{
                encryptedData:'',
                inputData:null,
                amount:null,
                Transactions:[],
                balance:null,
                id:null,

            }
        },
        
        methods: {
        
        async fetch_Balance(){
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1=await response1.json();
            this.id=data1.User.id   //gets current user id
            let response = await fetch("http://localhost:8000/api/users/"+this.id+"/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            //retrieve list of transport objects
            this.balance = data.user.balance;
        },
        async fetch_Transactions() {
            //ajax request to perform list recipes
            let response = await fetch("http://localhost:8000/api/transaction/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            //retrieve list of transport objects
            this.Transactions = data.Transaction;
        },
        // async saveWithdraw(){
        //     pass

        // },
        async saveNewObject() {
            const Transaction = JSON.stringify({
                amount:parseFloat(this.inputData).toFixed(2),
                type: "D",
                date: "2025-06-07",
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
            
        },

        async getSession(){
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
    },
    mounted(){
        this.fetch_Balance();
        this.getSession();
        // this.fetch_user();
        // this.fetch_Transactions();
    },
}
</script>

<style scoped>

</style>