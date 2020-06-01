const template6=document.createElement('template')
template6.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
        .card {
            display: inline-block;
        }
        .d-block {
            height: 20vw;
            object-fit: cover;
        }

        li {
            list-style-type: none;
        }

        .btn-group {
            margin: auto;
            display: flex;
            flex-direction: row;
            justify-content: center;
          }
    </style>
    <div class="row p-2">
    <div class="col-md-1 text-center">
    <img id="image" height="50px" width="50px" style="border:2px solid black;border-radius:10px;object-fit:cover">
    </div>

    <div class="col-md-3 text-start my-auto">
    <h5 class="font-weight-bold"><span id='name'></span></h5>
    </div>

    <div class="col-md-2 my-auto text-center">
    <h5>Rs. <span id='price'></span></h6>
    </div>

    <div class="col-md-2 my-auto">
    <div class="btn-toolbar ml-1 mb-2" role="toolbar" aria-label="Toolbar with button groups">
        
        <div class="btn-group ml-auto mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-success" id = "inc">+</button>
            <button type="button" class="btn btn-outline-secondary disabled" id = "quantity">0</button>
            <button type="button" class="btn btn-success" id = "dec">-</button>
            
        </div>
    </div>
    </div>

    <div class="col-md-2 text-center">
    <h5>Rs. <span id='result'> </span></h6>
    </div>
    </div>`
        
class CartCard extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template6.content.cloneNode(true))
        this.shadowRoot.querySelector('#name').innerText=this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText=this.getAttribute('price')
        this.shadowRoot.querySelector('#quantity').innerHTML = this.getAttribute('quantity')
        this.shadowRoot.querySelector('#image').src=this.getAttribute('image')
        //this.innerHTML=`${this.getAttribute('name')}`
        let decodedCookie = decodeURIComponent(document.cookie).split(';');
        if(decodedCookie.find(item => item.includes("product="))){
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                
                if(product.find(item=> item.name == this.getAttribute('name'))){
                    this.shadowRoot.querySelector("#result").innerHTML = product.find(item=> item.name == this.getAttribute('name')).price;
                    this.shadowRoot.querySelector("#quantity").innerHTML = product.find(item=> item.name == this.getAttribute('name')).quantity;
                }
            }
    }

    connectedCallback(){

        
        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        let img = this.shadowRoot.querySelector('#image').src;
        let provider = this.getAttribute('provider');
        //increments product in cookie
        this.shadowRoot.querySelector("#inc").addEventListener('click',()=>{
            
            let decodedCookie = decodeURIComponent(document.cookie).split(';');
            console.log(decodedCookie);
            if(!decodedCookie.find(item => item.includes("product="))){
                let product = [{name: name, quantity: 1,perPrice: price,price: price,img: img,provider: provider}]
                //console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);
                //console.log(document.cookie);
                this.shadowRoot.querySelector("#result").innerHTML = price;
                this.shadowRoot.querySelector("#quantity").innerHTML = product.quantity;
                console.log(product);
            }
            else{
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
               // console.log(product);// success
                if(!product.find(item=> item.name == name)){
                    let newProduct = {name: name,quantity: 1, perPrice: price, price: price, img: img,provider:provider};
                    this.shadowRoot.querySelector("#result").innerHTML = price;
                    this.shadowRoot.querySelector("#quantity").innerHTML = newProduct.quantity;
                    product = [...product,newProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);
                }
                else
                {
                let thisProduct = product.find(item => item.name == name);
                product = product.filter(item=> item.name !=name);
                thisProduct.quantity += 1;
                thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                this.shadowRoot.querySelector("#result").innerHTML = thisProduct.price;
                this.shadowRoot.querySelector("#quantity").innerHTML = thisProduct.quantity;
                product = [...product,thisProduct];
                console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);  
                }
            }
        });
            //decrements product in cookie
            this.shadowRoot.querySelector("#dec").addEventListener('click',  ()=>{
                let decodedCookie = decodeURIComponent(document.cookie).split(';');
               
                let productString = decodedCookie.find(item => item.includes("product="));
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                
                    if(product.find(item=> item.name == name)){
                      
                            
                        let thisProduct = product.find(item=> item.name == name);
                        product = product.filter(item=> item.name != name);
                        thisProduct.quantity -= 1;
                        
                        thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                        this.shadowRoot.querySelector('#result').innerHTML = thisProduct.price;
                        this.shadowRoot.querySelector("#quantity").innerHTML = thisProduct.quantity;
                        if(thisProduct.quantity!= 0){
                            product = [...product,thisProduct];
                        }
                        else{
                            document.cookie = 'product=' + JSON.stringify(product);
                            document.cookie = 'product=' + JSON.stringify(product);
                            window.location.href = "cart"
                            disconnect();
                        }
                        document.cookie = 'product=' + JSON.stringify(product);
                        
                    }
                
                
            });
        
    }

    disconnectedCallback() {
       // rerender();
       console.log('disconnected ...');
    }

}

window.customElements.define('cart-card',CartCard)
let disconnect = () => {
    document.querySelector('cart-card').remove(); // 'disconnected from the DOM'
}