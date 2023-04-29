<template>
    <div>
        
        <div class="Info">
        <h1 class="lead display-5">Transfer Funds</h1>
        <p class="lead text-muted">Transfer funds to a different user</p>
    </div>
    </div>
    <div class="container">
        <div class="row">
            <div class="t1 col-6">
                <h1>Transfer funds</h1>
                <hr>
                 <form @submit.prevent="sendTransfer">
                    Transfer to:
                    <input class="form-control" type="text" placeholder="Enter Username" v-model="username" required>
                    Description:
                    <input class="form-control" type="text" placeholder="Default input" v-model="desc" >
                    Amount:
                    <input class="form-control" type="Number" step="0.01" min="1" max="10000"  placeholder="enter a number" v-model="amount" required>
                    <button class="sub btn btn-dark" type="submit">Submit</button>
                    <p id="errorMessage"></p>
                </form>
            </div>
            <div class="col-6">
                <h1>Balance</h1>
                <hr>
                <div class="c2 col">
                    <h2 class="bal d-inline">Current Balance: £{{balancedp }}</h2>
                    <!-- id:{{ id }} -->
                </div>
            </div>
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
        x:null,
        balance:null,
        users:null,
        username:"",
        amount:null,
        desc:"",
        currentuser:"",


        }
    },
    computed:{
        balancedp(){
            let temp=Number(this.balance)
            return temp.toFixed(2);
        },
    },
    methods: {

        








        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
        async sendTransfer(){
            let response1 = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data1 = await response1.json();
            let response2 = await fetch("http://127.0.0.1:8000/api/users/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data2 = await response2.json();
            this.users=data2.user
            this.id = data1.User.id   //gets current user id
            let result=this.users.some(x=>x.username===this.username)
            if(this.username.toLowerCase() === data1.User.username.toLowerCase()){
                document.getElementById("errorMessage").innerHTML = "Error cannot be current username!"

            }
            else if(result==false){
                document.getElementById("errorMessage").innerHTML = "Error invalid username!"
            }
            else if (parseFloat(this.balance) < (parseFloat(parseFloat(this.inputData2).toFixed(2)))) {
                document.getElementById("errorMessage").innerHTML = "Error Transfer amount is larger than balance!"
            } else {
                document.getElementById("errorMessage").innerHTML = ""
                let current_day =new Date().toISOString().slice(0, 19).replace('T', ' ');
                const Transaction = JSON.stringify({
                    amount: parseFloat(this.amount).toFixed(2),
                    type: "T",
                    date: current_day,
                    desc:this.desc,
                    username:this.username,
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
                this.fetch_Balance();
                this.desc=""
                this.username="",
                this.amount=null

            }
        },
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

    },
    mounted(){
        this.getSession();
        this.fetch_Balance();
    },

}
</script>

<style  scoped>
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

.sub{
    margin-top:3%;
    margin-left:30%;
    padding-top:2%;
    padding-bottom:2%;
    padding-left:4%;
    padding-right:4%;
}
.bal{
    font-weight: 400;
    /* border:solid rgb(205, 205, 205) 2px; */
    border-radius: 2%;
    padding:1%;
    /* margin-left:5%; */
    margin-top:100%;
}
.t1{
    border-right:solid black 2px;
}
.container{
    margin-top:2%;

}

#errorMessage{
    color:red;
}
</style>