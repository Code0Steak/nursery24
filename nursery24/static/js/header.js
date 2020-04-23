const template=document.createElement('template')
template.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <nav class="navbar navbar-expand-lg navbar-light d-flex bg-warning">
        <a class="navbar-brand" href="#">
        <img src='../static/images/logo.png' width="100"
                style="margin-left:10"></a>
        
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <form  class="form-inline my-2 my-lg-0" action = "search" style="margin-left: 100px;">
            <input class="form-control mr-sm-2" size="80" type="search" placeholder="Search" aria-label="Search" name = "search">
            <button class="btn btn-success my-2 my-sm-0" type="submit">Search</button>
        </form>
        
        <form class="ml-auto">
            <button formaction="signup" class="btn btn-primary">Sign Up</button>
        </form>

        <form class="ml-auto mr-3">
            <button formaction="login" class="btn btn-primary">Log In</button>
        </form>
    </nav>`
        
class Header extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }

}

window.customElements.define('header-bar',Header)
