<template>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
        
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1"><router-link to="/"><img src="http://127.0.0.1:8000/media/logo.png" alt="logo">Cipher</router-link></span>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="budget">Budget</router-link></div>

                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="/transfer">Transfer Money</router-link></div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="savings">Saving Planner</router-link></div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="transaction-history">Transaction History</router-link></div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="/">Account Infomation</router-link></div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="setting">Settings</router-link></div>

                    </li>
                    <li class="nav-item">
                        <div class="nav-link"><router-link to="logout">Logout</router-link></div>

                    </li>
                    

                </ul>
            </div>
    </nav>

</template>

<script setup lang="ts">

</script>

<style scoped>
a {
    text-decoration: none;
    color: inherit;
}

h2{
 color:white;   
}

img{
    width:3em;
}
</style>