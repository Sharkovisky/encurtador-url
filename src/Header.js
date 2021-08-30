import React from 'react';
import './Header.css';


function Header(){

    return (
        <header>
            <div class="container d-flex justify-content-around text-light">
                <div class="d-flex justify-content-between">
                    <div class="p-3">O que é?</div>
                    <div class="p-3">Denúncias</div>
                    <div class="p-3">Contador de Cliques</div>
                </div>
                <div class="p-2">
                    <button type="button" class="btn btn-light">Login</button>
                </div>
            </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-U1DAWAznBHeqEIlVSCgzq+c9gqGAJn5c/t99JyeKa9xxaYpSvHU5awsuZVVFIhvj" crossorigin="anonymous"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous"></link>
        </header>
    );
}

export default Header;