<template>
    <!-- Footer -->
<footer class="footer pt-4">

<!-- Footer Links -->
<div class="container-fluid text-center text-md-left bg-dark text-light">

  <div class="row">
    <div class="col-md-6 mt-md-0 mt-3 pt-1">
      <!-- Content -->
      <h3 class="text-light lead">Information</h3>
      <p class="blockquote text-center">A banking application that uses homomorphic encryption. This application was made for the purpose showcasing the potential use case of homomorphic encryption</p>
    </div>

    <hr class="clearfix w-100 d-md-none pb-2">
    <div class="col-md-3 mb-md-0 mb-3">
      <h3 class="lead">Navigations</h3>
      <ul class="list-unstyled">
        <li>
            <div class="nav-link"><router-link to="/setting">Settings</router-link></div>
        </li>
        <li>
            <div class="nav-link"><router-link to="/">Account Information</router-link></div>
        </li>
        <li>
            <div class="nav-link"><router-link to="/transaction-history">Transaction History</router-link></div>
        </li>
        <li>
            <div class="nav-link"><router-link to="/savings">Saving Planner</router-link></div>        
        </li>
        <li>
            <div class="nav-link"><router-link to="/transfer">Transfer Money</router-link></div>        
        </li>
        <li>
            <div class="nav-link"><router-link to="/transfer">Transfer Money</router-link></div>        
        </li>
      </ul>

    </div>

    <div class="col-md-3 mb-md-0 mb-3">
      <!-- Links -->
      <h3 class="lead">Follow us</h3>
      <ul class="list-unstyled">
        <li>
          <a href=""><i class="bi bi-facebook"></i></a>
        </li>
        <li>
          <a href=""><i class="bi bi-instagram"></i></a>
        </li>
        <li>
          <a href=""><i class="bi bi-linkedin"></i></a>
        </li>
        <li>
          <a href=""><i class="bi bi-youtube"></i></a>
        </li>
      </ul>

    </div>
  </div>

</div>

<!-- Copyright -->
<div class="footer-copyright text-center py-3 bg-dark text-light">© 2023 Copyright:
  <a class="link" href="/"> Ritik Desai</a>
</div>
<!-- Copyright -->

</footer>
<!-- Footer -->
</template>

<script>
    export default {
        
    }
</script>


<style scoped>
a,.link{
    color:white;
    text-decoration: none;
}
.row{
    padding-top: 1%;
    font-size:1.2em;
}

.bi{
    color:white;
    font-size: 1.7em;
}

</style>