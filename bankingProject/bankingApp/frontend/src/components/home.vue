<template>
    <div>
    <h1>Home Page</h1>
    <form @submit.prevent="saveNewObject">
      <input type="text" v-model="inputData"/>
      <button type="submit">Send to Backend</button>
    </form>
    <p>Encrypted Data: {{ encryptedData }}</p>


    <div>
       <h1>Test</h1>
        <h2>Fetch Transactions:</h2>
        {{this.Transactions}}
        <h3>Post Transaction</h3>
        <button @click="saveNewObject">Click me to POST</button>
    </div>
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
                inputData:'',
                Transactions:[],
            }
        },
        
        methods: {
        async fetch_Transactions() {
            //ajax request to perform list recipes
            let response = await fetch("http://localhost:8000/api/test/");
            //turn the data into json and fetches the data from the backend
            let data = await response.json();
            //retrieve list of transport objects
            this.Transactions = data.Transaction;
        },
        async saveNewObject() {
           
            const Transaction = JSON.stringify({
                amount:150,
                type: "w",
                date: "2025-06-07",
            })
            if (this.id == null) {
                let response = await fetch("http://127.0.0.1:8000/api/test/", {
                    method: 'POST',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                    },
                    body: Transaction,
                })
            }
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
        this.getSession();
        // this.fetch_user();
        this.fetch_Transactions();
    },
}
</script>

<style scoped>

</style>